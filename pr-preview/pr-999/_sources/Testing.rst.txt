Testing
=======

Test packages (PR/MR/CI/CD)
---------------------------

You can use spack to test a PR/MR in your CI pipeline.
This is a common way to do it.

.. code-block:: console

    # cd into the packages repo!
    $ git clone --depth 1 --recurse-submodules --shallow-submodules -b v0.20.1.0 https://github.com/C2SM/spack-c2sm.git
    $ . spack-c2sm/setup-env.sh
    $ spack dev-build --test=root --show-log-on-error <package> @develop <variant>

You can also use spack in your end-to-end tests.
This is a common way to do it.

.. code-block:: console

    $ spack install --test=root --show-log-on-error <package> @<version> <variant>

Pull Request Testing for spack-c2sm on GitHub
---------------------------------------------

To test a PR, create a comment ``launch jenkins [<packages>] [<machines>]``.

It will test the listed packages on the listed machines.
No package means all packages. No machine means all machines.
The order is irrelevant.

Examples
^^^^^^^^

*   ``launch jenkins int2lm balfrin`` tests int2lm on balfrin.
*   ``launch jenkins cosmo int2lm balfrin`` tests

    *   cosmo on balfrin
    *   int2lm on balfrin

*   ``launch jenkins cosmo icon`` tests cosmo and icon on all machines.
*   ``launch jenkins balfrin`` tests all packages on balfrin.
*   ``launch jenkins`` tests all packages on all machines.
*   ``launch jenkins all`` tests all packages on all machines.


Supported packages: all folder names in folder `packages <https://github.com/C2SM/spack-c2sm/tree/main/packages>`__.

Supported machines:

*   balfrin
