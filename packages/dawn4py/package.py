# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import sys

class Dawn4py(PythonPackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage = 'https://github.com/MeteoSwiss-APN/dawn'
    url      = "https://github.com/MeteoSwiss-APN/dawn/archive/0.0.1.tar.gz"
    git      = 'https://github.com/MeteoSwiss-APN/dawn'
    maintainers = ['cosunae']

    version('master', branch='master')

    depends_on('cmake')
    extends('python@3.8.0', type=('build','run'))

    build_directory = 'dawn'
    phases = ['build', 'install']

    depends_on('py-setuptools', type='build')
    depends_on('py-protobuf', type=('build','run'))
