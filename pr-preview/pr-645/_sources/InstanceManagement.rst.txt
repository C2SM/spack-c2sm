How to manage your own Spack instance
========================================
Users are responsible for their own instance instead of relying
on an instance installed by C2SM. The main advantage is that the users
won't have any change in their Spack instance, unless they actively
decide to pull upstream changes from GitHub.
Therefore your workflow is not interupted i.e. during a production phase
with using software installed by Spack.

**But with more power comes more responsability!**

This page collects best practices for a safe and reliable Spack instance management.

Create new Spack instance
----------------------------------

To get an instance, git clone spack-c2sm and its submodule spack.
'--depth 1' and '--shallow-submodules' are optional, but they reduce the amount of downloaded data.

.. code-block:: bash

    git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git

At CSCS setup-env.sh automatically detects the machine. You may simply execute

.. code-block:: bash

    source spack-c2sm/setup-env.sh

It is recommended to clone spack-c2sm in a location that does **NOT** undergo a
regular cleanup. On Piz Daint ``$SCRATCH`` enforces deletion of all files older than 30 days. This may corrupt your Spack instance, therefore ``/project/XYZ/`` is a safer location.

Update Spack instance
----------------------
To update a spack instance, pull the latest version from the repository and update the submodule

.. code-block:: bash


  git pull
  git submodule update --recursive

This is required after upgrades at CSCS or if you need new features of a package.
It is recommended to clean the instance afterwards, for more infos
see below.

Clean Spack instance
-----------------------
To clean a spack instance, empty the caches, uninstall everything and remove misc caches

.. code-block:: bash

  spack clean -a
  spack uninstall -a
  rm -rf ~/.spack

Spack instance config files
------------------------------
There is a set of .yaml files that define machine specific things like compilers, modules, preinstalled packages
and more.

They are available under spack/etc/spack. Their structure is:

* **compilers.yaml**: all info about available compilers, machine specific compiler flags, module to load (PrgEnv) before compiling
* **packages.yaml**: all info about the already installed dependencies, i.e their module names or paths
* **modules.yaml**: all info about the created modules, i.e which env variable or modules should be set once loaded
* **config.yaml**: specifies the main installation path and the main module installation path, where to find thebinaries etc.
* **upstreams.yaml**: specifies where to find the pre-installed software, that are under /project/g110/spack-install/
* **repos.yaml**: specifies where to find the only mch packages that are stored in spack-c2sm repository
