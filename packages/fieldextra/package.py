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

    build_directory = 'src'
    
    @property
    def build_targets(self):
        spec = self.spec
        
        global mode

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
            optionsfilter.filter('lgrib1dir *=.*', 'lgrib1dir = ' + spec['fieldextra-grib1'].prefix + '/lib')
            optionsfilter.filter('laecdir *=.*', 'laecdir = ' + spec['libaec'].prefix + '/lib')
            optionsfilter.filter('ljasperdir *=.*', 'ljasperdir = ' + spec['jasper'].prefix + '/lib')
            optionsfilter.filter('leccdir *=.*', 'leccdir = ' + spec['eccodes'].prefix + '/lib')
            optionsfilter.filter('lzdir *=.*', 'lzdir = ' + spec['zlib'].prefix + '/lib')
            optionsfilter.filter('lhdf5dir *=.*', 'lhdf5dir = ' + spec['hdf5'].prefix + '/lib')
            optionsfilter.filter('lnetcdfcdir *=.*', 'lnetcdfcdir = ' + spec['netcdf-c'].prefix + '/lib')
            optionsfilter.filter('lnetcdffortrandir *=.*', 'lnetcdffortrandir = ' + spec['netcdf-fortran'].prefix + '/lib')
            optionsfilter.filter('lrttovdir *=.*', 'lrttovdir = ' + spec['rttov'].prefix + '/lib')
            optionsfilter.filter('licontoolsdir *=.*', 'licontoolsdir = ' + spec['icontools'].prefix + '/lib')  
            force_symlink('locale_mch/fxtr_operator_specific.f90', 'fxtr_operator_specific.f90')
            force_symlink('locale_mch/fxtr_write_specific.f90', 'fxtr_write_specific.f90')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            options = ['mode=' + mode]
            make('install', *options)
        install_tree('bin', prefix.bin)
        install_tree('cookbook', prefix.cookbook)
        install_tree('resources', prefix.resources)


    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        copy_tree(self.spec['eccodes'].prefix +'/bin', self.build_directory + '/../tools')
        copy_tree(self.spec['netcdf-c'].prefix +'/bin', self.build_directory + '/../tools')
        copy_tree(self.spec['netcdf-fortran'].prefix +'/bin', self.build_directory + '/../tools')
        with working_dir('cookbook'):
            run_cmd = './run.bash'
            if self.compiler.name == 'gcc':
                run_cmd += ' -c gnu'
            else:
                run_cmd +=  ' -c ' + self.compiler.name
            run_cmd += ' -m opt_omp'
            run_test = Executable(run_cmd)
            run_test()
