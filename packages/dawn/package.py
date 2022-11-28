# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Dawn(CMakePackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage = 'https://github.com/MeteoSwiss-APN/dawn'
    url = "https://github.com/MeteoSwiss-APN/dawn/archive/0.0.1.tar.gz"
    git = 'https://github.com/MeteoSwiss-APN/dawn'
    maintainers = ['cosunae']

    version('master', branch='master')

    depends_on('cmake')
    depends_on('llvm@10.0.0 +clang')
    depends_on('python@3.8.0:3.8.999')
    depends_on('py-setuptools', type='build')
    depends_on('py-protobuf', type=('build', 'run'))

    variant('build_type',
            default='Release',
            description='Build type',
            values=('Debug', 'Release', 'DebugRelease'))
    root_cmakelists_dir = 'dawn'

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DCMAKE_BUILD_TYPE={0}'.format(
            self.spec.variants['build_type'].value))
        args.append('-DPython3_EXECUTABLE=' + spec['python'].prefix +
                    '/bin/python3.8')
        args.append('-DLLVM_ROOT=' + spec['llvm'].prefix)
        args.append('-DDAWN_REQUIRE_PYTHON=ON')
        return args
