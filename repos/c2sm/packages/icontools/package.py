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

    homepage = 'https://c2sm.github.io/tools/icontools.html'
    c2sm = 'git@github.com:C2SM/icontools.git'
    dkrz = 'git@gitlab.dkrz.de:dwd-sw/dwd_icon_tools.git'

    maintainers = ['jonasjucker']

    version('c2sm-master', git=c2sm, branch='master', submodules=True)
    version('dkrz-master', git=dkrz, branch='master', submodules=True)
    version('2.5.2', git=dkrz, tag='icontools-2.5.2', submodules=True)

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    depends_on('netcdf-fortran', type=('build', 'link'))
    depends_on('netcdf-c ~mpi', type=('build', 'link'))
    depends_on('hdf5 ~mpi +hl', type=('build', 'link'))
    depends_on(
        'mpi',
        type=('build', 'link', 'run'),
    )
    depends_on('eccodes@2.19.0 +fortran ~aec', type=('build', 'link', 'run'))
    depends_on('jasper@1.900.1', type=('build', 'link'))

    variant('slave',
            default='none',
            description='Build on described slave (e.g daint)')
    variant('slurm_account',
            default='g110',
            description=
            'Slurm account used for mandatory testing during installation')

    conflicts('%pgi')
    conflicts('%nvhpc')
    conflicts('%cce')

    def configure_args(self):
        args = []
        args.append('acx_cv_fc_ftn_include_flag=-I')
        args.append('acx_cv_fc_pp_include_flag=-I')
        args.append('--disable-silent-rules')
        args.append('--disable-shared')
        args.append('--with-netcdf={0}'.format(
            self.spec['netcdf-fortran'].prefix))
        args.append('--enable-iso-c-interface')
        args.append('--enable-grib2')
        args.append('--with-eccodes={0}'.format(self.spec['eccodes'].prefix))

        return args

    def setup_build_environment(self, env):
        # Daint specific flags since cray-modules setting not recognized
        if self.spec.variants['slave'].value == 'daint':
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
        env.append_flags('LIBS', '-leccodes')
        env.append_flags('LIBS', '-leccodes_f90')

        # jasper needs to be after eccodes, otherwise linking error
        env.append_flags('LIBS', '-ljasper')

        env.append_flags('LIBS', '-lgfortran')

    def check(self):

        # only c2sm-versions have script for CSCS
        if self.spec.version in (Version('c2sm-master'), ):

            if self.spec.variants['slave'].value == 'daint':
                test_process = subprocess.run([
                    'sbatch', '-W', '--time=00:15:00', '-A',
                    self.spec.variants['slurm_account'].value, '-C', 'gpu',
                    '-p', 'normal', './C2SM/test/jenkins/test.sh'
                ],
                                              stderr=subprocess.STDOUT)

            if self.spec.variants['slave'].value == 'tsa':
                test_process = subprocess.run([
                    'sbatch', '-W', '--time=00:15:00', '-p', 'debug',
                    './C2SM/test/jenkins/test.sh'
                ],
                                              stderr=subprocess.STDOUT)
            if test_process.returncode != 0:
                cat_submit_process = subprocess.run(['cat', 'job.out'],
                                                    stderr=subprocess.STDOUT,
                                                    check=True)
                raise InstallError('Tests for Icontools failed')
            else:
                cat_submit_process = subprocess.run(['cat', 'job.out'],
                                                    stderr=subprocess.STDOUT,
                                                    check=True)
        else:
            print("\033[92m" + "==> " + "\033[0m" +
                  "icontools: No tests available for version {}".format(
                      self.spec.version))
