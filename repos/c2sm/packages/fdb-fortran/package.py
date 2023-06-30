from spack import *
from distutils.dir_util import copy_tree


class FdbFortran(CMakePackage):
    homepage = 'https://github.com/MeteoSwiss/fdb-fortran'
    git = 'https://github.com/MeteoSwiss/fdb-fortran.git'

    version('0.1.0', , tag='0.1.0')

    depends_on('cmake@3.10:', type='build')
    depends_on('fdb')


def cmake_args(self):
    args = [
        self.define('Deckit_DIR', self.spec['eckit'].prefix),
        self.define('Dmetkit_DIR', self.spec['metkit'].prefix),
        self.define('Deccodes_DIR', self.spec['eccodes'].prefix),
        self.define('Dfdb5_DIR', self.spec['fdb'].prefix),
    ]
    return args