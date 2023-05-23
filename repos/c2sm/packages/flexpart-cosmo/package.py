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
    url = 'https://github.com/C2SM-RCM/flexpart/archive/refs/tags/V8C3-preop.tar.gz'
    git = 'ssh://git@github.com/C2SM-RCM/flexpart.git'

    version('master', branch='master')

    depends_on('eccodes@2.19.0 jp2k=none +fortran')
    depends_on('netcdf-fortran')
    depends_on('jasper@1.900.1')

    conflicts('%nvhpc')
    conflicts('%pgi')

    build_directory = 'src'

    @property
    def build_targets(self):
        return ['ncf=yes', 'VERBOSE=1']

    def setup_build_environment(self, env):
        env.set('GRIB_API', self.spec['eccodes'].prefix)
        env.set('NETCDF', self.spec['netcdf-fortran'].prefix)
        env.set('JASPER', self.spec['jasper'].prefix)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share + '/test/')
        mkdir(prefix.share + '/options/')
        copy_tree('options/', prefix.share + '/options/')
        install('bin/FLEXPART', prefix.bin)
        # install('test/*', prefix.share + '/test/')
