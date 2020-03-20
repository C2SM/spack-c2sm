# The Meteoschweiz Spack Deployment

# <img src="https://cdn.rawgit.com/spack/spack/develop/share/spack/logo/spack-logo.svg" width="64" valign="middle" alt="Spack"/> Spack

Official Spack documentation [below](#-spack).

## Using the official MCH instance for CSCS

For CSCS environment, we maintain a spack instance under _/project/g110/spack/user/'machine'/spack_. 
If you want to use spack to build mch packages and you dont need to develop within the spack packages you can simply use that instance:

$ . /project/g110/spack/user/<machine>/spack/share/spack/setup-env.sh

## Installing your spack instance and mch packages

If you need to modify the spack packages for the mch repository you should install your own instance. 
First git clone the Meteoswiss spack configuration repository and install your own spack instance using the available config.sh script. 
Tell the script the machine you are working on using -m <machine> and where you want the instance to be installed using -i <spack-installation-directory>. 
You can also precise the spack version you want, or take the default value (last stable release).

    $ git clone git@github.com:MeteoSwiss-APN/spack-mch.git
    $ cd spack-mch
    $ ./config.sh -m <machine> -i <spack-installation-directory> -v <version>

Finally you need to source the spack file under spack/share/spack in order to activate spack.

    $ . <spack-installation-directory>/share/spack/setup-env.sh

## Building software on tsa/daint

You are then able to build any packages available (_spack list_ to print the whole list of available packages)

    $ spack install <package>@<version>%<compiler> +<variants>
 
Ex:
    
    $ spack install cosmo@master%pgi cosmo_target=gpu
    

This will clone the package, build it and then install the chosen package and all its dependencies under _/scratch/$USER/install/tsa_ (see _config.yaml_ file section for details). The build-stage of your package and its dependencies are not kept (add _--keep-stage_ after the install command in order to keep it). Module files are also created during this process and installed under _/scratch/$USER/modules/_

## CSCS users: automatically source the correct spack instance when using bash

As said above, if you are not wanting to develop for the spack-mch you can just source the correct spack instance depending on the machine you are working on. Add those line to your .bashrc file if you want to do that automatically when opening a new terminal.

	$ case $(hostname -s) in
	$ 	tsa*|arolla*) export SPACK_ROOT=/project/g110/spack/user/tsa/spack ;;
	$ 	daint*) export SPACK_ROOT=/project/g110/spack/user/daint/spack ;;
	$ esac
	$ source $SPACK_ROOT/share/spack/setup-env.sh
	
## Spack install --test=root 

Submits the adequate testsuites for cosmo-dycore and cosmo. The results are printed directly for cosmo-dycore but not for cosmo (you have to open the testsuite.out file). Also needed if you use the +serialize variant with cosmo. If you want to submit the **test manually** or after the installation, you can load the module of your package (module use _/project/g110/spack-modules/'architecture'_) created during its installation and then submit the tests.
	
## Dev-building software on tsa/daint

If you do not want to git clone the source of the package you want to install, especially if you are developing, you can use a local source in order to install your package. In order to do so, first go to the base directory of the package and then use spack _dev-build_ instead of spack install 
    
    $ cd <package_base_directory>
    $ spack dev-build <package>@<version>%<compiler> +<variants>
    
The package, its dependencies and its modules will be still installed under _/scratch/$USER/install/tsa_ & _/scratch/$USER/modules/_

## Spack info

Use the spack command

    $ spack info <package>
    
in order to get a list of all possible building configuration available such as: version available, list of dependencies and variants. Variants are a key-feature of spack since it tells it which build configuration we want (i.e COSMO with target gpu or cpu)

## Spack edit

Use the spack command

    $ spack edit <package>

in order to open the correspondig _package.py_ file and edit it directly

## Machine specific config files

Are available under _spack/etc/spack_. Their structure is:
<ul>
	<li>-compilers.yaml (all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling)</li>
	<li>-packages.yaml (all info about the already installed dependencies, i.e their module names or paths)</li>
	<li>-modules.yaml (all info about the created modules, i.e which env variable or modules should be set once loaded)</li>
	<li>-config.yaml (specifies the main installation path and the main module installation path, where to find thebinaries etc.)</li>
	<li>-upstreams.yaml (specifies where to find the pre-installed software, that are under /project/g110/spack-install/<machine> </li>
	<li>-repos.yaml (specifies where to find the only mch packages that are stored in spack-mch repository)</li>
</ul>

