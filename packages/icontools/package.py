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


class Icontools(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git = 'git@github.com:C2SM-ICON/dwd_icon_tools.git'

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions here.
    version('master', branch='master')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4', type='build')

    depends_on('netcdf-fortran +mpi', type=('build', 'link'))
    depends_on('netcdf-c +mpi', type=('build', 'link'))
    depends_on('mpi', type=('build', 'link', 'run'),)
    depends_on('eccodes ~aec', type=('build', 'link', 'run'))
    #depends_on('cosmo-grib-api-definitions', type=('build','link','run'))
    depends_on('hdf5', type=('build','link'))
    depends_on('jasper@1.900.1%gcc ~shared', type=('build','link'))

    def configure_args(self):
        args =['--disable-silent-rules',
               '--disable-shared',
               '--with-netcdf={0}'.format(self.spec['netcdf-fortran'].prefix),
               '--enable-iso-c-interface',
               '--with-eccodes={0}'.format(self.spec['eccodes'].prefix),
               '--enable-grib2',
                ]
        return args

    def setup_build_environment(self, env):
        self.setup_run_environment(env)

        cray_include =' -I{}/include'.format(self.spec['netcdf-fortran'].prefix)
        cray_include +=' -I{}/include'.format(self.spec['netcdf-c'].prefix)
        #cray_include +=' -I{}/include'.format(self.spec['cosmo-grib-api-definitions'].prefix)
        cray_include +=' -I{}/include'.format(self.spec['eccodes'].prefix)
        cray_include +=' -I{}/include'.format(self.spec['mpi'].prefix)
        cray_include +=' -I{}/include'.format(self.spec['jasper'].prefix)

        cray_libs =' -L{}/lib -lnetcdff'.format(self.spec['netcdf-fortran'].prefix)
        cray_libs +=' -L{}/lib -lnetcdf '.format(self.spec['netcdf-c'].prefix)
        cray_libs +=' -L{}/lib64 -leccodes -leccodes_f90'.format(self.spec['eccodes'].prefix)
        cray_libs +=' -L{}/lib64 -ljasper'.format(self.spec['jasper'].prefix)
        cray_libs +=' -L{}/lib '.format(self.spec['mpi'].prefix)
        cray_libs +=' -L{}/lib '.format(self.spec['hdf5'].prefix)
        #cray_libs +=' -L{}/lib  -lgrib_api_f90 -lgrib_api'.format(self.spec['cosmo-grib-api-definitions'].prefix)

        flags = ' -O2 -g -Wunused  -DHAVE_LIBNETCDF -DHAVE_NETCDF4 -DHAVE_CF_INTERFACE -DHAVE_LIBGRIB -DHAVE_LIBGRIB_API -D__ICON__ -DNOMPI'
        #flags = ' -O2 -g -Wunused  -DHAVE_LIBNETCDF -DHAVE_NETCDF4 -DHAVE_CF_INTERFACE -DHAVE_LIBGRIB -D__ICON__ -DNOMPI'

        cflags = cray_include + cray_libs
        cflags += flags
        env.set('CFLAGS', cflags)

        cxxflags = cray_include + cray_libs
        cxxflags += '-Wunused -DNOMPI'
        env.set('CXXLAGS', cxxflags)

        fcflags = cray_include + cray_libs
        fcflags += ' -O2 -g -cpp -Wunused -DNOMPI'
        env.set('FCFLAGS', fcflags)

        libs = '-lnetcdf -leccodes -leccodes_f90 -ljasper -lhdf5'
        env.set('LIBS', libs)

        ldflags = cray_libs
        env.set('LDFLAGS', ldflags)

        env.set('acx_cv_fc_ftn_include_flag', '-I')
        env.set('acx_cv_fc_pp_include_flag', '-I')
