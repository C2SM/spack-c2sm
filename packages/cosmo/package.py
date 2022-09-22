# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess, re, itertools, os
from spack import *


class Cosmo(MakefilePackage):
    """COSMO: Numerical Weather Prediction Model. Needs access to private GitHub."""

    homepage = "http://www.cosmo-model.org"
    url = "https://github.com/MeteoSwiss-APN/cosmo/archive/5.07.mch1.0.p5.tar.gz"
    git = 'ssh://git@github.com/COSMO-ORG/cosmo.git'
    apngit = 'ssh://git@github.com/MeteoSwiss-APN/cosmo.git'
    c2smgit = 'ssh://git@github.com/C2SM-RCM/cosmo.git'
    empagit = 'ssh://git@github.com/C2SM-RCM/cosmo-ghg.git'
    maintainers = ['elsagermann']

    version('org-master', branch='master', get_full_repo=True)
    version('dev-build', branch='master', get_full_repo=True)
    version('apn-mch', git=apngit, branch='mch', get_full_repo=True)
    version('c2sm-master', git=c2smgit, branch='master', get_full_repo=True)
    version('c2sm-features',
            git=c2smgit,
            branch='c2sm-features',
            get_full_repo=True)
    version('empa-ghg', git=empagit, branch='c2sm', get_full_repo=True)

    patch('patches/5.07.mch1.0.p4/patch.Makefile', when='@5.07.mch1.0.p4')
    patch('patches/5.07.mch1.0.p4/patch.Makefile', when='@5.07.mch1.0.p5')

    depends_on('netcdf-fortran', type=('build', 'link'))
    depends_on('netcdf-c +mpi', type=('build', 'link'))
    depends_on('slurm', type='run')
    depends_on('cuda', when='cosmo_target=gpu', type=('build', 'link', 'run'))
    depends_on('serialbox', when='+serialize', type='build')
    depends_on('mpi', type=('build', 'link', 'run'), when='cosmo_target=cpu')
    depends_on('mpi +cuda',
               type=('build', 'link', 'run'),
               when='cosmo_target=gpu')
    depends_on('libgrib1', type='build')
    depends_on('jasper@1.900.1', type=('build', 'link'))
    depends_on('cosmo-grib-api-definitions',
               type=('build', 'run'),
               when='~eccodes')
    depends_on('cosmo-eccodes-definitions',
               type=('build', 'link', 'run'),
               when='+eccodes')
    depends_on('perl@5.16.3:', type='build')
    depends_on('omni-xmod-pool', when='+claw', type='build')
    depends_on('claw', when='+claw', type='build')
    depends_on('boost', when='cosmo_target=gpu ~cppdycore', type='build')
    depends_on('cmake', type='build')
    depends_on('zlib_ng +compat', when='+zlib_ng', type=('link', 'run'))
    depends_on('oasis', when='+oasis', type=('build', 'link', 'run'))

    # cosmo-dycore dependency
    types = ['float', 'double']
    prod = [True, False]
    cuda = [True, False]
    testing = [True, False]
    gt1 = [True, False]
    comb = list(itertools.product(*[types, prod, cuda, testing, gt1]))
    for it in comb:
        real_type = it[0]
        prod_opt = '+production' if it[1] else '~production'
        cuda_opt = '+cuda' if it[2] else '~cuda'
        cuda_dep = 'cosmo_target=gpu' if it[2] else ' cosmo_target=cpu'
        test_opt = '+build_tests' if it[3] else '~build_tests'
        test_dep = '+dycoretest' if it[3] else '~dycoretest'
        gt1_dep = '+gt1' if it[4] else '~gt1'

        dep = f'cosmo-dycore@8.1.0:8.4.0 real_type={real_type} {prod_opt} {cuda_opt} {test_opt} {gt1_dep}'
        condition = f'real_type={real_type} {prod_opt} {cuda_dep} {test_dep} {gt1_dep} +cppdycore'
        depends_on(dep, when=condition, type='build')

    variant('cppdycore', default=True, description='Build with the C++ DyCore')
    variant('dycoretest',
            default=True,
            description='Build C++ dycore with testing')
    variant('serialize',
            default=False,
            description='Build with serialization enabled')
    variant('parallel', default=True, description='Build parallel COSMO')
    variant('debug', default=False, description='Build debug mode')
    variant('real_type',
            default='double',
            description='Build with double or single precision enabled',
            values=('double', 'float'),
            multi=False)
    variant('claw', default=False, description='Build with claw-compiler')
    variant('slave', default='none', description='Build on slave')
    variant('eccodes',
            default=True,
            description='Build with eccodes instead of grib-api')
    variant('pollen', default=False, description='Build with pollen enabled')
    variant('cosmo_target',
            default='gpu',
            description='Build with target gpu or cpu',
            values=('gpu', 'cpu'),
            multi=False)
    variant('verbose',
            default=False,
            description='Build cosmo with verbose enabled')
    variant('set_version',
            default=False,
            description='Pass cosmo tag version to Makefile')
    variant('gt1',
            default=False,
            description='Build dycore with gridtools 1.1.3')
    variant('cuda_arch',
            default='none',
            description='Build with cuda_arch',
            values=('80', '70', '60', '37'),
            multi=False)
    variant(
        'zlib_ng',
        default=False,
        description=
        'Run with faster zlib-implemention for compression of NetCDF output')
    variant('oasis',
            default=False,
            description='Build with the unified oasis interface')

    variant('slurm_bin',
            default='srun',
            description='Slurm binary on CSCS machines')
    variant('slurm_opt_partition',
            default='-p',
            description='Slurm option to specify partition for testing')
    variant('slurm_partition',
            default='normal',
            description='Slurm partition for testing')

    variant('slurm_opt_nodes',
            default='-n',
            description='Slurm option to specify number of nodes for testing')
    variant('slurm_nodes',
            default='1',
            description='Pattern to specify number of nodes for testing')

    variant('slurm_opt_account',
            default='-A',
            description='Slurm option to specify account for testing')
    variant('slurm_account',
            default='g110',
            description='Slurm option to specify account for testing')

    variant(
        'slurm_opt_constraint',
        default='-C',
        description='Slurm option to specify constraints for nodes requested')
    variant('slurm_constraint',
            default='gpu',
            description='Slurm constraints for nodes requested')

    conflicts('+claw', when='cosmo_target=cpu')
    conflicts('+pollen', when='@5.05:5.06,org-master,master')
    conflicts('cosmo_target=gpu', when='%gcc')

    # previous versions contain a bug affecting serialization
    conflicts('+serialize', when='@5.07.mch1.0.p2:5.07.mch1.0.p3')
    variant('production',
            default=False,
            description='Force all variants to be the ones used in production')

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
    conflicts('+cppdycore', when='%nvhpc cosmo_target=cpu')
    conflicts('+cppdycore', when='%pgi cosmo_target=cpu')
    # - ML - A conflict should be added there if the oasis variant is
    # chosen and the version is neither c2sm-features nor
    # dev-build. The problem is that this doesn't seem possible in a
    # native spack way. Hence the dirty check at the beginning of
    # setup_build_environment method

    build_directory = 'cosmo/ACC'

    def setup_build_environment(self, env):

        # - ML - Dirty conflict check (see above)
        if self.spec.variants['oasis'].value and self.spec.version not in (
                Version('c2sm-features'), Version('dev-build')):
            raise InstallError(
                '+oasis variant only compatible with the @c2sm-features and @dev-build versions'
            )

        self.setup_run_environment(env)

        # Check mpi provider
        self.mpi_spec = self.spec['mpi']

        # Grib-api. eccodes library
        if '~eccodes' in self.spec:
            grib_prefix = self.spec['cosmo-grib-api'].prefix
            grib_definition_prefix = self.spec[
                'cosmo-grib-api-definitions'].prefix
            env.set(
                'GRIBAPIL',
                '-L' + grib_prefix + '/lib -lgrib_api_f90 -lgrib_api -L' +
                self.spec['jasper'].prefix + '/lib64 -ljasper')
        else:
            grib_prefix = self.spec['eccodes'].prefix
            grib_definition_prefix = self.spec[
                'cosmo-eccodes-definitions'].prefix
            # Default installation lib path changed to from lib to lib64 after 2.19.0
            if self.spec['eccodes'].version >= Version('2.19.0'):
                eccodes_lib_dir = '/lib64'
            else:
                eccodes_lib_dir = '/lib'
            env.set(
                'GRIBAPIL', '-L' + grib_prefix + eccodes_lib_dir +
                ' -leccodes_f90 -leccodes -L' + self.spec['jasper'].prefix +
                '/lib64 -ljasper')
        grib_inc_dir_path = os.path.join(grib_prefix, 'include')
        if os.path.exists(grib_inc_dir_path):
            env.set('GRIBAPII', '-I' + grib_prefix + '/include')
        else:
            env.set('GRIBAPII', '')

        # libaec
        if 'libaec' in self.spec:
            env.set('AECL', '-L' + self.spec['libaec'].prefix + '/lib64 -laec')
            env.set('AECI', '-I' + self.spec['libaec'].prefix + '/include')

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
        elif self.compiler.name == 'nvhpc':
            env.set('GRIBDWDL',
                    '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_pgi')
        else:
            env.set(
                'GRIBDWDL', '-L' + self.spec['libgrib1'].prefix +
                '/lib -lgrib1_' + self.compiler.name)
        env.set('GRIBDWDI', '-I' + self.spec['libgrib1'].prefix + '/include')

        # MPI library
        if self.mpi_spec.name == 'openmpi':
            env.set('MPIL', '-L' + self.mpi_spec.prefix + ' -lmpi_cxx')

        # manually add libs to linker because of broke modules on Piz Daint for nvidia
        elif self.spec.variants[
                'slave'].value == 'daint' and self.compiler.name in ('pgi',
                                                                     'nvhpc'):
            env.set(
                'MPIL', '-L' + self.spec['mpi'].prefix +
                ' -lmpich -lnvcpumath -lnvhpcatm')

        env.set('MPII', '-I' + self.mpi_spec.prefix + '/include')

        # Dycoregt & Gridtools linrary
        if '+cppdycore' in self.spec:
            if '+gt1' in self.spec:
                env.set('GRIDTOOLS_DIR', self.spec['gridtools'].prefix)
                env.set('GRIDTOOLSL',
                        '-L' + self.spec['gridtools'].prefix + '/lib -lgcl')
                env.set(
                    'GRIDTOOLSI', '-I' + self.spec['gridtools'].prefix +
                    '/include/gridtools')
            env.set('DYCOREGT', self.spec['cosmo-dycore'].prefix)
            env.set('DYCOREGT_DIR', self.spec['cosmo-dycore'].prefix)
            env.set(
                'DYCOREGTL', '-L' + self.spec['cosmo-dycore'].prefix +
                '/lib -ldycore_bindings_' +
                self.spec.variants['real_type'].value +
                ' -ldycore_base_bindings_' +
                self.spec.variants['real_type'].value +
                ' -ldycore -ldycore_base -ldycore_backend -lstdc++ -lcpp_bindgen_generator -lcpp_bindgen_handle -lgt_gcl_bindings'
            )
            env.set('DYCOREGTI', '-I' + self.spec['cosmo-dycore'].prefix)

        # Serialbox library
        if '+serialize' in self.spec:
            env.set('SERIALBOX', self.spec['serialbox'].prefix)
            env.set(
                'SERIALBOXL', self.spec['serialbox'].prefix +
                '/lib/libSerialboxFortran.a ' + self.spec['serialbox'].prefix +
                '/lib/libSerialboxC.a ' + self.spec['serialbox'].prefix +
                '/lib/libSerialboxCore.a -lstdc++fs -lpthread -lstdc++')
            env.set('SERIALBOXI',
                    '-I' + self.spec['serialbox'].prefix + '/include')

        # Claw library
        if '+claw' in self.spec:
            claw_flags = ''
            # Set special flags after CLAW release 2.1
            if self.compiler.name in (
                    'pgi',
                    'nvhpc') and self.spec['claw'].version >= Version(2.1):
                claw_flags += ' --fc-vendor=portland --fc-cmd=${FC}'
            if 'cosmo_target=gpu' in self.spec:
                claw_flags += ' --directive=openacc'
            if self.spec.variants['verbose'].value:
                claw_flags += ' -v'
            env.set('CLAWDIR', self.spec['claw'].prefix)
            env.set('CLAWFC', self.spec['claw'].prefix + '/bin/clawfc')
            env.set('CLAWXMODSPOOL',
                    self.spec['omni-xmod-pool'].prefix + '/omniXmodPool/')
            if self.mpi_spec.name == 'mpich':
                claw_flags += ' -D__CRAYXC'
            env.set('CLAWFC_FLAGS', claw_flags)

        # OASIS library
        if '+oasis' in self.spec:
            oasis_prefix = self.spec['oasis'].prefix
            env.set(
                'PSMILEL',
                '-L{:s}/lib -lpsmile.MPI1 -lscrip -lmct -lmpeu'.format(
                    oasis_prefix))
            env.set(
                'PSMILEI',
                '-I{0:s}/build/lib/psmile.MPI1 -I{0:s}/build/lib/mct'.format(
                    oasis_prefix))
            env.set('MPPIOI', '-I{:s}/build/lib/mct'.format(oasis_prefix))

        # Linker flags
        if self.compiler.name in ('pgi',
                                  'nvhpc') and '~cppdycore' in self.spec:
            env.set('LFLAGS', '-lstdc++')

        # Compiler & linker variables
        if self.compiler.name in ('pgi', 'nvhpc'):
            env.set('F90', self.mpi_spec.mpifc + ' -D__PGI_FORTRAN__')
            env.set('LD', self.mpi_spec.mpifc + ' -D__PGI_FORTRAN__')
        else:
            env.set('F90', self.mpi_spec.mpifc)
            env.set('LD', self.mpi_spec.mpifc)

    @property
    def build_targets(self):
        build = []
        if self.spec.variants['pollen'].value:
            build.append('POLLEN=1')
        if self.spec.variants['oasis'].value:
            build.append('COUP_OAS=1')
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
        if '+set_version' in self.spec:
            build.append('COSMO_VERSION=' + self.spec.format('{version}'))
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
            OptionsFileName = 'Options'
            if self.compiler.name == 'gcc':
                OptionsFileName += '.gnu'
            elif self.compiler.name in ('pgi', 'nvhpc'):
                OptionsFileName += '.pgi'
            elif self.compiler.name == 'cce':
                OptionsFileName += '.cray'
            OptionsFileName += '.' + spec.variants['cosmo_target'].value
            OptionsFile = FileFilter(OptionsFileName)

            makefile = FileFilter('Makefile')
            makefile.filter('/Options.*', '/' + OptionsFileName)
            if self.spec.version == Version('empa-ghg'):
                if '~serialize' in spec:
                    makefile.filter(
                        'TARGET     :=.*', 'TARGET     := {0}'.format(
                            'cosmo-ghg_' +
                            spec.variants['cosmo_target'].value))
                else:
                    makefile.filter('TARGET     :=.*',
                                    'TARGET     := {0}'.format('cosmo-ghg'))
            else:
                if '~serialize' in spec:
                    makefile.filter(
                        'TARGET     :=.*', 'TARGET     := {0}'.format(
                            'cosmo_' + spec.variants['cosmo_target'].value))
                else:
                    makefile.filter('TARGET     :=.*',
                                    'TARGET     := {0}'.format('cosmo'))

            if 'cosmo_target=gpu' in self.spec:
                cuda_version = self.spec['cuda'].version
                fflags = 'CUDA_HOME=' + self.spec[
                    'cuda'].prefix + ' -ta=tesla,cc' + self.spec.variants[
                        'cuda_arch'].value + ',cuda' + str(
                            cuda_version.up_to(2))
                OptionsFile.filter('FFLAGS   = -Kieee.*',
                                   'FFLAGS   = -Kieee {0}'.format(fflags))
            # Pre-processor flags
            if self.mpi_spec.name == 'mpich':
                OptionsFile.filter(
                    'PFLAGS   = -Mpreprocess.*',
                    'PFLAGS   = -Mpreprocess -DNO_MPI_HOST_DATA')
            if 'cosmo_target=gpu' in self.spec and self.compiler.name in (
                    'pgi', 'nvhpc'):
                OptionsFile.filter(
                    'PFLAGS   = -Mpreprocess.*',
                    'PFLAGS   = -Mpreprocess -DNO_ACC_FINALIZE')

    def install(self, spec, prefix):

        with working_dir(self.build_directory):
            mkdir(prefix.bin)
            if self.spec.version == Version('empa-ghg'):
                if '+serialize' in spec:
                    install('cosmo-ghg_serialize', prefix.bin)
                else:
                    install(
                        'cosmo-ghg_' +
                        self.spec.variants['cosmo_target'].value, prefix.bin)
                    install(
                        'cosmo-ghg_' +
                        self.spec.variants['cosmo_target'].value,
                        'test/testsuite')
            else:
                if '+serialize' in spec:
                    install('cosmo_serialize', prefix.bin)
                else:
                    install(
                        'cosmo_' + self.spec.variants['cosmo_target'].value,
                        prefix.bin)
                    install(
                        'cosmo_' + self.spec.variants['cosmo_target'].value,
                        'test/testsuite')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        try:
            subprocess.run([
                self.build_directory + '/test/tools/test_cosmo.py', '-s',
                str(self.spec), '-b',
                str('.')
            ],
                           stderr=subprocess.STDOUT,
                           check=True)
        except:
            raise InstallError('Testsuite failed')
