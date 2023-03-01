from spack import *
import os
import shutil


class Icontools(AutotoolsPackage):
    """
    DWD ICON Tools.
    Set of tools to prepare the input files 
    (for example the boundary condition, initial condition file,...) for ICON.
    """

    homepage = 'https://wiki.c2sm.ethz.ch/MODELS/ICONDwdIconTools'
    c2sm = 'ssh://git@github.com/C2SM/icontools.git'
    dkrz = 'ssh://git@gitlab.dkrz.de/dwd-sw/dwd_icon_tools.git'

    maintainers = ['jonasjucker']

    version('c2sm-master', git=c2sm, branch='master', submodules=True)
    version('dkrz-master', git=dkrz, branch='master', submodules=True)
    version('2.5.2', git=dkrz, tag='icontools-2.5.2', submodules=True)

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('hdf5 +hl')
    depends_on('mpi')
    depends_on('eccodes +fortran')
    depends_on('jasper')

    variant('fxtr', default=False)
    variant('slave',
            default='none',
            description='Build on described slave (e.g daint)')

    conflicts('%pgi')
    conflicts('%nvhpc')
    conflicts('%cce')

    def configure_args(self):
        args = []
        args.append('acx_cv_fc_ftn_include_flag=-I')
        args.append('acx_cv_fc_pp_include_flag=-I')
        args.append('--disable-silent-rules')
        args.append('--disable-shared')
        args.append('--with-netcdf=' + self.spec['netcdf-fortran'].prefix)
        args.append('--enable-iso-c-interface')
        args.append('--enable-grib2')
        args.append('--with-eccodes=' + self.spec['eccodes'].prefix)

        return args

    def setup_build_environment(self, env):
        # Daint specific flags since cray-modules setting not recognized
        if self.spec.variants['slave'].value == 'daint':
            env.set('NETCDF_DIR', self.spec['netcdf-c'].prefix)

        #Setting CFLAGS
        env.append_flags('CFLAGS', '-O2')
        env.append_flags('CFLAGS', '-g')
        env.append_flags('CFLAGS', '-Wunused')
        env.append_flags('CFLAGS', '-DHAVE_LIBNETCDF')
        env.append_flags('CFLAGS', '-DHAVE_NETCDF4')
        env.append_flags('CFLAGS', '-DHAVE_CF_INTERFACE')
        env.append_flags('CFLAGS', '-DHAVE_LIBGRIB_API')
        env.append_flags('CFLAGS', '-D__ICON__')
        env.append_flags('CFLAGS', '-DNOMPI')
        #Setting CXXFLAGS
        env.append_flags('CXXFLAGS', '-O2')
        env.append_flags('CXXFLAGS', '-g')
        env.append_flags('CXXFLAGS', '-fopenmp')
        env.append_flags('CXXFLAGS', '-Wunused')
        env.append_flags('CXXFLAGS', '-DNOMPI')
        #Setting FCFLAGS
        env.append_flags('FCFLAGS', '-O2')
        env.append_flags('FCFLAGS', '-g')
        env.append_flags('FCFLAGS', '-cpp')
        env.append_flags('FCFLAGS', '-Wunused')
        env.append_flags('FCFLAGS', '-DNOMPI')
        #Setting LIBS
        env.append_flags('LIBS', '-lhdf5')
        env.append_flags('LIBS', '-leccodes')
        env.append_flags('LIBS', '-leccodes_f90')

        if '+fxtr' in self.spec:
            env.append_flags('FCFLAGS', '-DFXTR')

        # jasper needs to be after eccodes, otherwise linking error
        env.append_flags('LIBS', '-ljasper')

        env.append_flags('LIBS', '-lgfortran')

    @run_after('install')
    def add_include_files(self):
        with working_dir(
                os.path.join(self.stage.source_path, 'libicontools', 'src')):
            for file in os.listdir('.'):
                if file.startswith('mo_') and file.endswith('.mod'):
                    shutil.copy(file, self.prefix.include)
