#!/bin/bash

# TODO
# Place holder to lock the current spack instance to a specific uenv
# Maybe use a hash of the full recipe

conf_dir="$parent_dir"/sysconfigs/uenv
conf_files=(compilers.yaml upstreams.yaml packages.yaml)

for conf_file in ${conf_files[@]}; do
    [[ -f $conf_dir/$conf_file ]] || ln -s $uenv_mount/config/$conf_file $conf_dir
done
[[ -d "$parent_dir"/repos/uenv ]] || ln -s $uenv_mount/repo "$parent_dir"/repos/uenv
