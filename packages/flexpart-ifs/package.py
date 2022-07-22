# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
from distutils.dir_util import copy_tree


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
        build = ['ncf=yes', 'VERBOSE=1', 'serial']
        return build

    def edit(self, spec, prefix):
        copy('src/makefile.meteoswiss', 'src/makefile')

    def setup_build_environment(self, env):
        env.set('ECCODESROOT', self.spec['eccodes'].prefix)
        env.set(
            'ECCODES_LD_FLAGS', '-L' + self.spec['eccodes'].prefix +
            '/lib64 -leccodes_f90 -leccodes')
        env.set('EBROOTNETCDFMINFORTRAN', self.spec['netcdf-fortran'].prefix)
        #abuse of JASPER_LD_FLAGS since there is no other entrypoint var for LDFLAGS
        env.set('JASPER_LD_FLAGS', '-Wl,--no-relax')
        # not really required, just a default since the -I flags would be inconsistent with an empty string
        env.set('CURL_INCLUDES', '/usr')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share + '/test/')
        mkdir(prefix.share + '/options/')
        copy_tree('options/', prefix.share + '/options/')
        install('src/FLEXPART', prefix.bin)
        install('test/*', prefix.share + '/test/')
