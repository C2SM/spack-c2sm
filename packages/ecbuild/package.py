# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Ecbuild(CMakePackage):
    """A CMake-based build system, consisting of a collection of CMake macros and functions 
    that ease the managing of software build systems"""

    homepage = 'https://github.com/ecmwf/ecbuild.git'
    url      = "https://github.com/ecmwf/ecbuild/archive/3.4.0.tar.gz"
    git      = 'https://github.com/ecmwf/ecbuild.git'
    maintainers = ['cosunae']

    version('master', branch='master')
    version('3.4.0', sha256='dd17ae9128d7d158abbdd38f7fcea36a55cb45b29d3a6cd66d444c8d85afe6f8')

