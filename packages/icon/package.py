# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Icon(AutotoolsPackage):
    """The ICON modelling framework is a joint project between the
    German Weather Service and the
    Max Planck Institute for Meteorology for
    developing a unified next-generation global numerical weather prediction and
    climate modelling system. The ICON model has been introduced into DWD's
    operational forecast system in January 2015."""

    homepage = 'https://software.ecmwf.int/wiki/display/GRIB/Home'
    url = 'https://gitlab.dkrz.de/icon/icon-cscs/-/archive/mc10_for_icon-2.6.x-rc/icon-cscs-mc10_for_icon-2.6.x-rc.tar.gz'
    git = 'git@gitlab.dkrz.de:icon/icon-cscs.git'

    maintainers = ['egermann']

    version('master', branch='master', submodules=True)
    version('2.6.x-rc', commit='040de650', submodules=True)
    version('2.0.17', commit='39ed04ad', submodules=True)

    depends_on('m4')
    depends_on('autoconf%gcc')
    depends_on('automake%gcc')
    depends_on('libtool%gcc')
    depends_on('cmake%gcc')
    depends_on('jasper@1.900.1%gcc ~shared')
    depends_on('libxml2@2.9.7%gcc')
    depends_on('serialbox@2.6.0')
    depends_on('claw@2.0.1', when='+claw', type='build')
    depends_on('netcdf-c +mpi', type=('build', 'link'))
    depends_on('mpicuda', when='icon_target=gpu')
    depends_on('mpi', when='icon_target=cpu')
    depends_on('cuda%gcc', when='icon_target=gpu')

    variant('icon_target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('host', default='daint', description='Build on host daint', multi=False)
    variant('cuda_arch', default='none', description='Build with cuda_arch', values=('70', '60', '37'), multi=False)
    variant('claw', default=True, description='Build with claw directories enabled')
    variant('rte-rrtmgp', default=True, description='Build with rte-rrtmgp enabled')
    variant('mpi-checks', default=False, description='Build with mpi-check enabled')

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

        if self.spec.variants['icon_target'].value == 'gpu':
            env.set('CUDA_HOME', self.spec['cuda'].prefix)

    def configure_args(self):
        args = []
        if '+claw' in self.spec:
            args.append('CLAW=' + self.spec['claw'].prefix + '/bin/clawfc')
            args.append('CLAWFLAGS=-I${NETCDF_DIR}/include')
            args.append('--enable-claw')

        if '+rte-rrtmgp' in self.spec:
            args.append('--enable-rte-rrtmgp')

        if '~mpi-checks' in self.spec:
            args.append('--disable-mpi-checks')

        # Serialbox library
        SERIALBOXI='-I' + self.spec['serialbox'].prefix + '/include '
        SERIALBOXL='-L' + self.spec['serialbox'].prefix + '/lib '
        SERIALBOX_LIBS='-lSerialboxFortran '
        args.append('SB2PP=' + self.spec['serialbox'].prefix +  '/python/pp_ser/pp_ser.py ')

        # Libxml2 library
        XML2I='-I'  + self.spec['libxml2'].prefix + '/include/libxml2 '
        XML2L='-L' + self.spec['libxml2'].prefix + '/lib '
        XML2L_LIBS='-lxml2 '

        # Blas lapack library
        BLAS_LAPACK_LIBS='-llapack -lblas '

        # Standard cpp library
        STDCPPL='-L/opt/gcc/8.3.0/snos/lib64 '
        STDCPP_LIBS='-lstdc++'

        # Set MPI_LAUNCH
        args.append('MPI_LAUNCH=false')

        # Set CFLAGS
        args.append('CFLAGS=-g -O2')

        # Set CPPFLAGS
        args.append('CPPFLAGS=' + XML2I)

        if self.spec.variants['icon_target'].value == 'gpu':
            # Set NVCFLAGS
            args.append('NVCC=nvcc')
            args.append('NVCFLAGS=--std=c++11 -arch=sm_60 -g -O3')

        # Set FCFLAGS
        FCFLAGS='-g -O -Mrecursive -Mallocatable=03 '

        if self.spec.variants['icon_target'].value == 'gpu':
            args.append('--disable-loop-exchange')
            args.append('--enable-gpu')
            FCFLAGS+=' -acc=verystrict  -ta=nvidia:cc' + self.spec.variants['cuda_arch'].value + ' -Minfo=accel,inline '

        elif self.spec.variants['icon_target'].value == 'cpu':
            FCFLAGS+='-tp=haswell '

        FCFLAGS+= SERIALBOXI + ' -D__SWAPDIM'
        args.append('FCFLAGS=' + FCFLAGS)

        # Set LDFLAGS
        LDFLAGS= STDCPPL + SERIALBOXL + XML2L + ' -L/opt/pgi/20.1.1/linux86-64-llvm/20.1/lib/libomp '
        args.append('LDFLAGS=' + LDFLAGS)

        # Set LIBS
        #LIBS= '-lomptarget -Wl,--as-needed '
        LIBS= XML2L_LIBS + BLAS_LAPACK_LIBS + SERIALBOX_LIBS + STDCPP_LIBS
        args.append('LIBS=' + LIBS)

        return args
