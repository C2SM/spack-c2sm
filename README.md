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

### Machine specific config files

Are available under _spack/etc/spack_. Their structure is:
 - compilers.yaml (all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling)
 - packages.yaml (all info about the already installed dependencies, i.e their module names or paths)
 - modules.yaml (all info about the created modules, i.e which env variable or modules should be set once loaded)
 - config.yaml (specifies the main installation path and the main module installation path, where to find thebinaries etc.)
 - upstreams.yaml (specifies where to find the pre-installed software, that are under /project/g110/spack-install/<machine> 
 - repos.yaml (specifies where to find the only mch packages that are stored in spack-mch repository)
