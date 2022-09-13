#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

# Make 'python' refer to 'python3'
if test -f "/etc/xthostname"; then
    case $(cat /etc/xthostname) in
        manali*|balfrin*) module load python/3.9.13-11.3.0-bteihqu;;
        daint*|dom*) module load cray-python;;
    esac
else
    case $(hostname -s) in
        tsa*|arolla*) module load python;;
    esac
fi

python3 "$parent_dir"/install_sysconfig.py
source "$parent_dir"/spack/share/spack/setup-env.sh
