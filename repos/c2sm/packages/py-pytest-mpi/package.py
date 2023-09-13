# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPytestMpi(PythonPackage):
    """pytest_mpi is a plugin for pytest providing some useful tools when running tests under MPI,
    and testing MPI-related code."""

    homepage = "https://pytest-mpi.readthedocs.io"
    pypi     = "pytest-mpi/pytest-mpi-0.6.tar.gz"

    maintainers = ['halungge']

    version('0.6', sha256='09b3cd3511f8f3cd4d205f54d4a7223724fed0ab68b872ed1123d312152325a9')

    depends_on('py-setuptools', type='build')

