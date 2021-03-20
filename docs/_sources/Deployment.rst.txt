Deployment of COSMO to OSM
============================ 

First, source the admin spack instance:

.. code-block:: bash
  # source spack instance
  . /project/g110/spack/user/admin-$slave/spack/share/spack/setup-env.sh

Specify the release tag which you want to deploy, with which eccodes definitions version you want to deploy it and the installations paths of both cosmo and eccodes (always precise the tag, the compiler and the compiler version!). For example:
.. code-block:: bash
  COSMO_SPEC="cosmo@5.07.mch1.0.p12%pgi@19.9 +pollen real_type=float cosmo_target=gpu +gt1 +production +claw +eccodes ^cosmo-eccodes-definitions@2.18.0.1"
  ./project/g110/spack-mch/tsa/spack-mch/tools/osm/extract_env.py -s $COSMO_SPEC -i <cosmo_installation_dir> -j <eccodes_installation_dir>

This script is then installing both the tagged cosmo under <cosmo_installation_dir>/bin and eccodes under the given installations directories <eccodes_installation_dir>. A run-env file used to launch cosmo is also installed under the given cosmo install directory and is directly sourceable:

.. code-block:: bash
  cd <run_dir>
  source <cosmo_installation_dir>/run-env
  cp <cosmo_installation_dir>/bin/cosmo_gpu cosmo_gpu
  sbatch slurm_script.slurm
