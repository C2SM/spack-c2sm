#!/bin/bash

conf_dir="$parent_dir"/sysconfigs/uenv
conf_files=(compilers.yaml upstreams.yaml packages.yaml)

# lock the current spack instance to a specific uenv
if [[ ! -f $uenv_mount/meta/hash ]]; then
    echo "ERROR: file $uenv_mount/meta/hash not found, spack-c2sm cannot be configured for this uenv"
    return 1
fi
uenv_hash=$(cat $uenv_mount/meta/hash)
if [[ -f "$conf_dir"/uenv.hash ]]; then
    local_hash=$(cat "$conf_dir"/uenv.hash)
    if [[ $uenv_hash != $local_hash ]]; then
        echo "ERROR: This spack-c2sm instance was already once configured with a different uenv."
        echo "       Please reuse the same uenv with the current instance or setup a fresh spack-c2sm"
        echo "       with any uenv."
        return 1
    fi
else
    echo $uenv_hash > $conf_dir/uenv.hash
fi

# Link configuration files to sysconfig
for conf_file in ${conf_files[@]}; do
    [[ -f $conf_dir/$conf_file ]] || ln -s $uenv_mount/config/$conf_file $conf_dir
done
[[ -d "$parent_dir"/repos/uenv ]] || ln -s $uenv_mount/repo "$parent_dir"/repos/uenv
