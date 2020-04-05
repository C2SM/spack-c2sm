# The Meteoschweiz Spack Deployment

Official Spack documentation [Here](https://spack.readthedocs.io/en/latest/).

## Installation

### CSCS users

For the cscs users a spack instance including the mch packages and the mch machine configuration files will be maintained for both tsa and daint under _/project/g110/spack/user/'machine'/spack_. Therefore, if you are not interested in the developement of our spack packages and config files you can directly source those instances and skip the general installation section:

  	$ (cscs users): . /project/g110/spack/user/<machine>/spack/share/spack/setup-env.sh
	
#### Automatically source the correct spack instance when using bash

If you want to automatically source the correct spack instance depending on the machine you are working on, you can add the following lines to your .bashrc file:

	$ case $(hostname -s) in
	$ 	tsa*|arolla*) export SPACK_ROOT=/project/g110/spack/user/tsa/spack ;;
	$ 	daint*) export SPACK_ROOT=/project/g110/spack/user/daint/spack ;;
	$ esac
	$ source $SPACK_ROOT/share/spack/setup-env.sh
	
### General

**As said before a general installation is only needed if you wish to develop the mch packages/machines config files or if you are not a cscs user.**

First step is to clone this repository and use the available config.sh script to install your own spack instance with the corresponding mch packages and configuration files. 

Tell the script the machine you are working on using -m <machine> and where you want the instance to be installed using -i <spack-installation-directory>. You can also precise the spack version you want, or take the default value (last stable release). 
		
    $ git clone git@github.com:MeteoSwiss-APN/spack-mch.git
    $ cd spack-mch
    $ ./config.py -m <machine> -i <spack-installation-directory> -v <version> -r <repos.yaml-installation-directory> -p <spack packages, modules & stages installation-directory>
	
The -r option usually needs to point to the **site scope** of your newly installed spack-instance, that is, _$SPACK_DIR/etc/spack_. It can however also be used if you are a CSCS user and do not want to have your own spack instance *but still want to develop the mch-packages*. In that case, you can clone the spack-mch repo, let the -i, -m options void, BUT overwrite the *site scoped* repos.yaml files of the maintained spack instances by installing a new repos.yaml in your **user scope** _~/.spack_.

**Careful: the repos.yaml file is always modified in a way that it points to the spack-mch package repositories from which you call the config.sh script.**

Next and final step is to source your newly installed instance under _$SPACK_DIR/share/spack_ in order to activate it.

    $ . <spack-installation-directory>/share/spack/setup-env.sh

 ## Basic Usage

First thing to do when using spack is to check if the package you want to install is already available:

### Spack list

_list and search available packages_

	$ spack list <package>
	
Print the whole list of spack available packages

Second thing to do is to check the information of your package using the command:

### Spack info

_get detailed information on a particular package_

    $ spack info <package>
  
Get a list of all possible building configuration available such as: version available, list of dependencies and variants. Variants are a key-feature of spack since it describes which build configuration we want (i.e COSMO with target gpu or cpu).

Third step, you want to check how your package will be installed (i.e the spec of you package and its dependencies) before actually installing it.

### Spack spec

_show what would be installed, given a spec_

	$ spack spec <package>@<version>%<compiler> +<variants>
	
Finally you can install your package, using:

### Spack install

_build and install packages_

    $ spack install <package>@<version>%<compiler> +<variants>
 
Ex:
    
    $ spack install cosmo@master%pgi cosmo_target=gpu
    
This will clone the package, build it and install the chosen package plus all its dependencies under _/scratch/$USER/spack/install/tsa_ (see _config.yaml_ in the maching specific config file section for details). The build-stage of your package and its dependencies are not kept (add _--keep-stage_ after the install command in order to keep it). Module files are also created during this process and installed under _/scratch/$USER/spack/modules/_

You might want to run tests after the installation of your package. In that case you can use:

### Spack install --test=root 

_If 'root' is chosen, run package tests during installation for top-level packages (but skip tests for dependencies)._

	$ spack install --test=root cosmo@master%pgi cosmo_target=gpu
	
Submits the adequate testsuites for cosmo-dycore or cosmo after their installations. The results are printed out directly for cosmo-dycore but not for cosmo (you have to open the testsuite.out file). *Careful: If you use the +serialize variant of cosmo, you also need to add this command to your installation command*. 

If you want to submit your **tests manually** or after the installation, you first have to use the module of your package dependencies 

	$ module use /project/g110/spack-modules/'architecture'
	
and then load your package module:

	$ module load _/scratch/$USER/spack/modules/'architecture'/<package>/<version>-<hash>_
	
## Developer guide
	
### Spack dev-build

_developer build: build from code in current working directory_

    $ cd <package_base_directory>
    $ spack dev-build <package>@<version>%<compiler> +<variants>
    
If you do not want to git clone the source of the package you want to install, especially if you are developing, you can use a local source in order to install your package. In order to do so, first go to the base directory of the package and then use spack _dev-build_ instead of spack install.
    
The package, its dependencies and its modules will be still installed under _/scratch/$USER/spack/install_ & _/scratch/$USER/spack/modules/_

### Spack edit

_open package files in $EDITOR_

    $ spack edit <package>

Use this spack command in order to open the correspondig _package.py_ file and edit it directly.

### Machine specific config files

Are available under _spack/etc/spack_. Their structure is:
<ul>
	<li>-compilers.yaml (all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling)</li>
	<li>-packages.yaml (all info about the already installed dependencies, i.e their module names or paths)</li>
	<li>-modules.yaml (all info about the created modules, i.e which env variable or modules should be set once loaded)</li>
	<li>-config.yaml (specifies the main installation path and the main module installation path, where to find thebinaries etc.)</li>
	<li>-upstreams.yaml (specifies where to find the pre-installed software, that are under /project/g110/spack-install/<machine> </li>
	<li>-repos.yaml (specifies where to find the only mch packages that are stored in spack-mch repository)</li>
</ul>
