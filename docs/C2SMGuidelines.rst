C2SM Guidelines for Spack
=========================

Spack enables users to install software in a very user-friendly way,
for example by allowing different versions or specifications
of the same package to be installed simultaneously, or installing
without having to "manually" download the source code. This comes at
the expense of potentially losing control over the exact
version/specification being installed. For this reason, C2SM has
the following guidelines for building, running and installing your
libraries and executables.

Building 
^^^^^^^^

There are two possible ways of building software with Spack:
``spack install`` and  ``spack dev-build``.
Both are good, but have some special features that need to be taken into account.

Option 1: spack install
-----------------------

Every ``spack install`` command needs a version suffix, 
i.e. ``spack install <package>@<version-suffix>``
This version-suffix can have different meanings:

* branch in the git repository
* one out of several git repositories defined in the package
* a specifc version (git-tag) with a corresponding git-hash hardcoded in the package

Only for the last item in the list above you will always fetch and
compile the same code. The two other items can lead to different
codes in case the ``HEAD`` of this specific branch/repository has received some
additional commits in the meantime.

Especially for production it is very important to know which version of a code is actually used.

For example, there is a variety of different version suffixes for the ``cosmo`` package:

.. code-block:: python

    git      = 'ssh://git@github.com/COSMO-ORG/cosmo.git'
    apngit   = 'ssh://git@github.com/MeteoSwiss-APN/cosmo.git'
    c2smgit  = 'ssh://git@github.com/C2SM-RCM/cosmo.git'

    version('org-master', branch='master', get_full_repo=True)
    version('apn-mch', git=apngit, branch='mch', get_full_repo=True)
    version('c2sm-master', git=c2smgit, branch='master', get_full_repo=True)
    version('c2sm-features', git=c2smgit, branch='c2sm-features', get_full_repo=True)
    version(5.09, git=c2sm, tag=5.09, get_full_repo=True)

Here, there are three different git repositories available for the ``cosmo`` package:

* COSMO-ORG/cosmo.git: version-suffix ``org-master``
* MeteoSwiss-APN/cosmo.git: version-suffix ``apn-mch``
* C2SM-RCM/cosmo.git: version-suffix ``c2sm-master``
* C2SM-RCM/cosmo.git: version-suffix ``c2sm-features`` 

It is clear that only using ``spack install <package>@5.09`` will
always result in the same code, all other version only point to a
``HEAD`` of a git branch.

The list of versions, including tagged versions, is provided by ``spack
info <package_name>``. Note that tagged versions for COSMO on the
``c2sm-features`` branch are not yet provided but will be offered
soon. We thus recommend using the ``spack devbuildcosmo`` command for
now.

..  attention::
    Always use a valid git tag as a version-suffix when building
    software with ``spack install`` for production!

Option 2: spack dev-build
-------------------------

In order to install software with ``spack dev-build``, one needs a
local source code.  Spack will then compile the code as it is locally
present. Contrary to ``spack install``, the version suffix
(``@master``, ``@v2.7.9``, etc.) does not have any effect on the code version compiled.
To be safe, always use ``dev-build`` and copy the executable after installation
into the source folder.

..  attention::
    Always store the local sources and the corresponding executable in
    the same location!

Running
^^^^^^^

When used properly, Spack is able to manage many different
configurations of a package along with the corresponding
run environment.

Load run-environment of a package
---------------------------------

Spack provides the command ``spack load`` to load the environment
needed to run a binary into your current shell. There are two
different ways of using it (both of them are fine).

.. code-block:: console

    $ spack load <package>@<version>%<compiler> +<variants>

The executable now has the correct environment to run in your current shell.

The other possibility is use ``spack load`` to print the required
shell commands and store them in a file that can be sourced at a later
stage:

.. code-block:: console

    $ spack load --sh <package>@<version>%<compiler> +<variants> > run_package.env

An example output of ``spack load -sh`` for COSMO could look as follows:

.. code-block:: console

    export LIBRARY_PATH=/opt/cray/pe/mpt/7.7.15/gni/mpich-pgi/20.1/lib:/project/s903/juckerj/spack-install/daint/eccodes/2.19.0/pgi/ccigv3uvkdl5h3d2jtb6blxvvv4qsdpc/lib64:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib64:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib;
    export LD_LIBRARY_PATH=/opt/cray/pe/mpt/7.7.15/gni/mpich-pgi/20.1/lib:/project/s903/juckerj/spack-install/daint/eccodes/2.19.0/pgi/ccigv3uvkdl5h3d2jtb6blxvvv4qsdpc/lib64:/opt/cray/pe/gcc-libs:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib64:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib:/opt/cray/pe/papi/6.0.0.4/lib64:/opt/cray/job/2.2.4-7.0.2.1_2.86__g36b56f4.ari/lib64;
    export GRIB_SAMPLES_PATH=/project/s903/juckerj/spack-install/daint/cosmo-eccodes-definitions/2.19.0.5/pgi/egf6fp466u2cl3ckkmhpemzf4hz7loqr/cosmoDefinitions/samples;
    export GRIB_DEFINITION_PATH=/project/s903/juckerj/spack-install/daint/cosmo-eccodes-definitions/2.19.0.5/pgi/egf6fp466u2cl3ckkmhpemzf4hz7loqr/cosmoDefinitions/definitions/:/project/s903/juckerj/spack-install/daint/eccodes/2.19.0/pgi/ccigv3uvkdl5h3d2jtb6blxvvv4qsdpc/share/eccodes/definitions;

..  tip::
    Always load the run environment provided by Spack prior to any
    executions of an executable installed by Spack!

Spack in scripts
^^^^^^^^^^^^^^^^

The Spack commands are rather tailored for interacive use. For example,
it is very possible for commands such as ``spack find`` or ``spack
location`` to complain about multiple potential installed ``SPECS`` satisfying
the command line input. For this reason, it is advisable to
avoid spack commands in scripts. However, for ``spack find`` and 
``spack location``, this should not be aproblem. For ``spack load``, we rather
recommend to use it from the login nodes before submitting jobs, inheriting
the environment of the running job from the environment at submission time.
