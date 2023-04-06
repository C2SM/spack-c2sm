# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFactoryBoy(PythonPackage):
    """factory_boy is a fixtures replacement based on thoughtbot factory_bot"""

    pypi = "factory_boy/factory_boy-3.2.1.tar.gz"

    version("3.2.1",
            sha256=
            "a98d277b0c047c75eb6e4ab8508a7f81fb03d2cb21986f627913546ef7a2a55e")

    depends_on("python@3.7:")
    depends_on('py-faker@0.7.0:', type=('build', 'run'))
    depends_on("py-setuptools", type="build")
