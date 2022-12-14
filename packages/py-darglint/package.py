# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDarglint(PythonPackage):

    pypi = "darglint/darglint-1.8.1.tar.gz"

    version("1.8.1",
            sha256=
            "080d5106df149b199822e7ee7deb9c012b49891538f14a11be681044f0bb20da")

    depends_on("python@3.6:")
    depends_on("py-poetry")
    depends_on("py-setuptools", type="build")

