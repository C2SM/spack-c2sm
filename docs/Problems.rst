Known Problems with Spack
=============================

Known problems with Spack and how to resolve them.

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
