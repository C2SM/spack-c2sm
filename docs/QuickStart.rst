Quick Start
===========


At CSCS/ETHZ (Balfrin and Euler)
------------------------------------------------

To set up a Spack instance, clone the repository using a specific Spack tag (latest ``SPACK_TAG=v0.20.1.5``).

.. code-block:: console

  $ git clone --depth 1 --recurse-submodules --shallow-submodules -b $SPACK_TAG https://github.com/C2SM/spack-c2sm.git

To load it into your command line, execute one of the following commands:

.. code-block:: console

  $ . spack-c2sm/setup-env.sh
  $ . spack-c2sm/setup-env.sh /user-environment
  $ . spack-c2sm/setup-env.sh /mch-environment/v6
  $ . spack-c2sm/setup-env.sh /mch-environment/v7
  $ . spack-c2sm/setup-env.sh any_other_upstream

This will make upstream installation from user-environment available in spack-c2sm.

Local machines and Containers
-----------------------------

Spack can autodetect compilers and pre-installed packages with

.. code-block:: console

  $ spack compiler find
  $ spack external find --all


Use packages
------------
To get information about a package, query Spack


.. code-block:: console

  $ spack info <package>
  # e.g.
  $ spack info icon

To see what ``spack install`` would install, ask for a spec

.. code-block:: console

  $ spack spec <variant>
  # e.g.
  $ spack spec icon @master +ocean

An unspecfied variant (e.g. ``ocean``) can be concretized to ANY of its values. Spack isn't required to use the default value when a variant is unspecified. The default value only serves as a tiebreaker.

To install a package

.. code-block:: console

  $ spack install <variant>
  # e.g.
  $ spack install icon @master %gcc +ocean

To locate your install, query Spack

.. code-block:: console

  $ spack location --install-dir <variant>

This prints a list of all installs that satisfy the restrictions in your variant.

To run it, you may need to load environment variables

.. code-block:: console

  $ spack load <variant>


ICON
----

ICON is built using environments.
Environments are located in a folder named after the environment and are defined in a ``spack.yaml`` file.
For ICON, they are located in ``config/cscs/spack/<version>/<machine>_<target>_<compiler>``.
They work with a special Spack tag, that is provided in the ICON repository at ``config/cscs/SPACK_TAG_*``.
So make sure you clone Spack with the specified tag.

To activate the Spack environment, type

.. code-block:: console

    $ spack env activate -d <path_to_folder_with_spack_yaml>

To install the environment and so ICON, type

.. code-block:: console
    
    $ spack install

Example to build ICON for CPU with NVHPC on Piz Daint:

.. code-block:: console

    $ SPACK_TAG=$(cat "config/cscs/SPACK_TAG_DAINT")
    $ spack env activate -d config/cscs/spack/$SPACK_TAG/daint_cpu_nvhpc
    $ spack install

..  attention::
    Spack will skip the configure phase if ``icon.mk`` is found. In case you
    need to reconfigure you can either delete the file or run ``make distclean``.

Out-of-source builds are possible as follows:

.. code-block:: console

    $ mkdir cpu
    $ spack env activate config/cscs/spack/v0.20.1.5/daint_cpu_nvhpc
    $ # tell spack to build icon in folder cpu
    $ spack develop --path $(pwd) --build-directory cpu icon@develop
    $ spack install

By executing the commands above, spack will add some lines directly into ``spack.yaml``:

.. code-block:: yaml

  spack:                                                                                                                                                                                                                          
    packages:                                                                                                                                                                                                                     
      icon:                                                                                                                                                                                                                       
        package_attributes:                                                                                                                                                                                                       
          build_directory: /scratch/mch/juckerj/icon-nwp/cpu

Any further ``spack install`` command will use the build directory specified in the ``spack.yaml`` file.
In case you want to change the build directory, edit the ``spack.yaml`` file or remove the ``build_directory`` line
and run ``spack concretize -f`` afterwards.

COSMO
-----

Building COSMO is not supported anymore starting with spack-c2sm v0.20.1.0 for CSCS.

For Euler Cluster a CPU-only setup is supported using GCC 8.5.0

.. code-block:: console

    $ spack install cosmo%gcc@8.5.0
