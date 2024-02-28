# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Makedepf90(AutoreconfPackageTemplate):
    """ Makedepf90 is a program for automatic creation of
        Makefile-style dependency lists for Fortran source code."""

    homepage = "https://salsa.debian.org/science-team/makedepf90"
    git = "https://salsa.debian.org/science-team/makedepf90.git"
    url = "https://salsa.debian.org/science-team/makedepf90/-/archive/debian/3.0.1-1/makedepf90-debian-3.0.1-1.tar.gz"
    parallel = False  # Makefile is not thread-safe.

    maintainers("mjaehn")

    depends_on("gmake@4:")

    version('3.0.1', branch='debian/3.0.1-1')

    def configure_args(self):
        return ['--bindir={0}'.format(self.prefix.bin)]
