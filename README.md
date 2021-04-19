# The MeteoSwiss Spack Deployment
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://meteoswiss-apn.github.io/spack-mch/)

Official Spack documentation [Here](https://spack.readthedocs.io/en/latest/).

## Quickly build your local cosmo with spack (on Tsa):

```bash
module load python/3.7.4
source /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh # Source spack instance
spack info cosmo # Check available options 
spack spec cosmo # Check if your spec is precised enough, else precise more options
spack devbuildcosmo cosmo@dev-build # -t option for test, -c for clean build usually cosmo@dev-build%pgi is enough

```

 ## Basic Usage

First thing to do when using spack is to check if the package you want to install is already available:

### Spack list

_list and search available packages_

```bash
spack list <package>
```

Print the whole list of spack available packages

Second thing to do is to check the information of your package using the command:

### Spack info

_get detailed information on a particular package_

```bash
spack info <package>
```

Get a list of all possible building configuration available such as: version available, list of dependencies and variants. Variants are a key-feature of spack since it describes which build configuration we want (i.e COSMO with target gpu or cpu).

Third step, you want to check how your package will be installed (i.e the spec of you package and its dependencies) before actually installing it.

### Spack spec

_show what would be installed, given a spec_

```bash
spack spec <package>@<version>%<compiler> +<variants>
```

Finally you can install your package, using:

### Spack install

_build and install packages_

```bash
spack install <package>@<version>%<compiler> +<variants>
```

Ex:

```bash
spack install cosmo@master%pgi cosmo_target=gpu
```

This will clone the package, build it and install the chosen package plus all its dependencies under _/scratch/$USER/spack-install/tsa_ (see _config.yaml_ in the maching specific config file section for details). The build-stage of your package and its dependencies are not kept (add _--keep-stage_ after the install command in order to keep it). Module files are also created during this process and installed under _/scratch/$USER/modules/_

You might want to run tests after the installation of your package. In that case you can use:

### Spack install --test=root

_If 'root' is chosen, run package tests during installation for top-level packages (but skip tests for dependencies)._

```bash
spack install --test=root -v cosmo@master%pgi cosmo_target=gpu
```

Submits the adequate testsuites for cosmo-dycore or cosmo after their installations. The results are printed out directly for cosmo-dycore but not for cosmo (you have to open the testsuite.out file). *Careful: If you use the +serialize variant of cosmo, you also need to add this command to your installation command*.

If you want to submit your **tests manually** or after the installation, you first have to load the build environement of your spec:

```bash
spack build-env <spec> -- bash
```


## Developer guide

### Spack dev-build

_developer build: build from code in current working directory_

```bash
cd <package_base_directory>
spack dev-build <package>@<version>%<compiler> +<variants>
```

If you do not want to git clone the source of the package you want to install, especially if you are developing, you can use a local source in order to install your package. In order to do so, first go to the base directory of the package and then use spack _dev-build_ instead of spack install.

The package, its dependencies and its modules will be still installed under _/scratch/$USER/spack-install_ & _/scratch/$USER/modules/_
Notice that once installed, the package will not be rebuilt at the next attempt to _spack dev-build_, even if the sources of the local directory have changed.
In order to force spack to build the local developments anytime, you need to avoid the installation phase

```bash
spack dev-build --until build <package>@<version>%<compiler> +<variants>
```

### Spack edit

_open package files in $EDITOR_

```bash
spack edit <package>
```

Use this spack command in order to open the correspondig _package.py_ file and edit it directly.

### Machine specific config files

Are available under _spack/etc/spack_. Their structure is:
 - compilers.yaml (all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling)
 - packages.yaml (all info about the already installed dependencies, i.e their module names or paths)
 - modules.yaml (all info about the created modules, i.e which env variable or modules should be set once loaded)
 - config.yaml (specifies the main installation path and the main module installation path, where to find thebinaries etc.)
 - upstreams.yaml (specifies where to find the pre-installed software, that are under /project/g110/spack-install/<machine> 
 - repos.yaml (specifies where to find the only mch packages that are stored in spack-mch repository)
