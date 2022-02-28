#!/bin/bash

module load daint-gpu
module load cray-python
module load spack-config

export SPACK_USER_CONFIG_PATH=$(pwd)

./config.py -m daint -i . -u OFF

. spack/share/spack/setup-env.sh

rm packages.yaml

spack external find --not-buildable --scope=user

cat packages.yaml >> sysconfig/daint/packages.yaml

rm packages.yaml

./config.py -m daint -i . -u OFF

spack spec int2lm@c2sm-master%nvhpc




