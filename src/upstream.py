import shutil
import sys
import os
from ruamel import yaml


def read_upstream_from_spack_yaml(config_dir):
    spack_yaml = os.path.join(config_dir, 'spack.yaml')
    y = yaml.YAML(typ='unsafe', pure=True)
    spack_config = y.load(open(spack_yaml, 'r'))
    upstream = spack_config['spack']['config']['install_tree']['root']
    return upstream


def delete_upstream(upstream):
    print(f'Delete upstream {upstream}')
    shutil.rmtree(upstream)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError('Need path to folder containing a spack.yaml')
    else:
        delete_upstream(read_upstream_from_spack_yaml(sys.argv[2]))
