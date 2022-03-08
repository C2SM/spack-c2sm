#!/usr/bin/env python3
from ruamel import yaml
import warnings
import subprocess
import os

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)


def load_from_yaml(file):
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


spack_config_root = os.environ['SPACK_SYSTEM_CONFIG_PATH']

os.environ["SPACK_USER_CONFIG_PATH"] = os.getcwd()

command = [
    "./config.py", "-i", ".", "-u", "OFF", "-m", "daint", "--no_yaml_copy",
    "ON"
]
subprocess.run(command, check=True)
command = [
    'bash', '-c', "source spack/share/spack/setup-env.sh && \
           spack external find --not-buildable --scope=user"
]
subprocess.run(command, check=True)

os.environ.pop("SPACK_USER_CONFIG_PATH")

# compilers
c2sm_compilers = load_from_yaml(
    'sysconfigs/templates/daint/compilers.yaml')['compilers']
cscs_compilers = load_from_yaml(
    f'{spack_config_root}/compilers.yaml')['compilers']
joint_compilers = remove_duplicate_compilers(c2sm_compilers, cscs_compilers,
                                             ['compiler', 'spec'])

joint_yaml = {}
joint_yaml['compilers'] = joint_compilers
yaml.safe_dump(joint_yaml,
               open('sysconfigs/daint/compilers.yaml', 'w'),
               default_flow_style=False)

# packages
c2sm_packages = load_from_yaml(
    'sysconfigs/templates/daint/packages.yaml')['packages']
cscs_packages = load_from_yaml(
    f'{spack_config_root}/packages.yaml')['packages']
external_packages = load_from_yaml('packages.yaml')['packages']

joint_packages = remove_duplicate_packages(c2sm_packages, cscs_packages,
                                           external_packages)

joint_yaml = {}
joint_yaml['packages'] = joint_packages
yaml.safe_dump(joint_yaml,
               open('sysconfigs/daint/packages.yaml', 'w'),
               default_flow_style=False)
