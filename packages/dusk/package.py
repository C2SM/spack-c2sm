# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import sys

class Dusk(PythonPackage):
    """A minimal and lightweight front-end for dawn."""

    homepage = 'https://github.com/dawn-ico/dusk'
    git      = 'https://github.com/dawn-ico/dusk'
    maintainers = ['BenWeber42']

    version('master', branch='master')
    depends_on('python@3.8.0', type=('build', 'run'))

    depends_on('dawn4py')
    depends_on('py-setuptools', type='build')
    depends_on('py-pip', type='build')