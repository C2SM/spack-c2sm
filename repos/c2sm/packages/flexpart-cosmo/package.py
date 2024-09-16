# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import spack.error as error

from llnl.util.filesystem import working_dir, install_tree

def validate_mode(mode):
    if 'none' in mode and any([x in mode for x in ('omp', 'opt', 'ncdfout', 'debug')]):
        raise error.SpecError(
            'Cannot have mode none in addition to other modes (omp, opt, ncdfout, debug) in the same build'
        )

class FlexpartCosmo(MakefilePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/C2SM-RCM/flexpart'
    git = 'ssh://git@github.com/C2SM-RCM/flexpart.git'
    maintainers = ['pirmink']

    version('V8C4.0', tag='V8C4.0')
    version('main', branch='main')

    depends_on('eccodes +fortran')
    depends_on('netcdf-fortran')
    depends_on('makedepf90')

    conflicts('%gcc@:10')
    conflicts('%nvhpc')
    conflicts('%pgi')
    conflicts('%cce')

    # Make mode/Compile time options of Flexpart as defined in:
    # https://github.com/C2SM-RCM/flexpart/blob/main/documentation/installation.md#compile-time-options
    variant('none',
            default=False,
            description='Enable default flags only (do not combine with other variants); serial model.')
    variant('omp',
            default=False,
            description='Specify OpenMP parallelism explicitly in mode.')
    variant('opt',
            default=False,
            description='Specify code optimization explicitly in mode.')
    variant('ncdfout',
            default=False,
            description='Specify netcdf output explicitly in mode.')
    variant('debug',
            default=False,
            description='Specify netcdf output explicitly in mode.')

    build_directory = 'src'

    makefile_file = "Makefile.spack"

    @property
    def build_targets(self):
        return ['ncf=yes', 'VERBOSE=1']

    def setup_build_environment(self, env):
        env.set('GRIB_API', self.spec['eccodes'].prefix)
        env.set('NETCDF', self.spec['netcdf-fortran'].prefix)

    def build(self, spec, prefix):

        mode = ''

        for x in [
            'none',
            'omp',
            'opt',
            'ncdfout',
            'debug']:
            if f'+{x}' in self.spec:
                mode += x

        with working_dir(self.build_directory):
            make.jobs = 1
            if mode:
                validate_mode(mode)
                make('-f', self.makefile_file, f"mode={mode}")
            else:
                make('-f', self.makefile_file)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share + '/test/')
        mkdir(prefix.share + '/options/')
        install_tree('options/', prefix.share + '/options/')
        install('bin/FLEXPART', prefix.bin)
