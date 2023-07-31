# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# overwrite package from spack, otherwise downgrade of
#
# depends_on("py-setuptools@65:", type=("build", "run"))
#
# to
#
# depends_on("py-setuptools@63:", type=("build", "run"))
#
# is not possible. This is required, because py-numpy
# cannot be built with py-setuptools greater then 63.

# package py-gt4py and py-icon4py trigger this incompatability


class PySphinxcontribJquery(PythonPackage):
    """A sphinx extension which ensure that jQuery is installed with Sphinx."""

    homepage = "https://github.com/sphinx-contrib/jquery"
    pypi = "sphinxcontrib-jquery/sphinxcontrib-jquery-2.0.0.tar.gz"

    version("2.0.0",
            sha256=
            "8fb65f6dba84bf7bcd1aea1f02ab3955ac34611d838bcc95d4983b805b234daa")

    depends_on("python@3.5:", when="@2:", type=("build", "run"))
    depends_on("py-setuptools@63:", type=("build", "run"))
    depends_on("py-flit-core@3.7:", when="@3:", type="build")
