# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install terra-standalone
#
# You can edit this file again by typing:
#
#     spack edit terra-standalone
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class TerraStandalone(MakefilePackage):
    """TSA is an externalized version of the soil-vegetation-atmosphere transfer scheme of the COSMO model, originally developed by Felix Ament. It consists of the soil module TERRA combined with a simplified transfer scheme, parameterizations of the radiation interaction at the surface, and the annual cycles of vegetation parameters."""

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url      = "https://github.com/COSMO-ORG/terra-standalone/archive/5.03.tar.gz"
    git      = 'git@github.com:COSMO-ORG/terra-standalone.git'

    maintainers = ['vsharma-sonen']

    version('mch-snow-scheme', branch='mch_snow_scheme', preferred=True)
    version('master', branch='master')
    version('5.03', commit='72ec4dc03194b6160bf1987f545cc646db604706')

    depends_on('eccodes')
    depends_on('libaec')
    depends_on('libgrib1')

    def edit(self, spec, prefix):
        mkdirp('obj')
        mkdirp('work')
        makefile = FileFilter('Fopts')
        if '@master' in self.spec:
            makefile.filter('/uwork1/uschaett/lib_gfortran/libgrib1.a', self.spec['libgrib1'].prefix + '/lib/libgrib1_gnu.a')
        else:
            makefile.filter('LIBGRIB1     = .*', 'LIBGRIB1     =' + self.spec['libgrib1'].prefix + '/lib/libgrib1_gnu.a')
        makefile.filter('GRIBDIR      = .*', 'GRIBDIR      =' + self.spec['eccodes'].prefix)
        makefile.filter('LAECDIR      = .*', 'LAECDIR      =' + self.spec['libaec'].prefix)
        makefile = FileFilter('Makefile')
        makefile.filter('STDROOT      = .*', 'STDROOT      = ' + self.build_directory)  

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('tsa_exec', prefix.bin)
