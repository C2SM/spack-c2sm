# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import os


class PytorchFortran(CMakePackage):
    '''
    Infero runs a pre-trained ML model for inference. It can be deployed on a HPC system 
    without the need for high-level python libraries (e.g. TensorFlow, PyTorch, etc..)
    '''

    homepage = "https://github.com/alexeedm/pytorch-fortran"
    url = " https://github.com/alexeedm/pytorch-fortran.git"

    version('0.4',
            git=url,
            tag='v0.4')

    maintainers = ['juckerj']


    depends_on('cuda')
    depends_on('py-torch +cuda')

    def cmake_args(self):
        args = [
            self.define('OPENACC',1),
            self.define('ENABLE_TESTS', self.run_tests),
            self.define('CUDA_TOOLKIT_ROOT_DIR',self.spec['cuda'].prefix),
            self.define('TORCH_CUDA_ARCH_LIST',"6.0")]
