# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Fckit(CMakePackage):
    '''
    Fortran toolkit for interoperating Fortran with C/C++.
    In addition useful algorithms from ecKit are wrapped with Fortran.
    '''

    homepage = 'https://github.com/ecmwf/fckit.git'
    git = 'https://github.com/ecmwf/fckit.git'

    version('0.9.0', tag='0.9.0')
    version('develop', branch='develop')

    maintainers = ['juckerj']

    depends_on('ecbuild', type=('build'))

    def cmake_args(self):
        args = [self.define('ecbuild_ROOT', self.spec["ecbuild"].prefix)]
        return args
