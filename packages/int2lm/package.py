# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
from spack import *

import os
import subprocess

def get_releases(repo):
        git_obj = subprocess.run(["git","ls-remote","--refs",repo], stdout=subprocess.PIPE)
        git_tags = [re.match('refs/tags/(.*)', x.decode('utf-8')).group(1) for x in git_obj.stdout.split() if re.match('refs/tags/(.*)', x.decode('utf-8'))]
        return git_tags

def int2lm_deps(repo):
    tags = get_releases(repo)
    for tag in tags:
        version(tag, git=repo, tag=tag, get_full_repo=True)

    tags.append('master')
    tags.append('dev-build')
    tags.append('mch')
    tags.append('c2sm')

    for tag in tags:    
        prod = [True,False]
        testing = [True, False]
        comb=list(itertools.product(*[prod, testing]))
        for it in comb:
            prod_opt=it[0]
            prod_opt = '+production' if it[0] else '~production'
            test_opt = '+build_tests' if it[1] else '~build_tests'

class Int2lm(MakefilePackage):
    """INT2LM performs the interpolation from coarse grid model data to initial
    and/or boundary data for the COSMO-Model."""

    homepage = "http://www.cosmo-model.org/content/model/"
    git      = 'git@github.com:COSMO-ORG/int2lm.git'
    apngit   = 'git@github.com:MeteoSwiss-APN/int2lm.git'
    c2smgit  = 'git@github.com:C2SM-RCM/int2lm.git'

    maintainers = ['morsier']

    version('master', branch='master')
    version('dev-build', branch='master')
    version('2.08', commit='9e0d0bfe50f8e29676c7d1f0f4205597be8e86e1')
    version('2.07', commit='65ddb3af9b7d63fa2019d8bcee41e8d4a99baedd')
    version('2.06a', commit='eb067a01446f55e1b55f6341681e97a95f856865')
    version('2.06', commit='11065ff1b304129ae19e774ebde02dcd743d2005')
    version('2.05', commit='ef16f54f53401e99aef083c447b4909b8230a4a0')
    version('mch', git='git@github.com:MeteoSwiss-APN/int2lm.git', branch='master', get_full_repo=True)
    version('c2sm', git='git@github.com:C2SM-RCM/int2lm.git', branch='master', get_full_repo=True)

    depends_on('cosmo-grib-api-definitions', type=('build','run'), when='~eccodes')
    depends_on('cosmo-eccodes-definitions ~aec', type=('build','run'), when='+eccodes')
    depends_on('libgrib1@master', type='build')
    depends_on('mpi', type=('build', 'link', 'run'), when='+parallel')
    depends_on('netcdf-c',type=('build', 'link'))
    depends_on('netcdf-fortran +mpi', type=('build', 'link'))

    variant('org', default=False, description='Build INT2LM from COSMO-ORG')
    variant('c2sm', default=False, description='Build INT2LM from C2SM-RCM')
    variant('debug', default=False, description='Build debug INT2LM')
    variant('parallel', default=True, description='Build parallel INT2LM')
    variant('eccodes', default=True, description='Build with eccodes instead of grib-api')
    variant('pollen', default=False, description='Build with pollen enabled')

    variant('slave', default='tsa', description='Build on slave tsa or daint', multi=False)
    variant('verbose', default=False, description='Build with verbose enabled')

    int2lm_deps(git)

    build_directory='TESTSUITE'

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

        # Define the repo
        if '+c2sm' in self.spec:
            int2lm_deps(c2smgit)
            build_directory='./'

        if '+mch' in self.spec:
            int2lm_deps(apngit)
            build_directory='./'
            url = "https://github.com/MeteoSwiss-APN/int2lm/archive/v2.8.3.tar.gz"
            version('v2.8.3', commit='43796aa0a2c56071efc3277397abbbf78dab1247')
            version('v2.8.2', commit='7f8bf2e3f5e77489cfdb4443578a43431408e2bd')
            version('v2.8.1', commit='844d239cfa83bc9980696cae56f47da3d08ce4ec')
            version('v2.7.2', commit='7a460906e826142be1fb9338d2210ccf7566d5a2')
            variant('pollen', default=True, description='Build with pollen enabled')

        # Grib-api. Eccodes libraries
        if '~eccodes' in self.spec:
            grib_prefix = self.spec['cosmo-grib-api'].prefix
            grib_lib_names = ' -lgrib_api_f90 -lgrib_api'
            lib_dir='/lib'
        else:
            grib_prefix = self.spec['eccodes'].prefix
            grib_lib_names = ' -leccodes_f90 -leccodes'
            # Default installation lib path changed to from lib to lib64 after 2.19.0
            if self.spec['eccodes'].version >= Version('2.19.0'):
                lib_dir='/lib64'
            else:
                lib_dir='/lib'
        env.set('GRIBAPIL', '-L' + grib_prefix + lib_dir + grib_lib_names + ' -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
        env.set('GRIBAPII', '-I' + grib_prefix + '/include')

        # Netcdf library
        if self.spec.variants['slave'].value == 'daint':
            env.set('NETCDFL', '-L$(NETCDF_DIR)/lib -lnetcdff -lnetcdf')
            env.set('NETCDFI', '-I$(NETCDF_DIR)/include')
        else:
            env.set('NETCDFL', '-L' + self.spec['netcdf-fortran'].prefix + '/lib -lnetcdff -L' + self.spec['netcdf-c'].prefix + '/lib64 -lnetcdf')
            env.set('NETCDFI', '-I' + self.spec['netcdf-fortran'].prefix + '/include')

        # Grib1 library
        if self.compiler.name == 'gcc':
            env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_gnu')
        elif self.compiler.name == 'cce':
            env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_cray')
        else:
            env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_' + self.compiler.name)

        # MPI library
        if self.spec['mpi'].name == 'openmpi':
            env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpi_mpifh')
            env.set('MPII', '-I'+ self.spec['mpi'].prefix + '/include')
        else:
            env.set('MPII', '-I'+ self.spec['mpi'].prefix + '/include')
            if self.compiler.name != 'gcc':
                env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpich_' + self.compiler.name)

        # Compiler & linker variables
        if self.compiler.name == 'pgi':
            env.set('F90', 'pgf90 -D__PGI_FORTRAN__')
            env.set('LD', 'pgf90 -D__PGI_FORTRAN__')
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
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            OptionsFileName= 'Options'
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name == 'pgi':
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            makefile.filter('/Options.*', '/' + OptionsFileName)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.test)
        install('int2lm', prefix.bin)
        install('int2lm', 'test/testsuite')
        if '+org' in self.spec:
            install('int2lm', '../test/testsuite')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        with working_dir('test/testsuite'):
            try:
                subprocess.run(['./test_int2lm.py', str(self.spec)], stderr=subprocess.STDOUT, check=True)
            except:
                raise InstallError('Testsuite failed')
