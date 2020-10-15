# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Eckit(CMakePackage):
    """ecKit is a cross-platform c++ toolkit that supports development 
    of tools and applications at ECMWF"""

    homepage = 'https://software.ecmwf.int/wiki/display/ECKIT'
    url = "https://github.com/ecmwf/eckit/archive/1.13.0.tar.gz"
    git = 'https://github.com/ecmwf/eckit.git'
    maintainers = ['cosunae']

    version('1.13.0', sha256='90f809c66c7eef5045cce1dc2f50304541c1d7f5270d80a4483f79591eda90aa')
    version('master', branch='master')
    version('develop', branch='develop')

    depends_on('ecbuild@master', when='@develop')
    depends_on('ecbuild@master', when='@master')
    depends_on('ecbuild@3.4.0', when='@1.13.0')

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DCMAKE_MODULE_PATH={0}/share/ecbuild/cmake'.
                    format(spec['ecbuild'].prefix))
        args.append('-DENABLE_MPI=OFF')

        return args
