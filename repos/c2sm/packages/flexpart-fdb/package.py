from spack import *
from distutils.dir_util import copy_tree
import shutil


class FlexpartFdb(MakefilePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/MeteoSwiss-APN/flexpart-fdb'
    git = 'https://github.com/MeteoSwiss-APN/flexpart-fdb.git'

    version('fdb', branch='fdb')

    depends_on('eccodes +fortran')
    depends_on('netcdf-fortran')
    depends_on('fdb-fortran')
    depends_on('flexpart-opr')

    conflicts('%nvhpc')
    conflicts('%pgi')

    build_directory = 'src'

    @property
    def build_targets(self):
        return ['ncf=yes', 'VERBOSE=1', 'serial']

    def edit(self, spec, prefix):
        copy_tree(self.spec['flexpart-opr'].prefix + '/flexpartOpr/src', 'src')
        shutil.rmtree('options')
        copy_tree(self.spec['flexpart-opr'].prefix + '/flexpartOpr/options',
                  'options')
        copy('src/makefile.meteoswiss', 'src/makefile')

    def setup_build_environment(self, env):
        env.set('ECCODESROOT', self.spec['eccodes'].prefix)
        env.set(
            'ECCODES_LD_FLAGS', '-L' + self.spec['eccodes'].prefix +
            '/lib64 -leccodes_f90 -leccodes')
        env.set('EBROOTNETCDFMINFORTRAN', self.spec['netcdf-fortran'].prefix)
        env.set(
            'JASPER_LD_FLAGS', '-Wl,--no-relax -L' + self.spec['fdb'].prefix +
            '/lib -lfdb5 -L' + self.spec['fdb-fortran'].prefix + '/lib -lfdbf')
        env.set(
            'CURL_INCLUDES', self.spec['fdb-fortran'].prefix +
            '/include/fortran/fdb/modules -I' + self.spec['fdb'].prefix +
            '/include')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share + '/test/')
        mkdir(prefix.share + '/options/')
        copy_tree('options/', prefix.share + '/options/')
        install('src/FLEXPART', prefix.bin)
        install('test/*', prefix.share + '/test/')
