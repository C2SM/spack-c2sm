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
    depends_on('libxml2@2.9.7%gcc', type=('build', 'link', 'run'))
    depends_on('serialbox@2.6.0', when='+serialize', type=('build', 'link', 'run'))
    depends_on('hdf5', type=('build', 'link', 'run'))
    depends_on('claw@2.0.1', when='+claw', type=('build', 'link', 'run'))
    depends_on('netcdf-c ~mpi', type=('build', 'link', 'run'))
    depends_on('mpicuda', when='icon_target=gpu', type=('build', 'link', 'run'))
    depends_on('ompt-openmp', when='%pgi', type=('build', 'link', 'run'))
    depends_on('mpi', when='icon_target=cpu', type=('build', 'link', 'run'))
    depends_on('cuda%gcc', when='icon_target=gpu', type=('build', 'link', 'run'))

    variant('icon_target', default='gpu', description='Build with target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('host', default='daint', description='Build on host daint', multi=False)
    variant('cuda_arch', default='60', description='Build with cuda_arch', values=('70', '60', '37'), multi=False)
    variant('claw', default=True, description='Build with claw directories enabled')
    variant('rte-rrtmgp', default=True, description='Build with rte-rrtmgp enabled')
    variant('mpi-checks', default=False, description='Build with mpi-check enabled')
    variant('openmp', default=True, description='Build with openmp enabled')
    variant('serialize', default=True, description='Build with serialization enabled')

    conflicts('+openmp', when='%intel')
    conflicts('+openmp', when='%cce')
    conflicts('+claw', when='%intel')
    conflicts('+claw', when='%cce')
    conflicts('icon_target=gpu', when='%intel')
    conflicts('icon_target=gpu', when='%cce')

    def setup_build_environment(self, env):
        self.setup_run_environment(env)
        if self.spec.variants['icon_target'].value == 'gpu':
            env.set('CUDA_HOME', self.spec['cuda'].prefix)

    def configure_args(self):
        args = []

        CFLAGS=''
        CPPFLAGS=''
        FCFLAGS=''
        LDFLAGS=''
        LIBS=''

        # Claw library
        if '+claw' in self.spec:
            args.append('CLAW=' + self.spec['claw'].prefix + '/bin/clawfc')
            args.append('CLAWFLAGS=-I' + self.spec['netcdf-c'].prefix + '/' + self.compiler.name + '/' + str(self.compiler.version.up_to(2))  + '/include')
            args.append('--enable-claw')

        # Rte-rttmgp
        if '+rte-rrtmgp' in self.spec:
            args.append('--enable-rte-rrtmgp')

        # Mpi-checks
        if '~mpi-checks' in self.spec:
            args.append('--disable-mpi-checks')

        # OpenMP library
        if '~openmp' in self.spec:
            args.append('--disable-openmp')
        else:
            LIBS+='-lomptarget '
            LDFLAGS+=' -L' + self.spec['ompt-openmp'].prefix + ' '

        # Serialbox library
        if '+serialize' in self.spec:
            SERIALBOXI='-I' + self.spec['serialbox'].prefix + '/include '
            SERIALBOXL='-L' + self.spec['serialbox'].prefix + '/lib '
            SERIALBOX_LIBS='-lSerialboxFortran '
            args.append('SB2PP=' + self.spec['serialbox'].prefix +  '/python/pp_ser/pp_ser.py ')

        # Libxml2 library
        XML2I='-I' + self.spec['libxml2'].prefix + '/include/libxml2 '
        XML2L='-L' + self.spec['libxml2'].prefix + '/lib '
        XML2L_LIBS='-lxml2 '

        # Blas lapack library
        BLAS_LAPACK_LIBS='-llapack -lblas '

        # Netcdf library
        if self.compiler.name == 'cce':
            NETCDFL='-L' + self.spec['netcdf-c'].prefix + '/crayclang/9.0/lib '
        else:
            NETCDFL='-L' + self.spec['netcdf-c'].prefix + '/' + self.compiler.name + '/' + str(self.compiler.version.up_to(2))  + '/lib '
        NETCDF_LIBS='-lnetcdf -lnetcdff '

        # Set MPI_LAUNCH
        args.append('MPI_LAUNCH=false')

        # CPPFLAGS
        CPPFLAGS+=XML2I

        # PGI compiler flags
        if self.compiler.name == 'pgi':
            # Standard cpp library
            STDCPPL='-L/opt/gcc/8.3.0/snos/lib64 '
            STDCPP_LIBS='-lstdc++ '

            # CFLAGS
            CFLAGS+='-g -O2 '

            # FCFLAGS
            FCFLAGS+='-g -O -Mrecursive -Mallocatable=03 '

            # PGI GPU
            if self.spec.variants['icon_target'].value == 'gpu':
                # NVCFLAGS
                args.append('NVCC=nvcc')
                args.append('NVCFLAGS=--std=c++11 -arch=sm_60 -g -O3')
                args.append('--disable-loop-exchange')
                args.append('--enable-gpu')
                FCFLAGS+='-acc=verystrict  -ta=nvidia:cc' + self.spec.variants['cuda_arch'].value + ' -Minfo=accel,inline '
            # PGI CPU
            elif self.spec.variants['icon_target'].value == 'cpu':
                FCFLAGS+='-tp=haswell '

            FCFLAGS+=SERIALBOXI
            LDFLAGS+=STDCPPL + SERIALBOXL + XML2L + NETCDFL
            LIBS+=XML2L_LIBS + BLAS_LAPACK_LIBS + SERIALBOX_LIBS + STDCPP_LIBS + NETCDF_LIBS

        # INTEL compiler flags
        elif self.compiler.name == 'intel':
            CFLAGS+='-g -O3 -ftz '
            FCFLAGS+='-O2 -assume realloc_lhs -ftz '
            LDFLAGS+=XML2L + NETCDFL
            LIBS+='-Wl,--disable-new-dtags -Wl,--as-needed ' + XML2L_LIBS + BLAS_LAPACK_LIBS + NETCDF_LIBS

        # CRAY compiler flags
        elif self.compiler.name == 'cce':
            CFLAGS+='-g -O3 '
            FCFLAGS+='-hadd_paren -r am -Ktrap=divz,ovf,inv -hflex_mp=intolerant -hfp1 -O1,cache0 '
            LDFLAGS+=XML2L
            LIBS+='-Wl,--as-needed ' + XML2L_LIBS + BLAS_LAPACK_LIBS

        args.append('CFLAGS=' + CFLAGS)
        args.append('CPPFLAGS=' + CPPFLAGS)
        args.append('FCFLAGS=' + FCFLAGS)
        args.append('LDFLAGS=' + LDFLAGS)
        args.append('LIBS=' + LIBS)

        return args
