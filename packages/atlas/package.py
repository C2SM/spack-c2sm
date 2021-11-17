# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Atlas(CMakePackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage ='https://confluence.ecmwf.int/display/atlas'
    url = "https://github.com/ecmwf/atlas/archive/0.22.0.tar.gz"
    git = 'https://github.com/ecmwf/atlas.git'
    maintainers = ['cosunae']

    version('0.22.0', sha256='2f79de432238cfd3c3e6ad39e4f01e850dd0d37266b610f079fdbca0a71ce095')
    version('master', branch='master')
    version('develop', branch='develop')

    depends_on('ecbuild@master', when='@develop')
    depends_on('ecbuild@master', when='@master')
    depends_on('ecbuild@3.4.0', when='@0.22.0')
    depends_on('eckit@develop', when='@develop')
    depends_on('eckit@master', when='@master')
    depends_on('eckit@1.13.0', when='@0.22.0')

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
