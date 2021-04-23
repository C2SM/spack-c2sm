Spack Instance Management
============================

How to re-create the spack instance
------------------------------------

First, you might want to delete the old spack instances if you want to refresh them.

.. code-block:: bash

  rm -rf /project/g110/spack/user/admin-$slave /project/g110/spack/user/$slave

If you want to recreate them from scratch, don't forget to remove their associated installations directories (modules, stages & installations)

.. code-block:: bash

  rm -rf /project/g110/modules/admin-$slave/ /project/g110/spack-stages/$slave /project/g110/spack-install/$slave

Once this is done, you can use the config.py of the spack-mch instance to create the two mch instances (admin for the official installation under /project/g110/spack-install, users installation under /scratch/$user/spack/spack-install)

.. code-block:: bash

  git clone https://github.com/MeteoSwiss-APN/spack-mch/
  cd spack-mch
  ./config.py -m admin-$slave -i /project/g110/spack/user/admin-$slave
  ./config.py -m $slave -i /project/g110/spack/user/$slave

Finally install something with both instances to create a database file for the admin-instance respectively a junit-report file for the users instance, both files being needed to be able to source and install as a non-jenkins user. In order to do that first source the corresponding instances and then install something (Ex: the grib-api definitions).

Admin instance:

.. code-block:: bash

  . /project/g110/spack/user/admin-$slave/spack/share/spack/setup-env.sh
  spack install cosmo-grib-api-definition

Users instance:

.. code-block:: bash

  . /project/g110/spack/user/admin-$slave/spack/share/spack/setup-env.sh
  spack install cosmo-grib-api-definition

Change location for package installations
-----------------------------------------
Spack offers the possibility to overwrite the default installation
directory in */scratch/$USER/spack-install*. This is recommended on **Piz Daint**
due to the regular clean-up on scratch. 
To do so create the file **config.yaml** in *~/.spack* with a directory that is not deleted regularly like */project*
or */store*:

.. code-block:: yaml

  config:                                                                                                                     
     install_tree: /project/s903/juckerj/spack-install/          

