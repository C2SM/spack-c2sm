# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cosmo(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = "http://www.cosmo-model.org"
    url      = "https://github.com/COSMO-ORG/cosmo/archive/5.06.tar.gz" 
    git      = 'git@github.com:COSMO-ORG/cosmo.git'
    maintainers = ['elsagermann']

    version('master', branch='master')
    version('mch', git='git@github.com:MeteoSwiss-APN/cosmo.git', branch='mch')
    version('5.07.mch1.0.p5', git='git@github.com:MeteoSwiss-APN/cosmo.git', tag='5.07.mch1.0.p5')
    version('5.07.mch1.0.p4', git='git@github.com:MeteoSwiss-APN/cosmo.git', tag='5.07.mch1.0.p4')
    version('5.07.mch1.0.p3', git='git@github.com:MeteoSwiss-APN/cosmo.git', tag='5.07.mch1.0.p3')
    version('5.07.mch1.0.p2', git='git@github.com:MeteoSwiss-APN/cosmo.git', tag='5.07.mch1.0.p2')
    version('5.05a', tag='5.05a')
    version('5.05',  tag='5.05')
    version('5.06', tag='5.06')
    
    patch('patches/5.07.mch1.0.p4/patch.Makefile', when='@5.07.mch1.0.p4')
    patch('patches/5.07.mch1.0.p4/patch.Makefile', when='@5.07.mch1.0.p5')


    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('slurm', type='run')
    depends_on('cuda', type=('build', 'run'), when='cosmo_target=gpu')
    depends_on('cosmo-dycore%gcc +build_tests', when='+dycoretest')
    depends_on('cosmo-dycore%gcc +cuda', when='cosmo_target=gpu +cppdycore')
    depends_on('cosmo-dycore%gcc ~cuda cuda_arch=none', when='cosmo_target=cpu cuda_arch=none +cppdycore')
    depends_on('cosmo-dycore%gcc real_type=float', when='real_type=float +cppdycore')
    depends_on('cosmo-dycore%gcc real_type=double', when='real_type=double +cppdycore')
    depends_on('cosmo-dycore%gcc +production', when='+production +cppdycore')

    depends_on('serialbox@2.6.0%pgi@19.9-gcc', when='%pgi@19.9 +serialize')
    depends_on('serialbox@2.6.0%pgi@19.7.0-gcc', when='%pgi@19.7.0 +serialize')
    depends_on('serialbox@2.6.0', when='%gcc +serialize')
    depends_on('mpi', type=('build', 'run'))
    depends_on('libgrib1')
    depends_on('jasper@1.900.1%gcc')
    depends_on('cosmo-grib-api-definitions', when='~eccodes')
    depends_on('cosmo-eccodes-definitions@2.14.1.2', when='+eccodes')
    depends_on('perl@5.16.3:')
    depends_on('omni-xmod-pool', when='+claw')
    depends_on('claw', when='+claw')
    depends_on('boost', when='cosmo_target=gpu ~cppdycore')

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('serialize', default=False, description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO')
    variant('debug', default=False, description='Build debug mode')
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('claw', default=False, description='Build with claw-compiler')
    variant('slave', default='tsa', description='Build on slave tsa or daint', multi=False)
    variant('eccodes', default=False, description='Build with eccodes instead of grib-api')
    variant('pollen', default=False, description='Build with pollen enabled')
    variant('cuda_arch', default='70', description='Build with cuda_arch', values=('70', '60', '37'), multi=False)
    variant('cosmo_target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)

    conflicts('+pollen', when='@5.05:5.06,master')
    conflicts('+serialize', when='+parallel')
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
    conflicts('+cppdycore', when='%pgi cosmo_target=cpu')
    build_directory = 'cosmo/ACC'

    def setup_environment(self, spack_env, run_env):
        # Grib-api. eccodes library
        if '~eccodes' in self.spec:
            grib_prefix = self.spec['cosmo-grib-api'].prefix
            grib_definition_prefix = self.spec['cosmo-grib-api-definitions'].prefix
            spack_env.set('GRIBAPIL', '-L' + grib_prefix + '/lib -lgrib_api_f90 -lgrib_api -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
        else:
            grib_prefix = self.spec['eccodes'].prefix
            grib_definition_prefix = self.spec['cosmo-grib-api-definitions'].prefix
            spack_env.set('GRIBAPIL', '-L' + grib_prefix + '/lib -leccodes_f90 -leccodes -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
        spack_env.set('GRIBAPII', '-I' + grib_prefix + '/include')
        spack_env.set('GRIB_DEFINITION_PATH', grib_definition_prefix + '/cosmoDefinitions/definitions/:' + grib_prefix + '/share/grib_api/definitions/')
        spack_env.set('GRIB_SAMPLES_PATH', grib_definition_prefix + '/cosmoDefinitions/samples/')

        # Netcdf library
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
            spack_env.set('DYCOREGTL', '-L' + self.spec['cosmo-dycore'].prefix + '/lib' + ' -ldycore_bindings_' + self.spec.variants['real_type'].value + ' -ldycore_base_bindings_' + self.spec.variants['real_type'].value + ' -ldycore -ldycore_base -ldycore_backend -lstdc++ -lcpp_bindgen_generator -lcpp_bindgen_handle -lgt_gcl_bindings')
            spack_env.set('DYCOREGTI', '-I' + self.spec['cosmo-dycore'].prefix)
            spack_env.set('DYCOREGT', self.spec['cosmo-dycore'].prefix)
            spack_env.set('DYCOREGT_DIR', self.spec['cosmo-dycore'].prefix)
            spack_env.set('GRIDTOOLSL', '-L' + self.spec['gridtools'].prefix + '/lib -lgcl')
            spack_env.set('GRIDTOOLSI', '-I' + self.spec['gridtools'].prefix + '/include/gridtools')
            spack_env.set('GRIDTOOLS_DIR', self.spec['gridtools'].prefix)

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
        if 'cosmo_target=gpu' in self.spec:
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
            OptionsFileName = 'Options'
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name == 'pgi':
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            if 'cosmo_target=gpu' in spec:
                OptionsFileName += '.gpu'
            else:
                OptionsFileName += '.cpu'

            makefile.filter('/Options.*', '/' + OptionsFileName)
            if '~serialize' in spec:
                if 'cosmo_target=gpu' in spec:
                    makefile.filter('TARGET     :=.*', 'TARGET     := {0}'.format('cosmo_gpu'))
                else:
                    makefile.filter('TARGET     :=.*', 'TARGET     := {0}'.format('cosmo_cpu'))

            OptionsFile = FileFilter(OptionsFileName)
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
        install_tree('cosmo', prefix.cosmo)        
        with working_dir(self.build_directory):
            mkdir(prefix.bin)
            if '+serialize' in spec:
                install('cosmo_serialize', prefix.bin)            
            else:
                if 'cosmo_target=gpu' in spec:
                    install('cosmo_gpu', prefix.bin)
                    install('cosmo_gpu', prefix.cosmo + '/test/testsuite')
                else:
                    install('cosmo_cpu', prefix.bin)
                    install('cosmo_cpu', prefix.cosmo + '/test/testsuite')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        with working_dir(prefix.cosmo + '/test/testsuite/data'):
            get_test_data = Executable('./get_data.sh')
            get_test_data()
        if '~serialize' in self.spec:
            with working_dir(prefix.cosmo + '/test/testsuite'):
                env['ASYNCIO'] = 'ON'
                if 'cosmo_target=gpu' in self.spec:
                    env['TARGET'] = 'GPU'
                else:
                    env['TARGET'] = 'CPU'
                if '~cppdycore' in self.spec:
                    env['JENKINS_NO_DYCORE'] = 'ON'
                run_testsuite = Executable('sbatch submit.' + self.spec.variants['slave'].value + '.slurm')
                run_testsuite()
        if '+serialize' in self.spec:
            with working_dir(prefix.cosmo + '/ACC'):
                get_serialization_data = Executable('./test/serialize/generateUnittestData.py -v -e cosmo_serialize --mpirun=srun')
                get_serialization_data()
            with working_dir(prefix.cosmo + '/ACC/test/serialize'):
                copy_tree('data', prefix.data + '/' + self.spec.variants['real_type'].value) 
