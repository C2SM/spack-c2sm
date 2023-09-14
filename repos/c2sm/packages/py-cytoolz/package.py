# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCytoolz(PythonPackage):
    """Python implementation of the toolz package, 
    which provides high performance utility functions for iterables, 
    functions, and dictionaries."""

    homepage = "https://github.com/pytoolz/cytoolz"

    pypi = 'cytoolz/cytoolz-0.12.0.tar.gz'

    maintainers = ['samkellerhals']

    version('0.12.0',
            sha256=
            'c105b05f85e03fbcd60244375968e62e44fe798c15a3531c922d531018d22412')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-toolz@0.8.0:', type=('build', 'run'))

    def global_options(self, spec, prefix):
        options = []
        options.append('--with-cython')
        return options
