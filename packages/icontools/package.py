# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
#     spack install icontools
#
# You can edit this file again by typing:
#
#     spack edit icontools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import subprocess

class Icontools(AutotoolsPackage):
    """
    DWD ICON Tools for C2SM members. 
    Set of tools to prepare the input files 
    (for example the boundary condition, initial condition file,...) for ICON.
    """

    homepage= 'https://wiki.c2sm.ethz.ch/MODELS/ICONDwdIconTools'
    git = 'git@github.com:C2SM-ICON/dwd_icon_tools.git'

    maintainers = ['jonasjucker']

    version('master', branch='master')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4', type='build')

    depends_on('cray-libsci %cce', type=('build', 'link'))
    depends_on('netcdf-fortran %cce ~mpi', type=('build', 'link'))
    depends_on('netcdf-c %cce ~mpi', type=('build', 'link'))
    depends_on('mpi', type=('build', 'link', 'run'),)
    depends_on('eccodes ~aec', type=('build', 'link', 'run'))
    depends_on('cosmo-grib-api', type=('build','link','run'), when='~eccodes')
    depends_on('hdf5 ~mpi +hl', type=('build','link'))
    depends_on('jasper@1.900.1%gcc ~shared', type=('build','link'))

    variant('eccodes', default=True, description='Build with eccodes instead of grib-api')

    def configure_args(self):
        args =[]
        args.append('CC=cc')
        args.append('CXX=CC')
        args.append('FC=ftn')
        args.append('F77=ftn')
        args.append('acx_cv_fc_ftn_include_flag="-I"')
        args.append('acx_cv_fc_pp_include_flag="-I"')
        args.append('--disable-silent-rules')
        args.append('--disable-shared')
        args.append('--with-netcdf={0}'.format(self.spec['netcdf-fortran'].prefix))
        args.append('--enable-iso-c-interface')
        if '~eccodes' in self.spec:
            args.append('--with-grib_api={0}'.format(self.spec['cosmo-grib-api'].prefix))
        else:
            args.append('--enable-grib2')
            args.append('--with-eccodes={0}'.format(self.spec['eccodes'].prefix))

        return args

    def setup_build_environment(self, env):
        # Daint specific flags since cray-modules setting not recognized
        env.set('NETCDF_DIR', '{}'.format(self.spec['netcdf-c'].prefix))

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
        env.append_flags('LIBS', '-ljasper')
        env.append_flags('LIBS', '-lsci_cray')
        if '~eccodes' in self.spec:
            env.append_flags('LIBS', '-lgrib_api')
            env.append_flags('LIBS', '-lgrib_api_f90')
        else:
            env.append_flags('LIBS', '-leccodes')
            env.append_flags('LIBS', '-leccodes_f90')

    @run_after('build')
    def test(self):
            try:
                subprocess.run(['/bin/bash', 'C2SM-scripts/test/jenkins/test.sh'], stderr=subprocess.STDOUT, check=True)
            except:
                raise InstallError('Tests for Icontools failed')
