#!/bin/sh

parent_dir=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

echo ">>> GIT --VERSION <<<"
git --version
echo ""
echo ">>> GIT STATUS <<<"
git -C "$parent_dir" status
echo ""
echo ">>> PYTHON --VERSION <<<"
python --version
echo ""
echo ">>> PYTHON3 --VERSION <<<"
python3 --version
echo ""
echo ">>> SPACK --VERSION <<<"
spack --version
echo ""
echo ">>> SPACK_SYSTEM_CONFIG_PATH <<<"
echo $SPACK_SYSTEM_CONFIG_PATH
echo ""
echo ">>> MACHINE <<<"
"$parent_dir"/src/machine.sh
echo ""