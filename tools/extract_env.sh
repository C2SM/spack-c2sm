#!/bin/bash

TEMP=$@
eval set -- "$TEMP --"
while true; do
    case "$1" in
        --env_dir|-e) env_dir=$2; shift 2;;
        --help|-h) help_enabled=yes; fwd_args="$fwd_args $1"; shift;;
        -- ) shift; break ;;
        * ) fwd_args="$fwd_args $1"; shift ;;
    esac
done

if [[ "${help_enabled}" == "yes" ]]; then
    echo "Available Options:"
    echo "* --env_dir.  |-e {spack-build-env.txt directory} The directory where spack-build-env.txt is located, Default: \$(pwd)"
    echo "* --help.  |-h {print help}"
    exit 0
fi

touch env.txt

eval `grep -rw $env_dir/spack-build-env.txt -e LOADEDMODULES`
eval `grep -rw $env_dir/spack-build-env.txt -e SPACK_RUN_ENV`

IFS=':' read -r -a module_array <<< "$LOADEDMODULES"
for module in ${module_array[@]}; do
    echo "module load $module" >> env.txt
done

for item in ${SPACK_RUN_ENV[@]}; do
      echo $item >> env.txt
done
