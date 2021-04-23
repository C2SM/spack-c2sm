Spack Installation
==================

Preinstalled Instance
----------------------
For the CSCS users a spack instance including the mch packages and the mch machine 
configuration files will be maintained for both tsa and daint 
under */project/g110/spack/user/<machine>/spack*. 
Therefore, if you are not interested in the developement of our 
spack packages and config files you can directly source those instances:

.. code-block:: bash

  # module load python >= 3.6
  source /project/g110/spack/user/<machine>/spack/share/spack/setup-env.sh

Automatically source preinstalled Spack instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to automatically source the correct spack instance depending on the machine you are working on, you can add the following lines to your .bashrc file:

.. code-block:: bash

    case $(hostname -s) in
          tsa*|arolla*) module load python/3.7.4; export SPACK_ROOT=/project/g110/spack/user/tsa/spack ;;
          daint*) module load cray-python; export SPACK_ROOT=/project/g110/spack/user/daint/spack ;;
    esac
    source $SPACK_ROOT/share/spack/setup-env.sh

Error: Initialization hangs
"""""""""""""""""""""""""""""""
If `source $SPACK_ROOT/share/spack/setup-env.sh` hangs, clean your cache:

.. code-block:: bash

    rm -rf ~/.spack/cray ~/.spack/cache

Then try again.

Error: Could not determine host
""""""""""""""""""""""""""""""""
In case you have anything printing the hostname to the terminal in your .bashrc like

.. code-block:: bash
    
    echo $(hostname) 

the setup-env.sh script for Spack does not work. 
A possible workaround is to direct the "echo" to the stderr:

.. code-block:: bash
    
    echo $(hostname) >&2

Your own Spack instance
-------------------------

**Installing your own spack instance is only needed if you wish to 
develop the mch packages/machines config files or if you are not a cscs user.**

First step is to clone this repository and use the available config.sh script to install your own spack instance with the corresponding mch packages and configuration files.

Tell the script the machine you are working on using -m \<machine> and where you want the instance to be installed using -i <spack-installation-directory>. You can also precise the spack version you want, or take the default value (last stable release).

Notice the requirements.txt will install all python dependencies required by spack.

.. code-block:: bash

    git clone git@github.com:MeteoSwiss-APN/spack-mch.git
    virtualenv .venv
    source  .venv/bin/activate
    pip3 install -r requirements.txt

    cd spack-mch
    ./config.py -m <machine> -i <spack-installation-directory> -v <version> -r <repos.yaml-installation-directory> -p <spack packages, modules & stages installation-directory> -u <ON or OFF, install upstreams.yaml>

Note the config will append *spack/* directory to <spack-installation-directory>.  
The -r option usually needs to point to the **site scope** of your spack-instance installation, that is, *<spack-installation-directory>/spack/etc/spack*. 
It can however also be used if you are a CSCS user and do not want to have your own spack instance 
*but still want to develop the mch-packages*. In that case, you can clone the 
spack-mch repo, let the -i, -m options void, BUT overwrite the *site scoped* repos.yaml 
files of the maintained spack instances by installing a new 
repos.yaml in your **user scope** *~/.spack*.

Example:

.. code-block:: bash

    SPACK_DIR=$SCRATCH
    ./config.py -m tsa -i $SPACK_DIR -r $SPACK_DIR/spack/etc/spack -u ON

**Careful: the repos.yaml file is always modified in a way that it points to the spack-mch package repositories from which you call the config.sh script.**

Next and final step is to source your newly installed instance under *$SPACK_DIR/share/spack* 
in order to activate it.

.. code-block:: bash

    source <spack-installation-directory>/share/spack/setup-env.sh

Machine specific config files
------------------------------
There is a set of .yaml files that define machine specific things like compilers, modules, preinstalled packages
and more.

They are available under spack/etc/spack. Their structure is:

* compilers.yaml: all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling
* packages.yaml: all info about the already installed dependencies, i.e their module names or paths
* modules.yaml: all info about the created modules, i.e which env variable or modules should be set once loaded
* config.yaml: specifies the main installation path and the main module installation path, where to find thebinaries etc.
* upstreams.yaml: specifies where to find the pre-installed software, that are under /project/g110/spack-install/
* repos.yaml: specifies where to find the only mch packages that are stored in spack-mch repository
