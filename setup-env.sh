#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" ; pwd -P )

if [[ "$#" == 1 ]]; then
    upstream="$1"
    if [[ $upstream == "euler" ]]; then
        export SPACK_SYSTEM_CONFIG_PATH="$parent_dir"/sysconfigs/euler
    else
        export SPACK_UENV_PATH="$upstream"
        export SPACK_SYSTEM_CONFIG_PATH="$upstream"/config
    fi
fi

export SPACK_USER_CONFIG_PATH="$parent_dir"/user-config
export SPACK_USER_CACHE_PATH="$parent_dir"/user-cache
. "$parent_dir"/spack/share/spack/setup-env.sh

if [[ -n "$upstream" ]]; then
    echo Spack configured with upstream "$upstream".
else
    echo Spack configured with no upstream.
fi
