# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cosmo(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = "http://www.cosmo-model.org"
    url      = "https://github.com/MeteoSwiss-APN/cosmo/archive/5.07.mch1.0.p5.tar.gz"
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
    depends_on('cuda', type=('build', 'run'))
    depends_on('cosmo-dycore%gcc +build_tests', when='+dycoretest')
    depends_on('cosmo-dycore%gcc +cuda', when='cosmo_target=gpu +cppdycore')
    depends_on('cosmo-dycore%gcc ~cuda cuda_arch=none', when='cosmo_target=cpu +cppdycore')
    depends_on('cosmo-dycore%gcc real_type=float', when='real_type=float +cppdycore')
    depends_on('cosmo-dycore%gcc real_type=double', when='real_type=double +cppdycore')
    depends_on('cosmo-dycore%gcc +production', when='+production +cppdycore')

    depends_on('serialbox@2.6.0', when='+serialize')
    depends_on('mpi', type=('build', 'run'))
    depends_on('libgrib1')
    depends_on('jasper@1.900.1%gcc ~shared')
    depends_on('cosmo-grib-api-definitions', when='~eccodes')
    depends_on('cosmo-eccodes-definitions@2.14.1.2 ~aec', when='+eccodes')
    depends_on('perl@5.16.3:')
    depends_on('omni-xmod-pool', when='+claw')
    depends_on('claw', when='+claw')
    depends_on('boost', when='cosmo_target=gpu ~cppdycore')

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('serialize', default=False, description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO')
    variant('debug', default=False, description='Build debug mode')
    variant('cosmo_target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('claw', default=False, description='Build with claw-compiler')
    variant('slave', default='tsa', description='Build on slave tsa or daint', multi=False)
    variant('eccodes', default=False, description='Build with eccodes instead of grib-api')
    variant('pollen', default=False, description='Build with pollen enabled')
    variant('verbose', default=False, description='Build cosmo with verbose enabled')

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
    conflicts('+cppdycore', when='%pgi cosmo_target=cpu')
    build_directory = 'cosmo/ACC'

    def setup_environment(self, spack_env, run_env):
        if '~eccodes' in self.spec:
          grib_definition_path = self.spec['cosmo-grib-api-definitions'].prefix + '/cosmoDefinitions/definitions/:' + self.spec['cosmo-grib-api'].prefix + '/share/grib_api/definitions/'
          spack_env.set('GRIB_DEFINITION_PATH', grib_definition_path)
          grib_samples_path = self.spec['cosmo-grib-api-definitions'].prefix + '/cosmoDefinitions/samples/'
          spack_env.set('GRIB_SAMPLES_PATH', grib_samples_path)
          spack_env.set('GRIBAPI_DIR', self.spec['cosmo-grib-api'].prefix)
        else:
          eccodes_definition_path = self.spec['cosmo-eccodes-definitions'].prefix + '/cosmoDefinitions/definitions/:' + self.spec['eccodes'].prefix + '/share/eccodes/definitions/'
          spack_env.set('GRIB_DEFINITION_PATH', eccodes_definition_path)
          eccodes_samples_path = self.spec['cosmo-eccodes-definitions'].prefix + '/cosmoDefinitions/samples/'
          spack_env.set('GRIB_SAMPLES_PATH', eccodes_samples_path)
          spack_env.set('GRIBAPI_DIR', self.spec['eccodes'].prefix)
        spack_env.set('GRIB1_DIR', self.spec['libgrib1'].prefix + '/lib')
        spack_env.set('JASPER_DIR', self.spec['jasper'].prefix)
        spack_env.set('MPI_ROOT', self.spec['mpi'].prefix)
        if self.spec.variants['cosmo_target'].value == 'gpu' or '+serialize' in self.spec:
            spack_env.set('BOOST_ROOT',  self.spec['boost'].prefix)
        if '+cppdycore' in self.spec:
            spack_env.set('GRIDTOOLS_DIR', self.spec['gridtools'].prefix)
            spack_env.set('DYCOREGT', self.spec['cosmo-dycore'].prefix)
            spack_env.set('DYCOREGT_DIR', self.spec['cosmo-dycore'].prefix)
        if '+serialize' in self.spec:
          spack_env.set('SERIALBOX_DIR', self.spec['serialbox'].prefix)
          spack_env.set('SERIALBOX_FORTRAN_LIBRARIES', self.spec['serialbox'].prefix + '/lib/libSerialboxFortran.a ' +  self.spec['serialbox'].prefix + '/lib/libSerialboxC.a ' + self.spec['serialbox'].prefix + '/lib/libSerialboxCore.a -lstdc++fs -lpthread')
        if '+claw' in self.spec:
            spack_env.set('CLAWDIR', self.spec['claw'].prefix)
            spack_env.set('CLAWFC', self.spec['claw'].prefix + '/bin/clawfc')
            spack_env.set('CLAWXMODSPOOL', self.spec['omni-xmod-pool'].prefix + '/omniXmodPool/')
            if self.spec['mpi'].name == 'mpich':
                spack_env.append_flags('CLAWFC_FLAGS', '-U__CRAYXC')
        spack_env.set('UCX_MEMTYPE_CACHE', 'n')
        if '+cppdycore' in self.spec and self.spec.variants['cosmo_target'].value == 'gpu':
          spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cuda_copy,cuda_ipc,cma')
        else:
          spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cma')

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
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifc
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            OptionsFileName= 'Options.' + self.spec.variants['slave'].value
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name == 'pgi':
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            OptionsFileName += '.' + spec.variants['cosmo_target'].value
            optionsfilter = FileFilter(OptionsFileName)
            if self.spec.variants['slave'].value == 'tsa':
                optionsfilter.filter('NETCDFI *=.*', 'NETCDFI = -I{0}/include'.format(spec['netcdf-fortran'].prefix))
                optionsfilter.filter('NETCDFL *=.*', 'NETCDFL = -L{0}/lib -lnetcdff -L{1}/lib64 -lnetcdf'.format(spec['netcdf-fortran'].prefix, spec['netcdf-c'].prefix))
            else:
                optionsfilter.filter('NETCDFI *=.*', 'NETCDFI = -I$(NETCDF_DIR)/include')
                optionsfilter.filter('NETCDFL *=.*', 'NETCDFL = -L$(NETCDF_DIR)/lib -lnetcdff -lnetcdf')
            optionsfilter = FileFilter('Options.lib.' + spec.variants['cosmo_target'].value)
            if '+eccodes' in spec:
              optionsfilter.filter('GRIBAPIL *=.*', 'GRIBAPIL = -L$(GRIBAPI_DIR)/lib -leccodes_f90 -leccodes -L$(JASPER_DIR)/lib -ljasper')
            makefile.filter('/Options.*', '/' + OptionsFileName)
            if '~serialize' in spec:
              makefile.filter('TARGET     :=.*', 'TARGET     := {0}'.format('cosmo_'+ spec.variants['cosmo_target'].value))

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
                install('cosmo_' + self.spec.variants['cosmo_target'].value, prefix.bin)
                install('cosmo_' + self.spec.variants['cosmo_target'].value, prefix.cosmo + '/test/testsuite')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        with working_dir(prefix.cosmo + '/test/testsuite/data'):
            get_test_data = Executable('./get_data.sh')
            get_test_data()
        if '~serialize' in self.spec:
            with working_dir(prefix.cosmo + '/test/testsuite'):
                env['ASYNCIO'] = 'ON'
                if self.spec.variants['cosmo_target'].value == 'gpu':
                    env['TARGET'] = 'GPU'
                else:
                    env['TARGET'] = 'CPU'
                if self.spec.variants['real_type'].value == 'float':
                    env['REAL_TYPE'] = 'FLOAT'
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
