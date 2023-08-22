Develop packages
================

Spack offers several options for package development.
Depending on your workflow, one or the other option is preferred.
Also some packages like ICON or COSMO have their own 
development workflow which is maintained by C2SM.

Plain dev-build
---------------

This is the easiest way to build local sources.
Enter the root of your source repository and execute:

.. code-block:: console

    $ spack dev-build  <package> @develop <variant>

This will install the package as is. The downside of this approach is that
you need to go through all phases of a package build.

Dev-build in combination with build-env
---------------------------------------

We assume that developers of a package are familiar with its build system.
Therefore, we reccomend to use Spack to set up the environment for the package.
Building and testing should be done with the package's build and test system.

.. code-block:: console

    # Load Spack!
    $ spack dev-build --before build <package> @develop <variant> # stops dev-build before executing the phase 'build'
    $ spack build-env <package> @develop <variant> -- bash # nests a bash shell with the build env vars loaded
    # Work on the package!
    # Use the build system of the package! (e.g. 'make')
    # Use the testing infrastructure of the package!
    $ exit # to exit the nested bash

If you want multiple dev-builds at the same time, label them with separate ``@<your-label>``.
The identifier ``@develop`` is common in the Spack documentation but you can use any string.


Environments with Spack develop
-------------------------------

Environments sit in a folder with a name and are defined in a ``spack.yaml`` file.
For more information about environments in general, consider reading the 
`official Spack docs <https://spack.readthedocs.io/en/latest/environments.html>`__.

.. code-block:: yaml
    :caption: Example environment for ICON
  
    # This is a Spack Environment file.
    #
    # It describes a set of packages to be installed, along with
    # configuration settings.
    spack:
      # add package specs to the `specs` list
      specs:
      - icon@develop%nvhpc +ecrad +rte-rrtmgp claw=std +cuda
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
          spec: icon@develop%nvhpc +ecrad +rte-rrtmgp claw=std +cuda
          path: ../../../../

The key part of the environments is the ``develop`` keyword.
This tells Spack to look for a certain spec in ``path``.
It is possible to specify multiple packages under ``develop``.

To activate a Spack environment, type

.. code-block:: console

    $ spack env activate <path_to_folder_with_spack_yaml>

To install the environment, type

.. code-block:: console
    
    $ spack install

To deactivate a Spack environment, type

.. code-block:: console

    $ spack env deactivate

Most of the Spack commands are sensitive to environments, see 
`Spack docs <https://spack.readthedocs.io/en/latest/environments.html#environment-sensitive-commands>`__.

