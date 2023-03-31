# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from spack.pkg.builtin.py_fprettify import PyFprettify as SpackPyFprettify


class PyFprettify(SpackPyFprettify):
    """fprettify is an auto-formatter for modern Fortran code (Fortran 90
    and later) that imposes strict whitespace formatting, written in
    Python."""

    version('0.3.7',
            sha256=
            '1488a813f7e60a9e86c56fd0b82bd9df1b75bfb4bf2ee8e433c12f63b7e54057')
