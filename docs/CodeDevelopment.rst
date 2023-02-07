Develop packages
================
Spack provides multiple ways of developing packages.
Depending on your workflow one or another option is preferred.
Also some packages like ICON or COSMO come with its own custom
development workflow maintained by C2SM.

Plain dev-build
----------------
This is the easiest way to build local sources.
Enter the root of your source-repo and execute:

.. code-block:: bash
  spack dev-build  <package> @develop <variant>

This will install the package as is. The downside of this approach is that
you need to go through all phases of a package build.

Dev-build in combination with build-env
----------------------------------------
We assume that developers of a package are familiar with its build system. Therefor we reccomend to use spack to set up the environment for the package. Building and testing should be done with the package's build system and test system.

.. code-block:: bash

  # Load spack!
  spack dev-build --before build <package> @develop <variant> # stops dev-build before executing the phase 'build'
  spack build-env <package> @develop <variant> -- bash # nests a bash shell with the build env vars loaded
  # Work on the package!
  # Use the package's build system! (e.g. 'make')
  # Use the package's testing infrastructure!
  exit # to exit the nested bash

If you want multiple dev-builds at the same time, label them with separate '@<your-label>'.
The identifier '@develop' is common in the spack documentation but you can use any string.


Environments with Spack develop
-------------------------------
Environments sit in a folder with a name and are defined in a **spack.yaml**
file. For more infos about environments in 
general read the `official spack docs <https://spack.readthedocs.io/en/latest/environments.html>`__.

**Environment defined in ICON**
.. code-block:: yaml

    # This is a Spack Environment file.
    #
    # It describes a set of packages to be installed, along with
    # configuration settings.
    spack:
      # add package specs to the `specs` list
      specs:
      - icon@develop%nvhpc +ecrad +rte-rrtmgp claw=std gpu=60
      - eccodes@2.19.0%nvhpc
      - claw@2.0.3%nvhpc
      - nvidia-blas%nvhpc
      - nvidia-lapack%nvhpc
      - libxml2@2.9.13%gcc
      view: true
      concretizer:
        unify: true
      develop:
        icon:
          spec: icon@develop%nvhpc +ecrad +rte-rrtmgp claw=std gpu=60
          path: ../../../../

The key part of the environments is the **develop** keyword.
This tells spack to look for a certain spec in **path**.
It is possible to specify multiple packages under **develop**.


To activate a spack environment

.. code-block:: bash

  spack env activate -p <path_to_spack_yaml>

To install the environment

.. code-block:: bash
    
  spack install

To deactivate a spack environment

.. code-block:: bash

  spack env deactivate

Most of the spack commands are sensitive to environments see `spack docs <https://spack.readthedocs.io/en/latest/environments.html#environment-sensitive-commands>`__.

