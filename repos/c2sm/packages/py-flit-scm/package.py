# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *

# TODO (magdalena) remove after upgrade to spack 0.20.0
#   copy of https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-flit-scm/package.py
class PyFlitScm(PythonPackage):
    """A PEP 518 build backend that uses setuptools_scm
    to generate a version file from your version control system,
    then flit to build the package.
    """

    homepage = "https://gitlab.com/WillDaSilva/flit_scm"
    pypi = "flit-scm/flit_scm-1.7.0.tar.gz"

    version("1.7.0", sha256="961bd6fb24f31bba75333c234145fff88e6de0a90fc0f7e5e7c79deca69f6bb2")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-flit-core@3.5:3", type=("build", "run"))
    depends_on("py-setuptools-scm@6.4:", type=("build", "run"))
    depends_on("py-tomli", when="^python@:3.10", type=("build", "run"))