# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.fdb import Fdb as SpackFdb


class Fdb(SpackFdb):
    """FDB (Fields DataBase) is a domain-specific object store developed at
    ECMWF for storing, indexing and retrieving GRIB data."""

    version("5.11.17",
            sha256=
            "375c6893c7c60f6fdd666d2abaccb2558667bd450100817c0e1072708ad5591e")

    depends_on("ecbuild@3.7:", type="build", when="@5.11.6:")

    @property
    def libs(self):
        return find_libraries("libfdb5",
                              root=self.prefix,
                              shared=True,
                              recursive=True)

    def setup_build_environment(self, env):
        env.set('CTEST_OUTPUT_ON_FAILURE', 1)
