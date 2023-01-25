PR testing
===================================
To test a PR create a comment ``launch jenkins [<packages>] [<machines>]``.

It will test the listed packages on the listed machines.
No package means all packages. No machine means all machines.
Order is irrelevant.

Examples:
``launch jenkins int2lm daint`` tests int2lm on daint.

``launch jenkins cosmo int2lm daint tsa`` tests

* cosmo on daint
* cosmo on tsa
* int2lm on daint
* int2lm on tsa

``launch jenkins cosmo icon`` tests cosmo and icon on all machines.

``launch jenkins daint`` tests all packages on daint.

``launch jenkins`` tests all packages on all machines.

``launch jenkins all`` tests all packages on all machines.


Supported packages: all folder names in folder 'packages'.

Supported machines:

* balfrin
* daint
* tsa
