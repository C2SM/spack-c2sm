# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.libxml2 import Libxml2 as SpackLibxml2


class Libxml2(SpackLibxml2):
    conflicts('%nvhpc @21.1:')
    conflicts('%pgi')
