Code Development
==================

COSMO
-------------

Before we can start, we need to load the spack instance

On Tsa:

.. code-block:: bash

  module load python/3.7.4
  . /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh

On Daint:
  
.. code-block:: bash
  
  module load cray-python
  . /project/g110/spack/user/daint/spack/share/spack/setup-env.sh

Compile a local version of COSMO using devbuildcosmo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this section we show how to compile a version of COSMO with a local C++ dycore. 
Note: This is only required for GPU. For cpu we recomend to compile without
c++ dycore.

Here we assume the user has clone cosmo, is in the required branch/release and
in the root folder of the cosmo repository. 

The recommanded method to build with spack is to use the devbuildcosmo command. This takes the
cosmo specification as input and will automatically compile and install the
local dycore with the correct configuration and then compile and install
cosmo. Here is an example for gpu in double:

.. code-block:: bash 
  
  cd </path/to/cosmo>
  COSMO_SPEC="cosmo@dev-build%pgi real_type=double cosmo_target=gpu +cppdycore +claw" # careful +claw doesn't work on Daint!
  spack devbuildcosmo $COSMO_SPEC # add -c for clean build, -t for testing
  

For cpu, double and no c++ dycore one would use:

.. code-block:: bash 

  COSMO_SPEC="cosmo@dev-build%gcc real_type=double cosmo_target=cpu ~cppdycore"
  spack devbuildcosmo $COSMO_SPEC


Testing COSMO with the Testsuite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following commands demonstrates how to launch the testsuite for a COSMO
executable compiled using spack. Assuming the user starts from the root folder
of cosmo.

.. code-block:: bash 

  # copy executable to the testsuite folder
  cp -f cosmo/ACC/cosmo_gpu cosmo/test/testsuite # cosmo_cpu for cpu

  # source the run environment
  spack load $COSMO_SPEC

  # launch tests

  ./cosmo/ACC/test/tools/test_cosmo.py -s $COSMO_SPEC -b .
  

Serialized unittest data
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to run test the C++ dycore, the regression tests require a set of serialized data files from COSMO. 
Jenkins runs periodically the serialization (`<https://jenkins-mch.cscs.ch/job/cosmo_serialize/>`_), which installs all the serialized data set corresponding to the latest master in the g110 project space. In order to find the location of the jenkins serialized data follow the steps described in :ref:`Locate jenkins serialized data`.

In a different development situation where you are modifying the FORTRAN COSMO dycore, the master serialized data by jenkins will not be compatible with your modifications. 
In that case you need to serialize your own data (see :ref:`Serialize your own data`).

Before we can start, we need to load the spack instance

.. code-block:: bash

  module load python/3.7.4  
  . /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh


Locate jenkins serialized data
""""""""""""""""""""""""""""""""
This section describes how to find the location of the serialized data by jenkins for the master version of COSMO. 

Set the spack spec of COSMO for serialization mode: 

.. code-block:: bash

  COSMO_SERIALIZE_SPEC="cosmo@dev-build%pgi real_type=float cosmo_target=cpu +serialize ~cppdycore"

Find the spack install location of the serialized data

.. code-block:: bash

  SERIALIZE_DATA=$(spack location -i ${COSMO_SERIALIZE_SPEC})/data


Serialize your own data
""""""""""""""""""""""""""

Set the spack spec (for dev-build version) of COSMO for serialization mode: 

.. code-block:: bash

  COSMO_SERIALIZE_SPEC="cosmo@dev-build%pgi real_type=float cosmo_target=cpu +serialize ~cppdycore"

In your working directory of cosmo, build a spack COSMO executable for serialization

.. code-block:: bash

  cd </path/to/cosmo>
  spack dev-build --until=build ${COSMO_SERIALIZE_SPEC}

Load the correct run environment

.. code-block:: bash

  spack load ${COSMO_SERIALIZE_SPEC}

Launch the serialization script

.. code-block:: bash

  ./cosmo/ACC/test/tools/serialize_cosmo.py -s ${COSMO_SERIALIZE_SPEC} -b .

Set the path to the serialized data (later it will be used in this guide)

.. code-block:: bash

  SERIALIZE_DATA=</path/to/cosmo>/cosmo/ACC/test/serialize/data/

Compile and Test a Local C++ dycore
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section describes how to compile and test a version of the COSMO C++ dycore from your working directory. 

Set a COSMO C++ dycore spec

.. code-block:: bash

  DYCORE_SPEC="cosmo-dycore@dev-build real_type=float build_type=Release"

In your working directory of cosmo, build a C++ dycore executable 

.. code-block:: bash

  cd </path/to/cosmo>
  spack dev-build --until=build cosmo-dycore@dev-build real_type=float build_type=Release +cuda

Load the correct run environment

.. code-block:: bash

  spack load ${DYCORE_SPEC}

Launch the dycore test script

.. code-block:: bash
  ./dycore/test/tools/test_dycore.py -s ${DYCORE_SPEC} -b spack-build -d ${SERIALIZE_DATA}


Any Other Package
------------------------

The command `spack dev-build` can be used to compile any modified version of a MeteoSwiss software from your working directory. 
However being able to compile any other package might require installing your spack instance, if that package is installed by a jenkins plan.
An attempt to build your working copy with the command

.. code-block:: bash

  spack install <package>@master ... 

will not perform any compilation if spack identifies that the requested version of the software was already installed by a jenkins plan. 

That problem is circumvented for COSMO and the C++ dycore by reserving an specific version (`dev-build`) of the spack recipe of the package 
(see `link <https://github.com/MeteoSwiss-APN/spack-mch/blob/0092230d325525197f8991b172b321ffdb4a118a/packages/cosmo/package.py#L54>`_), 
which will not be used by jenkins. Therefore, `spack dev-build cosmo@dev-build` will find that version among the installed in the default spack instance.
For any other package that does not contain this `dev-build` version, we will install our own spack instance. 

.. code-block:: bash

  module load python/3.7.4 
  git clone git@github.com:MeteoSwiss-APN/spack-mch.git
  cd spack-mch
  ./config.py -m tsa -i . -p $PWD/spack -u ON

  . spack/share/spack/setup-env.sh

And then compile our package with spack in dev-build mode

.. code-block:: bash

  cd </path/to/package> 
  spack dev-build <package>@<version>

