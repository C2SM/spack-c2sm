# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from collections import defaultdict


class Icon(AutotoolsPackage):
    """The ICON modelling framework is a joint project between the
    German Weather Service and the
    Max Planck Institute for Meteorology for
    developing a unified next-generation global numerical weather prediction and
    climate modelling system. The ICON model has been introduced into DWD's
    operational forecast system in January 2015."""

    homepage = 'https://gitlab.dkrz.de/icon/icon'
    url = 'https://gitlab.dkrz.de/icon/icon/-/archive/icon-2.6.2.2/icon-icon-2.6.2.2.tar.gz'
    git = 'ssh://git@gitlab.dkrz.de/icon/icon.git'

    maintainers = ['egermann']

    version('master', branch='master', submodules=True)
    version('2.6.5', tag='icon-2.6.4', submodules=True)
    version('2.6.4.2', tag='icon-2.6.4.2', submodules=True)
    version('2.6.3', tag='icon-2.6.3', submodules=True)
    version('2.6.2.2', tag='icon-2.6.2.2', submodules=True)
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
            git='ssh://git@github.com/C2SM/icon-exclaim.git',
            branch='master',
            submodules=True)
    version('c2sm-master',
            git='ssh://git@github.com/C2SM/icon.git',
            branch='master',
            submodules=True)

    # Model Features:
    variant('atmo',
            default=False,
            description='Enable the atmosphere component')
    variant('ocean', default=False, description='Enable the ocean component')
    variant('jsbach', default=False, description='Enable the land component')
    variant('coupling', default=False, description='Enable the coupling')
    variant('ecrad',
            default=False,
            description='Enable usage of the ECMWF radiation scheme')
    variant(
        'rte-rrtmgp',
        default=False,
        description=
        'Enable usage of the RTE+RRTMGP toolbox for radiation calculations')
    variant(
        'rttov',
        default=False,
        description='Enable usage of the radiative transfer model for TOVS')
    variant('dace',
            default=False,
            description='Enable the DACE modules for data assimilation')
    variant('emvorado',
            default=False,
            description='Enable the radar forward operator EMVORADO')
    variant('art',
            default=False,
            description='Enable the aerosols and reactive trace component ART')
    variant('silent-rules',
            default=False,
            description='Build with Make silent rules ON')

    # Infrastructural Features:
    variant('mpi',
            default=False,
            description='Enable MPI (parallelization) support')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('grib2', default=False, description='Enable GRIB2 I/O')
    variant('parallel-netcdf',
            default=False,
            description='Enable usage of the parallel features of NetCDF')
    # variant('cdi-pio', default=False, description='Enable usage of the parallel features of CDI') #TODO: add this eventually!
    # variant('sct', default=False, description='Enable the SCT timer') #TODO: add this eventually!
    # variant('yaxt', default=False, description='Enable the YAXT data exchange') #TODO: add this eventually!
    variant('claw',
            default=False,
            description='Build with claw directories enabled')

    serialization_values = ('read', 'perturb', 'create')
    variant('serialization',
            default='none',
            values=('none', ) + serialization_values,
            description='Enable the Serialbox2 serialization')

    # Optimization Features:
    variant('mixed-precision',
            default=False,
            description='Enable mixed precision dycore')

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
    variant('config_dir',
            default='.',
            description='Enable out-of-source build by describing config_dir')

    variant('ham',
            default=False,
            description='Build with hammoz and atm_phy_echam enabled.')

    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')

    depends_on('libxml2')

    for x in serialization_values:
        depends_on('serialbox', when=f'serialization={x}')

    depends_on('eccodes +aec jp2k=openjpeg', when='+grib2')
    depends_on('eccodes +aec jp2k=openjpeg +fortran', when='+emvorado')

    depends_on('lapack')
    depends_on('blas')

    depends_on('netcdf-fortran')

    depends_on('netcdf-c')
    depends_on('netcdf-c +mpi', when='+parallel-netcdf')

    depends_on('hdf5 +szip +hl +fortran', when='+emvorado')

    depends_on('zlib', when='+emvorado')
    depends_on('mpi +wrappers', when='+mpi')

    depends_on('cuda', when='icon_target=gpu')

    depends_on('claw', when='+claw', type='build')
    depends_on('claw@:2.0.2', when='@:2.6.2.2 +claw', type='build')

    depends_on('cdo', type='test')

    conflicts('+rte-rrtmgp', when='@:2.6.2.2')
    conflicts('+art', when='@:2.6.2.2')
    # conflicts('+dace', when='@:2.6.2.2~rttov')
    conflicts('+dace', when='~mpi')
    conflicts('+dace', when='+rttov')
    conflicts('+emvorado', when='~mpi')
    conflicts('icon_target=cpu', when='+claw')
    conflicts('icon_target=gpu', when='%intel')
    conflicts('icon_target=gpu', when='%gcc')

    @run_before('configure')
    def generate_hammoz_nml(self):
        dir = self.spec.variants["config_dir"].value
        if '+ham' in self.spec:
            with working_dir(f'{dir}/externals/atm_phy_echam_submodels/namelists'):
                make()

    def setup_build_environment(self, env):
        env.set('XML2_ROOT', self.spec['libxml2'].prefix)
        if '+dace' in self.spec:
            env.set('ICON_FCFLAGS', '-O2')
            env.set('ICON_DACE_FCFLAGS', '-O1')
        if self.spec.variants['serialization'].value != 'none':
            env.set('SERIALBOX2_ROOT', self.spec['serialbox'].prefix)
        if '+claw' in self.spec:
            env.set('CLAW', self.spec['claw'].prefix + '/bin/clawfc')
        if '+grib2' in self.spec or '+emvorado' in self.spec:
            env.set('ECCODES_ROOT', self.spec['eccodes'].prefix)
        if self.run_tests:
            # setting BB_SYSTEM sets d56 as account in file create_target_header
            env.set('BB_SYSTEM', 'use_d56_account')

    # def enable_or_disable(self, name):
    #     if f'+{name}' in self.spec:
    #         prefix = 'enable'
    #     else:
    #         prefix = 'disable'
    #     return [f'--{prefix}-{name}']

    def configure_args(self):
        config_args = []
        # config_vars = defaultdict(list)
        # libs = LibraryList([])


        for x in [
                'atmo', 'ocean', 'jsbach', 'coupling', 'ecrad', 'rte-rrtmgp',
                'rttov', 'dace', 'emvorado', 'art', 'silent-rules', 'mpi',
                'openmp', 'grib2', 'parallel-netcdf', 'claw', 'mixed-precision'
        ]:
            config_args += self.enable_or_disable(x)

        serialization = self.spec.variants['serialization'].value
        if serialization == 'none':
            config_args.append('--disable-serialization')
        else:
            config_args.append(f'--enable-serialization={serialization}')

        # Icon-hammoz:
        if '+ham' in self.spec:
            config_args.append('--enable-atm-phy-echam-submodels')
            config_args.append('--enable-hammoz')

        # libs += self.spec['lapack:fortran'].libs
        # libs += self.spec['blas:fortran'].libs
        # libs += self.spec['netcdf-fortran'].libs

        # if '+mpi' in self.spec:
        #     config_args.extend([
        #         'CC=' + self.spec['mpi'].mpicc,
        #         'FC=' + self.spec['mpi'].mpifc,
        #         # We cannot provide a universal value for MPI_LAUNCH, therefore
        #         # we have to disable the MPI checks:
        #         '--disable-mpi-checks'])

        # if '~claw' in self.spec:
        #     config_vars['CLAWFLAGS'].append(self.spec['netcdf-fortran'].headers.include_flags)
        #     if '+cdi-pio' in self.spec:
        #         config_vars['CLAWFLAGS'].append(self.spec['libcdi-pio'].headers.include_flags)

        # if self.spec.variants['icon_target'].value == 'cpu':
        #     config_args.append('--disable-gpu')
        # else:
        #     config_args.extend([
        #         '--enable-gpu',
        #         '--disable-loop-exchange',
        #         'NVCC={0}'.format(self.spec['cuda'].prefix.bin.nvcc)])

        #     config_vars['NVCFLAGS'].extend(['-g', '-O3', '-arch=sm_80']) #TODO: sm_80 should not be hard coded!

        # if self.compiler.name in ['pgi', 'nvhpc']:
        #     config_vars['CFLAGS'].extend(['-g', '-O2'])
        #     config_vars['FCFLAGS'].extend(['-g', '-O', '-Mrecursive', '-Mallocatable=03', '-Mbackslash'])
        #     if self.spec.variants['icon_target'].value == 'gpu':
        #         config_vars['FCFLAGS'].extend(
        #             ['-acc=verystrict', '-Minfo=accel,inline',
        #              '-ta=nvidia:cc80']) #TODO: 80 is the cuda_arch. This should not be hard coded!
        #         config_vars['ICON_FCFLAGS'].append('-D__SWAPDIM')
        #         if '+dace' in self.spec:
        #             # Different implementation of link and acc declare between
        #             # cray and pgi (see
        #             # externals/dace_icon/src_for_icon/parallel_utilities.f90):
        #             if self.version <= ver('2.6.4'):
        #                 config_vars['ICON_FCFLAGS'].append('-DPGI_FIX_ACCLINK')

        # # Finalize the LIBS variable (we always put the real collected
        # # libraries to the front):
        # config_vars['LIBS'].insert(0, libs.link_flags)

        # config_args.extend(['{0}={1}'.format(var, ' '.join(val))
        #                     for var, val in config_vars.items()])

        return config_args

    def configure(self, spec, prefix):
        dir = self.spec.variants["config_dir"].value
        site = self.spec.variants["site"].value
        host = self.spec.variants["host"].value
        PU = self.spec.variants["icon_target"].value

        if self.compiler.name == 'cce':
            compiler = 'cray'
        elif self.compiler.name == 'nvhpc' or self.compiler.name == 'pgi':
            compiler = 'nvidia'
        else:
            compiler = self.compiler.name

        configure = Executable(
            f'{dir}/config/{site}/{host}.{PU}.{compiler} --prefix={prefix}')
        configure(*self.configure_args())
