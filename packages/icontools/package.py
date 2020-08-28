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
#     spack install icontools
#
# You can edit this file again by typing:
#
#     spack edit icontools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Icontools(MakefilePackage):
    """The ICON tools are a set of command-line tools for remapping, extracting and querying ICON data files. They are based on a common library, and written in Fortran 90/95. Interfaces to C are available. The code is multi- threaded with OpenMP and MPI-parallel. The DWD ICON tools have replaced the former prepicon utility program."""

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url = "https://github.com/MeteoSwiss-APN/fieldextra-icontools.git"
    git      = 'git@github.com:COSMO-ORG/fieldextra.git'
    maintainers = ['elsagermann']

    version('2.4.3', commit='38a9f830ab15fb9f3b770173f63a3692a6a381a4')

    variant('build_type', default='optimized', description='Build type', values=('debug', 'optimized'))
    variant('openmp', default=True)

    depends_on('netcdf-c')
    depends_on('netcdf-fortran')

    build_directory= 'icontools/icontools-2.4.3/'
    @property
    def build_targets(self):
        spec = self.spec

        if self.compiler.name == 'gcc':
            mode = 'gnu'
        else:
            mode = self.compiler.name
        if spec.variants['build_type'].value == 'debug':
            mode += ',dbg'
        elif spec.variants['build_type'].value == 'optimized':
            mode += ',opt'
        if self.spec.variants['openmp'].value:
            mode += ',omp'

        return ['mode=' + mode,
        ]

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            optionsfilter = FileFilter('Makefile')
            optionsfilter.filter('LIBDIR *=.*', 'LIBDIR = ' + self.prefix + '/lib')
            optionsfilter.filter('INCLUDEDIR *=.*', 'INCLUDEDIR = ' + self.prefix + '/include')
            optionsfilter.filter('lnetcdfdir *=.*', 'lnetcdfdir = ' + spec['netcdf-c'].prefix + '/lib')
            optionsfilter.filter('lnetcdffortrandir *=.*', 'lnetcdffortrandir = ' + spec['netcdf-fortran'].prefix + '/lib')

    def install(self, spec, prefix):
        if self.compiler.name == 'gcc':
            mode = 'gnu'
        else:
            mode = self.compiler.name
        if spec.variants['build_type'].value == 'debug':
            mode += ',dbg'
        elif spec.variants['build_type'].value == 'optimized':
            mode += ',opt'
        if self.spec.variants['openmp'].value:
            mode += ',omp'

        with working_dir(self.build_directory):
            options = ['mode=' + mode]
            make('install', *options)
