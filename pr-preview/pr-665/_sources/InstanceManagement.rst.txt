How to manage your own Spack instance
=====================================

Users are responsible for their own instance, rather than relying on an
instance installed by C2SM. The main advantage is that users do not make
changes to their Spack instance unless they actively choose to pull upstream
changes from GitHub. Therefore, your workflow is not interrupted, for example,
during a production phase with software installed from Spack.

..  attention::
    With more power comes more responsability!

This page collects best practices for a safe and reliable Spack instance management.

Versions
--------

Generally, we recommend to host a released version of spack-c2sm and upgrade to newer versions when you see fit.
But if you fancy the latest developments before they are released, you may follow the branch 'main'.
For automated systems that regularly set up a new Spack instance, using a fixed version and updating on demand, is more robust and limits the dependencies of your project. Following 'main' on the other hand automatically updates to the newest features but breaks upon API chaning commits in spack-c2sm.

Create a new Spack instance
---------------------------

To get an instance, clone spack-c2sm and its submodule spack.

.. code-block:: console

    $ git clone --depth 1 --recurse-submodules --shallow-submodules -b <branch/tag> https://github.com/C2SM/spack-c2sm.git

The arguments ``--depth 1`` and ``--shallow-submodules`` are optional, but they reduce the amount of downloaded data.
It is recommended to clone ``spack-c2sm`` in a location that does **not** undergo a
regular cleanup. On Piz Daint, ``$SCRATCH`` enforces the deletion of all files older than 30 days.
This may corrupt your Spack instance, therefore ``/project/XYZ/`` is a safer location.

Setup Spack environment
-----------------------

``setup-env.sh`` automatically detects the machine it is running on, or falls back to a generic configuration called 'unknown'.
``setup-env.sh <machine>`` forces a machine. This also works with 'unknown' as a machine, which is useful in a container.
It prints which machine it detected. Currently it's able to detect Balfrin, Piz Daint and Tsa.
You may simply execute

.. code-block:: console

    $ . spack-c2sm/setup-env.sh


Update Spack instance
----------------------

Before updating, we recommend to clean the instance, as this avoids occasional, hard to debug problems. For more infos, see below.
To update a Spack instance, pull the latest version from the repository and update the submodules:

.. code-block:: console

    $ git pull
    $ git submodule update --recursive

This is required after upgrades at CSCS or if you need new features of a package.

Clean Spack instance
--------------------

To clean a Spack instance, empty the caches, uninstall everything and remove misc caches:

.. code-block:: console

    $ spack clean -a #[cleans all misc caches](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-clean)
    $ spack uninstall -a #[uninstalls all packages](https://spack.readthedocs.io/en/v0.18.1/command_index.html?highlight=spack%20load#spack-uninstall)
    $ rm -rf ~/.spack #removes user scope data
