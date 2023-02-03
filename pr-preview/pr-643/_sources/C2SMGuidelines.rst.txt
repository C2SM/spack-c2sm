C2SM Guidelines for Spack
=========================

Spack enables the users to install pieces of software in a very
user-friendly way, allowing e.g. different versions or specifications
of the same package to be installed simultaneously or installing
without having to "manually" download the source code. This comes at
the expense of potentially losing control over the exact
version/specification being installed. That's why C2SM came up with
the following guidelines for building, running and installing your
libraries and executables.

Building 
^^^^^^^^
There are two possible ways of building software with Spack.
*spack install* and  *spack dev-build*.
Both of them are fine, but have some specialties one needs to take
into account.

Spack install (C2SM Guidelines)
-------------------------------
Every *spack-install* needs a version suffix, i.e *spack install <package>@<version-suffix>*.
This version-suffix can have different meanings:

* branch in the git repository
* one out of several git repositories defined in the package
* a specifc version (git-tag) with a corresponding git-hash hardcoded in the package

Only for the last item in the list above you will always fetch and
compile the same code.  The two other items can lead to different
codes in case the *HEAD* of this specific branch/repository got some
additional commits in the meantime.

Especially for production it is very important to now which version of a code is actually used.

The variety of different version-suffix for the cosmo-package:

.. code-block:: python

    git      = 'ssh://git@github.com/COSMO-ORG/cosmo.git'
    apngit   = 'ssh://git@github.com/MeteoSwiss-APN/cosmo.git'
    c2smgit  = 'ssh://git@github.com/C2SM-RCM/cosmo.git'

    version('org-master', branch='master', get_full_repo=True)
    version('apn-mch', git=apngit, branch='mch', get_full_repo=True)
    version('c2sm-master', git=c2smgit, branch='master', get_full_repo=True)
    version('c2sm-features', git=c2smgit, branch='c2sm-features', get_full_repo=True)
    version(5.09, git=c2sm, tag=5.09, get_full_repo=True)

There are three different git repositories available for the cosmo-package:

* COSMO-ORG/cosmo.git: version-suffix *org-master*
* MeteoSwiss-APN/cosmo.git: version-suffix *apn-mch*
* C2SM-RCM/cosmo.git: version-suffix *c2sm-master*
* C2SM-RCM/cosmo.git: version-suffix *c2sm-features* 

It is clear that only using *spack install <package>@5.09* will
always result in the same code, all other version only point to a
*HEAD* of a git branch.

The list of versions, including tagged versions, is provided by *spack
info package_name*. Note that tagged versions for COSMO on the
*c2sm-features* branch are not yet provided but will be offered
soon. We thus recommend using the *spack devbuildcosmo* command for
now.

So long story short:

**Always use a valid git tag as a version-suffix when building
software with** *spack install* **for production!**

Spack dev-build (C2SM Guidelines)
---------------------------------

In order to install software with *spack dev-build* one needs a
local source code.  Spack will compile the code as it is locally
present. Contrary to *spack install*, version-suffix (@master, @v2.7.9, etc,) does not have
any effect on the code version compiled.
To be safe always use *@mdev-build* and copy the executable after installation
into the source-folder.

So long story short:

**Always store the local sources and the corresponding executable in
the same location!**

Installation
^^^^^^^^^^^^

Per default, Spack installs software under ``/$SCRATCH/spack-install``.
On Piz Daint ``$SCRATCH`` undergoes regular cleanup with deletion of
files older than 30 days. This may corrupt the internal Spack database
and lead to unexpected behaviour of Spack.

Change location for package installations
-----------------------------------------

Spack offers the possibility to overwrite the default installation
directory. To do so create the file *~/.spack/config.yaml* and
specify there an install directory that is not deleted regularly like
*/project* or */store* in the following way:

.. code-block:: yaml

  config:                                                                                                                     
     install_tree: /project/s903/juckerj/spack-install/          

**Always change the installation directory to a location that is not
wiped-out regularly!**

Running
^^^^^^^

When used properly, Spack is able to manage many different
configurations of a package along with the corresponding
run-environment.

Load run-environment of a package
---------------------------------

Spack provides the command *spack load* to load the environment
needed to run a binary into your current shell. There are two
different ways of using it and both of them are fine.

.. code-block:: bash

    spack load <package>@<version>%<compiler> +<variants>

The executable now has the correct environment to run in your current shell.

The other possibility is use *spack load* to print the required
shell commands and store them in a file that can be sourced at a later
stage:

.. code-block:: bash

    spack load --sh <package>@<version>%<compiler> +<variants> > run_package.env

An example output of *spack load -sh* for COSMO could look as follows:

.. code-block:: bash

    export LIBRARY_PATH=/opt/cray/pe/mpt/7.7.15/gni/mpich-pgi/20.1/lib:/project/s903/juckerj/spack-install/daint/eccodes/2.19.0/pgi/ccigv3uvkdl5h3d2jtb6blxvvv4qsdpc/lib64:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib64:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib;
    export LD_LIBRARY_PATH=/opt/cray/pe/mpt/7.7.15/gni/mpich-pgi/20.1/lib:/project/s903/juckerj/spack-install/daint/eccodes/2.19.0/pgi/ccigv3uvkdl5h3d2jtb6blxvvv4qsdpc/lib64:/opt/cray/pe/gcc-libs:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib64:/apps/daint/UES/xalt/xalt2/software/xalt/2.8.10/lib:/opt/cray/pe/papi/6.0.0.4/lib64:/opt/cray/job/2.2.4-7.0.2.1_2.86__g36b56f4.ari/lib64;
    export GRIB_SAMPLES_PATH=/project/s903/juckerj/spack-install/daint/cosmo-eccodes-definitions/2.19.0.5/pgi/egf6fp466u2cl3ckkmhpemzf4hz7loqr/cosmoDefinitions/samples;
    export GRIB_DEFINITION_PATH=/project/s903/juckerj/spack-install/daint/cosmo-eccodes-definitions/2.19.0.5/pgi/egf6fp466u2cl3ckkmhpemzf4hz7loqr/cosmoDefinitions/definitions/:/project/s903/juckerj/spack-install/daint/eccodes/2.19.0/pgi/ccigv3uvkdl5h3d2jtb6blxvvv4qsdpc/share/eccodes/definitions;

**Always load the run-environment provided by Spack prior to any
executions of an executable installed by Spack!**

Spack in scripts
^^^^^^^^^^^^^^^^

The Spack commands are rather tailored for interacive use. It is for
instance very possible that commands like *spack find* or *spack
location* complain about several potential installed *SPECS* meeting
the command line input. For this reason it's rather recommended to
avoid spack commands in scripts. This shouldn't be too problematic for
*spack find* and *spack location*. For *spack load* we rather
advise to use it from the login nodes before submitting jobs, the
environment of the running job being inherited from the environment at
submission time.
