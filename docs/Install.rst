Spack Instance
==============

To get an instance, git clone spack-c2sm and its submodule spack.
'--depth 1' and '--shallow-submodules' are optional, but they reduce the amount of downloaded data.

.. code-block:: bash

    git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git

On **Daint, Dom, Tsa and Arolla** setup-env.sh automatically detects the machine. You may simply execute

.. code-block:: bash

    source spack-c2sm/setup-env.sh

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
* repos.yaml: specifies where to find the only mch packages that are stored in spack-c2sm repository
