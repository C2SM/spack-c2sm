##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import subprocess, re

class Mlir(CMakePackage):
    """Build for MLIR with llvm"""
    
    homepage = "https://github.com/llvm/llvm-project.git"
    git      = "git@github.com:llvm/llvm-project.git"
    maintainers = ['cosunae']
    
    version('master', branch='master')
    version('dawn', commit='10643c9ad85')

    depends_on('cmake@3.12:%gcc', type='build')
    depends_on('cuda', when='+cuda', type=('build', 'run'))

    root_cmakelists_dir='llvm'
    
    def cmake_args(self):
      spec = self.spec

      args = []
      args.append("-DLLVM_BUILD_EXAMPLES=OFF")
      args.append("-DLLVM_TARGETS_TO_BUILD=host;NVPTX;AMDGPU")
      args.append("-DLLVM_ENABLE_PROJECTS=mlir;lld")
      args.append("-DLLVM_OPTIMIZED_TABLEGEN=ON")
      args.append("-DLLVM_ENABLE_OCAMLDOC=OFF")
      args.append("-DLLVM_ENABLE_BINDINGS=OFF")
      args.append("-DLLVM_INSTALL_UTILS=ON")
      args.append("-DMLIR_CUDA_RUNNER_ENABLED=ON")
      
      return args
