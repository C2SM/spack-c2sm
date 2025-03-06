# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
from collections import defaultdict

from spack.util.environment import is_system_path
from llnl.util import tty


class Icontools(AutotoolsPackage):
    """A set of routines which may be suitable for reading, remapping and
    writing of fields from and to predefined grids, e.g. regular (lat-lon,
    gaussian) or triangular (ICON)."""

    homepage = 'https://gitlab.dkrz.de/dwd-sw/dwd_icon_tools'
    url = 'https://gitlab.dkrz.de/dwd-sw/dwd_icon_tools'
    dkrz = 'git@gitlab.dkrz.de:dwd-sw/dwd_icon_tools.git'
    c2sm = 'git@github.com:C2SM/icontools.git'

    version('c2sm-master', git=c2sm, branch='master', submodules=True)
    version('dkrz-master', git=dkrz, branch='master', submodules=True)
    version('2.5.2', git=dkrz, tag='icontools-2.5.2', submodules=True)

    variant('mpi', default=True, description='enable MPI support')
    variant('grib2', default=True, description='enable GRIB2 support')
    variant('szip',
            default=True,
            description='enable szip compression for GRIB1')

    depends_on('python', type='build')

    depends_on('netcdf-fortran')
    depends_on('netcdf-c')
    depends_on('hdf5')
    depends_on('eccodes')

    depends_on('mpi', when='+mpi')
    depends_on('eccodes', when='+grib2')
    depends_on('szip', when='+szip')

    # There are currently several issues related to NAG:
    #   1. File libicontools/src/libicontools/mo_util_nml.f90 is empty after
    #      preprocessing.
    #   2. Error: libiconremap/mo_rbfqr_math.f90, line 934: KIND value (8) does
    #      not specify a valid representation method.
    #   3. It's yet unclear what additional flags g++ needs to link
    #      OpenMP-enabled Fortran code compiled with NAG.
    #   4. It's yet unclear what additional NAG runtime libraries we need to
    #      link to.
    conflicts('%nag')

    # There is currently an issue related to PGI:
    #   PGF90-S-0081-Illegal selector - KIND value must be non-negative
    #     (libiconbase/mo_delaunay_types.f90: 332)
    conflicts('%pgi')
    conflicts('%nvhpc')

    def flag_handler(self, name, flags):
        if name == 'cflags' or name == 'cxxflags':
            # Set OpenMP flags:
            flags.append(self.compiler.openmp_flag
                         # We assume that NAG is mixed with GCC:
                         if self.compiler.name != 'nag' else '-fopenmp')
        elif name == 'fflags':
            # Enable building with 'gcc@10:':
            if self.spec.satisfies('%gcc@10:'):
                flags.append('-fallow-argument-mismatch')
            # Set OpenMP flags:
            flags.append(self.compiler.openmp_flag)
            # Disable MPI support:
            if '~mpi' in self.spec:
                flags.append('-DNOMPI')
        elif name == 'cppflags':
            # Disable MPI support:
            if '~mpi' in self.spec:
                flags.append('-DNOMPI')

        return flags, None, None

    def configure_args(self):
        args = [
            # Get verbose output in the logs:
            '--disable-silent-rules',
            # Do not trigger regeneration of the source files:
            '--disable-maintainer-mode',
            # Simplify linking of the bundled libraries:
            '--enable-static',
            '--disable-shared',
            # Tune CDI:
            '--disable-cdi-app',
            '--disable-cf-interface',
            '--disable-extra',
            '--disable-ieg',
            '--disable-service',
            '--enable-cgribex',
            '--enable-grib',
            '--enable-iso-c-interface',
            '--disable-util-linux-uuid',
            '--disable-ossp-uuid',
            '--disable-dce-uuid',
            '--without-grib_api',
            '--without-threads',
            # Do not install CDI:
            'CDO_DISABLE_CDILIB=1',
            # There is only one argument for netcdf-c and netcdf-fortran but
            # we specify path to netcdf-c here to make CDI happy (we also have
            # to provide the prefix regardless of whether it is in the system
            # path because the configure script of icontools fails otherwise):
            '--with-netcdf={0}'.format(self.spec['netcdf-c'].prefix)
        ]

        flags = defaultdict(list)

        def help_libtool(spec):
            # Help libtool to find the right library in case it is installed to
            # a non-system directory by extending LDFLAGS.
            if not is_system_path(spec.prefix):
                flags['LDFLAGS'].append(spec.libs.search_flags)

        # Help the libtool script of CDI to find the right HDF5 library:
        hdf5_spec = self.spec['hdf5']
        help_libtool(hdf5_spec)
        # The package links directly to libcdi.a giving Libtool no chance to
        # figure out that it should link to libhdf5:
        flags['LIBS'].append(hdf5_spec.libs.link_flags)

        if '+szip' in self.spec:
            args.append('--with-szlib')
            szip_spec = self.spec['szip']
            help_libtool(szip_spec)
            # The package links directly to libcdi.a giving Libtool no chance to
            # figure out that it should link to libsz:
            flags['LIBS'].append(szip_spec.libs.link_flags)
        else:
            args.append('--without-szlib')

        if '+grib2' in self.spec:
            args.append('--with-eccodes')
            eccodes_spec = self.spec['eccodes']
            help_libtool(eccodes_spec)
            # The package links directly to libcdi.a giving Libtool no chance to
            # figure out that it should link to libeccodes:
            flags['LIBS'].append(eccodes_spec.libs.link_flags)
        else:
            args.append('--without-eccodes')
        args.append('--without-grib_api')

        if '+mpi' in self.spec:
            mpi_spec = self.spec['mpi']
            args.extend(['FC=' + mpi_spec.mpifc, 'CXX=' + mpi_spec.mpicxx])

            # We need to link C++ programs to Fortran MPI libraries:
            mpifc_libs = None
            try:
                mpifc_exe = Executable(mpi_spec.mpifc)
                mpifc_libs = ' '.join(
                    re.findall(
                        r'\s(-l\s*[^\s]+)',
                        mpifc_exe('-show', output=str, error=os.devnull)))
            except ProcessError:

                def find_mpi_fc_link_flags(*libnames):
                    for shared in [True, False]:
                        libraries = find_libraries(libnames,
                                                   mpi_spec.prefix,
                                                   shared=shared,
                                                   recursive=True)
                        if libraries:
                            return libraries.link_flags
                    return None

                if mpi_spec.name.endswith('mpich'):
                    # Check for the new name of the library (in this case,
                    # libmpichf90 is just a symlink, which we do not want to
                    # overlink to):
                    mpifc_libs = find_mpi_fc_link_flags('libmpifort')
                    if not mpifc_libs:
                        # Check for the old name of the library (this is
                        # usually the case on Cray platforms):
                        mpifc_libs = find_mpi_fc_link_flags('libmpichf90')
                elif mpi_spec.name == 'openmpi':
                    mpifc_libs = find_mpi_fc_link_flags(
                        'lib*_usempif08', 'lib*_usempi_ignore_tkr',
                        'lib*_usempi', 'lib*_mpifh')

            if mpifc_libs:
                flags['LIBS'].append(mpifc_libs)
            else:
                tty.warn('unable to detect Fortran MPI libraries')

        # We need to link C++ programs to Fortran runtime libraries:
        if self.compiler.name == 'gcc':
            flags['LIBS'].append('-lgfortran')
        elif self.compiler.name == 'intel':
            flags['LIBS'].append('-lifcore')
        elif self.compiler.name == 'pgi':
            flags['LIBS'].append('-pgf90libs')
        else:
            tty.warn('unable to detect Fortran runtime libraries')

        args.extend([
            '{0}={1}'.format(var, ' '.join(val)) for var, val in flags.items()
        ])

        return args
