# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGridtoolsCpp(PythonPackage):
    """Python package for GridTools headers and CMake files"""

    homepage = "https://gridtools.github.io/gridtools/latest/index.html"

    pypi = "gridtools-cpp/gridtools-cpp-2.2.3.tar.gz"
    whl_url = "https://pypi.io/packages/py3/g/gridtools-cpp/gridtools_cpp-2.3.0-py3-none-any.whl"

    maintainers = ['samkellerhals']

    version("2.3.0",
            url=whl_url,
            sha256=
            "0af02845a538a7c20791ecaeeb3b68c8b976b653ef8593a00beea60445ec38b6",
            expand=False)
    version("2.2.2",
            sha256=
            "d45316379440b6d96d04b3fb47f6a432946e9f9d906bcb10af51d9a92e95353e")

    version("2.2.3",
            sha256=
            "0bc4b72c9f2786f70c80092bba7bd2eedd216d8c16946b7b32704d248e0d97e6")

    depends_on("python@3.8:")
    depends_on("py-setuptools", type="build")