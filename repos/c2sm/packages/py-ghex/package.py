# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyGhex(PythonPackage):
    """A library for numerical weather prediction and climate modelling"""

    homepage = 'https://github.com/ghex-org/GHEX'
    url = "https://github.com/ghex-org/GHEX"
    git = 'https://github.com/ghex-org/GHEX.git'
    maintainers = ['boeschf', 'halungge']

    version('0.0.3', commit='5361031f72520b4531ef41de8b2a3c7d84f35ceb', git=git, submodules=True)
    version('main', branch='master', git=git, submodules=True)

    build_directory = 'bindings/python'

    depends_on("mpi")
    depends_on('py-scikit-build-core@0.5.0 +pyproject',  type='build')
    depends_on('py-pybind11', type='build')
    depends_on('py-mpi4py', type=('build', 'run'))
    depends_on('cmake@3.17:', type='build')
    depends_on('boost@1.65.1:', type=('build', 'run'))
    depends_on('py-numpy', type=('build','run'))
    depends_on('py-pytest', type=('build', 'run'))





