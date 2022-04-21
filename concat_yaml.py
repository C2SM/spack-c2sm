#!/usr/bin/env python3
from ruamel import yaml
import warnings
import subprocess
import os
import argparse
import sys

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

# CONSISTENCY CHECKS


def allign_cuda_versions(joint_packages, module_packages_file, version):
    '''
    Take to prefix provided by spack-config and replace the one
    taken from sysconfig/templates
    '''

    print('Allign cuda versions')

    module_packages = load_from_yaml(module_packages_file)['packages']

    cuda_joint = joint_packages['packages']['cuda']

    spec_joint = cuda_joint['externals'][0]['spec']

    if version not in spec_joint:
        raise ValueError(
            f'Cuda version {version} not provided by yaml from templates')

    specs_module = [ex['spec'] for ex in module_packages['cuda']['externals']]
    prefix_module = [
        ex['prefix'] for ex in module_packages['cuda']['externals']
    ]

    try:
        prefix = next(prefix
                      for spec, prefix in zip(specs_module, prefix_module)
                      if version in spec)
    except StopIteration:
        raise ValueError(
            f'Cuda version {version} not provided by spack-config module')

    joint_packages['packages']['cuda']['externals'][0]['prefix'] = prefix

    return joint_packages


def rename_cray_mpich_to_mpich(packages):
    '''
    Rename cray-mpich from spack-config module
    to mpich to be compatible with spack-c2sm
    '''

    print('Rename cray-mpich to mpich')
    cray_mpich = packages['packages']['cray-mpich']

    spec = cray_mpich['externals'][0]['spec']
    spec = spec.replace('cray-', '')

    cray_mpich['externals'][0]['spec'] = spec

    packages['packages']['mpich'] = cray_mpich

    packages['packages']['mpich']['buildable'] = False

    packages['packages'].pop('cray-mpich')

    return packages


def allow_xml_to_be_built(packages):
    print('Allow building of xml')
    packages['packages']['libxml2']['buildable'] = True
    return packages


# SPACK COMMANDS


def spack_external_find(machine, packages_file):
    '''
    run spack external find and write
    packages.yaml to current workingdir
    '''

    print(f'Find externals on {machine}')

    os.environ["SPACK_USER_CONFIG_PATH"] = os.getcwd()

    if os.path.exists(packages_file): os.remove(packages_file)

    command = [
        "./config.py",
        "-i",
        ".",
        "-u",
        "OFF",
        "-m",
        machine,
        "--no_yaml_copy",
    ]
    subprocess.run(command, check=True)
    command = [
        'bash', '-c', "source spack/share/spack/setup-env.sh && \
               spack external find --not-buildable --scope=user"
    ]
    subprocess.run(command, check=True)

    os.environ.pop("SPACK_USER_CONFIG_PATH")


# MERGE OF INDIVIDUAL YAML-FILES


def disambiguate_compilers_with_precedence(primary, secondary, key_1, key_2):
    primary_specs = {item[key_1][key_2] for item in primary}
    return primary + [
        item for item in secondary if item[key_1][key_2] not in primary_specs
    ]


def join_compilers(primary, secondary):
    print('Join compilers')

    primary_compilers = load_from_yaml(primary)
    secondary_compilers = load_from_yaml(secondary)

    compilers = disambiguate_compilers_with_precedence(
        primary_compilers['compilers'], secondary_compilers['compilers'],
        'compiler', 'spec')

    return {'compilers': compilers}


def join_packages(primary, secondary, tertiary):
    print('Join packages')
    primary_packages = load_from_yaml(primary)['packages']
    secondary_packages = load_from_yaml(secondary)['packages']
    tertiary_packages = load_from_yaml(tertiary)['packages']

    tertiary_packages.update(secondary_packages)
    tertiary_packages.update(primary_packages)
    return {'packages': tertiary_packages}


# HELPERS


def load_from_yaml(file):
    print(f'Load yaml file: {file}')
    with open(file, "r") as f:
        try:
            data = yaml.load(f)
        except yaml.error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))
    return data


def dump_to_yaml(yaml_content, yaml_name):
    print(f'Dump to yaml: {yaml_name}')
    yaml.safe_dump(yaml_content,
                   open(yaml_name, 'w'),
                   default_flow_style=False)


def git_diff(machine):
    print('Running git diff')

    command = ['/usr/bin/git', 'diff', '--exit-code', '--name-only']
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print('Could not find git -> Abort')
        sys.exit(1)

    # git diff exits with 1 if differences are found
    except subprocess.CalledProcessError:
        commit_and_push_to_git(machine)


def commit_and_push_to_git(machine):
    print('Commit to Git')
    branch = f'{machine}_automatic_update'

    command = ['/usr/bin/git', 'switch', '-c', branch]
    subprocess.run(command, check=True)

    command = ['/usr/bin/git', 'add', f'sysconfigs/{machine}/*']
    subprocess.run(command, check=True)

    command = ['/usr/bin/git', 'commit', '-m', f'update config for {machine}']
    subprocess.run(command, check=True)

    command = ['/usr/bin/git', 'push', 'origin', branch]
    subprocess.run(command, check=True)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--machine', '-m', dest='machine')
    parser.add_argument('--publish_to_git',
                        action='store_true',
                        dest='publish_to_git')
    args = parser.parse_args()

    try:
        spack_config_root = os.environ['SPACK_SYSTEM_CONFIG_PATH']
    except KeyError:
        raise KeyError('module spack-config not loaded')

    c2sm_compiler_file = f'sysconfigs/templates/{args.machine}/compilers.yaml'
    module_compiler_file = f'{spack_config_root}/compilers.yaml'
    joint_compiler_file = f'sysconfigs/{args.machine}/compilers.yaml'

    c2sm_packages_file = f'sysconfigs/templates/{args.machine}/packages.yaml'
    module_packages_file = f'{spack_config_root}/packages.yaml'
    external_packages_file = 'packages.yaml'
    joint_packages_file = f'sysconfigs/{args.machine}/packages.yaml'

    print('Cleanup')
    if os.path.exists(joint_packages_file): os.remove(joint_packages_file)
    if os.path.exists(joint_compiler_file): os.remove(joint_compiler_file)

    spack_external_find(args.machine, external_packages_file)

    joint_compilers = join_compilers(c2sm_compiler_file, module_compiler_file)

    joint_packages = join_packages(c2sm_packages_file, module_packages_file,
                                   external_packages_file)

    joint_packages = rename_cray_mpich_to_mpich(joint_packages)

    # currently the cuda version cannot be taken from the config-module
    #joint_packages = allign_cuda_versions(joint_packages, module_packages_file,
    #                                      '11.0')

    joint_packages = allow_xml_to_be_built(joint_packages)

    dump_to_yaml(joint_compilers, joint_compiler_file)
    dump_to_yaml(joint_packages, joint_packages_file)

    if args.publish_to_git:
        git_diff(args.machine)
