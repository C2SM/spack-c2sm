Code Development [MCH]
======================

COSMO
-----

Testing COSMO with the Testsuite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^

In order to run test the C++ dycore, the regression tests require a set of serialized data files from COSMO. 
Jenkins runs periodically the serialization (`<https://jenkins-mch.cscs.ch/job/cosmo_serialize/>`_), which installs all the serialized data set corresponding to the latest master in the g110 project space. In order to find the location of the jenkins serialized data follow the steps described in :ref:`Locate jenkins serialized data`.

In a different development situation where you are modifying the FORTRAN COSMO dycore, the master serialized data by jenkins will not be compatible with your modifications. 
In that case you need to serialize your own data (see :ref:`Serialize your own data`).

Locate jenkins serialized data
""""""""""""""""""""""""""""""
This section describes how to find the location of the serialized data by jenkins for the master version of COSMO. 

Set the spack spec of COSMO for serialization mode: 

.. code-block:: bash

  COSMO_SERIALIZE_SPEC="cosmo@dev-build%pgi real_type=float cosmo_target=cpu +serialize ~cppdycore"

Find the spack install location of the serialized data

.. code-block:: bash

  SERIALIZE_DATA=$(spack location -i ${COSMO_SERIALIZE_SPEC})/data


Serialize your own data
"""""""""""""""""""""""

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

COSMO C++ Dycore
----------------

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
