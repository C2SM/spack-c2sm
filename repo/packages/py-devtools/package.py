# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDevtools(PythonPackage):
    """Python's missing debug print command and other development tools."""

    homepage = "https://github.com/samuelcolvin/python-devtools"

    pypi = "devtools/devtools-0.10.0.tar.gz"

    maintainers = ['samkellerhals']

    version('0.10.0',
            sha256=
            '6eb7c4fa7c4b90e5cfe623537a9961d1dc3199d8be0981802c6931cd8f02418f')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-hatchling', type=('build', 'run'))

    depends_on('py-executing@1.1.1:', type=('build', 'run'))
    depends_on('py-asttokens@2.0.0:2.9', type=('build', 'run'))
