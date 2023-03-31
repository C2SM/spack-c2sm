# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHatchling(PythonPackage):
    """This is the extensible, standards compliant 
    build backend used by Hatch.
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://hatch.pypa.io/latest/"

    pypi = "hatchling/hatchling-1.11.1.tar.gz"

    maintainers = ['samkellerhals']

    version('1.11.1',
            sha256=
            '9f84361f70cf3a7ab9543b0c3ecc64211ed2ba8a606a71eb6a473c1c9b08e1d0')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.7:', type=('build', 'run'))

    # Be less strict with py-pluggy, otherwise concretizer
    # fails due to 0.12 and 1.0 required at the same time
    #depends_on('py-pluggy@1.0.0:', type=('build', 'run'))

    depends_on('py-pluggy@0.12:1', type=('build', 'run'))
    depends_on('py-pathspec@0.10.1:', type=('build', 'run'))
    depends_on('py-tomli@1.2.2:', type=('build', 'run'))
    depends_on('py-packaging@21.3:', type=('build', 'run'))
    depends_on('py-editables@0.3:', type=('build', 'run'))
    depends_on('py-importlib-metadata', type=('build', 'run'))
