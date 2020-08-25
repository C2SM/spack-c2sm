# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess, re, itertools
from spack import *

def get_releases(repo):
        git_obj = subprocess.run(["git","ls-remote",repo], stdout=subprocess.PIPE)
        git_tags = [re.match('refs/tags/(.*)', x.decode('utf-8')).group(1) for x in git_obj.stdout.split() if re.match('refs/tags/(.*)', x.decode('utf-8'))]
        return git_tags
def dycore_deps(repo):
    tags = get_releases(repo)
    for tag in tags:
        version(tag, git=repo, tag=tag)

    tags.append('master')
    tags.append('dev-build')
    tags.append('mch')

    for tag in tags:    
        types = ['float','double']
        prod = [True,False]
        cuda = [True, False]
        testing = [True, False]
        gt1 = [True, False]
        comb=list(itertools.product(*[types, prod, cuda, testing, gt1]))
        for it in comb:
            real_type=it[0]
            prod_opt = '+production' if it[1] else '~production'
            cuda_opt = '+cuda' if it[2] else '~cuda cuda_arch=none'
            cuda_dep = 'cosmo_target=gpu' if it[2] else ' cosmo_target=cpu'
            test_opt = '+build_tests' if it[3] else '~build_tests'
            test_dep = '+dycoretest' if it[3] else '~dycoretest'
            gt1_dep = '+gt1' if it[4] else '~gt1'

            orig='cosmo-dycore@'+tag+'%gcc real_type='+real_type+' '+ prod_opt + ' ' + cuda_opt+' ' +test_opt + ' ' + gt1_dep
            dep='@'+tag+' real_type='+real_type+' '+ prod_opt + ' '+ cuda_dep + ' +cppdycore'+' '+test_dep + ' ' + gt1_dep
            depends_on(orig, when=dep)

class Cosmo(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = "http://www.cosmo-model.org"
    url      = "https://github.com/MeteoSwiss-APN/cosmo/archive/5.07.mch1.0.p5.tar.gz"
    git      = 'git@github.com:COSMO-ORG/cosmo.git'
    apngit   = 'git@github.com:MeteoSwiss-APN/cosmo.git'
    maintainers = ['elsagermann']

    version('master', branch='master', get_full_repo=True)
    version('dev-build', branch='master', get_full_repo=True)
    version('mch', git='git@github.com:MeteoSwiss-APN/cosmo.git', branch='mch', get_full_repo=True)

    patch('patches/5.07.mch1.0.p4/patch.Makefile', when='@5.07.mch1.0.p4')
    patch('patches/5.07.mch1.0.p4/patch.Makefile', when='@5.07.mch1.0.p5')

    dycore_deps(apngit)

    depends_on('netcdf-fortran +mpi')
    depends_on('netcdf-c +mpi')
    depends_on('slurm%gcc', type='run')
    depends_on('cuda%gcc', when='cosmo_target=gpu', type=('build', 'run'))
    depends_on('serialbox@2.6.0', when='+serialize')
    depends_on('mpi', type=('build', 'run'))
    depends_on('libgrib1')
    depends_on('jasper@1.900.1%gcc ~shared')
    depends_on('cosmo-grib-api-definitions', when='~eccodes')
    depends_on('cosmo-eccodes-definitions@2.14.1.2 ~aec', when='+eccodes')
    depends_on('perl@5.16.3:')
    depends_on('omni-xmod-pool', when='+claw')
    depends_on('claw', when='+claw')
    depends_on('boost%gcc', when='cosmo_target=gpu ~cppdycore')
    depends_on('cmake%gcc')

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('dycoretest', default=True, description='Build C++ dycore with testing')
    variant('serialize', default=False, description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO')
    variant('debug', default=False, description='Build debug mode')
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('claw', default=False, description='Build with claw-compiler')
    variant('slave', default='tsa', description='Build on slave tsa, daint or kesch', multi=False)
    variant('eccodes', default=True, description='Build with eccodes instead of grib-api')
    variant('pollen', default=False, description='Build with pollen enabled')
    variant('cosmo_target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('verbose', default=False, description='Build cosmo with verbose enabled')
    variant('gt1', default=False, description='Build dycore with gridtools 1.1.3')
    variant('cuda_arch', default='none', description='Build with cuda_arch', values=('70', '60', '37'), multi=False)

    conflicts('+claw', when='cosmo_target=cpu')
    conflicts('+pollen', when='@5.05:5.06,master')
    # previous versions contain a bug affecting serialization
    conflicts('+serialize', when='@5.07.mch1.0.p2:5.07.mch1.0.p3')
    variant('production', default=False, description='Force all variants to be the ones used in production')

    conflicts('+production', when='~cppdycore')
    conflicts('+production', when='+serialize')
    conflicts('+production', when='+debug')
    conflicts('+production', when='~claw')
    conflicts('+production', when='~parallel')
    conflicts('+production', when='cosmo_target=cpu')
    conflicts('+production', when='~pollen')
    conflicts('+production', when='%gcc')
    conflicts('+production', when='~eccodes')
    conflicts('~gt1', when='@5.07.mch1.0.p11')
    conflicts('~gt1', when='@5.07a.mch1.0.p1')
    conflicts('~gt1', when='@5.07a.mch1.0.base')
    conflicts('~gt1', when='@5.07.mch1.0.p10')
    conflicts('+cppdycore', when='%pgi cosmo_target=cpu')

    build_directory = 'cosmo/ACC'

    def setup_environment(self, spack_env, run_env):
        # Grib-api. eccodes library
        if '~eccodes' in self.spec:
            grib_prefix = self.spec['cosmo-grib-api'].prefix
            grib_definition_prefix = self.spec['cosmo-grib-api-definitions'].prefix
            spack_env.set('GRIBAPIL', '-L' + grib_prefix + '/lib -lgrib_api_f90 -lgrib_api -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
            spack_env.set('GRIBAPII', '-I' + grib_prefix + '/include')
            spack_env.set('GRIB_DEFINITION_PATH', grib_definition_prefix + '/cosmoDefinitions/definitions/:' + grib_prefix + '/share/grib_api/definitions/')
            spack_env.set('GRIB_SAMPLES_PATH', grib_definition_prefix + '/cosmoDefinitions/samples/')
        else:
            grib_prefix = self.spec['eccodes'].prefix
            grib_definition_prefix = self.spec['cosmo-eccodes-definitions'].prefix
            spack_env.set('GRIBAPIL', '-L' + grib_prefix + '/lib -leccodes_f90 -leccodes -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
            spack_env.set('GRIBAPII', '-I' + grib_prefix + '/include')
            spack_env.set('ECCODES_DEFINITION_PATH', grib_definition_prefix + '/cosmoDefinitions/definitions/:' + grib_prefix + '/share/eccodes/definitions/')
            spack_env.set('ECCODES_SAMPLES_PATH', grib_definition_prefix + '/cosmoDefinitions/samples/')

        # Netcdf library
        if self.spec.variants['slave'].value == 'daint':
            spack_env.set('NETCDFL', '-L$(NETCDF_DIR)/lib -lnetcdff -lnetcdf')
            spack_env.set('NETCDFI', '-I$(NETCDF_DIR)/include')
        else:
            spack_env.set('NETCDFL', '-L' + self.spec['netcdf-fortran'].prefix + '/lib -lnetcdff -L' + self.spec['netcdf-c'].prefix + '/lib64 -lnetcdf')
            spack_env.set('NETCDFI', '-I' + self.spec['netcdf-fortran'].prefix + '/include')

        # Grib1 library
        if self.compiler.name == 'gcc':
            spack_env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_gnu')
        else:
            spack_env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_' + self.compiler.name)
        spack_env.set('GRIBDWDI', '-I' + self.spec['libgrib1'].prefix + '/include')
        
        # MPI library
        if self.spec['mpi'].name == 'openmpi':
            spack_env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpi_cxx')        
        spack_env.set('MPII', '-I'+ self.spec['mpi'].prefix + '/include')
        
        # Dycoregt & Gridtools linrary
        if '+cppdycore' in self.spec:
            if '+gt1' in self.spec:
                spack_env.set('GRIDTOOLS_DIR', self.spec['gridtools'].prefix)
                spack_env.set('GRIDTOOLSL', '-L' + self.spec['gridtools'].prefix + '/lib -lgcl')
                spack_env.set('GRIDTOOLSI', '-I' + self.spec['gridtools'].prefix + '/include/gridtools')
            spack_env.set('DYCOREGT', self.spec['cosmo-dycore'].prefix)
            spack_env.set('DYCOREGT_DIR', self.spec['cosmo-dycore'].prefix)
            spack_env.set('DYCOREGTL', '-L' + self.spec['cosmo-dycore'].prefix + '/lib -ldycore_bindings_' + self.spec.variants['real_type'].value + ' -ldycore_base_bindings_' + self.spec.variants['real_type'].value + ' -ldycore -ldycore_base -ldycore_backend -lstdc++ -lcpp_bindgen_generator -lcpp_bindgen_handle -lgt_gcl_bindings')
            spack_env.set('DYCOREGTI', '-I' + self.spec['cosmo-dycore'].prefix)

        # Serialbox library
        if '+serialize' in self.spec:
            spack_env.set('SERIALBOX', self.spec['serialbox'].prefix)
            spack_env.set('SERIALBOXL', self.spec['serialbox'].prefix + '/lib/libSerialboxFortran.a ' +  self.spec['serialbox'].prefix + '/lib/libSerialboxC.a ' + self.spec['serialbox'].prefix + '/lib/libSerialboxCore.a -lstdc++fs -lpthread -lstdc++')
            spack_env.set('SERIALBOXI','-I' + self.spec['serialbox'].prefix + '/include')

        # Claw library
        if '+claw' in self.spec:
            if 'cosmo_target=gpu' in self.spec:
                spack_env.append_flags('CLAWFC_FLAGS', '--directive=openacc -v')
            spack_env.set('CLAWDIR', self.spec['claw'].prefix)
            spack_env.set('CLAWFC', self.spec['claw'].prefix + '/bin/clawfc')
            spack_env.set('CLAWXMODSPOOL', self.spec['omni-xmod-pool'].prefix + '/omniXmodPool/')
            if self.spec['mpi'].name == 'mpich':
                spack_env.set('CLAWFC_FLAGS', '-U__CRAYXC')

        # Linker flags
        if self.compiler.name == 'pgi' and '~cppdycore' in self.spec:
            env['LFLAGS'] = '-lstdc++'

        # Test-enabling variables
        spack_env.set('UCX_MEMTYPE_CACHE', 'n')
        if self.spec.variants['cosmo_target'].value == 'gpu':
          spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cuda_copy,cuda_ipc,cma')
        else:
            spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cma')

        # Compiler & linker variables
        if self.compiler.name == 'pgi':
            spack_env.set('F90', self.spec['mpi'].mpifc + ' -D__PGI_FORTRAN__')
            spack_env.set('LD', self.spec['mpi'].mpifc + ' -D__PGI_FORTRAN__')
        else:
            spack_env.set('F90', self.spec['mpi'].mpifc)
            spack_env.set('LD', self.spec['mpi'].mpifc)

    @property
    def build_targets(self):
        build = []
        if self.spec.variants['pollen'].value:
            build.append('POLLEN=1')
        if self.spec.variants['real_type'].value == 'float':
            build.append('SINGLEPRECISION=1')
        if '+cppdycore' in self.spec:
            build.append('CPP_GT_DYCORE=1')
        if '+claw' in self.spec:
            build.append('CLAW=1')
        if '+serialize' in self.spec:
            build.append('SERIALIZE=1')
        if self.spec.variants['verbose'].value:
            build.append('VERBOSE=1')
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
            OptionsFileName= 'Options'
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name == 'pgi':
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            OptionsFileName += '.' + spec.variants['cosmo_target'].value
            OptionsFile = FileFilter(OptionsFileName)
            
            makefile = FileFilter('Makefile')
            makefile.filter('/Options.*', '/' + OptionsFileName)
            if '~serialize' in spec:
                makefile.filter('TARGET     :=.*', 'TARGET     := {0}'.format('cosmo_'+ spec.variants['cosmo_target'].value))
            else:
                makefile.filter('TARGET     :=.*', 'TARGET     := {0}'.format('cosmo'))

            if 'cosmo_target=gpu' in self.spec:
                cuda_version = self.spec['cuda'].version
                fflags = 'CUDA_HOME=' + self.spec['cuda'].prefix + ' -ta=tesla,cc' + self.spec.variants['cuda_arch'].value + ',cuda' + str(cuda_version.up_to(2))
                OptionsFile.filter('FFLAGS   = -Kieee', 'FFLAGS   = -Kieee {0}'.format(fflags))
            # Pre-processor flags
            if self.spec['mpi'].name == 'mpich':
                OptionsFile.filter('PFLAGS   = -Mpreprocess', 'PFLAGS   = -Mpreprocess -DNO_MPI_HOST_DATA')
            if 'cosmo_target=gpu' in self.spec and self.compiler.name == 'pgi':
                OptionsFile.filter('PFLAGS   = -Mpreprocess', 'PFLAGS   = -Mpreprocess -DNO_ACC_FINALIZE')

    def install(self, spec, prefix):
        mkdir(prefix.cosmo)
        if '+serialize' in self.spec:
            mkdirp('data/' + self.spec.variants['real_type'].value, prefix.data + '/' + self.spec.variants['real_type'].value)
        with working_dir(self.build_directory):
            mkdir(prefix.bin)
            if '+serialize' in spec:
                install('cosmo_serialize', prefix.bin)
            else:
                install('cosmo_' + self.spec.variants['cosmo_target'].value, prefix.bin)
                install('cosmo_' + self.spec.variants['cosmo_target'].value, 'test/testsuite')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        if '~serialize' in self.spec:
            try:
                subprocess.run([self.build_directory + '/test/tools/test_cosmo.py', str(self.spec), '.'], stderr=subprocess.STDOUT, check=True)
            except:
                raise InstallError('Testsuite failed')
        if '+serialize' in self.spec:
            try:
                subprocess.run([self.build_directory + '/test/tools/serialize_cosmo.py', str(self.spec), '.'], stderr=subprocess.STDOUT, check=True)
            except:
                raise InstallError('Serialization failed')
