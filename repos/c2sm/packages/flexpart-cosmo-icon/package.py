# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
from llnl.util.filesystem import working_dir, install_tree


class FlexpartCosmoIcon(MakefilePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/C2SM/flexpart-cosmo-icon'
    git = 'git@github.com:C2SM/flexpart-cosmo-icon.git'
    maintainers = ['pirmink']

    version('V8C4.0', tag='V8C4.0')
    version('main', branch='main')

    depends_on('eccodes +fortran')
    # WORKAROUND: '%gcc' should not be necessary, but without it, spack concretizes to nvhpc.
    depends_on('netcdf-fortran %gcc')
    depends_on('makedepf90')

    requires('%gcc@11:')

    build_directory = 'src'

    makefile_file = "Makefile.spack"

    @property
    def build_targets(self):
        return ['ncf=yes', 'VERBOSE=1']

    def setup_build_environment(self, env):
        env.set('GRIB_API', self.spec['eccodes'].prefix)
        env.set('NETCDF', self.spec['netcdf-fortran'].prefix)

    def build(self, spec, prefix):

        with working_dir(self.build_directory):
            make.jobs = 1
            make('-f', self.makefile_file)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share + '/test/')
        mkdir(prefix.share + '/options/')
        install_tree('options/', prefix.share + '/options/')
        install('bin/FLEXPART', prefix.bin)
