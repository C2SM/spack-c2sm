#!/usr/bin/env python3
from ruamel import yaml
import warnings
import subprocess
import os
import argparse

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)


def load_from_yaml(file):
    print(f'Load yaml file: {file}')
    with open(file, "r") as f:
        try:
            data = yaml.load(f)
        except yaml.error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))
    return data


def specs_from_list_with_keys(spec_list, key_1, key_2):
    specs = set()
    for item in spec_list:
        specs.add(item[key_1][key_2])

    return specs


def dictkeys_as_set(dict):
    keys = set()
    for spec in dict.keys():
        keys.add(spec)
    return keys


def remove_duplicate_compilers(c2sm, cscs, keys):
    c2sm_specs = specs_from_list_with_keys(c2sm, keys[0], keys[1])
    cscs_specs = specs_from_list_with_keys(cscs, keys[0], keys[1])

    duplicates = (c2sm_specs & cscs_specs)
    for dupl in duplicates:
        cscs_specs.remove(dupl)

    c2sm = [item for item in c2sm if item[keys[0]][keys[1]] in c2sm_specs]
    cscs = [item for item in cscs if item[keys[0]][keys[1]] in cscs_specs]

    return c2sm + cscs


def remove_from_dict(dict, filter):
    filtered = {}
    for key, value in dict.items():
        if key in filter:
            filtered[key] = value
    return filtered


def remove_duplicate_packages(c2sm, cscs, external):
    c2sm_package_names = dictkeys_as_set(c2sm)
    cscs_package_names = dictkeys_as_set(cscs)
    external_package_names = dictkeys_as_set(external)

    duplicates = (c2sm_package_names & cscs_package_names)
    for dupl in duplicates:
        cscs_package_names.remove(dupl)

    duplicates = (c2sm_package_names & external_package_names)
    for dupl in duplicates:
        external_package_names.remove(dupl)

    c2sm = remove_from_dict(c2sm, c2sm_package_names)
    cscs = remove_from_dict(cscs, cscs_package_names)
    external = remove_from_dict(external, external_package_names)

    c2sm.update(cscs)
    c2sm.update(external)
    return c2sm


def allign_cuda_versions(joint, cscs, version):
    spec_joint = joint['cuda']['externals'][0]['spec']
    specs_cscs = []
    prefix_cscs = []
    for i in range(len(cscs['cuda']['externals'])):
        specs_cscs.append(cscs['cuda']['externals'][i]['spec'])
        prefix_cscs.append(cscs['cuda']['externals'][i]['prefix'])

    i = 0
    for spec in specs_cscs:
        if version in spec:
            prefix = prefix_cscs[i]
            break
        i += 1

    joint['cuda']['externals'][0]['prefix'] = prefix

    return joint


def spack_external_find(machine, packages_file):

    print(f'Find externals on {machine}')

    os.environ["SPACK_USER_CONFIG_PATH"] = os.getcwd()

    if os.path.exists(packages_file): os.remove(packages_file)

    command = [
        "./config.py", "-i", ".", "-u", "OFF", "-m", machine, "--no_yaml_copy",
        "ON"
    ]
    subprocess.run(command, check=True)
    command = [
        'bash', '-c', "source spack/share/spack/setup-env.sh && \
               spack external find --not-buildable --scope=user"
    ]
    subprocess.run(command, check=True)

    os.environ.pop("SPACK_USER_CONFIG_PATH")


def dump_yaml_to_file(yaml_content, yaml_name):
    print(f'Dump to yaml: {yaml_name}')
    yaml.safe_dump(yaml_content,
                   open(yaml_name, 'w'),
                   default_flow_style=False)


def join_compilers(primary, secondary):
    print('Join compilers')

    primary_compilers = load_from_yaml(primary)
    secondary_compilers = load_from_yaml(secondary)

    joint = {}
    joint['compilers'] = remove_duplicate_compilers(
        primary_compilers['compilers'], secondary_compilers['compilers'],
        ['compiler', 'spec'])

    return joint


def join_packages(primary, secondary, external):
    print('Join packages')
    primary_packages = load_from_yaml(primary)['packages']
    secondary_packages = load_from_yaml(secondary)['packages']
    external_packages = load_from_yaml(external)['packages']

    primary_package_names = dictkeys_as_set(primary_packages)
    secondary_package_names = dictkeys_as_set(secondary_packages)
    external_package_names = dictkeys_as_set(external_packages)

    duplicates = (primary_package_names & secondary_package_names)
    for dupl in duplicates:
        secondary_package_names.remove(dupl)

    duplicates = (primary_package_names & external_package_names)
    for dupl in duplicates:
        external_package_names.remove(dupl)

    primary = remove_from_dict(primary_packages, primary_package_names)
    secondary = remove_from_dict(secondary_packages, secondary_package_names)
    external = remove_from_dict(external_packages, external_package_names)

    primary.update(secondary)
    primary.update(external)
    dict = {}
    dict['packages'] = primary

    return dict


def rename_cray_mpich_to_mpich(packages):
    print('Rename cray-mpich to mpich')
    cray_mpich = packages['packages']['cray-mpich']

    spec = cray_mpich['externals'][0]['spec']
    spec = spec.replace('cray-', '')

    cray_mpich['externals'][0]['spec'] = spec

    packages['packages']['mpich'] = cray_mpich

    packages['packages']['mpich']['buildable'] = False

    packages['packages'].pop('cray-mpich')

    return packages


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--machine', '-m', dest='machine')
    args = parser.parse_args()

    spack_config_root = os.environ['SPACK_SYSTEM_CONFIG_PATH']

    c2sm_compiler_file = f'sysconfigs/templates/{args.machine}/compilers.yaml'
    module_compiler_file = f'{spack_config_root}/compilers.yaml'
    joint_compiler_file = f'sysconfigs/{args.machine}/compilers.yaml'

    c2sm_packages_file = f'sysconfigs/templates/{args.machine}/packages.yaml'
    module_packages_file = f'{spack_config_root}/packages.yaml'
    external_packages_file = 'packages.yaml'
    joint_packages_file = f'sysconfigs/{args.machine}/packages.yaml'

    spack_external_find(args.machine, external_packages_file)

    joint_compilers = join_compilers(c2sm_compiler_file, module_compiler_file)

    joint_packages = join_packages(c2sm_packages_file, module_packages_file,
                                   external_packages_file)

    joint_packages = rename_cray_mpich_to_mpich(joint_packages)

    dump_yaml_to_file(joint_compilers, joint_compiler_file)
    dump_yaml_to_file(joint_packages, joint_packages_file)
