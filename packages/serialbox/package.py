# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install serialbox
#
# You can edit this file again by typing:
#
#     spack edit serialbox
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Serialbox(CMakePackage):
    """Serialbox is part of the GridTools Framework. Serialbox is a serialization library and tools for C/C++, Python3 and Fortran."""
    homepage = "https://github.com/GridTools/serialbox"
    git      = "git@github.com:GridTools/serialbox.git"

    maintainers = ['elsagermann']

    version('master', branch='master')
    version('2.6.0', commit='eed195c47ab771c1682121ccbc89d2a556cdcb86')
    version('2.5.4', commit='26de94919c1b405b5900df5825791be4fa703ec0')
    version('2.4.3', commit='f15bd29db2e75d4e775bd133400bab33df55856b')

    depends_on('boost@1.67.0%gcc')

    variant('build_type', default='Release', description='Build type', values=('Debug', 'Release', 'DebugRelease'))
    variant('fortran', default=True, description='Build the C interface of Serialbox (libSerialboxFortran)')
    variant('shared', default=True, description='Build shared libraries of Serialbox')
    
    def cmake_args(self):
        args = []
        
        args.append('-DBOOST_ROOT={0}'.format(self.spec['boost'].prefix))
        args.append('-DBoost_NO_SYSTEM_PATHS=ON')
        args.append('-DCMAKE_BUILD_TYPE={0}'.format(self.spec.variants['build_type'].value))
        args.append('-DSERIALBOX_ENABLE_EXPERIMENTAL_FILESYSTEM=ON')
        args.append('-DSERIALBOX_ENABLE_FTG=ON')
        args.append('-DBoost_NO_BOOST_CMAKE=ON')
        args.append('-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON')
        args.append('-DSERIALBOX_USE_NETCDF=OFF')
        args.append('-DSERIALBOX_TESTING_GRIDTOOLS=OFF')
        args.append('-DSERIALBOX_TESTING_STELLA=OFF')
        args.append('-DSERIALBOX_TESTING_FORTRAN=OFF')

        if '+fortran' in self.spec:
            args.append('-DSERIALBOX_ENABLE_FORTRAN=ON')
        if '+shared' in self.spec:
            args.append('-DSERIALBOX_BUILD_SHARED=ON')
        else:
            args.append('-DSERIALBOX_BUILD_SHARED=OFF')
        return args
