# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_isort import PyIsort as SpackPyIsort


class PyIsort(SpackPyIsort):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    pypi = "isort/isort-4.2.15.tar.gz"

    version("5.12.0",
            sha256=
            "8bef7dde241278824a6d83f44a544709b065191b95b6e50894bdc722fcba0504")
    version("5.10.1",
            sha256=
            "e8443a5e7a020e9d7f97f1d7d9cd17c88bcb3bc7e218bf9cf5095fe550be2951")

    variant("colors",
            default=False,
            description="Install colorama for --color support")

    depends_on("python@3.8:", when="@5.12:", type=("build", "run"))
    depends_on("python@3.6.1:3", when="@5:5.10", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-colorama@0.4.3:",
               when="+colors @5.12:",
               type=("build", "run"))
    depends_on("py-colorama@0.4.3:0.4",
               when="+colors @:5.11",
               type=("build", "run"))

    # https://github.com/PyCQA/isort/issues/2077
    conflicts("^py-poetry-core@1.5:", when="@:5.11.4")
