# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Infero(CMakePackage):
    '''
    Infero runs a pre-trained ML model for inference. It can be deployed on a HPC system 
    without the need for high-level python libraries (e.g. TensorFlow, PyTorch, etc..)
    '''

    git = "https://github.com/jonasjucker/infero.git"

    version('master', branch='ecrad')

    maintainers = ['juckerj']

    depends_on('eckit@1.20.0:')
    depends_on('fckit')
    depends_on('ecbuild',type('build'))
    depends_on('tensorflowc')


    def cmake_args(self):
        args = [
            self.define('CMAKE_PREFIX_PATH',f'{self.spec["ecbuild"].prefix}/share/ecbuild/cmake'),
            self.define('CMAKE_Fortran_MODULE_DIRECTORY',self.prefix.module),

            self.define('ENABLE_TESTS', self.run_tests),
            self.define('ENABLE_MPI',False),
            self.define('ENABLE_FCKIT',False),
            self.define('ENABLE_TENSORRT',False),
            self.define('ENABLE_ONNX',False),
            self.define('ENABLE_ONNX',False),

            self.define('ENABLE_FCKIT',True),
            self.define(f'FCKIT_ROOT',f'{self.spec["fckit"].prefix}'),

            self.define('ENABLE_TF_C',True),
            self.define(f'TENSORFLOWC_ROOT',f'{self.spec["tensorflowc"].prefix}')
            ]
        return args
