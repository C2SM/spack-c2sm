#!/usr/bin/env python3
from ruamel import yaml
import warnings
import os

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

def load_from_yaml(file):
    with open(file,
              "r") as f:
        try:
            data = yaml.load(f)
        except yaml.error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))
    return data

def create_set_of_specs(spec_list,key_1,key_2):
    specs=set()
    for item in spec_list:
        specs.add(item[key_1][key_2])

    print(specs)
    return specs


def remove_duplicate_entries(c2sm,cscs):
    print(c2sm,cscs)

    c2sm_specs=create_set_of_specs(c2sm,'compiler','spec')
    cscs_specs=create_set_of_specs(cscs,'compiler','spec')

    duplicates=(c2sm_specs & cscs_specs)
    for dupl in duplicates:
        cscs_specs.remove(dupl)

    c2sm=[item for item in c2sm if item['compiler']['spec'] in c2sm_specs]
    cscs=[item for item in cscs if item['compiler']['spec'] in cscs_specs]

    return c2sm + cscs




c2sm_compilers=load_from_yaml('sysconfigs/daint/compilers.yaml')['compilers']

spack_config_root=os.getenv('SPACK_SYSTEM_CONFIG_PATH')
cscs_compilers=load_from_yaml(f'{spack_config_root}/compilers.yaml')['compilers']
joint_compilers=remove_duplicate_entries(c2sm_compilers,cscs_compilers)
print(joint_compilers)

yaml_dummy=load_from_yaml('sysconfigs/daint/compilers.yaml')
yaml_dummy['compilers']=joint_compilers

yaml.safe_dump(yaml_dummy,
    open('joint.yaml', 'w'),
    default_flow_style=False)

