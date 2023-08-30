# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PytorchFortran(CMakePackage):
    '''
    Pytorch Fortran bindings - Fortran Frontend

    The goal of this code is to provide Fortran HPC codes with a simple way to use 
    Pytorch deep learning framework. We want Fortran developers to take advantage 
    of rich and optimized Torch ecosystem from within their existing codes.
    ''' 

    homepage = "https://github.com/alexeedm/pytorch-fortran"
    url = "https://github.com/alexeedm/pytorch-fortran.git"

    version('0.4', git=url, tag='v0.4')

    maintainers = ['juckerj']

    depends_on('pytorch-fortran-proxy')

    root_cmakelists_dir = 'src/f90_bindings'

    def cmake_args(self):
        args = [self.define('OPENACC', 1)]

        return args
