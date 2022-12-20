# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyInflection(PythonPackage):
    """Inflection is a string transformation library."""

    homepage = "https://github.com/jpvanhal/inflection"

    pypi = "inflection/inflection-0.5.1.tar.gz"

    maintainers = ['samkellerhals']

    version('0.5.1',
            sha256=
            '1a29730d366e996aaacffb2f1f1cb9593dc38e2ddd30c91250c6dde09ea9b417')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-isort', type=('build', 'run'))
    depends_on('py-flake8', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
