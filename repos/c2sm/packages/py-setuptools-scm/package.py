# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_setuptools_scm import PySetuptoolsScm as SpackPySetuptoolsScm


# TODO (magdalena) remove after upgrade to spack 0.20.0
# version available in spack 0.20.0
class PySetuptoolsScm(SpackPySetuptoolsScm):
    """The blessed package to manage your versions by scm tags."""

    version("7.1.0",
            sha256=
            "6c508345a771aad7d56ebff0e70628bf2b0ec7573762be9960214730de278f27")
    version("7.0.5",
            sha256=
            "031e13af771d6f892b941adb6ea04545bbf91ebc5ce68c78aaf3fff6e1fb4844")
    version("7.0.3",
            sha256=
            "cf8ab8e235bed840cd4559b658af0d8e8a70896a191bbc510ee914ec5325332d")
    version("6.3.2",
            sha256=
            "a49aa8081eeb3514eb9728fa5040f2eaa962d6c6f4ec9c32f6c1fba88f88a0f2")
