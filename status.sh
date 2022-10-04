#!/bin/sh

echo ">>> GIT STATUS <<<"
git status
echo ""
echo ">>> SPACK --VERSION <<<"
spack --version
echo ""
echo ">>> SPACK_SYSTEM_CONFIG_PATH <<<"
echo $SPACK_SYSTEM_CONFIG_PATH
echo ""
echo ">>> MACHINE <<<"
env-setup/machine.sh
echo ""
echo ""
echo ">>> PYTHON --VERSION <<<"
python --version
echo ""
echo ">>> PYTHON3 --VERSION <<<"
python3 --version
echo ""
echo ">>> GIT --VERSION <<<"
git --version
echo ""