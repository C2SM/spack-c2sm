from spack import *
import os
import subprocess


class FieldextraIcontools(MakefilePackage):
    """A subset of the icon tools."""

    homepage = 'https://github.com/COSMO-ORG/fieldextra-icontools/'
    url = 'https://github.com/COSMO-ORG/fieldextra-icontools/archive/refs/tags/v2.5.2.1.tar.gz'
    git = 'ssh://git@github.com/COSMO-ORG/fieldextra-icontools.git'

    maintainers = ['PanicSheep']

    version('master', branch='master')
    version('2.5.2.1', tag='v2.5.2.1')

    depends_on('netcdf-c')
    depends_on('netcdf-fortran')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter(
            r'^\s*lnetcdfdir\s*=.*',
            'lnetcdfcdir = ' + ':'.join(spec['netcdf-c'].libs.directories))
        makefile.filter(
            r'^\s*lnetcdffortrandir\s*=.*', 'lnetcdffortrandir = ' +
            ':'.join(spec['netcdf-fortran'].libs.directories))

    # @run_after('install')
    # def add_include_files(self):
    #     with working_dir(os.path.join(self.stage.source_path, 'libicontools', 'src')):
    #         for file in os.listdir('.'):
    #             if file.startswith('mo_') and file.endswith('.mod'):
    #                 shutil.copy(file, self.prefix.include)

    # @run_before('build')
    # def pre_build(self):
    #     # if not os.path.exists('eccodes'):
    #     #     os.symlink(spec['eccodes'].prefix, 'eccodes')
    #     # if not os.path.exists('jasper'):
    #     #     os.symlink(spec['jasper'].prefix, 'jasper')
    #     # if not os.path.exists('libaec'):
    #     #     os.symlink(spec['libaec'].prefix, 'libaec')
    #     # os.symlink(spec['netcdf-c'].prefix, '???')
    #     # os.symlink(spec['netcdf-fortran'].prefix, '???')
    #     # os.symlink(spec['hdf5'].prefix, 'hdf5')
    #     # os.symlink(spec['zlib'].prefix, 'zlib')

    #     subprocess.run(['tools/build_fieldextra.sh', '--target=' + self.spec.variants['target'].value])
