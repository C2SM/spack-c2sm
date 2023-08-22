Quick Start
===========


At CSCS (Daint and Balfrin)
-----------------------------

To set up a Spack instance, clone the repository

.. code-block:: console

  $ git clone --depth 1 --recurse-submodules --shallow-submodules -b v0.20.1.0 https://github.com/C2SM/spack-c2sm.git

To load it into your command line, execute

.. code-block:: console

  $ . spack-c2sm/setup-env.sh

This auto-detects your machine and configures your instance for it.
You can force a machine with an argument. The name has to match a folder in sysconfigs.

.. code-block:: console

  $ . spack-c2sm/setup-env.sh daint


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

..  tip::
    **On Balfrin:** 
    In case your Spack environment requires Python, a compatability issue
    with `openssl` and `git` appears.

    ``/usr/bin/ssh: symbol lookup error: /usr/bin/ssh: undefined symbol: EVP_KDF_CTX_free, version OPENSSL_1_1_1d``
   
    To circumvent that simply do
    ``spack load git`` prior to activation of the environment.

To activate the Spack environment, type

.. code-block:: console

    $ spack env activate -d <path_to_folder_with_spack_yaml>

To install the environment and so ICON, type

.. code-block:: console
    
    $ spack install --reuse -v

Example to build ICON for CPU with NVHPC:

.. code-block:: console

    $ spack env activate -d config/cscs/spack/v0.20.1.0/daint_cpu_nvhpc
    $ spack install --reuse -v

..  attention::
    Spack will skip the configure phase if ``icon.mk`` is found. In case you
    need to reconfigure you can either delete the file or run ``make distclean``.

Out-of-source builds are possible as follows:

.. code-block:: console

    $ mkdir cpu && cd cpu
    $ cp -r ../config .
    $ spack env activate -d config/cscs/spack/v0.20.1.0/daint_cpu_nvhpc
    $ spack install -v --reuse

..  attention::
    Out-of-source build for AutotoolsPackages is not supported by Spack.
    The implementation for ICON relies on some hacks inside package.py and
    only works if the build-folder is located inside the Git repo of ICON.

COSMO
-----

Building COSMO is not supported anymore starting with spack-c2sm v0.20.1.0!
