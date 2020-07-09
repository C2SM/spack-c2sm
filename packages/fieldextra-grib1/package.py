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
#     spack install fieldextra-grib1
#
# You can edit this file again by typing:
#
#     spack edit fieldextra-grib1
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class FieldextraGrib1(MakefilePackage):

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url      = "https://github.com/MeteoSwiss-APN/fieldextra-grib1.git"
    git      = 'git@github.com:MeteoSwiss-APN/fieldextra-grib1.git'
    maintainers = ['elsagermann']

    version('2.15', commit='26d9f416adf395779813e67e37f51f2b5cef7da2')

    variant('build_type', default='optimized', description='Build type', values=('debug', 'optimize    d', 'profiling'))
    variant('openmp', default=True)

    build_directory = 'src'

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
        elif spec.variants['build_type'].value == 'profiling':
            mode += ',prof'
        if self.spec.variants['openmp'].value:
            mode += ',omp'

        return ['mode=' + mode,
        ]

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            optionsfilter = FileFilter('Makefile')
            optionsfilter.filter('INCDIR *=.*', 'INCDIR = ../include')
            optionsfilter.filter('LIBDIR *=.*', 'LIBDIR = ' + self.prefix + '/lib')
            optionsfilter.filter('INCLUDEDIR *=.*', 'INCLUDEDIR = ' + self.prefix + '/include')

    def install(self, spec, prefix):
        if self.compiler.name == 'gcc':
            mode = 'gnu'
        else:
            mode = self.compiler.name
        if spec.variants['build_type'].value == 'debug':
            mode += ',dbg'
        elif spec.variants['build_type'].value == 'optimized':
            mode += ',opt'
        elif spec.variants['build_type'].value == 'profiling':
            mode += ',prof'
        if self.spec.variants['openmp'].value:
            mode += ',omp'

        with working_dir(self.build_directory):
            options = ['mode=' + mode]
            make('install', *options)
