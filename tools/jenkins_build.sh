echo ${GITHUB_COMMENT}
spec=${GITHUB_COMMENT#"launch jenkins "}

# install spack temp instance with branch config files and mch spack packages
./tools/config.py -m tsa -i . -r ./spack/etc/spack -p $PWD/spack -u OFF

# source spack instance
. spack/share/spack/setup-env.sh

echo "spack install $spec"
spack install $spec
