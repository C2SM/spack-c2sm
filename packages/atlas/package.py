# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Atlas(CMakePackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage = 'https://confluence.ecmwf.int/display/atlas'
    url = "https://github.com/ecmwf/atlas/archive/0.20.2.tar.gz"
    git = 'https://github.com/ecmwf/atlas.git'
    maintainers = ['cosunae']

    version('master', branch='master')
    version('develop', branch='develop')

    depends_on('ecbuild')
    depends_on('eckit@develop', when='@develop')
    depends_on('eckit@master', when='@master')

    # patch('patches/find.gtstorage.patch', when='@develop')
    # patch('patches/find.gtstorage.patch', when='@master')

    variant('build_type', default='Release', description='Build type',
            values=('Debug', 'Release', 'DebugRelease'))

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DCMAKE_MODULE_PATH={0}/share/ecbuild/cmake'.
                    format(spec['ecbuild'].prefix))
        args.append('-Deckit_DIR={0}'.format(spec['eckit'].prefix))
        args.append('-DENABLE_GRIDTOOLS_STORAGE=OFF')
        args.append(
            '-DCMAKE_BUILD_TYPE={0}'.format(self.spec.variants['build_type'].value))

        return args
