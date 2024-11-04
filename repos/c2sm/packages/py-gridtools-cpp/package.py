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
    version("2.3.6",
            url=whl_url_prefix + "gridtools_cpp-2.3.6-py3-none-any.whl",
            sha256=
            "9d047e66558fd5b8b677f6805c61a41b4add0cafde0969e5ee09c339108c4e1f",
            expand=False)

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
