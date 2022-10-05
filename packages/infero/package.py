# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Infero(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    git = "https://github.com/jonasjucker/infero.git"

    version('master', branch='ecrad')

    maintainers = ['juckerj']

    depends_on('eckit@1.20.0:')
    depends_on('fckit@1.20.0:')
    depends_on('ecbuild')
    depends_on('libtensorflow')

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
            self.define(f'FCKIT_ROOT', f'{self.spec["fckit"].prefix}'),
            self.define('ENABLE_TF_C', True),
            self.define(f'TENSORFLOWC_ROOT',
                        f'{self.spec["libtensorflow"].prefix}')
        ]
        return args
