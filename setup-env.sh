#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" ; pwd -P )

export SPACK_USER_CONFIG_PATH="${parent_dir}/user-config/default"

if [[ "$#" == 1 ]]; then
    upstream="$1"
    if [[ $upstream == "euler" ]]; then
        export SPACK_SYSTEM_CONFIG_PATH="${parent_dir}/sysconfigs/euler"
        export SPACK_USER_CONFIG_PATH="${parent_dir}/user-config/default"
    else
        # NOTE: SPACK_UENV_PATH used tests/spack_commands.py
        export SPACK_UENV_PATH="${upstream}"
        export SPACK_SYSTEM_CONFIG_PATH="${upstream}/config"
        export SPACK_USER_CONFIG_PATH="${parent_dir}/user-config/alps"
    fi
fi

export SPACK_USER_CACHE_PATH="${parent_dir}/user-cache"
. "${parent_dir}/spack/share/spack/setup-env.sh"

if [[ -n "$upstream" ]]; then
    echo Spack configured with upstream "${upstream}".
else
    echo Spack configured with no upstream.
fi
