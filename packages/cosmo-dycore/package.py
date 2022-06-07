from spack import *
import subprocess, re
from version_detection import set_versions


class CosmoDycore(CMakePackage):
    """C++ dycore of cosmo based on GridTools library"""

    homepage = "https://github.com/COSMO-ORG/cosmo/tree/master/dycore"

    git = "git@github.com:COSMO-ORG/cosmo.git"
    apngit = "git@github.com:MeteoSwiss-APN/cosmo.git"
    c2smgit = "git@github.com:C2SM-RCM/cosmo.git"
    empagit = 'git@github.com:C2SM-RCM/cosmo-ghg.git'

    maintainers = ['elsagermann']

    version('org-master', branch='master')
    version('dev-build', branch='master')
    version('apn-mch',
            git='git@github.com:MeteoSwiss-APN/cosmo.git',
            branch='mch')
    version('c2sm-master',
            git='git@github.com:C2SM-RCM/cosmo.git',
            branch='master')
    version('c2sm-features',
            git='git@github.com:C2SM-RCM/cosmo.git',
            branch='c2sm-features')
    version('empa-ghg', git=empagit, branch='c2sm')

    set_versions(version, apngit, 'apn', regex_filter='.*mch.*')
    set_versions(version, c2smgit, 'c2sm')
    set_versions(version, git, 'org')
    set_versions(version, empagit, 'empa')

    #deprecated
    version('master', branch='master')
    version('mch', git='git@github.com:MeteoSwiss-APN/cosmo.git', branch='mch')

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
    variant('slave',
            default='tsa',
            description='Build on slave tsa or daint',
            multi=False)
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
            values=('70', '60', '37'),
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
    depends_on('boost@1.67.0')
    depends_on('serialbox@2.6.0', when='+build_tests')
    depends_on('mpicuda', type=('build', 'link', 'run'), when='+cuda')
    depends_on('mpi', type=('build', 'link', 'run'), when='~cuda')
    depends_on('slurm%gcc', type='run')
    depends_on('cmake@3.12:%gcc')
    depends_on('cuda%gcc', when='+cuda', type=('build', 'link', 'run'))

    conflicts('+production', when='build_type=Debug')
    conflicts('+production', when='+pmeters')

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
            GridToolsDir = spec['gridtools'].prefix + '/lib/cmake'
            args.append('-DGridTools_DIR={0}'.format(GridToolsDir))

        args.append('-DCMAKE_BUILD_TYPE={0}'.format(
            self.spec.variants['build_type'].value))
        args.append('-DCMAKE_INSTALL_PREFIX={0}'.format(self.prefix))
        args.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))
        args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
        args.append('-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON')
        args.append('-DBoost_USE_STATIC_LIBS=ON')

        if spec.variants['pmeters'].value:
            args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=ON')
        else:
            args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=OFF')
        if spec.variants['real_type'].value == 'float':
            args.append('-DPRECISION=float')
        else:
            args.append('-DPRECISION=double')

        if not spec.variants['build_tests'].value:
            args.append('-DBUILD_TESTING=OFF')
        else:
            args.append('-DBUILD_TESTING=ON')
            SerialBoxRoot = spec['serialbox'].prefix + '/cmake'
            args.append('-DSerialbox_DIR={0}'.format(SerialBoxRoot))
        # target=gpu
        if '+cuda' in spec:
            args.append('-DENABLE_CUDA=ON')
            cuda_arch = spec.variants['cuda_arch'].value
            if cuda_arch is not None:
                args.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch))
            if '~gt1' in spec:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=gpu')
            else:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=CUDA')
        # target=cpu
        else:
            args.append('-DENABLE_CUDA=OFF')
            if '~gt1' in spec:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=cpu_ifirst')
            else:
                args.append('-DDYCORE_TARGET_ARCHITECTURE=x86')

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        if '+build_tests' in self.spec:
            try:
                subprocess.run([
                    './test_dycore.py', '-s',
                    self.spec.__str__(), '-b',
                    str(self.build_directory)
                ],
                               cwd=self.root_cmakelists_dir + '/test/tools',
                               check=True,
                               stderr=subprocess.STDOUT)
            except:
                raise InstallError('Dycore tests failed')
