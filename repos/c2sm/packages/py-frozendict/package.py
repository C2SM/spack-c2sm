# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFrozendict(PythonPackage):
    """frozendict is a simple immutable dictionary."""

    homepage = "https://github.com/Marco-Sulla/python-frozendict"

    pypi = 'frozendict/frozendict-2.3.4.tar.gz'

    maintainers = ['samkellerhals']

    # FIXME: Add proper versions and checksums here.
    version('2.3.4',
            sha256=
            '15b4b18346259392b0d27598f240e9390fafbff882137a9c48a1e0104fb17f78')

    depends_on('python@3.6:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
