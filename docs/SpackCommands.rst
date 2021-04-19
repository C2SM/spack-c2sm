Important Spack Commands
========================

Spack install
--------------
The command `spack install` fetches the package from the specified source in `package.py`.
It then builds the code in `spack-stages` folder  with a subsequent installation in `spack-install` 
folder.

Usage
^^^^^^^
.. code-block:: bash

  spack install <package>@<version>%<compiler>

Options
^^^^^^^^^
* -v: print output of configuration and compilation for all dependencies to terminal
* --test=root: run built-in tests (e.g COSMO testsuite) of a packages as part of the spack installation command

Spack dev-build
---------------
The command `spack dev-build` can be used to compile any modified version of a C2SM software from your working directory. 
However being able to compile any other package might require installing your spack instance, if that package is installed by a jenkins plan.
An attempt to build your working copy with the command

.. code-block:: bash

  spack install <package>@master ... 

will not perform any compilation if spack identifies that the requested version of the software was already installed by a jenkins plan. 

That problem is circumvented for COSMO, C++ dycore and other C2SM-hosted software by reserving an specific version (`dev-build`) of the spack recipe of the package 
(see `int2lm package  https://github.com/MeteoSwiss-APN/spack-mch/blob/37908c7ac7171c4d886fe5ccf84051056e12ec0e/packages/int2lm/package.py#L25`), 
which will not be used by jenkins. Therefore, `spack dev-build int2lm@dev-build` will find that version among the installed in the default spack instance.
For any other package that does not contain this `dev-build` version, you need to install our own spack instance. 

Usage
^^^^^^^
.. code-block:: bash

  cd </path/to/package> 
  spack dev-build <package>@<version>%<compiler>

Options
^^^^^^^^^
* --test=root: run built-in tests (e.g COSMO testsuite) of a packages as part of the spack dev-build command

Spack build-env
------------------

Spack devbuildcosmo
---------------------

Spack depinstallcosmo
---------------------



