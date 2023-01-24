# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEditables(PythonPackage):
    """This library supports the building of wheels which, 
    when installed, will expose packages in a local 
    directory on sys.path in "editable mode."""

    homepage = "https://github.com/pfmoore/editables"

    pypi = 'editables/editables-0.3.tar.gz'

    maintainers = ['samkellerhals']

    version('0.3',
            sha256=
            '167524e377358ed1f1374e61c268f0d7a4bf7dbd046c656f7b410cde16161b1a')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.7:', type=('build', 'run'))
