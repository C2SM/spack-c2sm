Quick Start for Spack
=====================
It is recommended to read the entire documentation to get familiar with Spack.
For those of you with lack of time or interest the following short manuals do the job as well.

COSMO
-----
In order install COSMO fetched from a GitHub repository, use *spack depinstallcosmo*:

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
  spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=gpu +cppdycore

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

