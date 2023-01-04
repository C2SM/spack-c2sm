# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGridtoolsCpp(PythonPackage):
    """Python package for GridTools headers and CMake files"""

    homepage = "https://gridtools.github.io/gridtools/latest/index.html"

    pypi = "gridtools-cpp/gridtools-cpp-2.2.2.tar.gz"

    maintainers = ['samkellerhals']

    version("2.2.2",
            sha256=
            "d45316379440b6d96d04b3fb47f6a432946e9f9d906bcb10af51d9a92e95353e")

    depends_on("python@3.8:")
    depends_on("py-setuptools", type="build")
