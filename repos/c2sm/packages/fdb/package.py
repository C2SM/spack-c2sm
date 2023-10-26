# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fdb(SpackFdb):
    """FDB (Fields DataBase) is a domain-specific object store developed at
    ECMWF for storing, indexing and retrieving GRIB data."""

    version("5.11.23", 
            sha256=
            "09b1d93f2b71d70c7b69472dfbd45a7da0257211f5505b5fcaf55bfc28ca6c65")
    version("5.11.17",
            sha256=
            "375c6893c7c60f6fdd666d2abaccb2558667bd450100817c0e1072708ad5591e")
