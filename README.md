# C2SM and MeteoSwiss' extension of spack
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://C2SM.github.io/spack-c2sm/)

Spack is the package manager used by C2SM and MeteoSwiss to install and deploy our software on supercomputers, mostly at the Swiss Super Computing Center (CSCS).

Documentation of [spack-C2SM](https://C2SM.github.io/spack-c2sm/)

Documentation of [spack](https://spack.readthedocs.io/en/v0.18.1/)

## Quick start for Daint, Dom, Tsa
Clone the repo
```bash
git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git #TODO: Remove branch!
```
Get spack in your command line
```bash
source spack-c2sm/setup-env.sh
```