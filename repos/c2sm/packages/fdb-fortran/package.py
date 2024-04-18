from spack import *
from distutils.dir_util import copy_tree


class FdbFortran(CMakePackage):
    """An experimental Fortran interface to ECMWF's FDB (Fields DataBase)."""

    homepage = 'https://github.com/MeteoSwiss/fdb-fortran'
    git = 'https://github.com/MeteoSwiss/fdb-fortran.git'
    maintainers = ['victoria-cherkas']

    version('0.1.0', tag='0.1.0')

    depends_on('cmake@3.10:', type='build')
    depends_on('eckit')
    depends_on('metkit')
    depends_on('eccodes +fortran')
    depends_on('fdb@5.11.0:')

    @property
    def libs(self):
        return find_libraries("libfdbf",
                              root=self.prefix,
                              shared=False,
                              recursive=True)

    def cmake_args(self):
        args = [
            self.define('Deckit_DIR', self.spec['eckit'].prefix),
            self.define('Dmetkit_DIR', self.spec['metkit'].prefix),
            self.define('Deccodes_DIR', self.spec['eccodes'].prefix),
            self.define('Dfdb5_DIR', self.spec['fdb'].prefix),
        ]
        return args
