# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class FlexpartOpr(Package):
    """MeteoSwiss' addition to Flexpart."""

    homepage = 'https://github.com/MeteoSwiss-APN/flexpart-opr'
    git = 'git@github.com:MeteoSwiss-APN/flexpart-opr.git'

    version('main', branch='main', preferred=True)
    version('fdb', branch='fdb')

    def install(self, spec, prefix):
        mkdir(prefix.flexpartOpr)
        mkdir(prefix.flexpartOpr + '/options')
        mkdir(prefix.flexpartOpr + '/src')
        mkdir(prefix.flexpartOpr + '/test')
        install_tree('options', prefix.flexpartOpr + '/options')
        install_tree('src', prefix.flexpartOpr + '/src')
        install_tree('test', prefix.flexpartOpr + '/test')
