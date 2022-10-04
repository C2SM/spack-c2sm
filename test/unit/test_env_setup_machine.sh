#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

if [ $($parent_dir/../../env-setup/machine.sh) == $1 ]; then
    echo PASS
    exit 0
else
    echo FAIL
    exit 1
fi