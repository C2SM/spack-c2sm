Quick Start
===========


At CSCS (Daint, Tsa, Balfrin)
-----------------------------

To set up a Spack instance, clone the repository

.. code-block:: console

  $ git clone --depth 1 --recurse-submodules --shallow-submodules -b v0.18.1.7 https://github.com/C2SM/spack-c2sm.git

To load it into your command line, execute

.. code-block:: console

  $ . spack-c2sm/setup-env.sh

This auto-detects your machine and configures your instance for it.
You can force a machine with an argument. The name has to match a folder in sysconfigs.

.. code-block:: console

  $ . spack-c2sm/setup-env.sh tsa


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
Environments sit in a folder with a name and are defined in a ``spack.yaml`` file.
For ICON, they are located in ``config/cscs/spack/<version>/<machine>_<target>_<compiler>``.

To activate the Spack environment, type

.. code-block:: console

    $ spack env activate -d <path_to_folder_with_spack_yaml>

To install the environment and so ICON, type

.. code-block:: console
    
    $ spack install

Example to build ICON for CPU with NVHPC:

.. code-block:: console

    $ spack env activate -d config/cscs/spack/v0.18.1.7/daint_cpu_nvhpc
    $ spack install

..  attention::
    Spack will skip the configure phase if ``icon.mk`` is found. In case you
    need to reconfigure you can either delete the file or run ``make distclean``.

Out-of-source builds are possible as follows:

.. code-block:: console

    $ mkdir cpu && cd cpu
    $ cp -r ../config .
    $ spack env activate -d config/cscs/spack/v0.18.1.7/daint_cpu_nvhpc
    $ spack install

..  attention::
    Out-of-source build for AutotoolsPackages is not supported by Spack.
    The implementation for ICON relies on some hacks inside package.py and
    only works if the build-folder is located inside the Git repo of ICON.

COSMO
-----

COSMO is currently receiving special treatment. It has its own commands in spack-c2sm.
The reason for this is that the optional depencendy on the C++ dycore lives in the same repository as COSMO.

To install COSMO

.. code-block:: console

  $ spack installcosmo cosmo @<version> %nvhpc <variants> ^mpich%nvhpc

To develop COSMO

.. code-block:: console

  $ cd </path/to/package>
  $ spack devbuildcosmo cosmo @<version> %nvhpc <variants> ^mpich%nvhpc

Example variants:

.. code-block:: console

  $ spack installcosmo cosmo @org-master cosmo_target=cpu # CPU variant of https://github.com/COSMO-ORG/cosmo master
  $ spack installcosmo cosmo @org-master cosmo_target=gpu # GPU variant of https://github.com/COSMO-ORG/cosmo master
  $ spack installcosmo cosmo @apn_5.09a.mch1.2.p1 cosmo_target=gpu # GPU variant of https://github.com/MeteoSwiss-APN/cosmo/releases/tag/5.09a.mch1.2.p1


Changelog to v0.17.0
--------------------

* Users manage their own instance instead of sourcing a pre-installed instance.
* Users decide on their own when they would like to update their instance (i.e. after upgrades at CSCS).
* Due to the new concretizer, COSMO needs an explicit ``^mpich%nvhpc`` (Daint) or ``openmpi%nvhpc`` (Tsa) in the spec, otherwise the build fails.
* On Daint, ICON is built using environments and ``dev-build`` no longer supported. On Balfrin, ICON can still be built using ``dev-build``.
