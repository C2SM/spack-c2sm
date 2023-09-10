# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-pytest-mpi
#
# You can edit this file again by typing:
#
#     spack edit py-pytest-mpi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPytestMpi(PythonPackage):
    """pytest_mpi is a plugin for pytest providing some useful tools when running tests under MPI,
    and testing MPI-related code."""

    homepage = "https://pytest-mpi.readthedocs.io"
    pypi     = "pytest-mpi/pytest-mpi-0.6.tar.gz"

    maintainers = ['halungge']

    version('0.6', sha256='09b3cd3511f8f3cd4d205f54d4a7223724fed0ab68b872ed1123d312152325a9')

    depends_on('py-setuptools', type='build')

