from spack import *
import os
import subprocess


class Fieldextra(MakefilePackage):
    """Fieldextra is a generic tool to manipulate NWP model data and gridded observations."""

    homepage = 'https://github.com/COSMO-ORG/fieldextra/'
    url = 'https://github.com/COSMO-ORG/fieldextra/archive/refs/tags/v14.0.3.tar.gz'
    git = 'ssh://git@github.com/COSMO-ORG/fieldextra.git'

    maintainers = ['PanicSheep']

    version('develop', branch='develop')
    version('14.0.3', tag='v14.0.3')

    variant('target', default='cscs@alps')

    depends_on('eccodes @2.25.0')
    depends_on('jasper @2.0.14 ~shared')
    depends_on('libaec @1.0.0')
    depends_on('zlib @1.2.11')
    depends_on('hdf5 @1.8.21')
    depends_on('netcdf-c @4.4.0')
    depends_on('netcdf-fortran @4.4.4')
    # depends_on('rttov')
    # depends_on('icontools')

    build_directory = 'src'

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter(r'^\s*laecdir\s*=.*', 'laecdir = ' + ':'.join(spec['libaec'].libs.directories))
            makefile.filter(r'^\s*ljasperdir\s*=.*', 'ljasperdir = ' + ':'.join(spec['jasper'].libs.directories))
            makefile.filter(r'^\s*leccdir\s*=.*', 'leccdir = ' + ':'.join(spec['eccodes'].libs.directories))
            makefile.filter(r'^\s*lzdir\s*=.*', 'lzdir = ' + ':'.join(spec['zlib'].libs.directories))
            makefile.filter(r'^\s*lhdf5dir\s*=.*', 'lhdf5dir = ' + ':'.join(spec['hdf5'].libs.directories))
            makefile.filter(r'^\s*lnetcdfcdir\s*=.*', 'lnetcdfcdir = ' + ':'.join(spec['netcdf-c'].libs.directories))
            makefile.filter(r'^\s*lnetcdffortrandir\s*=.*', 'lnetcdffortrandir = ' + ':'.join(spec['netcdf-fortran'].libs.directories))
            # makefile.filter(r'^\s*lrttovdir\s*=.*', 'lrttovdir = ' + ':'.join(spec['rttov'].libs.directories))
            # makefile.filter(r'^\s*licontoolsdir\s*=.*', 'licontoolsdir = ' + ':'.join(spec['icontools'].libs.directories))

    @run_before('build')
    def pre_build(self):
        # if not os.path.exists('eccodes'):
        #     os.symlink(spec['eccodes'].prefix, 'eccodes')
        # if not os.path.exists('jasper'):
        #     os.symlink(spec['jasper'].prefix, 'jasper')
        # if not os.path.exists('libaec'):
        #     os.symlink(spec['libaec'].prefix, 'libaec')
        # os.symlink(spec['netcdf-c'].prefix, '???')
        # os.symlink(spec['netcdf-fortran'].prefix, '???')
        # os.symlink(spec['hdf5'].prefix, 'hdf5')
        # os.symlink(spec['zlib'].prefix, 'zlib')

        subprocess.run(['tools/build_fieldextra.sh', '--target=' + self.spec.variants['target'].value])
