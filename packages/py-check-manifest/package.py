# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCheckManifest(PythonPackage):

    pypi = "check-manifest/check-manifest-0.49.tar.gz"

    version("0.49",
            sha256=
            "64a640445542cf226919657c7b78d02d9c1ca5b1c25d7e66e0e1ff325060f416")

    depends_on("python@3.7:")
    depends_on("py-tomli")
    depends_on("py-setuptools", type="build")

