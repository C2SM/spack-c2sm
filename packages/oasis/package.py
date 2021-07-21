
# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Oasis(MakefilePackage):

    homepage = "https://portal.enes.org/oasis"
    git      = 'https://gitlab.com/cerfacs/oasis3-mct.git'
    maintainers = ['pheidippides']

    version('master', branch='OASIS3-MCT_4.0')
    version('dev-build', branch='OASIS3-MCT_4.0')

    depends_on('mpi', type=('build', 'link', 'run'))

    build_directory = 'util/make_dir/'

    makefile_file = 'TopMakefileOasis3'

    def setup_build_environment(self, env):

        env.set('F90', self.spec['mpi'].mpifc)
        env.set('ARCHDIR', self.build_directory)

    def edit(self,spec,prefix):
        with working_dir(self.build_directory):

            makefile = FileFilter(self.makefile_file)

            makefile.filter('include make.inc', '')

    def build(self,spec,prefix):
        with working_dir(self.build_directory):
            make('-f', self.makefile_file)

    def setup_run_environment(self, env):
        print('void')
