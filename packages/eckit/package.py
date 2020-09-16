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
    url = "https://github.com/ecmwf/eckit/archive/1.10.1.tar.gz"
    git = 'https://github.com/ecmwf/eckit.git'
    maintainers = ['cosunae']

    version('master', branch='master')
    version('develop', branch='develop')

    depends_on('ecbuild')

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DCMAKE_MODULE_PATH={0}/share/ecbuild/cmake'.
                    format(spec['ecbuild'].prefix))
        args.append('-DENABLE_MPI=OFF')

        return args
