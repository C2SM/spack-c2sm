from spack import *
import subprocess, re, os


class CosmoDycore(CMakePackage):
    """C++ dycore of cosmo based on GridTools library"""

    homepage = "https://github.com/COSMO-ORG/cosmo/tree/master/dycore"
    url = "https://github.com/COSMO-ORG/cosmo/archive/6.0.tar.gz"
    git = "git@github.com:COSMO-ORG/cosmo.git"
    apngit = "git@github.com:MeteoSwiss-APN/cosmo.git"
    c2smgit = "git@github.com:C2SM-RCM/cosmo.git"
    empagit = 'git@github.com:C2SM-RCM/cosmo-ghg.git'

    maintainers = ['huppd']

    version('org-master', branch='master')
    version('6.0', tag='6.0')

    version('apn-mch', git=apngit, branch='mch')
    version('5.09a.mch1.2.p2', git=apngit, tag='5.09a.mch1.2.p2')

    version('c2sm-master', git=c2smgit, branch='master')
    version('6.1', git=c2smgit, tag='6.1')
    version('c2sm-features', git=c2smgit, branch='c2sm-features')

    version('empa-ghg', git=empagit, branch='c2sm')

    variant('build_type',
            default='Release',
            description='Build type',
            values=('Debug', 'Release', 'DebugRelease'))
    variant('build_tests',
            default=True,
            description="Compile Dycore unittests & regressiontests")
    variant('real_type',
            default='double',
            description='Build with double or single precision enabled',
            values=('double', 'float'),
            multi=False)
    variant('slave', default='none', description='Build on slave')
    variant(
        'pmeters',
        default=False,
        description="Enable the performance meters for the dycore stencils")
    variant('data_path',
            default='.',
            description='Serialization data path',
            multi=False)
    variant('cuda_arch',
            default='none',
            description='Build with cuda_arch',
            values=('80', '70', '60', '37'),
            multi=False)
    variant('cuda', default=True, description='Build with cuda or target gpu')
    variant('gt1', default=False, description='Build with gridtools 1.1.3')

    depends_on('gridtools@1.1.3 ~cuda', when='~cuda +gt1')
    depends_on('gridtools@1.1.3 +cuda', when='+cuda +gt1')
    depends_on('boost@1.65.1: +program_options +system')
    depends_on('serialbox@2.6.0', when='+build_tests', type='run')
    depends_on('mpi')
    depends_on('mpi +cuda', when='+cuda')
    depends_on('slurm', type='run')
    depends_on('cmake@3.12:')
    depends_on('cuda', when='+cuda')

    conflicts('%nvhpc')
    conflicts('%pgi')

    # hardcode srun arguments, replaces all srun related variants
    patch('patches/patch.srun_args')

    # in file dycore/src/common/GCLExchange.hpp
    # add #include <map>
    patch('patches/patch.include_map')

    root_cmakelists_dir = 'dycore'

    def setup_run_environment(self, env):
        if '+cuda' in self.spec and self.spec['mpi'].name == 'mpich':
            env.set('MPICH_G2G_PIPELINE', '64')
            env.set('MPICH_RDMA_ENABLED_CUDA', '1')

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

    def cmake_args(self):
        spec = self.spec

        args = []

        if '+gt1' in spec:
            args.append(
                f'-DGridTools_DIR={spec["gridtools"].prefix}/lib/cmake')

        args.append(f'-DCMAKE_BUILD_TYPE={spec.variants["build_type"].value}')
        args.append(f'-DCMAKE_INSTALL_PREFIX={self.prefix}')
        args.append(f'-DBOOST_ROOT={spec["boost"].prefix}')
        args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
        args.append('-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON')
        args.append('-DBoost_USE_STATIC_LIBS=ON')

        if spec.variants['pmeters'].value:
            args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=ON')
        else:
            args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=OFF')
        args.append(f'-DPRECISION={spec.variants["real_type"].value}')

        if not spec.variants['build_tests'].value:
            args.append('-DBUILD_TESTING=OFF')
        else:
            args.append('-DBUILD_TESTING=ON')
            args.append(f'-DSerialbox_DIR={spec["serialbox"].prefix}/cmake')

        if '+cuda' in spec:
            args.append('-DENABLE_CUDA=ON')
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch is not None:
                args.append(f'-DCUDA_ARCH=sm_{cuda_arch}')
            if '+gt1' in spec:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=CUDA')
            else:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=gpu')
        else:
            args.append('-DENABLE_CUDA=OFF')
            if '+gt1' in spec:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=x86')
            else:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=cpu_ifirst')

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        if '+build_tests' in self.spec:
            try:
                subprocess.run([
                    './test_dycore.py', '-s',
                    str(self.spec), '-b',
                    str(self.build_directory)
                ],
                               cwd=self.root_cmakelists_dir + '/test/tools',
                               check=True,
                               stderr=subprocess.STDOUT)
            except:
                raise InstallError('Dycore tests failed')
