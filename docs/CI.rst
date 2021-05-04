Using the Jenkins Continuous Integration Executables
====================================================

This section describes how to find executables installed by jenkins and how to load the environment to run the application. 

Taking COSMO as an example, the first step is to specify a spack spec that identifies an specific build with a set of variants. 
For example

.. code-block:: bash

  COSMO_SPEC="cosmo@master%pgi real_type=float cosmo_target=gpu +cppdycore +claw"

Before we can use spack commands, we need to load the spack instance

.. code-block:: bash
  
  module load python/3.7.4
  . /project/g110/spack/user/tsa/spack/share/spack/setup-env.sh

In order to find the location of that build,

.. code-block:: bash

  spack location -i ${COSMO_SPEC}

The spec has to be complete and match all variants that were use to build the executable. Jenkins is not building all variant possibilities (it would not be possible). If you need to know the set of variants that are installed, run the following

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

Once you have localized a COSMO executable, you can run it provided you load first the needed environment. 
In order to use the executable on a compute node, we need first to load the spack module environment for COSMO.

.. code-block:: bash

  module use /project/g110/modules/admin-tsa/linux-rhel7-skylake_avx512/
  source <( spack module tcl loads ${SPACK_SPEC} )


For an example of how to run the COSMO testsuite on the compute nodes of tsa, see :ref:`Testing COSMO with the Testsuite`
