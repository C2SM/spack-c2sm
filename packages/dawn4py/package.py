# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Dawn4py(PythonPackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage = 'https://github.com/MeteoSwiss-APN/dawn'
    url = "https://github.com/MeteoSwiss-APN/dawn/archive/0.0.1.tar.gz"
    git = 'https://github.com/MeteoSwiss-APN/dawn'
    maintainers = ['cosunae']

    version('master', branch='master')

    build_directory = 'dawn'

    extends('python@3.8.0:3.8.999')

    depends_on('cmake', type='build')
    depends_on('llvm@10.0.0')
    depends_on('py-setuptools', type='build')
    depends_on('py-protobuf', type=('build', 'run'))
    depends_on('py-attrs', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('py-black', type=('build', 'run'))

    # will test that dawn4py is importable after the install
    import_modules = ['dawn4py']

    def setup_build_environment(self, env):
        env.set('LLVM_ROOT', self.spec['llvm'].prefix)
