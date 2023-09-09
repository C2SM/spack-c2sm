# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyGhex(PythonPackage):
    """
    Python bindings for Generic exascale-ready library for halo-exchange operations
    on variety of grids/meshes.
    """

    homepage = 'https://github.com/ghex-org/GHEX'
    url = "https://github.com/ghex-org/GHEX/archive/refs/tags/v0.3.0.tar.gz"
    git = 'https://github.com/ghex-org/GHEX.git'
    maintainers = ['boeschf', 'halungge']

    version('0.3.1', commit='7ced96a69ab502b0ab0eddc1c0d743e06ccde919', git=git, submodules=True)

    build_directory = 'bindings/python'
    import_modules = ['ghex', 'ghex.unstructured']

    depends_on("mpi")
    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-scikit-build-core@0.5.0 +pyproject',  type='build')
    depends_on('py-pybind11', type=('build', 'run'))
    depends_on('py-mpi4py', type=('build', 'run'))
    depends_on('cmake@3.17:', type='build')
    depends_on('boost@1.65.1:', type=('build', 'run'))
    depends_on('py-numpy', type=('build','run'))
    depends_on('py-pytest', type=('build', 'run'))

    patch("add_origin_install_rpath.patch", when="@0.3.1")












