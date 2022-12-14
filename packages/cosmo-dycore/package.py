from spack import *
import subprocess, re, os


class CosmoDycore(CMakePackage):
    """C++ dycore of cosmo based on GridTools library"""

    homepage = "https://github.com/COSMO-ORG/cosmo/tree/master/dycore"

    git = "ssh://git@github.com/COSMO-ORG/cosmo.git"
    apngit = "ssh://git@github.com/MeteoSwiss-APN/cosmo.git"
    c2smgit = "ssh://git@github.com/C2SM-RCM/cosmo.git"
    empagit = 'ssh://git@github.com/C2SM-RCM/cosmo-ghg.git'

    maintainers = ['elsagermann']

    version('org-master', branch='master')
    version('6.0', tag='6.0')

    version('apn-mch',
            git='ssh://git@github.com/MeteoSwiss-APN/cosmo.git',
            branch='mch')
    version('5.09a.mch1.2.p2', git=apngit, tag='5.09a.mch1.2.p2')
    version('c2sm-master',
            git='ssh://git@github.com/C2SM-RCM/cosmo.git',
            branch='master')
    version('c2sm-features',
            git='ssh://git@github.com/C2SM-RCM/cosmo.git',
            branch='c2sm-features')
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
    variant('production',
            default=False,
            description='Force all variants to be the ones used in production')
    variant('cuda_arch',
            default='none',
            description='Build with cuda_arch',
            values=('80', '70', '60', '37'),
            multi=False)
    variant('cuda', default=True, description='Build with cuda or target gpu')
    variant('gt1', default=False, description='Build with gridtools 1.1.3')

    variant('slurm_bin',
            default='srun',
            description='Slurm binary on CSCS machines')
    variant('slurm_opt_partition',
            default='-p',
            description='Slurm option to specify partition for testing')
    variant('slurm_partition',
            default='normal',
            description='Slurm partition for testing')

    variant('slurm_gpu',
            default='-',
            description='Slurm GPU reservation for testing')

    variant('slurm_opt_nodes',
            default='-n',
            description='Slurm option to specify number of nodes for testing')
    variant('slurm_nodes',
            default='{0}',
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

    depends_on('gridtools@1.1.3 ~cuda', when='~cuda+gt1')
    depends_on('gridtools@1.1.3 +cuda', when='+cuda+gt1')
    depends_on('boost@1.65.1: +program_options +system')
    depends_on('serialbox@2.6.0', when='+build_tests', type=('run'))
    depends_on('mpi', type=('build', 'link', 'run'), when='~cuda')
    depends_on('mpi +cuda', type=('build', 'link', 'run'), when='+cuda')
    depends_on('slurm', type='run')
    depends_on('cmake@3.12:')
    depends_on('cuda', type=('build', 'link', 'run'), when='+cuda')

    conflicts('%nvhpc')
    conflicts('+production', when='build_type=Debug')
    conflicts('+production', when='+pmeters')

    # pass spec from spec to test_dycore.py in yaml-format
    patch('patches/c2sm-master/spec_as_yaml/patch.test_dycore',
          when='@c2sm-master')
    patch('patches/org-master/spec_as_yaml/patch.test_dycore',
          when='@org-master')
    patch('patches/c2sm-features/spec_as_yaml/patch.test_dycore',
          when='@c2sm-features')

    patch('patches/apn-mch/spec_as_yaml/patch.test_dycore', when='@apn-mch')
    patch('patches/5.09a.mch1.2.p2/spec_as_yaml/patch.test_dycore',
          when='@5.09a.mch1.2.p2')

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
        cwd = os.path.join(self.root_cmakelists_dir, 'test/tools')
        if '+build_tests' in self.spec:
            with open(os.path.join(cwd, 'spec.yaml'), mode='w') as f:
                f.write(self.spec.to_yaml())
            try:
                subprocess.run([
                    './test_dycore.py', '-s', 'spec.yaml', '-b',
                    str(self.build_directory)
                ],
                               cwd=cwd,
                               check=True,
                               stderr=subprocess.STDOUT)
            except:
                raise InstallError('Dycore tests failed')
