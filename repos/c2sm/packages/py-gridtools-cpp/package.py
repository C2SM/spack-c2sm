# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGridtoolsCpp(PythonPackage):
    """Python package for GridTools headers and CMake files"""

    homepage = "https://gridtools.github.io/gridtools/latest/index.html"

    whl_url_prefix = "https://pypi.io/packages/py3/g/gridtools-cpp/"

    maintainers = ['havogt']

    version("2.3.1",
            url=whl_url_prefix + "gridtools_cpp-2.3.1-py3-none-any.whl",
            sha256=
            "90cf40287c4df7586bc497f9e612b1b79d5751cb41c62ac557d2d4999aaed954",
            expand=False)
    version("2.3.0",
            url=whl_url_prefix + "gridtools_cpp-2.3.0-py3-none-any.whl",
            sha256=
            "0af02845a538a7c20791ecaeeb3b68c8b976b653ef8593a00beea60445ec38b6",
            expand=False)
    version("2.2.2",
            sha256=
            "d45316379440b6d96d04b3fb47f6a432946e9f9d906bcb10af51d9a92e95353e")

    version("2.2.3",
            sha256=
            "0bc4b72c9f2786f70c80092bba7bd2eedd216d8c16946b7b32704d248e0d97e6")

    depends_on("python@3.10:")
    depends_on("py-setuptools", type="build")

    @property
    def headers(self):
        '''Workaround to hide the details of the installation path, 
        i.e "lib/python3.10/site-packages/icon4py/atm_dyn_iconam"
        from upstream packages. It needs to be part of the "Spec" object,
        therefore choose the headers-function
        '''

        query_parameters = self.spec.last_query.extra_parameters
        if len(query_parameters) > 1:
            raise ValueError('Only one query parameter allowed')

        if 'data' in query_parameters:
            header = self._find_folder_and_add_dummy_header(
                self.prefix, 'data')
        else:
            header = HeaderList([])

        return header

    def _find_folder_and_add_dummy_header(self, prefix, name):
        folder = find(prefix, name)
        headerlist = HeaderList(f'{folder[0]}/dummy.h')
        return headerlist
