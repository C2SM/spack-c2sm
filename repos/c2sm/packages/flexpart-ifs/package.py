from spack import *


class FlexpartIfs(MakefilePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/MeteoSwiss/flexpart'
    url = 'https://github.com/MeteoSwiss/flexpart/archive/refs/tags/v10.4.4.tar.gz'
    git = 'git@github.com:MeteoSwiss/flexpart.git'
    maintainers = ['pirmink']

    version('main', branch='main')
    version('fdb', branch='fdb')
    version(
        'add_opr',
        branch='add_opr',
        git='git@github.com:dominichofer/flexpart.git')  #TODO: Remove this!
    version('10.4.4', tag='10.4.4')

    depends_on('eccodes +fortran')
    depends_on('netcdf-fortran')

    conflicts('%nvhpc')
    conflicts('%pgi')

    build_directory = 'src'

    def setup_build_environment(self, env):
        env.set('ECCODES_INCLUDE', self.spec['eccodes'].prefix.include)
        env.set('ECCODES_LD_FLAGS', self.spec['eccodes'].libs.ld_flags)
        env.set('NETCDF_FORTRAN_INCLUDE',
                self.spec['netcdf-fortran'].prefix.include)
        env.set('NETCDF_FORTRAN_LD_FLAGS',
                self.spec['netcdf-fortran'].libs.ld_flags)

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make('-f', 'makefile_meteoswiss')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install(join_path(self.build_directory, 'FLEXPART'), prefix.bin)
        install_tree('test_meteoswiss', prefix.share.test_meteoswiss)
        install_tree('options', join_path(prefix.share, 'options'))
        install_tree('options.meteoswiss',
                     join_path(prefix.share, 'options.meteoswiss'))
