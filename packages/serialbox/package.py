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
    url      = "https://github.com/GridTools/serialbox/archive/v2.6.0.tar.gz"
    git      = "https://github.com/GridTools/serialbox.git"

    maintainers = ['elsagermann']

    version('master', branch='master')
    version('2.6.0', commit='eed195c47ab771c1682121ccbc89d2a556cdcb86')
    version('2.5.4', commit='26de94919c1b405b5900df5825791be4fa703ec0')
    version('2.4.3', commit='f15bd29db2e75d4e775bd133400bab33df55856b')

    depends_on('boost@1.67.0%gcc')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('netcdf-cxx4', when='+netcdf')

    variant('build_type', default='Release', description='Build type', values=('Debug', 'Release', 'DebugRelease'))
    variant('fortran', default=True, description='Build the C interface of Serialbox (libSerialboxFortran)')
    variant('shared', default=True, description='Build shared libraries of Serialbox')
    variant('exp_filesystem', default=True, description='Build with experimental filesystem')
    variant('ftg', default=True, description='Build with ftg')
    variant('no_pckg_registery', default=True, description='Build with Cmake export no package registey')
    variant('testing_gridtools', default=False, description='Build with testing gridtools')
    variant('testing_fortran', default=False, description='Build with testing fortran')
    variant('testing_stella', default=False, description='Build with testing stella')
    variant('netcdf', default=False, description='Build using netcdf')
    variant('boost_sys_paths', default=True, description='Build boost with no system paths')
    variant('boost_cmake', default=True, description='Build boost without using CMake')
    variant('python', default=True, description='Build Python3 interface of SerialboxBuild')
    variant('sdb', default=True, description='Build stencil debugger sdb')

    def cmake_args(self):
        args = []
        
        args.append('-DCMAKE_C_COMPILER=gcc')
        args.append('-DCMAKE_CXX_COMPILER=g++')
        args.append('-DCMAKE_BUILD_TYPE={0}'.format(self.spec.variants['build_type'].value))
        args.append('-DBOOST_ROOT={0}'.format(self.spec['boost'].prefix))

        if '+boost_sys_paths' in self.spec:
            args.append('-DBoost_NO_SYSTEM_PATHS=ON')
        else:
            args.append('-DBoost_NO_SYSTEM_PATHS=OFF')
        if '+boost_cmake' in self.spec:
            args.append('-DBoost_NO_BOOST_CMAKE=ON')
        else:
            args.append('-DBoost_NO_BOOST_CMAKE=OFF')
        if '+netcdf' in self.spec:
            args.append('-DSERIALBOX_USE_NETCDF=ON')
        else:
            args.append('-DSERIALBOX_USE_NETCDF=OFF')
        if '+testing_gridtools' in self.spec:
            args.append('-DSERIALBOX_TESTING_GRIDTOOLS=ON')
        else:
            args.append('-DSERIALBOX_TESTING_GRIDTOOLS=OFF')
        if '+testing_stella' in self.spec:
            args.append('-DSERIALBOX_TESTING_STELLA=ON')
        else:
            args.append('-DSERIALBOX_TESTING_STELLA=OFF')
        if '+testing_stella' in self.spec:
            args.append('-DSERIALBOX_TESTING_FORTRAN=ON')
        else:
            args.append('-DSERIALBOX_TESTING_FORTRAN=OFF')
        if '+no_pckg_registery' in self.spec:
            args.append('-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON')
        else:
            args.append('-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=OFF')
        if '+ftg' in self.spec:
            args.append('-DSERIALBOX_ENABLE_FTG=ON')
        else:
            args.append('-DSERIALBOX_ENABLE_FTG=OFF')
        if '+exp_filesystem' in self.spec:
            args.append('-DSERIALBOX_ENABLE_EXPERIMENTAL_FILESYSTEM=ON')
        else:
            args.append('-DSERIALBOX_ENABLE_EXPERIMENTAL_FILESYSTEM=OFF')
        if '+fortran' in self.spec:
            args.append('-DSERIALBOX_ENABLE_FORTRAN=ON')
        else:
            args.append('-DSERIALBOX_ENABLE_FORTRAN=OFF')
        if '+shared' in self.spec:
            args.append('-DSERIALBOX_BUILD_SHARED=ON')
        else:
            args.append('-DSERIALBOX_BUILD_SHARED=OFF')
        if '~python' in self.spec:
            args.append('-DSERIALBOX_ENABLE_PYTHON=OFF')
        if '~sdb' in self.spec:
            args.append('-DSERIALBOX_ENABLE_SDB=OFF')

        return args
