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
import subprocess

class Fieldextra(CMakePackage):
    """Fieldextra is a generic tool to manipulate NWP model data and gridded observations; simple data processing and more complex data operations are supported. Fieldextra is designed as a toolbox; a large set of primitive operations which can be arbitrarily combined are provided."""

    homepage = "http://www.cosmo-model.org/content/support/software/default.html"
    url      = "https://github.com/COSMO-ORG/fieldextra"
    git      = 'git@github.com:COSMO-ORG/fieldextra.git'
    maintainers = ['elsagermann']

    version('develop', branch='develop')
    version('v13_2_2', commit='38a9f830ab15fb9f3b770173f63a3692a6a381a4')
    version('v13_2_1', commit='1f0d57cdb5819bca3249648e9accaabf8f540e00')
    version('v13_2_0', commit='fe0a8b14314d7527168fd5684d89828bbd83ebf2')
    version('v13_1_0', commit='9649ec36dc36dfe3ef679a507f9a849dc2fdd452')

    variant('build_type', default='Optimized', description='Build type', values=('Optimized', 'Profiling', 'Debug'))
    variant('openmp', default=True)

    depends_on('libaec@1.0.0 ~build_shared_libs')
    depends_on('jasper@1.900.1 ~shared', when='@v13_2_0:v13_2_1')
    depends_on('jasper@2.0.14 ~shared', when='@v13_2_2:')
    depends_on('hdf5@1.8.21 +hl +fortran ~mpi')
    depends_on('zlib@1.2.11')
    depends_on('netcdf-c@4.4.0 ~mpi')
    depends_on('netcdf-fortran@4.4.4 ~shared ~mpi')
    depends_on('rttov@11.2.0')

    # parallelization
    depends_on('cosmo-eccodes-definitions@2.18.0.1 ~aec +openmp', when='@v13_2_2:+openmp')
    depends_on('cosmo-eccodes-definitions@2.18.0.1 ~aec ~openmp', when='@v13_2_2:~openmp')
    depends_on('cosmo-eccodes-definitions@2.14.1.2 ~aec +openmp', when='@v13_2_0:v13_2_1+openmp')
    depends_on('cosmo-eccodes-definitions@2.14.1.2 ~aec ~openmp', when='@v13_2_0:v13_2_1~openmp')
    depends_on('eccodes@2.18.0 ~aec +openmp', when='@v13_2_2: +openmp')
    depends_on('eccodes@2.18.0 ~aec ~openmp', when='@v13_2_2: ~openmp')
    depends_on('eccodes@2.14.1 ~aec +openmp', when='+openmp@v13_2_0:v13_2_1')
    depends_on('eccodes@2.14.1 ~aec ~openmp', when='~openmp@v13_2_0:v13_2_1')
    depends_on('icontools@2.4.3 +openmp', when='+openmp')
    depends_on('icontools@2.4.3 ~openmp', when='~openmp')
    depends_on('fieldextra-grib1@v13_2_2 +openmp', when='+openmp @v13_2_2')
    depends_on('fieldextra-grib1@v13_2_2 ~openmp', when='~openmp @v13_2_2')
    depends_on('fieldextra-grib1@v13_2_1 +openmp', when='+openmp @v13_2_1')
    depends_on('fieldextra-grib1@v13_2_1 ~openmp', when='~openmp @v13_2_1')

    # optimization
    # optimized
    depends_on('icontools build_type=optimized', when='build_type=Optimized')
    depends_on('fieldextra-grib1 build_type=optimized', when='build_type=Optimized')

    # debug
    depends_on('icontools build_type=debug', when='build_type=Debug')
    depends_on('fieldextra-grib1 build_type=debug', when='build_type=Debug')

    # profiling
    depends_on('icontools build_type=debug', when='build_type=Profiling')
    depends_on('fieldextra-grib1 build_type=profiling', when='build_type=Profiling')

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

    def cmake_args(self):
        spec = self.spec

        args = []

        exe_name='fieldextra'

        if self.compiler.name == 'gcc':
            exe_name = exe_name + '_gnu'
        else:
            exe_name = exe_name + self.compiler.name
        if self.spec.variants['build_type'].value == 'Optimized':
            exe_name = exe_name + '_opt'
        elif self.spec.variants['build_type'].value == 'Debug':
            exe_name = exe_name + '_dbg'
        elif self.spec.variants['build_type'].value == 'Profiling':
            exe_name = exe_name + '_prof'
        if '+openmp' in spec:
            exe_name = exe_name + '_omp'
        elif '~openmp' in spec:
            exe_name = exe_name + '_noomp'

        args.append('-DFXTREXE=' + exe_name)

        # needed to avoid conflicts with CMake Rpath settings
        args.append('-DCMAKE_BUILD_WITH_INSTALL_RPATH=1')
        args.append('-DRTTOV_VERSION={0}'.format(spec.format('{^rttov.version}')))

        if '~openmp' in spec:
            args.append('-DMULTITHREADED_BUILD=OFF')
        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        if self.compiler.name == 'gcc':
            compiler_name = 'gnu'
        else:
            compiler_name = self.compiler.name

        # Check if correct mode
        if '~openmp' in self.spec or self.spec.variants['build_type'].value != 'Optimized':
            raise InstallError('Tests only available for optimized openmp mode!')

        force_symlink(self.prefix + '/bin', 'bin')
        # Installing cookbook input and reference_cookbook
        with working_dir('cookbook/support'):
            force_symlink('/store/s83/tsm/fieldextra/static/cookbook/input' ,'input')
        force_symlink('/store/s83/tsm/fieldextra/static/cookbook/' + self.spec.format('{version}'), 'reference_cookbook')

        # Installing eccodes definitions and samples
        with working_dir('resources'):
            force_symlink(self.spec['cosmo-eccodes-definitions'].prefix + '/cosmoDefinitions/definitions', 'eccodes_definitions_cosmo')
            force_symlink(self.spec['eccodes'].prefix + '/share/eccodes/definitions/', 'eccodes_definitions_vendor')
            force_symlink(self.spec['cosmo-eccodes-definitions'].prefix + '/cosmoDefinitions/samples', 'eccodes_samples')

        # Creating symlinks for tools/support
        with working_dir('tools/support'):
            force_symlink('../../resources', 'dictionaries')
            force_symlink('../../resources/eccodes_definitions_cosmo', 'eccodes_definitions_1')
            force_symlink('../../resources/eccodes_definitions_vendor', 'eccodes_definitions_2')
            force_symlink('../../bin/fieldextra_gnu_opt_omp', 'fieldextra')
            force_symlink('../../resources/eccodes_samples/COSMO_GRIB2_default.tmpl', 'grib2_sample')

        # Launching tests
        try:
            subprocess.run(['./cookbook/run.bash', '-c', compiler_name, '-m', 'opt_omp'])
        except:
            raise InstallError('Tests failed')

