PR testing
===================================
To test a PR create a comment ``launch jenkins [--upstream] [--exclusive] [--tsa] [--daint] ...``
with either
* a space separated list of predefined commands (see "supported commands")
or
* a raw spack command

``--upstream`` links the instance with the upstream spack-admin instance.
``--exclusive`` invokes only tests from the listed commands.
``--tsa`` runs tests only on Tsa.
``--daint`` runs tests only on Piz Daint.

What is tested
^^^^^^^^^^^^^^^^
Using predefined commands will trigger a set of packages, plus (if ``--exclusive`` is not set) all packages that depend on them. (See test_spack.py)

Examples:
^^^^^^^^^^^^
``launch jenkins atlas cuda zlib_ng``
No upstream will be used.
All tests from atlas, cuda and zlib_ng will be run, plus all tests from all packages that depend on them.

``launch jenkins --upstream all``
Upstream will be used.
All packages and all use cases will be tested.

``launch jenkins spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore``
No upstream will be used.
``spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore`` will be executed on all machines.

``launch jenkins --exclusive cosmo-dycore``
No upstream will be used.
Only the tests of cosmo-dycore will be run.

Supported commands
^^^^^^^^^^^^^^^^^^^^^
Others:

* all (tests all use cases)
* a raw spack command

Package-name based:

* atlas_utilities
* cosmo
* cosmo-dycore
* cosmo-eccodes-definitions
* cosmo-grib-api
* cosmo-grib-api-definitions
* dawn
* dawn4py
* dusk
* flexpart-ifs
* gridtools
* icon
* icontools
* int2lm
* libgrib1
* oasis
* omni-xmod-pool
* xcodeml-tools
* zlib_ng
