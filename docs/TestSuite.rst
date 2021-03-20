Testsuite DevOps
====================

The testsuite is a verification framework that ensures results of a set of COSMO use cases produce an output that is statistically verified up to a tolerance error, specified in the configuration. 

HowTo update the tolerances
----------------------------

Often, modifications of the COSMO code or update of the environment can cause the testsuite to fail surpassing the thresholds defined for some variables/use cases.
Here we describe the steps to capture and update the tolerance (thresholds) for the COSMO tests that are failing.

First step is to identify from jenkins the path to the COSMO testsuite of the variant that is failing. 

Copy the testsuite folder in a local working copy and update the tolerances for the desired cases

.. code-block:: bash

  git clone git@github.com:COSMO-ORG/cosmo.git
  cd cosmo/
  cp -r </path/to/jenkins/failing/testsuite>/cosmo/cosmo/test/testsuite testsuite_update
  cd testsuite_update
  ./src/testsuite.py --update-thresholds --tolerance=TOLERANCE_sp --only=cosmo1_pollen,test_1_gpu -l testlist_gpu.xml 
