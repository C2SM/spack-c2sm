#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

if [ "$#" -eq 1 ]; then
    machine="$1"
else
    machine="$( . "$parent_dir"/env-setup/machine.sh )"
fi

#. "$parent_dir"/env-setup/load_python.sh
#python "$parent_dir"/install_sysconfig.py

export SPACK_SYSTEM_CONFIG_PATH="$parent_dir"/sysconfigs/"$machine"
. "$parent_dir"/spack/share/spack/setup-env.sh

echo Spack configured for "$machine".