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
#     spack install fieldextra
#
# You can edit this file again by typing:
#
#     spack edit fieldextra
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Fieldextra(MakefilePackage):
    """Fieldextra is a generic tool to manipulate NWP model data and gridded observations; simple data processing and more complex data operations are supported. Fieldextra is designed as a toolbox; a large set of primitive operations which can be arbitrarily combined are provided."""

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url      = "https://github.com/COSMO-ORG/fieldextra/archive/v13.2.0.tar.gz"
    git      = 'git@github.com:COSMO-ORG/fieldextra.git'
    maintainers = ['elsagermann']

    version('v13.2.0', 'fe0a8b14314d7527168fd5684d89828bbd83ebf2')
    version('v13.1.0', '9649ec36dc36dfe3ef679a507f9a849dc2fdd452')

    depends_on('libaec@1.0.0')
    depends_on('jasper@1.900.1')
    depends_on('eccodes@2.14.1 jp2k=jasper +openmp')
    depends_on('hdf5@1.8.21')
    depends_on('zlib@1.2.11')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    depends_on('rttov')
    depends_on('libgrib1')
    depends_on('icontools@2.3.6')

    va
    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
