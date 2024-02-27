# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

from spack.pkg.builtin.py_pathspec import PyPathspec as SpackPyPathspec


class PyPathspec(SpackPyPathspec):
    """pathspec extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    version('0.10.3',
            sha256=
            '56200de4077d9d0791465aa9095a01d421861e405b5096955051deefd697d6f6')
