# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os, subprocess
from spack import *

import llnl.util.tty as tty


class Icon(Package):
    """The ICON modelling framework is a joint project between the
    German Weather Service and the
    Max Planck Institute for Meteorology for
    developing a unified next-generation global numerical weather prediction and
    climate modelling system. The ICON model has been introduced into DWD's
    operational forecast system in January 2015."""

    homepage = 'https://gitlab.dkrz.de/icon/icon'
    url = 'https://gitlab.dkrz.de/icon/icon/-/archive/icon-2.6.2.2/icon-icon-2.6.2.2.tar.gz'
    git = 'ssh://git@gitlab.dkrz.de/icon/icon.git'

    maintainers = ['jonasjucker', 'PanicSheep']

    version('master', branch='master', submodules=True)
    version('2.6.5', tag='icon-2.6.5', submodules=True)
    version('nwp',
            git='ssh://git@gitlab.dkrz.de/icon/icon-nwp.git',
            submodules=True)
    version('cscs',
            git='ssh://git@gitlab.dkrz.de/icon/icon-cscs.git',
            submodules=True)
    version('aes',
            git='ssh://git@gitlab.dkrz.de/icon/icon-aes.git',
            submodules=True)
    version('ham',
            git='ssh://git@git.iac.ethz.ch:hammoz/icon-hammoz.git',
            branch='hammoz/gpu/master',
            submodules=True)
    version('exclaim-master',
            branch='master',
            git='ssh://git@github.com/C2SM/icon-exclaim.git',
            submodules=True)
    version('c2sm-master',
            branch='master',
            git='ssh://git@github.com/C2SM/icon.git',
            submodules=True)

    depends_on('cmake')
    depends_on('libxml2')
    depends_on('serialbox +fortran', when='serialize_mode=create')
    depends_on('serialbox +fortran', when='serialize_mode=read')
    depends_on('serialbox +fortran', when='serialize_mode=perturb')
    depends_on('eccodes +aec +fortran', when='+eccodes')
    # depends_on('hdf5 +szip +hl +fortran')
    depends_on('zlib')
    depends_on('mpi +wrappers')
    depends_on('claw', when='+claw', type='build')
    depends_on('claw@:2.0.2', when='@:2.6.2.2 +claw', type='build')
    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('cuda', when='icon_target=gpu')
    depends_on('cdo', type='test')

    variant('icon_target',
            default='gpu',
            description='Build with target gpu or cpu',
            values=('gpu', 'cpu'),
            multi=False)
    variant('host',
            default='none',
            description='Build on described host (e.g daint)')
    variant('site',
            default='cscs',
            description='Build on described site (e.g cscs)',
            multi=False)
    variant('claw',
            default=False,
            description='Build with claw directories enabled')
    variant('rte-rrtmgp',
            default=True,
            description='Build with rte-rrtmgp enabled')
    variant('mpi-checks',
            default=False,
            description='Build with mpi-check enabled')
    variant('openmp', default=True, description='Build with openmp enabled')
    variant('serialize_mode',
            default='none',
            description='Build with serialization, with serialze_mode enabled',
            values=('none', 'create', 'read', 'perturb'))
    variant('eccodes', default=False, description='Build with grib2 enabled')
    variant('test_name',
            default='none',
            description='Launch test: test_name after installation')
    variant('skip-config', default=False, description='Skip configure phase')
    variant('config_dir',
            default='.',
            description='Enable out-of-source build by describing config_dir')
    variant('ham',
            default=False,
            description='Build with hammoz and atm_phy_echam enabled.')
    variant('art', default=False, description='Build with art enabled')
    variant('ocean', default=True, description='Build with ocean enabled')
    variant('dace', default=False, description='Build with DACE enabled')
    variant('rttov', default=False, description='Build with RTTOV enabled')
    variant('mixed-precision',
            default=False,
            description='Build the ICON dycore in mixed precision')
    variant('silent-rules',
            default=True,
            description='Build with Make silent rules ON')

    conflicts('icon_target=cpu', when='+claw')
    conflicts('icon_target=gpu', when='%intel')
    conflicts('icon_target=gpu', when='%gcc')
    conflicts('+dace', when='+rttov')

    phases = ['configure', 'build', 'install']

    @run_before('configure')
    def generate_hammoz_nml(self):
        if '+ham' in self.spec:
            with working_dir('./externals/atm_phy_echam_submodels/namelists'):
                make()

    def setup_build_environment(self, env):
        self.config_dir = self.spec.variants['config_dir'].value
        _config_file_name = self.spec.variants[
            'host'].value + '.' + self.spec.variants['icon_target'].value
        if self.compiler.name == 'cce':
            _config_file_name += '.cray'
        elif self.compiler.name == 'nvhpc' or self.compiler.name == 'pgi':
            _config_file_name += '.nvidia'
        else:
            _config_file_name += '.' + self.compiler.name

        self._config_file_name = _config_file_name

        if '+dace' in self.spec:
            env.set('ICON_FCFLAGS', '-O2')
            env.set('ICON_DACE_FCFLAGS', '-O1')

        if '~skip-config' in self.spec:
            env.set('XML2_ROOT', self.spec['libxml2'].prefix)
            if self.spec.variants['serialize_mode'].value != 'none':
                env.set('SERIALBOX2_ROOT', self.spec['serialbox'].prefix)
            if '+claw' in self.spec:
                env.set('CLAW', self.spec['claw'].prefix + '/bin/clawfc')
            if '+eccodes' in self.spec:
                env.set('ECCODES_ROOT', self.spec['eccodes'].prefix)
        if self.run_tests:
            # setting BB_SYSTEM sets d56 as account in file create_target_header
            env.set('BB_SYSTEM', 'use_d56_account')

    def configure_args(self):

        args = []

        # Icon-hammoz:
        if '+ham' in self.spec:
            args.append('--enable-atm-phy-echam-submodels')
            args.append('--enable-hammoz')

        # Serialization
        if self.spec.variants['serialize_mode'].value != 'none':
            args.append('--enable-serialization=' +
                        self.spec.variants['serialize_mode'].value)

        # Art
        if '+art' in self.spec:
            args.append('--enable-art')

        # Claw
        if '+claw' in self.spec:
            args.append('--enable-claw')

        # Eccodes
        if '+eccodes' in self.spec:
            args.append('--enable-grib2')

        # DACE
        if '+dace' in self.spec:
            args.append('--enable-dace')

        # Ocean
        if '+ocean' in self.spec:
            args.append('--enable-ocean')
        else:
            args.append('--disable-ocean')

        # Rte-rrtmgp
        if '~rte-rrtmgp' in self.spec:
            args.append('--disable-rte-rrtmgp')

        # RTTOV
        if '~rttov' in self.spec:
            args.append('--disable-rttov')

        # Mixed-precision
        if '+mixed-precision' in self.spec:
            args.append('--enable-mixed-precision')

        # Silent rules
        if '~silent-rules' in self.spec:
            args.append('--disable-silent-rules')

        return args

    def configure(self, spec, prefix):
        if '~skip-config' in spec:
            configure = Executable(
                f'{self.config_dir}/config/{self.spec.variants["site"].value}/{self._config_file_name} --prefix={prefix}'
            )
            configure(*self.configure_args())

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')

    @run_before('install')
    @on_package_attributes(run_tests=True)
    def check(self):
        if os.path.exists('scripts/spack/test.py'):
            try:
                subprocess.run(
                    ['./scripts/spack/test.py', '--spec',
                     str(self.spec)],
                    check=True)
            except:
                raise InstallError('Tests failed')
        else:
            tty.warn('Cannot find test.py -> skipping tests')

    @run_after('build')
    def test(self):
        if self.spec.variants['test_name'].value == 'none':
            return

        if '+ham' in self.spec:
            try:
                subprocess.run([
                    'indata_hammoz_root=/store/c2sm/c2sme/input_gcm/icon/input_hammoz/ ./make_runscripts -s '
                    + self.spec.variants['test_name'].value
                ],
                               shell=True,
                               stderr=subprocess.STDOUT,
                               check=True)
            except:
                raise InstallError('make runscripts failed')
        else:
            try:
                subprocess.run([
                    './make_runscripts', '-s',
                    self.spec.variants['test_name'].value
                ],
                               stderr=subprocess.STDOUT,
                               check=True)
            except:
                raise InstallError('make runscripts failed')
        try:
            if self.spec.variants['host'].value == 'daint':
                subprocess.run([
                    'sbatch', '-W', '--time=00:15:00', '-A', 'g110', '-C',
                    'gpu', '-p', 'debug',
                    'exp.' + self.spec.variants['test_name'].value + '.run'
                ],
                               stderr=subprocess.STDOUT,
                               cwd='run',
                               check=True)
            if self.spec.variants['host'].value == 'tsa':
                subprocess.run([
                    'sbatch', '-W', '--time=00:15:00', '-p', 'dev',
                    'exp.' + self.spec.variants['test_name'].value + '.run'
                ],
                               stderr=subprocess.STDOUT,
                               cwd='run',
                               check=True)
        except:
            raise InstallError('Submitting test failed')

        test_status = subprocess.check_output(
            ['cat', 'finish.status'],
            cwd=os.path.join('experiments',
                             self.spec.variants['test_name'].value))
        if 'OK' in str(test_status):
            print('Test OK!')
        else:
            raise InstallError('Test failed')
