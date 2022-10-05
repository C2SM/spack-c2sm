# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Fckit(CMakePackage):

    git = 'https://github.com/ecmwf/fckit.git'

    version('develop', branch='develop')

    maintainers = ['juckerj']

    depends_on('ecbuild')

    def cmake_args(self):
        args = [
            self.define('ecbuild_ROOT',self.spec["ecbuild"].prefix)
            ]
        return args
