#!/usr/bin/python3

import os
import subprocess

spack_c2sm_path = os.path.dirname(os.path.realpath(__file__)) + '/../..'


def spack(command):
    subprocess.run(f'. {spack_c2sm_path}/setup-env.sh; spack {command}',
                   check=True,
                   shell=True)


def spack_info(package):
    spack(f'info {package}')


def spack_spec(package):
    spack(f'spec {package}')
