# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
from spack import *

import os
import subprocess


class Int2lm(MakefilePackage):
    """INT2LM performs the interpolation from coarse grid model data to initial
    and/or boundary data for the COSMO-Model."""

    homepage = "http://www.cosmo-model.org/content/model/"
    url = "https://github.com/MeteoSwiss-APN/int2lm/archive/refs/tags/v2.8.4.tar.gz"
    git = 'git@github.com:MeteoSwiss-APN/int2lm.git'
    c2smgit = 'git@github.com:C2SM-RCM/int2lm.git'
    orggit = 'git@github.com:COSMO-ORG/int2lm.git'

    maintainers = ['mjaehn', 'juckerj']

    # APN tags
    version('apn-master', git=git, branch='master')

    # C2SM tags
    version('v2.8.4', git=c2smgit, tag='v2.8.4')
    version('c2sm-master', git=c2smgit, branch='master')
    version('c2sm-features', git=c2smgit, branch='c2sm-features')

    # ORG tags
    version('org-master', git=orggit, branch='master')
    version('int2lm-3.00', git=orggit, tag='int2lm-3.00')

    depends_on('eccodes +fortran')
    depends_on('cosmo-eccodes-definitions', type=('build', 'run'))
    depends_on('libgrib1 @22-01-2020', type='build')
    depends_on('mpi', type=('build', 'link', 'run'), when='+parallel')
    depends_on('netcdf-c', type=('build', 'link'))
    depends_on('netcdf-fortran', type=('build', 'link'))
    depends_on('jasper@1.900.1', type=('build', 'link'))

    variant('debug', default=False, description='Build debug INT2LM')
    variant('parallel', default=True, description='Build parallel INT2LM')
    variant('pollen', default=True, description='Build with pollen enabled')
    variant('slave', default='none', description='Build on slave')
    variant('verbose', default=False, description='Build with verbose enabled')

    # from Spack v0.18 we don't load a Python module prior sourcing Spack.
    # Therefore #!/usr/bin/env python points to python2.
    # Replace with #!/usr/bin/env python3 instead
    patch('patches/testsuite/patch.to_python3',
          when="@apn-master,c2sm-master,c2sm-features")

    conflicts(
        'pollen=True',
        when='@org-master,int2lm-3.00',
        msg=
        'int2lm-org is currently broken with pollen, set variant pollen=False')

    build_directory = 'TESTSUITE'

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

        # Eccodes libraries
        grib_prefix = self.spec['eccodes'].prefix
        env.set(
            'GRIBAPIL',
            str(self.spec['eccodes:fortran'].libs.ld_flags) + ' ' +
            str(self.spec['jasper'].libs.ld_flags))
        grib_inc_dir_path = os.path.join(grib_prefix, 'include')
        if os.path.exists(grib_inc_dir_path):
            env.set('GRIBAPII', '-I' + grib_inc_dir_path)
        else:
            env.set('GRIBAPII', '')

        # Netcdf library
        if self.spec.variants['slave'].value == 'daint':
            env.set('NETCDFL', '-L$(NETCDF_DIR)/lib -lnetcdff -lnetcdf')
            env.set('NETCDFI', '-I$(NETCDF_DIR)/include')
        else:
            env.set(
                'NETCDFL', '-L' + self.spec['netcdf-fortran'].prefix +
                '/lib -lnetcdff -L' + self.spec['netcdf-c'].prefix +
                '/lib64 -lnetcdf')
            env.set('NETCDFI',
                    '-I' + self.spec['netcdf-fortran'].prefix + '/include')

        # Grib1 library
        if self.compiler.name == 'gcc':
            env.set('GRIBDWDL',
                    '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_gnu')
        elif self.compiler.name == 'cce':
            env.set('GRIBDWDL',
                    '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_cray')
        elif self.compiler.name in ('pgi', 'nvhpc'):
            env.set('GRIBDWDL',
                    '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_pgi')
        else:
            env.set(
                'GRIBDWDL', '-L' + self.spec['libgrib1'].prefix +
                '/lib -lgrib1_' + self.compiler.name)

        # MPI library
        if self.spec['mpi'].name == 'openmpi':
            env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpi_mpifh')
            env.set('MPII', '-I' + self.spec['mpi'].prefix + '/include')
        else:
            env.set('MPII', '-I' + self.spec['mpi'].prefix + '/include')
            if self.compiler.name != 'gcc':
                env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpich')

        # Compiler & linker variables
        if self.compiler.name == 'pgi':
            env.set('F90', 'pgf90 -D__PGI_FORTRAN__')
            env.set('LD', 'pgf90 -D__PGI_FORTRAN__')
        elif self.compiler.name == 'nvhpc':
            env.set('F90', 'nvfortran -D__PGI_FORTRAN__')
            env.set('LD', 'nvfortran -D__PGI_FORTRAN__')
        elif self.compiler.name == 'cce':
            env.set('F90', 'ftn -D__CRAY_FORTRAN__')
            env.set('LD', 'ftn -D__CRAY_FORTRAN__')
        else:
            env.set('F90', self.spec['mpi'].mpifc)
            env.set('LD', self.spec['mpi'].mpifc)

    @property
    def build_targets(self):
        build = []
        if self.spec.variants['verbose'].value:
            build.append('VERBOSE=1')
        if self.spec.variants['pollen'].value:
            build.append('ART=1')
        MakeFileTarget = ''
        if '+parallel' in self.spec:
            MakeFileTarget += 'par'
        else:
            MakeFileTarget += 'seq'
        if '+debug' in self.spec:
            MakeFileTarget += 'debug'
        else:
            MakeFileTarget += 'opt'
        build.append(MakeFileTarget)

        return build

    def edit(self, spec, prefix):
        print(os.getcwd())
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            OptionsFileName = 'Options'
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name in ('pgi', 'nvhpc'):
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            makefile.filter('/Options.*', '/' + OptionsFileName)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            install('int2lm', prefix.bin)
            install('int2lm', '../test/testsuite')

    @run_before('edit')
    def create_build_directory(self):
        os.makedirs(self.build_directory, exist_ok=True)

        # link all files for APN and C2SM version of int2lm
        if not os.path.isfile(self.build_directory + '/Options.tsa.pgi'):
            os.chdir(self.build_directory)

            for item in os.listdir('../'):
                os.symlink('../' + item, item)

            os.chdir('..')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        with working_dir('test/testsuite'):
            try:
                subprocess.run(
                    ['./test_int2lm.py', str(self.spec)],
                    stderr=subprocess.STDOUT,
                    check=True)
            except:
                raise InstallError('Testsuite failed')
