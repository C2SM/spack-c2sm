# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install rttov
#
# You can edit this file again by typing:
#
#     spack edit rttov
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Rttov(MakefilePackage):
    """RTTOV (Radiative Transfer for TOVS) is a very fast radiative transfer model for passive visible, infrared and microwave downward-viewing satellite radiometers, spectrometers and interferometers. It is a FORTRAN 90 code for simulating satellite radiances, designed to be incorporated within user applications"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.nwpsaf.eu/site/software/rttov/"
    url      = "https://github.com/C2SM-RCM/rttov.git"
    git      = 'git@github.com:C2SM-RCM/rttov.git'

    maintainers = ['elsagermann']

    version('11.2.0', branch='master')

    build_directory = 'rttov11/rttov-11.2.0/src'
    
    @property
    def build_targets(self):
        build = []
        if self.compiler.name == 'gcc':
            build.append('CC=gcc')
            build.append('ARCH=gfortran')
        elif self.compiler.name == 'intel':
            build.append('CC=icc')
            build.append('ARCH=ifort')

        return build
    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.mod)
        mkdir(prefix.lib)
        mkdir(prefix.include)
        with working_dir('rttov11/rttov-11.2.0'):
            install_tree('bin', prefix.bin)
            install_tree('mod', prefix.mod)
            install_tree('lib', prefix.lib)
            install_tree('include', prefix.include)
