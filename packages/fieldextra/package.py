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


class Fieldextra(CMakePackage):
    """Fieldextra is a generic tool to manipulate NWP model data and gridded observations; simple data processing and more complex data operations are supported. Fieldextra is designed as a toolbox; a large set of primitive operations which can be arbitrarily combined are provided."""

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url      = "https://github.com/COSMO-ORG/fieldextra"
    git      = 'git@github.com:COSMO-ORG/fieldextra.git'
    maintainers = ['elsagermann']

    version('v13.2.0', commit='fe0a8b14314d7527168fd5684d89828bbd83ebf2')
    version('v13.1.0', commit='9649ec36dc36dfe3ef679a507f9a849dc2fdd452')
    
    variant('build_type', default='optimized', description='Build type', values=('debug', 'optimized', 'profiling'))
    variant('openmp', default=True)

    depends_on('libaec@1.0.0 ~build_shared_libs')
    depends_on('jasper@1.900.1 ~shared')
    depends_on('hdf5@1.8.21 +hl ~mpi +fortran')
    depends_on('zlib@1.2.11')
    depends_on('netcdf-c ~mpi')
    depends_on('netcdf-fortran ~mpi')
    depends_on('rttov@11.2.0')

    # parallelization
    depends_on('eccodes@2.14.1 build_type=Production jp2k=jasper +openmp', when='+openmp')
    depends_on('eccodes@2.14.1 build_type=Production jp2k=jasper ~openmp', when='~openmp')
    depends_on('icontools@2.3.6 +openmp', when='+openmp')
    depends_on('icontools@2.3.6 ~openmp', when='~openmp')
    depends_on('fieldextra-grib1@2.15 +openmp', when='+openmp')
    depends_on('fieldextra-grib1@2.15 ~openmp', when='~openmp')
    
    # optimization
    # optimized
    depends_on('icontools@2.3.6 build_type=optimized', when='build_type=optimized')
    depends_on('fieldextra-grib1@2.15 build_type=optimized', when='build_type=optimized')

    # debug
    depends_on('icontools@2.3.6 build_type=debug', when='build_type=debug')
    depends_on('fieldextra-grib1@2.15 build_type=debug', when='build_type=debug')

    # profiling
    depends_on('icontools@2.3.6 build_type=debug', when='build_type=debug')
    depends_on('fieldextra-grib1@2.15 build_type=profiling', when='build_type=profiling')
    
    
    def cmake_args(self):
        spec = self.spec
        
        args = []

        return args

    # @run_after('install')
    # @on_package_attributes(run_tests=True)
    # def test(self):
