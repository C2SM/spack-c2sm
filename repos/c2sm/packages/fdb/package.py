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

    def cmake_args(self):
        enable_build_tools = "+tools" in self.spec

        args = [
            self.define("CTEST_OUTPUT_ON_FAILURE", '1'),
            self.define("ENABLE_FDB_BUILD_TOOLS", enable_build_tools),
            self.define("ENABLE_BUILD_TOOLS", enable_build_tools),
            # We cannot disable the FDB backend in indexed filesystem with
            # table-of-contents because some default test programs and tools
            # cannot be built without it:
            self.define("ENABLE_TOCFDB", True),
            self.define("ENABLE_LUSTRE", "backends=lustre" in self.spec),
            self.define("ENABLE_PMEMFDB", False),
            self.define("ENABLE_RADOSFDB", False),
            # The tests download additional data (~10MB):
            self.define("ENABLE_TESTS", self.run_tests),
            # We do not need any experimental features:
            self.define("ENABLE_EXPERIMENTAL", False),
            self.define("ENABLE_SANDBOX", False),
        ]
        return args
