# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_scikit_build_core import PyScikitBuildCore as SpackPyScikitBuildCore


class PyScikitBuildCore(SpackPyScikitBuildCore):
    """scikit-build-core is a doubly improved build system generator
    for CPython C/C++/Fortran/Cython extensions. It features several
    improvements over the classic scikit-build build system generator."""

    version("0.5.0", sha256="a42a95029b34b5cf892855342d9b9445c774cb797fcb24c8fc4c2fb42b18dfca")
