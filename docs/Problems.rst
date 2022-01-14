Known Problems with Spack
=============================

Known problems with Spack and how to resolve them.

Error: __init__() got an unexpected keyword argument 'capture_output'
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Spack uses a Python version < 3.6. To fix this issue start again with a **clean shell**
and execute the following (code below is for Daint):

.. code-block:: bash

   module load cray-python # on daint
   source $SPACK_ROOT/share/spack/setup-env.sh
   

Error: Initialization hangs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If `source $SPACK_ROOT/share/spack/setup-env.sh` hangs, clean your cache:

.. code-block:: bash

    rm -rf ~/.spack/cray ~/.spack/cache

Then try again.

Error: Could not determine host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In case you have anything printing the hostname to the terminal in your .bashrc like

.. code-block:: bash
    
    echo $(hostname) 

the setup-env.sh script for Spack does not work. 
A possible workaround is to direct the "echo" to the stderr:

.. code-block:: bash
    
    echo $(hostname) >&2

Error: Broken cache
^^^^^^^^^^^^^^^^^^^^^
(Happening when mixing spack installations and caches)

If ``spack install <package>@<version>%<compiler>`` prints an error message like:

.. code-block:: bash

   ==> Error: 'str' object has no attribute 'get'

you should remove your spack user config scope which is containing the broken cache:

.. code-block:: bash

    rm -rf ~/.spack

Then try again.

Delete entire Spack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As a last option it sometimes helps to delete all directories used by Spack.
These are:

* spack-install
* spack-stages
* modules
* cache

It is important to completely whipe out the folders listed above using the following commands:

**Beware you loose all your installed packages installed by Spack**

.. code-block:: bash
    
    # delete spack-install folder
    rm -rf your_path_to/spack-install

    # delete spack-stages folder
    rm -rf your_path_to/spack-stages

    # delete modules folder
    rm -rf your_path_to/modules

    # delete cache folder
    rm -rf ~/.spack/cache

Known Problems with Spack & ICON
====================================

Error: FetchError: Archive was empty for icon
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Usually happens when trying to do an out-of-source build of ICON, inside of an **empty** directory.
Spack unfortunately does not allow to build in a empty directory, you should therefore create a fake file:


.. code-block:: bash

    touch fake.file
    spack dev-build ...

Error: ProcessError: ./config/cscs/<machine>.<target>.<compiler>: No such file or directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Usually happens when trying to do an out-of-source build of ICON. Either you are in a branch of icon, which indeed
do not contrain <machine>.<target>.<compiler>, or you did give a wrong config_dir argument which should point to icon base directory.

Check your config_dir argument and its given relative path again:

.. code-block:: bash

   spack dev-build -u build icon@dev-build%nvhpc config_dir=./.. icon_target=gpu





