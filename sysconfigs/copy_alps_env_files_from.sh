#!/bin/bash

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" ; pwd -P )

if [[ "$#" == 1 ]]; then
    env_path="$1"
    machine="$( "$parent_dir"/../src/machine.sh )"
else
    echo "Requires path to environment as argument!"
    exit 0
fi

# Copy files
cp "$env_path"/config/compilers.yaml "$parent_dir/$machine"
cp "$env_path"/config/upstreams.yaml "$parent_dir/$machine"
cp -r "$env_path"/repo/* "$parent_dir"/../repos/alps

# Display success message
echo "Files copied successfully."
