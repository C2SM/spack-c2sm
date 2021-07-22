
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
    depends_on('netcdf-fortran', type=('build','link','run'))

    build_directory = '/scratch/snx3000/juckerj/oasis/util/make_dir'
    arch_dir = build_directory + '/spack'

    makefile_file = 'TopMakefileOasis3'

    def setup_build_environment(self, env):

        env.set('F90', self.spec['mpi'].mpifc)
        env.set('f90', self.spec['mpi'].mpifc)
        env.set('F', self.spec['mpi'].mpifc)
        env.set('f', self.spec['mpi'].mpifc)
        env.set('COUPLE', '/scratch/snx3000/juckerj/oasis')
        env.set('ARCHDIR', self.arch_dir)
        env.set('MAKE', 'gmake')

    def edit(self,spec,prefix):
        with working_dir(self.build_directory):

            makefile = FileFilter(self.makefile_file)

            makefile.filter('include make.inc', '')
            makefile.filter('$(modifmakefile) ; $(MAKE) all 1>> $(LOG) 2>> $(ERR)' , '$(MAKE) all 1>> $(LOG) 2>> $(ERR)')

    def build(self,spec,prefix):
        with working_dir(self.build_directory):
            make('-f', self.makefile_file)

    def setup_run_environment(self, env):
        print('void')
