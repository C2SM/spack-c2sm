# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_asttokens import PyAsttokens as SpackPyAsttokens


class PyAsttokens(SpackPyAsttokens):
    """Annotate AST trees with source code positions."""

    version("2.2.1",
            sha256=
            "4622110b2a6f30b77e1473affaa97e711bc2f07d3f10848420ff1898edbe94f3")
    version("2.0.8",
            sha256=
            "c61e16246ecfb2cde2958406b4c8ebc043c9e6d73aaa83c941673b35e5d3a76b")
