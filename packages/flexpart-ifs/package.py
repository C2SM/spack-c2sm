# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class FlexpartIfs(MakefilePackage):
    """flexpart is a Lagrangian dispersion model"""

    homepage = 'https://github.com/MeteoSwiss-APN/flexpart-ifs'
    url = 'https://github.com/MeteoSwiss-APN/flexpart-ifs/archive/refs/tags/v9.2mch.tar.gz'
    version('meteoswiss-10',
            git='git@github.com:MeteoSwiss-APN/flexpart-ifs.git',
            branch='meteoswiss-10')

    depends_on('eccodes jp2k=none +fortran', type=('build', 'link'))
    depends_on('netcdf-fortran', type=('build', 'link'))
    build_directory = 'src'

    @property
    def build_targets(self):
        build = ['nfc=yes', 'VERBOSE=1', 'serial']
        return build

    def setup_build_environment(self, env):
        env.set('ECCODESROOT', self.spec['eccodes'].prefix)
        env.set(
            'ECCODES_LD_FLAGS', '-L' + self.spec['eccodes'].prefix +
            '/lib64 -leccodes_f90 -leccodes')
        env.set('EBROOTNETCDFMINFORTRAN', self.spec['netcdf-fortran'].prefix)
#        env.set(
#            'JASPER_LD_FLAGS', '-Wl,--no-relax')
        env.set('CURL_INCLUDES', '/usr')

    def install(self, spec, prefix):
        install('src/FLEXPART', prefix.bin)
