# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class DyiconBenchmarks(CMakePackage):
    """benchmarks for dynamical core of ICON"""

    homepage = 'https://github.com/cosunae/cuda_stencil'
    url      = "https://github.com/cosunae/cuda_stencil"
    git      = 'https://github.com/cosunae/cuda_stencil'
    maintainers = ['cosunae']

    version('master', branch='master')
    version('cmake', branch='cmake')
    depends_on('atlas_utilities')
    depends_on('atlas')
    depends_on('cuda')

    def cmake_args(self):
        args = []
        print("===========", self.spec['atlas_utilities'], self.spec['atlas_utilities'].prefix)
        spec = self.spec
        args.append('-Datlas_DIR={0}'.format(spec['atlas'].prefix))
        args.append('-Datlas_utils_DIR={0}'.format(spec['atlas_utilities'].prefix+'/lib/cmake'))
        args.append('-DCMAKE_CUDA_FLAGS=-L/apps/arolla/UES/jenkins/RH7.6/generic/easybuild/software/CUDA/10.1.243/lib64')
        return args

