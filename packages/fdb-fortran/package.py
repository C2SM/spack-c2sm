# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
from distutils.dir_util import copy_tree


class FdbFortran(CMakePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/MeteoSwiss/fdb-fortran'
    version('archive_retreive',
            git='https://github.com/MeteoSwiss/fdb-fortran.git',
            branch='archive_retreive')

    depends_on('cmake@3.10:', type=('build'))
    depends_on(
        'fdb@5.10.8 ^eckit@1.20.2: ^eccodes@2.19.0 ^metkit@1.9.2',
        type=('build', 'link'))


def cmake_args(self):
    args = [
        self.define('Deckit_DIR', self.spec['eckit'].prefix),
        self.define('Dmetkit_DIR', self.spec['metkit'].prefix),
        self.define('Deccodes_DIR', self.spec['eccodes'].prefix),
        self.define('Dfdb5_DIR', self.spec['fdb'].prefix),
    ]
    return args
