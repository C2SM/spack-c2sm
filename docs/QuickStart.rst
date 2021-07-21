Quick Start for Spack
=====================
It is recommended to read the entire documentation to get familiar with Spack.
For those of you with lack of time or interest the following short manuals do the job as well.

Source Spack instance on Piz Daint
----------------------------------

.. code-block:: bash

  module load cray-python
  source /project/g110/spack/user/daint/spack/share/spack/setup-env.sh


COSMO-Model
-----------
In order install COSMO fetched from a GitHub repository, use *spack installcosmo*:

.. code-block:: bash

  spack installcosmo cosmo@<version>%<compiler> +<variants>

The second option *spack devbuildcosmo* allows to build COSMO with a local source:

.. code-block:: bash

  cd </path/to/package> 
  spack devbuildcosmo cosmo@<version>%<compiler> +<variants>


COSMO GPU build
^^^^^^^^^^^^^^^
The commands below build COSMO with the C++ Dycore for the target GPU.

.. code-block:: bash

  spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore 

or

.. code-block:: bash

  cd </path/to/package> 
  spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=gpu +cppdycore


COSMO CPU build
^^^^^^^^^^^^^^^
The commands below build COSMO without the C++ Dycore  for the target CPU.

.. code-block:: bash

  spack installcosmo cosmo@master%pgi cosmo_target=cpu ~cppdycore 

or

.. code-block:: bash

  cd </path/to/package> 
  spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=cpu ~cppdycore

Int2lm
------
In order to install int2lm fetched from a GitHub repository, use *spack install*:

.. code-block:: bash

  spack install int2lm@<version>%<compiler> +<variants>

The second option *spack dev-build* allows to build int2lm with a local source:

.. code-block:: bash

  cd </path/to/package> 
  spack dev-build int2lm@<version>%<compiler> +<variants>

Int2lm from C2SM-RCM
^^^^^^^^^^^^^^^^^^^^
In order to build int2lm from the C2SM-RCM GitHub organization use the following command:

.. code-block:: bash

  spack install int2lm@c2sm_master%pgi

Int2lm from COSMO-ORG
^^^^^^^^^^^^^^^^^^^^^
In order to build int2lm from the COSMO-ORG GitHub organization use the following command:

.. code-block:: bash

  spack install int2lm@org_master%pgi pollen=False

ICON
------
In order to install icon fetched from a GitHub repository, use *spack install*:

.. code-block:: bash

  spack install icon@<version>%<compiler> +<variants> #@nwp, @cscs, ...

The second option *spack dev-build* allows to build icon with a local source:

.. code-block:: bash

  cd </path/to/package> 
  spack dev-build icon@dev-build%<compiler> +<variants>

ICON CPU BUILD
^^^^^^^^^^^^^^^^^^^^
In order to build a CPU icon binary from a local source

.. code-block:: bash

  cd </path/to/package> 
  mkdir pgi_cpu
  cd pgi_cpu
  spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=cpu # don't forget +eccodes if you want eccodes, add +skip-config to only do make

ICON GPU BUILD
^^^^^^^^^^^^^^^^^^^^
In order to build a GPU icon binary from a local source

.. code-block:: bash

  cd </path/to/package> 
  mkdir pgi_gpu
  cd pgi_gpu
  spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=gpu # don't forget +eccodes if you want eccodes, add +skip-config to only do make

Accessing executables
---------------------
`As stated in the official spack documentation
<https://spack.readthedocs.io/en/latest/workflows.html#find-and-run>`_,
"The simplest way to run a Spack binary is to find it and run it" as
it is build with `RPATH`. In most cases there is no need to adjust the
environment. In order to find the directory where a package was
installed, use the ``spack location`` command like this:

.. code-block:: bash

  spack location -i cosmo@dev-build%pgi cosmo_target=gpu +cppdycore

or

.. code-block:: bash

  spack location -i int2lm@c2sm_master%pgi

Note that the package location is also given on the last log line of
the install process. For cosmo you'll find the executable, either
``cosmo_cpu`` or ``cosmo_gpu``, under the ``bin`` subdirectory whereas the
int2lm executable will be the ``bin`` *file* itself.
