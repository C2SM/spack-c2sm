# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.makefile import MakefilePackage
from spack.directives import depends_on, version
from llnl.util.filesystem import working_dir, FileFilter, install_tree
import os
import re
from pathlib import Path
from typing import Dict


class Oasis(MakefilePackage):
    """The OASIS coupler is a software allowing synchronized exchanges
    of coupling information between numerical codes representing
    different components of the climate system."""

    homepage = "https://portal.enes.org/oasis"
    git = 'https://gitlab.com/cerfacs/oasis3-mct.git'
    maintainers = ['leclairm']

    version('4.0', commit='13a9100e26d6d30a61fe8c3c056768d558adffd9')

    depends_on('mpi', type=('build', 'link', 'run'))
    depends_on('netcdf-fortran', type=('build', 'link', 'run'))

    variant(
        'fix_mct_conflict',
        default=False,
        description=
        'rename mct modules xxx as xxx_oasis to solve conflict with other mct instance at runtime'
    )

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

        if self.compiler.name == 'gcc':
            FFLAGS += ' -ffree-line-length-512'

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

    @run_before('build')
    def fix_mct_conflict(self):
        """Rename modules mct_xxx as mct_xxx_oasis"""

        # Only do something when the fix_mct_conflict variant is set to True
        if not self.spec.variants['fix_mct_conflict'].value:
            return

        # Define regexps
        re_module = re.compile(
            r'^(?P<indent>\s*)(?P<statement>module|end\s+module)'
            r'(?P<space>\s*)(?P<name>m\w*)(?P<rest>.*)$', re.IGNORECASE)
        re_use = re.compile(
            r'^(?P<indent>\s*)use(?P<space>\s*)'
            r'(?P<name>m_\w*)(?P<rest>.*)$', re.IGNORECASE)
        re_mct_mod = re.compile(r'^(?P<begining>.*)mct_mod(?P<end>.*)$',
                                re.IGNORECASE)

        # File modification function
        def mod_file(file: Path, regex_subs: Dict, indent=3) -> None:

            print(' ' * indent + file.name)
            data = file.read_text()
            data_oasis = []
            for line in data.splitlines():
                for regex, sub_str in regex_subs.items():
                    line = regex.sub(sub_str, line)
                data_oasis.append(line)
            file.write_text('\n'.join(data_oasis) + '\n')

        # Modify mct and mpeu source files
        for direc in 'mct', 'mpeu':
            print(direc)
            for src_file in Path(f'lib/mct/{direc}').glob('*90'):
                mod_file(
                    src_file, {
                        re_module:
                        r'\g<indent>\g<statement>\g<space>\g<name>_oasis\g<rest>',
                        re_use: r'\g<indent>use\g<space>\g<name>_oasis\g<rest>'
                    })

        # Modify psmile source files
        print('psmile')
        for src_file in Path(f'lib/psmile/src').glob('*90'):
            mod_file(src_file,
                     {re_mct_mod: r'\g<begining>mct_mod_oasis\g<end>'})

    def build(self, spec, prefix):

        with working_dir(self.build_directory):
            make('-f', self.makefile_file)

    def install(self, spec, prefix):

        with working_dir(os.path.join(self.rel_ARCHDIR, 'lib')):
            os.symlink('libmct.a', 'libmct_oasis.a')
            os.symlink('libmpeu.a', 'libmpeu_oasis.a')

        install_tree(self.rel_ARCHDIR, prefix)
