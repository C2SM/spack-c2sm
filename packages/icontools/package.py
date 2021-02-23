# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install icontools
#
# You can edit this file again by typing:
#
#     spack edit icontools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os


class Icontools(AutotoolsPackage):
    """
    DWD ICON Tools for C2SM members. 
    Set of tools to prepare the input files 
    (for example the boundary condition, initial condition file,...) for ICON.
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage= 'https://wiki.c2sm.ethz.ch/MODELS/ICONDwdIconTools'
    git = 'git@github.com:C2SM-ICON/dwd_icon_tools.git'

    maintainers = ['jonasjucker']

    version('master', branch='remove_omp')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4', type='build')

    depends_on('netcdf-fortran', type=('build', 'link'))
    depends_on('netcdf-c', type=('build', 'link'))
    depends_on('mpi', type=('build', 'link', 'run'),)
    depends_on('eccodes ~aec', type=('build', 'link', 'run'))
    depends_on('cosmo-grib-api', type=('build','link','run'), when='~eccodes')
    depends_on('hdf5', type=('build','link'))
    depends_on('jasper@1.900.1%gcc ~shared', type=('build','link'))

    variant('eccodes', default=True, description='Build with eccodes instead of grib-api')

    def configure_args(self):
        args =['--disable-silent-rules',
               '--disable-shared',
               '--with-netcdf={0}/CRAYCLANG/9.0'.format(self.spec['netcdf-fortran'].prefix),
               '--enable-iso-c-interface',
                ]

        if '~eccodes' in self.spec:
            args.append('--with-grib_api={0}'.format(self.spec['cosmo-grib-api'].prefix))
        else:
            args.append('--enable-grib2')
            args.append('--with-eccodes={0}'.format(self.spec['eccodes'].prefix))
        
        return args

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

        # construct all includes/libraries for **FLAGS
        include = ''
        libs = ''

        # NetCDF
        #netcdf_root = os.getenv('NETCDF_DIR')
        #include +=' -I{}/include'.format(netcdf_root)
        #libs +=' -L{}/lib -lnetcdff'.format(netcdf_root)
        include += ' -L{}/CRAYCLANG/9.0/include'.format(self.spec['netcdf-fortran'].prefix)
        #include +=' -I{}/include'.format(self.spec['netcdf-fortran'].prefix)

        #libs =' -L{}/lib -lnetcdff'.format(self.spec['netcdf-fortran'].prefix)
        libs += ' -L{}/CRAYCLANG/9.0/lib -lnetcdff'.format(self.spec['netcdf-fortran'].prefix)


        include += ' -L{}/CRAYCLANG/9.0/include'.format(self.spec['netcdf-c'].prefix)
        #include +=' -I{}/include'.format(self.spec['netcdf-c'].prefix)

        #libs +=' -L{}/lib -lnetcdf '.format(self.spec['netcdf-c'].prefix)
        libs += ' -L{}/CRAYCLANG/9.0/lib -lnetcdf '.format(self.spec['netcdf-c'].prefix)
        
        # MPI
        include +=' -I{}/include'.format(self.spec['mpi'].prefix)
        libs +=' -L{}/lib '.format(self.spec['mpi'].prefix)

        # Jasper
        include +=' -I{}/include'.format(self.spec['jasper'].prefix)
        libs +=' -L{}/lib -ljasper'.format(self.spec['jasper'].prefix)

        #HDF5
        libs +=' -L{}/lib '.format(self.spec['hdf5'].prefix)

        # Grib-Api/Eccodes
        if '~eccodes' in self.spec:
            include +=' -I{}/include'.format(self.spec['cosmo-grib-api'].prefix)
            libs +=' -L{}/lib  -lgrib_api_f90 -lgrib_api'.format(self.spec['cosmo-grib-api'].prefix)
        else:
            include +=' -I{}/include'.format(self.spec['eccodes'].prefix)

            if self.spec['eccodes'].version >= Version('2.19.0'):
                eccodes_lib_dir='lib64'
            else:
                eccodes_lib_dir='lib'

            libs +=' -L{}/{} -leccodes -leccodes_f90'.format(self.spec['eccodes'].prefix, eccodes_lib_dir)


        flags = ' -O2 -g -Wunused  -DHAVE_LIBNETCDF -DHAVE_NETCDF4 -DHAVE_CF_INTERFACE -DHAVE_LIBGRIB -DHAVE_LIBGRIB_API -D__ICON__ -DNOMPI'

        cflags = include + ' ' + libs + ' ' + flags
        env.set('CFLAGS', cflags)

        cxxflags = include 
        cxxflags += '-Wunused -DNOMPI'
        env.set('CXXLAGS', cxxflags)

        fcflags = include 
        fcflags += ' -O2 -g -cpp -Wunused -DNOMPI'
        env.set('FCFLAGS', fcflags)

        ldflags = libs
        env.set('LDFLAGS', ldflags)

        libs_env = ''

        #libs_env += ' -L{}/lib -lnetcdf '.format(self.spec['netcdf-c'].prefix)
        #libs_env += ' -L{}/lib -lnetcdff'.format(self.spec['netcdf-fortran'].prefix)

        libs_env += ' -L{}/CRAYCLANG/9.0/lib -lnetcdf '.format(self.spec['netcdf-c'].prefix)
        libs_env += ' -L{}/CRAYCLANG/9.0/lib -lnetcdff'.format(self.spec['netcdf-fortran'].prefix)

        if '~eccodes' in self.spec:
            libs_env += ' -lgrib_api  -lgrib_api_f90'
        else:
            libs_env += ' -leccodes -leccodes_f90'
        
        # needs to be after griblibs, otherwise linking error during configure
        libs_env += ' -ljasper'

        env.set('LIBS', libs_env)

        # Daint specific flags to cache
        env.set('acx_cv_fc_ftn_include_flag', '-I')
        env.set('acx_cv_fc_pp_include_flag', '-I')
