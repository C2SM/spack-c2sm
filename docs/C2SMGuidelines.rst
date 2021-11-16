C2SM Guidelines for Spack
=========================
With Spack it is easy to mess up different versions of the same code
as well as handling Spack executables and Spack specs needs to be done
in a Spack way.
In this section C2SM proposes a safe and sustainable way of using Spack
for building, running and storing your libraries and executables.


Building 
^^^^^^^^^
There are two possible ways of building software with Spack.
*spack install* and  *spack dev-build*.
Both of them are fine, but have some specialties one needs to take
into account.

Spack install (C2SM Guidelines)
--------------------------------
Every *spack install* needs a version suffix, i.e *spack install <package>@<version-suffix>*.
This version-suffix can have different meanings:

* branch in the git repository
* one out of several git repositories defined in the package
* a specifc version (git-tag) with a corresponding git-hash hardcoded in the package

Only for the last item in the list above you will always fetch and compile the same code.
The two other items can lead to different codes in case the `HEAD` of this specific branch/repository
got some additional commits in the meantime.

Especially for production it is very important to now which version of a code is actually used.

The variety of different version-suffix for the cosmo-package:

.. code-block:: python

    git      = 'git@github.com:COSMO-ORG/cosmo.git'
    apngit   = 'git@github.com:MeteoSwiss-APN/cosmo.git'
    c2smgit  = 'git@github.com:C2SM-RCM/cosmo.git'

    version('master', branch='master', get_full_repo=True)
    version('mch', git=apngit, branch='mch', get_full_repo=True)
    version('c2sm-master', git=c2smgit, branch='master', get_full_repo=True)
    version('c2sm-features', git=c2smgit, branch='c2sm-features', get_full_repo=True)
    version(5.09, git=c2sm, tag=5.09, get_full_repo=True)

There are three different git repositories available for the cosmo-package:

* COSMO-ORG/cosmo.git: version-suffix *master*
* MeteoSwiss-APN/cosmo.git: version-suffix *mch*
* C2SM-RCM/cosmo.git: version-suffix *c2sm-master*
* C2SM-RCM/cosmo.git: version-suffix *c2sm-features* 

It is clear that only using *spack install <package>@5.09* will always result in the
same code, all other version only point to a `HEAD` of a git branch.

So long story short:

**Always use a valid git tag as a version-suffix when building software for production!**

Spack dev-build (C2SM Guidelines)
--------------------------------
In order to install software with *spack dev-build* one needs a local source code.
Spack will compile the code as it is locally present. Contrary to *spack install*, version-suffix
does not have any affect on the code version compiled. Of course the version-suffix will appear
in the installation path and the Spack database later on.

Using *dev-build* may limit your version-suffix to *dev-build* because of the version already installed
by Jenkins. Therefore you may run into trouble of not being able to install two different
executables from different sources at one time.

In this case it is recommended to store the executables in the source folder they were initially built.
Otherwise the conncection between a specific version-suffix and the corresponding local source is lost.

So long story short:

**Always store the local source and the corresponding executables in the same location**
