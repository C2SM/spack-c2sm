Important Spack Commands
========================

Spack find
----------
List and search installed packages

Usage (spack find)
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
  
  spack find <package>@<version>%<compiler> +<variants>

Example output:

.. code-block:: bash

  spack find -v cosmo
  
  ==> 8 installed packages
  -- linux-rhel7-skylake_avx512 / gcc@8.3.0 -----------------------
  cosmo@master~claw cosmo_target=cpu ~cppdycore~debug+dycoretest+eccodes+parallel~pollen~production real_type=double ~serialize slave=tsa ~verbose
  cosmo@master~claw cosmo_target=cpu ~cppdycore~debug+dycoretest+eccodes+parallel~pollen~production real_type=float ~serialize slave=tsa ~verbose

  -- linux-rhel7-skylake_avx512 / pgi@19.9 ------------------------
  cosmo@dev-build~claw cosmo_target=cpu ~cppdycore~debug+dycoretest~eccodes+parallel~pollen~production real_type=float +serialize slave=tsa ~verbose
  cosmo@5.07.mch1.0.p6+claw cosmo_target=gpu +cppdycore~debug+eccodes+parallel+pollen+production real_type=double ~serialize slave=tsa ~verbose
  cosmo@5.07.mch1.0.p6+claw cosmo_target=gpu +cppdycore~debug+eccodes+parallel+pollen+production real_type=float ~serialize slave=tsa ~verbose

Options (spack find)
^^^^^^^^^^^^^^^^^^^^^
* \--paths, -p: show paths to package install directories
* \--variants, -v: show variants in output (can be long)


Machine processing (spack find)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For a raw list of installation folders, use

.. code-block:: bash

  spack find --format "{prefix}" <spec>

Example output:

.. code-block:: bash

  spack find --format "{prefix}" cosmo
  /project/g110/spack-install/tsa/cosmo/apn_5.09a.mch1.2.p2/pgi/qh4lqyvz73zcm2emfwwhcfue6kkm3xyo
  /project/g110/spack-install/tsa/cosmo/apn_5.09a.mch1.2.p2/pgi/ssezzpu36dc4j5lc35rkytuieicoptfr
  /project/g110/spack-install/tsa/cosmo/mch/pgi/4h7b7x62dcpvrctghjv23jrpnkep4ela
  /project/g110/spack-install/tsa/cosmo/mch/pgi/6ijz5756a65p6wblxbr3enllmpdzcvh5
  /project/g110/spack-install/tsa/cosmo/5.09a.mch1.2.p1/pgi/us5kk56wraktww7e543cxi4dbud2lalv
  /project/g110/spack-install/tsa/cosmo/5.09a.mch1.2.p1/pgi/o3jtuao2gwrz7uwyekvxvr7ylltwnt4w
  /project/g110/spack-install/tsa/cosmo/master/gcc/aejk4rps3es6o5trdwppzew3f2j37kl6
  /project/g110/spack-install/tsa/cosmo/master/pgi/vkwywww3z52ttmlzzpn4df5jnr5paiw4
  /project/g110/spack-install/tsa/cosmo/master/gcc/l52ikknglfrfolr462lc4ez6abulmphs
  /project/g110/spack-install/tsa/cosmo/master/pgi/bbjwypwllbba6nmkvronktzo2vt6k3dw
  /project/g110/spack-install/tsa/cosmo/master/pgi/gnm6i4pya3lrscgdnvvzgt77bssbfcab
  /project/g110/spack-install/tsa/cosmo/master/pgi/koaxr3hlillunjtywkh46vcpzgrarnxc
  /project/g110/spack-install/tsa/cosmo/master/pgi/i72unz2dzlp4donztoi7kxbubj4kfqtw
  /project/g110/spack-install/tsa/cosmo/master/pgi/rvqs2tqltwlohpkyedzwnjggtwtgu4ly
  /project/g110/spack-install/tsa/cosmo/master/pgi/i2hc4rhlhhapga6gheq3tcnbyrytadoy
  /project/g110/spack-install/tsa/cosmo/master/pgi/kmrbrer2mlzz2rkn3ykhxr6h6glbwptn

Tip:
If you want just any installation folder that matches the spec, the output can be truncated with '| head -n 1' to get the first.
If you want the installation folder of the spec that matches your spec, filled with the current defaults, you have to use Python.

.. code-block:: python

  #!/usr/bin/env spack python
  from spack.spec import Spec
  s = Spec('cosmo')
  s.concretize()
  install_dir = s.format('{prefix}')
  print(install_dir)

or as a one-liner

.. code-block:: bash

  spack python -c "print(spack.spec.Spec('cosmo').concretized().format('{prefix}'))"


Spack list
----------
List and search available packages

Usage (spack list)
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack list <package>

Spack info
----------
Get a list of all possible building configuration available such as: 
* versions available
* list of dependencies
* variants

Variants are a key-feature of spack since it describes which build configuration we want (i.e COSMO with target gpu or cpu).

Usage (spack info)
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack info <package>

Spack spec
----------
Check how your package will be installed (i.e the spec of you package and its dependencies) 
before actually installing it.

Usage (spack spec)
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack spec <package>@<version>%<compiler> +<variants>

Spack install
-------------
This will clone the package, build it and install the chosen package 
plus all its dependencies under */scratch/$USER/spack-install/<your_machine>* 
(see config.yaml in the maching specific config file section for details). 
The build-stage of your package and its dependencies are not kept 
(add --keep-stage after the install command in order to keep it). 
Module files are also created during this process and installed under */scratch/$USER/modules/*

However being able to compile any other package might require installing your spack instance, if that package is installed by a jenkins plan.
An attempt to build your working copy with the command

.. code-block:: bash

  spack install <package>@master ... 

will not perform any compilation if spack identifies that the requested version of the software was already installed by a jenkins plan. 

That problem is circumvented for COSMO, C++ dycore and other C2SM-hosted software by reserving an specific version (`dev-build`) of the spack recipe of the package 
(see `int2lm package  <https://github.com/MeteoSwiss-APN/spack-mch/blob/37908c7ac7171c4d886fe5ccf84051056e12ec0e/packages/int2lm/package.py#L25>`__), 
which will not be used by jenkins. Therefore, *spack install int2lm@dev-build* will find that version among the installed in the default spack instance.
For any other package that does not contain this *dev-build* version, you need to install our own spack instance. 

Usage (spack install)
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack install <package>@<version>%<compiler>

Options (spack install)
^^^^^^^^^^^^^^^^^^^^^^^
* -v: print output of configuration and compilation for all dependencies to terminal
* \--test=root: run package tests during installation for top-level packages (but skip tests for dependencies)
* \--keep-stage: keep all source needed to build the package

Spack installcosmo
------------------
Installcosmo can only be used to build COSMO. This command will clone, 
build and install COSMO as you would expect using *spack install*. 
Due to the complex dependency structure of COSMO an additional file called *spec.yaml* was introduced.
*Spec.yaml* contains the version of key dependencies like *eccodes* or *cosmo-eccodes-definition*. 
This file fetched from the code prior to the build.
The version of the C++ Dycore is always set
equal to the COSMO-version.
Versions of dependencies can be overwritten with user input. The precedence is the following:

#. user-input
#. version defined in spec.yaml
#. package default

Usage (spack installcosmo)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack installcosmo cosmo@<version>%<compiler> +<variants>

Options (spack installcosmo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* \--test {root,all}: If root is chosen, run COSMO testsuite before installation 
                     (but skip tests for dependencies). If all is chosen, 
                     run package tests during installation for all packages.
* -j \--jobs: Explicitly set number of parallel jobs
* \--only {package,dependencies}: Select the mode of installation.
                                 the default is to install the package along with all its dependencies.
                                 alternatively one can decide to install only the package or only
                                 the dependencies.
* \--keep-stage: Don't remove the build after compilation
* -v, \--verbose: Verbose installation
* \--force_uninstall: Force uninstall if COSMO-package is already installed
* \--dont-restage: If a partial install is detected, don't delete prior
* -u, \--until: Phase to stop after when installing

Spack dev-build
---------------
If you do not want to git clone the source of the package you want to install, 
especially if you are developing, you can use a local source in 
order to install your package. In order to do so, first go to the base directory 
of the package and then use *spack dev-build* instead of *spack install*.

However being able to compile any other package might require installing your spack instance, if that package is installed by a jenkins plan.

Notice that once installed, the package will not be rebuilt at the next attempt to spack dev-build, 
even if the sources of the local directory have changed. 
In order to force spack to build the local developments anytime, 
you need to avoid the installation phase (see option *--until* below).

Usage (spack dev-build)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  cd </path/to/package> 
  spack dev-build <package>@<version>%<compiler>

Options (spack dev-build)
^^^^^^^^^^^^^^^^^^^^^^^^^
* \--test=root: run package tests during installation for top-level packages (but skip tests for dependencies)
* \--until <stage>: only run installation until certain stage, like *build* or *install*

.. code-block:: bash

  spack dev-build --until build <package>@<version>%<compiler> +<variants>

Spack devbuildcosmo
-------------------
Devbuildcosmo can only be used to build COSMO using a local source.
Similar to *spack installcosmo* it uses the file *spec.yaml* to determine the version
of key dependencies. The version of the C++ Dycore is alway set equal to the COSMO-version.
Versions of dependencies can be overwritten with user input. The precedence is the following:

#. user-input
#. version defined in spec.yaml
#. package default

There is an option the completely ignore all version specified in *spec.yaml* to allow builds of older 
COSMO version.

Usage (spack devbuildcosmo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  cd </path/to/package> 
  spack devbuildcosmo <cosmo>@<version>%<compiler> +<variants>

Options (spack devbuildcosmo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* \--no_specyaml: Ignore *spec.yaml*
* -c --clean_build: Clean build
* -j <JOBS>, \--jobs <JOBS>: Explicitly set number of parallel jobs

* \--test {root,dycore,all}: If root is chosen, run COSMO testsuite before installation
                            (but skip tests for dependencies). If dycore is chosen,
                            run test for Dycore and COSMO testsuite.
                            If all is chosen,
                            run package tests during installation for all packages.
* -c, \--clean_build: Clean dev-build
* \--dont-restage: If a partial install is detected, don't delete prior
* -u, \--until: Phase to stop after when installing

Spack location
--------------
Locate paths related to some spec. This command is mainly usefull to
get the path where a package was installed (a long path with hashes)
and access the coresponding binary (somewhere under that location).

`As stated in the official spack documentation
<https://spack.readthedocs.io/en/latest/workflows.html#find-and-run>`_,
"The simplest way to run a Spack binary is to find it and run it" as
it is build with `RPATH`. In most cases there is no need to adjust the
environment.

Other options can be used to retrieve other paths like the build
directory or the path to the package definition (`see official spack
documentation
<https://spack.readthedocs.io/en/latest/command_index.html#spack-location>`_
or ``spack location -h``)

Usage (spack location)
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack location -i <spec>

Spack build-env
---------------
Run a command in a specs install environment, or dump its environment to screen or file
This command can either be used to run a command in a specs install environment or to dump
a sourceable file with the install environment. In case you want to run test of packages manually this
is what you need.


Usage (spack build-env)
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack build-env <spec> -- <command>

Replacing *<command>* with *bash* allows to interactively execute programmes in the install environment.

Options (spack build-env)
^^^^^^^^^^^^^^^^^^^^^^^^^
* \--dump <filename>: dump environment to <filename> to be sourced at some point

Spack edit
----------
Spack edit opens package files in $EDITOR. Use this command
in order to open the correspondig package.py file and edit it directly.

Usage (spack edit)
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

  spack edit <package>

Spack load
----------
Add package to the user environment. It can be used i. e. to set all runtime paths 
like `LD_LIBRARY_PATH` as defined in the respective package.
`More information in the official Spack documentation <https://spack.readthedocs.io/en/latest/command_index.html?highlight=spack%20load#spack-load>`_

It is recommended to load the corresponding environment prior to any execution of an executable
compiled by Spack.

Usage (spack load)
^^^^^^^^^^^^^^^^^^

.. code-block:: bash
  
  spack load <spec>

Options (spack load)
^^^^^^^^^^^^^^^^^^^^
* \--first: load the first match if multiple packages match the spec
