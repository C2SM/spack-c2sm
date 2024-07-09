#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" ; pwd -P )

if [[ "$#" == 1 ]]; then
    machine="$1"
else
    machine="$( "$parent_dir"/src/machine.sh )"
fi

if [[ ${machine:0:1} == "/" ]]; then
    uenv_mount=$machine
    machine=uenv
    export SPACK_SYSTEM_CONFIG_PATH="$uenv_mount"/config
    export SPACK_USER_CONFIG_PATH="$parent_dir"/sysconfigs/"$machine"
else
    export SPACK_SYSTEM_CONFIG_PATH="$parent_dir"/sysconfigs/"$machine"
    export SPACK_USER_CONFIG_PATH="$parent_dir"/user-config
fi

export SPACK_USER_CACHE_PATH="$parent_dir"/user-cache

. "$parent_dir"/spack/share/spack/setup-env.sh

echo Spack configured for "$machine".
