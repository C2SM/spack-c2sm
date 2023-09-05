# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
from distutils.dir_util import copy_tree


class FlexpartCosmo(MakefilePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/C2SM-RCM/flexpart'
    git = 'ssh://git@github.com/C2SM-RCM/flexpart.git'

    version('main', branch='testing')

    depends_on('eccodes +fortran')
    depends_on('netcdf-fortran')

    conflicts('%nvhpc')
    conflicts('%pgi')

    build_directory = 'src'

    makefile = "Makefile.spack"

    @property
    def build_targets(self):
        return ['ncf=yes', 'VERBOSE=1']

    def setup_build_environment(self, env):
        env.set('GRIB_API', self.spec['eccodes'].prefix)
        env.set('NETCDF', self.spec['netcdf-fortran'].prefix)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share + '/test/')
        mkdir(prefix.share + '/options/')
        copy_tree('options/', prefix.share + '/options/')
        install('bin/FLEXPART', prefix.bin)
        # install('test/*', prefix.share + '/test/')
