# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.cdo import Cdo as SpackCdo


class Cdo(SpackCdo):
    conflicts('%nvhpc@22.7')
