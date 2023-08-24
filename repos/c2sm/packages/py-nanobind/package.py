# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNanobind(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/wjakob/nanobind"
    url      = "https://files.pythonhosted.org/packages/cd/90/300cac4677ffdd95c5fac9cd1a64348370ce7f5f30e6c1042642ad907b1f/nanobind-1.5.1-py3-none-any.whl"

    maintainers = ['abishekg7']

    version('1.5.1', sha256='e4408ca6bcd424cb4555c6217cf7624d334862a6d497c549b01b9bc509e25b21', expand=False)


    depends_on('py-scikit-build', type=('build', 'run'))
    depends_on('ninja', type='build')
    depends_on('py-setuptools@42:', type='build')
    depends_on('cmake@3.17:', type='build')

