# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Makedepf90(AutotoolsPackage):
    """ Makedepf90 is a program for automatic creation of
        Makefile-style dependency lists for Fortran source code."""

    homepage = "https://salsa.debian.org/science-team/makedepf90"
    git = "https://salsa.debian.org/science-team/makedepf90.git"
    url = "https://salsa.debian.org/science-team/makedepf90/-/archive/debian/3.0.1-1/makedepf90-debian-3.0.1-1.tar.gz"

    maintainers("mjaehn")

    version('3.0.1',
            git='https://salsa.debian.org/science-team/makedepf90.git',
            branch='debian/3.0.1-1')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    def install(self, spec, prefix):
        # Run the configure script
        configure = Executable('./configure')
        configure('--prefix={0}'.format(prefix),
                  '--bindir={0}'.format(prefix.bin))

        # Build and install
        make()
        make('install')
