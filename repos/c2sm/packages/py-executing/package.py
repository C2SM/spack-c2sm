# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_executing import PyExecuting as SpackPyExecuting


class PyExecuting(SpackPyExecuting):
    """Get the currently executing AST node of a frame, and other information."""

    version("1.2.0",
            sha256=
            "19da64c18d2d851112f09c287f8d3dbbdf725ab0e569077efb6cdcbd3497c107")
    version("1.1.0",
            sha256=
            "2c2c07d1ec4b2d8f9676b25170f1d8445c0ee2eb78901afb075a4b8d83608c6a")
    version("1.0.0",
            sha256=
            "98daefa9d1916a4f0d944880d5aeaf079e05585689bebd9ff9b32e31dd5e1017")
