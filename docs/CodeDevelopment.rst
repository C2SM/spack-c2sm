Develop packages
================

Spack offers several options for package development.
Depending on your workflow, one or the other option is preferred.

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
      - icon-nwp@develop%nvhpc +ecrad +rte-rrtmgp +cuda
      - eccodes@2.19.0%nvhpc
      - nvidia-blas%nvhpc
      - nvidia-lapack%nvhpc
      - libxml2@2.9.13%gcc
      view: true
      concretizer:
        unify: true
      develop:
        icon-nwp:
          spec: icon-nwp@develop%nvhpc +ecrad +rte-rrtmgp +cuda
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

Plain dev-build
---------------

This is the easiest way to build local sources.
Enter the root of your source repository and execute:

.. code-block:: console

    $ spack dev-build --until build <package> @<version>

This will build the package as is. The downside of this approach is that
you need to go through all phases of a package build.
