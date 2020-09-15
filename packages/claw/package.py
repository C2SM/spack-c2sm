# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Claw(CMakePackage):
    """CLAW Compiler targets performance portability problem in climate and
       weather application written in Fortran. From a single source code, it
       generates architecture specific code decorated with OpenMP or OpenACC"""

    homepage = 'https://claw-project.github.io/'
    git      = 'https://github.com/claw-project/claw-compiler.git'
    maintainers = ['clementval']

    version('master', branch='master', submodules=True)
    version('2.0.2', commit='8c012d58484d8caf79a4fe45597dc74b4367421c', submodules=True)
    version('2.0.1', commit='f5acc929df74ce66a328aa4eda9cc9664f699b91', submodules=True)
    version('2.0',   commit='53e705b8bfce40a5c5636e8194a7622e337cf4f5', submodules=True)
    version('1.2.3', commit='eaf5e5fb39150090e51bec1763170ce5c5355198', submodules=True)
    version('1.2.2', commit='fc27a267eef9f412dd6353dc0b358a05b3fb3e16', submodules=True)
    version('1.2.1', commit='939989ab52edb5c292476e729608725654d0a59a', submodules=True)
    version('1.2.0', commit='fc9c50fe02be97b910ff9c7015064f89be88a3a2', submodules=True)
    version('1.1.0', commit='16b165a443b11b025a77cad830b1280b8c9bcf01', submodules=True)
    
    variant('omni-master', default=False, description='Build with the master version of the omni-compiler')

    depends_on('cmake@3.0:%gcc', type='build')
    depends_on('java@8:', when="@2.0:")
    depends_on('java@7:', when="@1.1.0:1.2.3")
    depends_on('ant@1.9:%gcc')
    depends_on('libxml2%gcc')
    depends_on('bison%gcc')
    depends_on('flex%gcc')
    
    def setup_environment(self, spack_env, run_env):
        spack_env.set('YACC', 'bison -y')
    def cmake_args(self):
        args = []
        spec = self.spec
        
        if spec.variants['omni-master'].value:
            args.append('-DOMNI_GIT_HASH=master')

        args.append('-DOMNI_CONF_OPTION=--with-libxml2={0}'.
                    format(spec['libxml2'].prefix))

        args.append('-DCMAKE_Fortran_COMPILER={0}'.
                    format(self.compiler.fc))

        return args
