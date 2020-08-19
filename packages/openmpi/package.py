# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import itertools
import os
import sys
import llnl.util.tty as tty
from spack.pkg.builtin.openmpi import Openmpi

class Openmpi(Openmpi):

    provides('mpicuda', when='+cuda')
    
    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        env.set('UCX_MEMTYPE_CACHE', 'n')
        if '+cuda' in self.spec:
            env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cuda_copy,cuda_ipc,cma')
        else:
            env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cma')
