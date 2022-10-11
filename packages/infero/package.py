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

    ecmwf = "https://github.com/ecmwf-projects/infero.git"

    version('0.1.2',
            git=ecmwf,
            commit='4c229a16ce75a249c83cbf43e0c953a7a42f2f83')

    maintainers = ['juckerj']

    variant('quiet', description='Disable calls to Log::info', default=False)

    depends_on('eckit@1.20.0:')
    depends_on('fckit')
    depends_on('ecbuild', type=('build'))
    depends_on('tensorflowc')

    patch('comment_out_log-level_info.patch', when='@0.1.2 +quiet')

    conflicts('%nvhpc', msg='Some unittests fail for nvhpc -> please use gcc')

    def flag_handler(self, name, flags):
        cmake_flags = []

        if self.compiler.name == 'nvhpc' and name in ['cflags', 'cxxflags']:
            cmake_flags.append('-D__GCC_ATOMIC_TEST_AND_SET_TRUEVAL=1')
            cmake_flags.append('-D__BYTE_ORDER__')
            cmake_flags.append('-D__ORDER_LITTLE_ENDIAN__')
            cmake_flags.append('-D__BYTE_ORDER__=__ORDER_LITTLE_ENDIAN__')

        return flags, None, (cmake_flags or None)

    def cmake_args(self):
        args = [
            self.define('CMAKE_PREFIX_PATH',
                        f'{self.spec["ecbuild"].prefix}/share/ecbuild/cmake'),
            self.define('CMAKE_Fortran_MODULE_DIRECTORY', self.prefix.module),
            self.define('ENABLE_TESTS', self.run_tests),
            self.define('ENABLE_MPI', False),
            self.define('ENABLE_FCKIT', False),
            self.define('ENABLE_TENSORRT', False),
            self.define('ENABLE_ONNX', False),
            self.define('ENABLE_ONNX', False),
            self.define('ENABLE_FCKIT', True),

            # enable Fortran interfaces
            self.define(f'FCKIT_ROOT', f'{self.spec["fckit"].prefix}'),

            # enable TF-C backend
            self.define('ENABLE_TF_C', True),
            self.define(f'TENSORFLOWC_ROOT',
                        f'{self.spec["tensorflowc"].prefix}')
        ]
        return args
