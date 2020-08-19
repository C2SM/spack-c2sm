# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob
from llnl.util.filesystem import LibraryList
import os
import platform
import llnl.util.tty as tty
from spack.pkg.builtin.cuda import Cuda

class Cuda(Cuda):

    def setup_run_environment(self, env):
       env.set('CUDA_HOME', self.prefix)
        env.append_path('CPATH', self.prefix + '/extras/CUPTI/include:' + self.prefix + '/nvvm/include')
        env.append_path('LD_LIBRARY_PATH', self.prefix + '/extras/CUPTI/lib64:/cm/local/apps/cuda/libs/current/lib64')
        env.append_path('LIBRARY_PATH', self.prefix + '/lib64/stubs')
        env.append_path('PATH', self.prefix + ':' + self.prefix + '/nvvm/bin')
