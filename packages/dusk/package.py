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
    
    extends('python@3.8.0:3.8.999')

    depends_on('dawn4py', type='run')
    depends_on('py-setuptools', type='build')

    # will test that dusk is importable after the install
    import_modules = ['dusk']