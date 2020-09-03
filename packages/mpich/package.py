# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os
import sys
from spack.pkg.builtin.mpich import Mpich as SpackMpich

class Mpich(SpackMpich):

    provides('mpicuda')
