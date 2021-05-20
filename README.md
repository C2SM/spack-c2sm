# The C2SM Spack Deployment
Spack is the package manager used by C2SM and MeteoSwiss to install 
and deploy our software on supercomputers 
mostly at the Swiss Super Computing Center (CSCS)

[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://MeteoSwiss-APN.github.io/spack-mch/)

[Detailed C2SM/MeteoSwiss spack documentation](https://meteoswiss-apn.github.io/spack-mch/)

More about spack in general : [Official Spack documentation](https://spack.readthedocs.io/en/latest/).

## Quickly build your local cosmo with spack:

* **Tsa**

```bash
module load python/3.7.4
source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh # Source spack instance
spack info cosmo # Check available options 
spack spec cosmo # Check if your spec is precised enough, else precise more options
spack devbuildcosmo cosmo@dev-build # -t option for test, -c for clean build usually cosmo@dev-build%pgi is enough

```
* **Daint**

```bash
module load cray-python
source /project/g110/spack/user/daint/spack/share/spack/setup-env.sh # Source spack instance
spack info cosmo # Check available options 
spack spec cosmo # Check if your spec is precised enough, else precise more options
spack devbuildcosmo cosmo@dev-build # -t option for test, -c for clean build usually cosmo@dev-build%pgi is enough

```
