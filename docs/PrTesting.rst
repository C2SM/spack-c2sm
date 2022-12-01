PR testing
===================================
To test a PR create a comment ``launch jenkins [<packages>] [<machines>] [all_packages] [all_machines] [all]``.

It will test the listed packages on the listed machines. ``all`` is equivalent to ``all_packages all_machines``. Order is irrelevant.

Supported packages:

* cosmo-dycore
* cosmo-eccodes-definitions
* cosmo-grib-api
* cosmo-grib-api
* cosmo
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
* omnicompiler
* xcodeml-tools
* zlib_ng

Supported machines:

* balfrin
* daint
* tsa

Examples:
^^^^^^^^^^^^
``launch jenkins int2lm daint`` tests int2lm on daint.

``launch jenkins cosmo int2lm daint tsa`` tests

* cosmo on daint
* cosmo on tsa
* int2lm on daint
* int2lm on tsa

``launch jenkins cosmo icon all_machines`` tests cosmo and icon on all machines.

``launch jenkins all_packages daint`` tests all packages on daint.

``launch jenkins all`` tests all packages on all machines.
