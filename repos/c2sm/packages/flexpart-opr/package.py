# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class FlexpartOpr(Package):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/MeteoSwiss-APN/flexpart-opr'
    git = 'git@github.com:MeteoSwiss-APN/flexpart-opr.git'

    version('fdb', branch='fdb')

    def install(self, spec, prefix):
        mkdir(prefix.flexpartOpr)
        mkdir(prefix.flexpartOpr + '/options')
        mkdir(prefix.flexpartOpr + '/src')
        install_tree('options', prefix.flexpartOpr + '/options')
        install_tree('src', prefix.flexpartOpr + '/src')