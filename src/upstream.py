import shutil
import sys
import os

sys.path.insert(1, 'spack/lib/spack/external')
from ruamel import yaml


def read_upstream_from_spack_yaml(config_dir):
    spack_yaml = os.path.join(config_dir, 'spack.yaml')
    with open(spack_yaml, 'r') as f:
        spack_config = yaml.load(f)
    upstream = spack_config['spack']['config']['install_tree']['root']
    return upstream


def delete_upstream(upstream):
    print(f'Delete upstream {upstream}')
    shutil.rmtree(upstream, ignore_errors=True)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        raise ValueError('Need path to folder containing a spack.yaml')
    else:
        delete_upstream(read_upstream_from_spack_yaml(sys.argv[1]))
