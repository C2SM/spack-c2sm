Quick Start
===========

Set up (Daint, Dom, Tsa, Manali, Balfrin)
-----------------------------------------
To set up a spack instance, clone the repository

.. code-block:: bash

  git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git

To load it into your command line, execute

.. code-block:: bash

  . spack-c2sm/setup-env.sh
This auto-detects your machine and configures your instance for it.
You can force a machine with an argument. The name has to match a folder in sysconfigs.

.. code-block:: bash

  . spack-c2sm/setup-env.sh tsa

Set up (local machines)
-----------------------
Same as above, but probably you want spack to auto detect compilers and preinstalled packages

.. code-block:: bash

  git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git
  . spack-c2sm/setup-env.sh
  spack compiler find
  spack external find --all

Update
------
To update a spack instance, pull the latest version from the repository and update the submodule

.. code-block:: bash

  git pull
  git submodule update --recursive

Clean
-----
To clean a spack instance, empty the caches, uninstall everything and remove misc caches

.. code-block:: bash

  spack clean -a
  spack uninstall -a
  rm -rf ~/.spack

Use packages
------------
To get information about a package, query spack

.. code-block:: bash

  spack info <package>
  e.g.
  spack info icon

To see what 'spack install' would install, ask for a spec

.. code-block:: bash

  spack spec <variant>
  e.g.
  spack spec icon @master +ocean
An unspecfied variant (e.g. 'ocean') can be concretized to ANY of its values. Spack isn't required to use the default value when a variant is unspecified. The default value only serves as a tiebreaker.

To install a package

.. code-block:: bash

  spack install <variant>
  e.g.
  spack install icon @master %gcc +ocean

To locate your install, query spack

.. code-block:: bash

  spack location --install-dir <variant>
This prints a list of all installs that satisfy the restrictions in your variant.

To run it, you may need to load environment variables

.. code-block:: bash

  spack load <variant>

Develop packages
----------------
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

Environments
------------
Environments sit in a folder with a name. That's the name of the environment.

To activate a spack environment

.. code-block:: bash

  spack env activate -p <env_name>

To deactivate a spack environment

.. code-block:: bash

  spack env deactivate

Most of the spack commands are sensitive to environments (`see spack doc<https://spack.readthedocs.io/en/latest/environments.html#environment-sensitive-commands>`__).

Test packages (PR/MR/CI/CD)
---------------------------
You can use spack to test a PR/MR in your CI pipeline.
This is a common way to do it.

.. code-block:: bash

  # cd into the packages repo!
  git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git
  . spack-c2sm/setup-env.sh
  spack dev-build --test=root --show-log-on-error <package> @develop <variant>

You can also use spack in your end-to-end tests.
This is a common way to do it.

.. code-block:: bash

  git clone --depth 1 --recurse-submodules --shallow-submodules -b dev_v0.18.1 https://github.com/C2SM/spack-c2sm.git
  . spack-c2sm/setup-env.sh
  spack install --test=root --show-log-on-error <package> @<version> <variant>


COSMO
-----
COSMO is currently treated specially. It has its own commands in spack-c2sm.
The reason for this is that the optional depencendy on the C++ dycore lives in the same repository as COSMO.

To install COSMO

.. code-block:: bash

  spack installcosmo cosmo @<version> %<compiler> <variants>

To develop COSMO

.. code-block:: bash

  cd </path/to/package>
  spack devbuildcosmo cosmo @<version> %<compiler> <variants>

Example variants:

.. code-block:: bash

  spack installcosmo cosmo @org-master cosmo_target=cpu # CPU variant of https://github.com/COSMO-ORG/cosmo master
  spack installcosmo cosmo @org-master cosmo_target=gpu # GPU variant of https://github.com/COSMO-ORG/cosmo master
  spack installcosmo cosmo @apn_5.09a.mch1.2.p1 cosmo_target=gpu # GPU variant of https://github.com/MeteoSwiss-APN/cosmo/releases/tag/5.09a.mch1.2.p1

ICON
----
ICON currently needs a workaround when dev-building. Spack refuses to build in an empty folder. So you need to populate it with something

.. code-block:: bash

  touch .not_empty
