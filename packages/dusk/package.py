# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Dusk(PythonPackage):
    """A minimal and lightweight front-end for dawn."""

    homepage = 'https://github.com/dawn-ico/dusk'
    git = 'https://github.com/dawn-ico/dusk'
    maintainers = ['BenWeber42']

    # old version before _dusk horizon_
    # (put on hold until _dusk horizon_ is over)
    version('master', branch='master')
    # development version for phase _dusk horizon_
    version('horizon', branch='horizon', preferred=True)

    extends('python@3.8.0:3.8.999')

    depends_on('dawn4py', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # will test that dusk is importable after the install
    import_modules = ['dusk']
