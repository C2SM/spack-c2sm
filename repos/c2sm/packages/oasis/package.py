# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.makefile import MakefilePackage
from spack.directives import depends_on, version
from llnl.util.filesystem import working_dir, FileFilter, install_tree
import os


class Oasis(MakefilePackage):
    """The OASIS coupler is a software allowing synchronized exchanges
    of coupling information between numerical codes representing
    different components of the climate system."""

    homepage = "https://portal.enes.org/oasis"
    git = 'https://gitlab.com/cerfacs/oasis3-mct.git'
    maintainers = ['leclairm']

    version('master', branch='OASIS3-MCT_4.0')

    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('netcdf-fortran', type=('build', 'link', 'run'))

    build_directory = 'util/make_dir'

    makefile_file = 'TopMakefileOasis3'

    # Relative path where the built libraries are stored (corresponds
    # to the absolute path called ARCHDIR in the Makefile)
    rel_ARCHDIR = 'spack-build'

    def setup_build_environment(self, env):

        CHAN = 'MPI1'
        env.set('CHAN', CHAN)
        env.set('F90', self.spec['mpi'].mpifc)
        env.set('f90', self.spec['mpi'].mpifc)
        env.set('F', self.spec['mpi'].mpifc)
        env.set('f', self.spec['mpi'].mpifc)
        env.set('MAKE', 'gmake')

        LIBBUILD = os.path.join('../..', self.rel_ARCHDIR, 'build/lib')
        INCPSMILE = '-I{LIBBUILD}/psmile.{CHAN} -I{LIBBUILD}/mct -I{LIBBUILD}/scrip'.format(
            LIBBUILD=LIBBUILD, CHAN=CHAN)

        CPPDEF = '-Duse_comm_{CHAN} -D__VERBOSE -DTREAT_OVERLAY -D__NO_16BYTE_REALS'.format(
            CHAN=CHAN)
        env.set('CPPDEF', CPPDEF)

        FFLAGS = '-O2 {INCPSMILE} {CPPDEF}'.format(CPPDEF=CPPDEF,
                                                   INCPSMILE=INCPSMILE)
        env.set('F90FLAGS', FFLAGS)
        env.set('f90FLAGS', FFLAGS)
        env.set('FFLAGS', FFLAGS)
        env.set('fFLAGS', FFLAGS)
        env.set('CCFLAGS', FFLAGS)

    def edit(self, spec, prefix):

        COUPLE = os.getcwd()
        ARCHDIR = os.path.join(COUPLE, self.rel_ARCHDIR)
        with working_dir(self.build_directory):
            makefile = FileFilter(self.makefile_file)
            makefile.filter(
                'include make.inc',
                'export COUPLE = {}\nexport ARCHDIR = {}'.format(
                    COUPLE, ARCHDIR))
            makefile.filter('\$\(modifmakefile\)\s\;\s', '')

    def patch(self):

        # Remove old directives for Fujitsu comilers. Already fixed in MCT [1] but not merged in OASIS yet
        # [1] https://github.com/MCSclimate/MCT/commit/dcb4fa4527bbc51729fb67fbc2e0179bfcb4baa2
        with working_dir('lib/mct/mct'):
            m_AttrVect = FileFilter('m_AttrVect.F90')
            m_AttrVect.filter('\s*\!DIR\$ COLLAPSE', '')

    def build(self, spec, prefix):

        with working_dir(self.build_directory):
            make('-f', self.makefile_file)

    def install(self, spec, prefix):

        with working_dir(os.path.join(self.rel_ARCHDIR, 'lib')):
            os.symlink('libmct.a', 'libmct_oasis.a')
            os.symlink('libmpeu.a', 'libmpeu_oasis.a')

        install_tree(self.rel_ARCHDIR, prefix)
