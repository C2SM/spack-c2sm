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

Create new Spack instance
-------------------------

To get an instance, clone spack-c2sm and its submodule spack.

.. code-block:: console

    $ git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git

The arguments ``--depth 1`` and ``--shallow-submodules`` are optional,
but they reduce the amount of downloaded data.

At CSCS, ``setup-env.sh`` automatically detects the machine. You may simply execute

.. code-block:: console

    $ . spack-c2sm/setup-env.sh

It is recommended to clone ``spack-c2sm`` in a location that does **not** undergo a
regular cleanup. On Piz Daint, ``$SCRATCH`` enforces the deletion of all files older than 30 days.
This may corrupt your Spack instance, therefore ``/project/XYZ/`` is a safer location.

Update Spack instance
----------------------

To update a Spack instance, pull the latest version from the repository and update the submodules:

.. code-block:: console

    $ git pull
    $ git submodule update --recursive

This is required after upgrades at CSCS or if you need new features of a package.
It is recommended to clean the instance afterwards. For more infos, see below.

Clean Spack instance
--------------------

To clean a Spack instance, empty the caches, uninstall everything and remove misc caches:

.. code-block:: console

    $ spack clean -a
    $ spack uninstall -a
    $ rm -rf ~/.spack

