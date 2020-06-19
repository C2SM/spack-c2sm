# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import sys

class IconduskE2e(CMakePackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage = 'https://github.com/dawn-ico/icondusk-e2e'
    git      = 'git@github.com:dawn-ico/icondusk-e2e.git'
    maintainers = ['cosunae']

    version('master', branch='master')

    depends_on('atlas_utilities', type=('build','run'))
    depends_on('dawn4py',  type=('build','run'))
    depends_on('python@3.8.0')
    depends_on('atlas')
    depends_on('cuda', type=('build', 'run'))

    variant('build_type', default='Release', description='Build type', values=('Debug', 'Release', 'DebugRelease'))
    variant('precision', default='double', values=('double','float'))

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append('-DCMAKE_BUILD_TYPE={0}'.format(self.spec.variants['build_type'].value))
        args.append('-DPython3_EXECUTABLE=' + spec['python'].prefix +'/bin/python3.8')
        args.append('-Datlas_utils_ROOT='+spec['atlas_utilities'].prefix)
        args.append('-Ddawn4py_DIR='+spec['dawn4py'].prefix)
        args.append('-Datlas_DIR='+spec['atlas'].prefix)
        args.append('-DPRECISION='+spec.variants['precision'].value)

        return args

