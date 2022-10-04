#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

. "$parent_dir"/spack/share/spack/setup-env.sh

mkdir "$parent_dir"/sysconfigs/"$1"

spack env create "$1"
spack env activate "$1"
spack compiler find
spack external find --all
spack config get compilers > "$parent_dir"/sysconfigs/"$1"/compilers.yaml
spack config get packages > "$parent_dir"/sysconfigs/"$1"/packages.yaml
spack env deactivate
spack env remove "$1" -y
