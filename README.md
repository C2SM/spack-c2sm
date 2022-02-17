# The C2SM Spack Deployment
Spack is the package manager used by C2SM and MeteoSwiss to install 
and deploy our software on supercomputers 
mostly at the Swiss Super Computing Center (CSCS)

[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://C2SM.github.io/spack-c2sm/)

[Detailed C2SM/MeteoSwiss spack documentation](https://c2sm.github.io/spack-c2sm/)

More about spack in general : [Official Spack documentation](https://spack.readthedocs.io/en/v0.15.4/).

## Quickly build your local cosmo with spack:

* **Tsa**

```bash
module load python/3.7.4
source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh # Source spack instance
spack info cosmo # Check available options 
spack spec cosmo # Check if your spec is precised enough, else precise more options
cd <cosmo_base_dir> # cosmo, not cosmo/cosmo
spack devbuildcosmo cosmo@dev-build # -t option for test, -c for clean build usually cosmo@dev-build%pgi is enough

```
* **Daint**

```bash
module load cray-python
source /project/g110/spack/user/daint/spack/share/spack/setup-env.sh # Source spack instance
spack info cosmo # Check available options 
spack spec cosmo # Check if your spec is precised enough, else precise more options
cd <cosmo_base_dir> # cosmo, not cosmo/cosmo
spack devbuildcosmo cosmo@dev-build # -t option for test, -c for clean build usually cosmo@dev-build%pgi is enough

```

## Automatically source the correct spack instance & python3 when using bash

If you want to automatically source the correct spack instance depending on the machine you are working on, you can add the following lines to your .bashrc file:

```bash
case $(hostname -s) in
      tsa*|arolla*) module load python; export SPACK_ROOT=/project/g110/spack/user/tsa/spack ;;
      daint*) module load cray-python; export SPACK_ROOT=/project/g110/spack/user/daint/spack ;;
esac
source $SPACK_ROOT/share/spack/setup-env.sh
```

## PR testing
To test a PR create a comment ```launch jenkins [--upstream] [--exclusive] ...```

with either
* a space separated list of predefined commands (see "supported commands")

or
* a raw spack command

```--upstream``` links the instance with the upstream spack-admin instance.

```--exclusive``` invokes only tests from the listed commands.

### What is tested:
Using predefined commands will trigger a set of packages, plus (if ```--exclusive``` is not set) all packages that depend on them. (See test_spack.py)

### Examples:

```launch jenkins atlas cuda zlib_ng```
No upstream will be used.
All tests from atlas, cuda and zlib_ng will be run, plus all tests from all packages that depend on them.

```launch jenkins --upstream all```
Upstream will be used.
All packages and all use cases will be tested.

```launch jenkins spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore```
No upstream will be used.
```spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore``` will be executed on all machines.

```launch jenkins --exclusive cosmo-dycore```
No upstream will be used.
Only the tests of cosmo-dycore will be run.

### Supported commands
Others:
* all (tests all use cases)
* a raw spack command

Package-name based:
* atlas
* atlas_utilities
* claw
* cosmo
* cosmo-dycore
* cosmo-eccodes-definitions
* cosmogrib-api
* cosmo-grib-api-definitions
* cuda
* dawn
* dawn4py
* dusk
* dyicon_benchmarks
* ecbuild
* eccodes
* eckit
* gridtools
* icon
* icondusk-e2e
* icontools
* int2lm
* libgrib1
* mpich
* oasis
* omnicompiler
* omni-xmod-pool
* openmpi
* serialbox
* xcodeml-tools
* zlib_ng
