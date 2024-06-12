# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install libgrib1
#
# You can edit this file again by typing:
#
#     spack edit libgrib1
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Libgrib1(MakefilePackage):
    """To code / decode the meteorological data to GRIB, special software is needed. While a DWD-written software, the GRIB1-library is used to work with GRIB 1 data, the new application programmers interface grib_api from ECMWF is used for dealing with GRIB 2. But grib_api can also deal with GRIB 1 data. The approach, how data is coded to / decoded from GRIB messages is rather different in these software packages. While the GRIB1-library provides interfaces to code / decode the full GRIB message in one step, the grib_api uses the so-called key/value approach, where the single meta data could be set"""

    homepage = "https://github.com/C2SM-RCM/libgrib1"
    git = "git@github.com:C2SM-RCM/libgrib1.git"

    maintainers = ['jonasjucker']
    build_directory = 'libgrib1_cosmo/source'

    version('master', branch='master')
    version('22-01-2020', commit='3d3db9a9a090f6798c2fd4290c271dd58ff694e0')

    # conflicts('@22-01-2020', when='%gcc@11.3.0')
    # conflicts('@22-01-2020', when='%nvhpc@22.7')

    def edit(self, spec, prefix):
        _makefile_name = 'Makefile.linux'
        if self.compiler.name == 'gcc':
            _makefile_name += '.gnu'
        elif self.compiler.name in ('pgi', 'nvhpc'):
            _makefile_name += '.pgi'
        elif self.compiler.name == 'cce':
            _makefile_name += '.cray'
        self._makefile_name = _makefile_name

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            MakeFileFilter = FileFilter(self._makefile_name)
            stage_path = self.stage.source_path + '/libgrib1_cosmo'
            MakeFileFilter.filter('INCDIR   =.*',
                                  'INCDIR   = {0}/include'.format(stage_path))
            MakeFileFilter.filter('LIBDIR   =.*',
                                  'LIBDIR   = {0}/lib'.format(stage_path))
            options = ['-f', self._makefile_name]
            make(*options)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            options = ['-f', self._makefile_name, 'install']
            make(*options)
        with working_dir('libgrib1_cosmo'):
            install_tree('lib', prefix.lib)
