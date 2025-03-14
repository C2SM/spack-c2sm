# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_tabulate import PyTabulate as SpackPyTabulate


class PyTabulate(SpackPyTabulate):
    """Pretty-print tabular data"""

    #BACKPORT: Add missing versions
    version("0.9.0",
            sha256=
            "0095b12bf5966de529c0feb1fa08671671b3368eec77d7ef7ab114be2c068b3c")
    version("0.8.10",
            sha256=
            "6c57f3f3dd7ac2782770155f3adb2db0b1a269637e42f27599925e64b114f519")
