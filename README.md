# The MeteoSwiss Spack Deployment
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://jonasjucker.github.io/spack-mch/)

[Official Spack documentation](https://spack.readthedocs.io/en/latest/).

## Quickly build your local cosmo with spack (on Tsa):

```bash
module load python/3.7.4
source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh # Source spack instance
spack info cosmo # Check available options 
spack spec cosmo # Check if your spec is precised enough, else precise more options
spack devbuildcosmo cosmo@dev-build # -t option for test, -c for clean build usually cosmo@dev-build%pgi is enough

```
