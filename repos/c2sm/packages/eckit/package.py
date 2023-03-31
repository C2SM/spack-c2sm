# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
from spack.pkg.builtin.eckit import Eckit as SpackEckit


class Eckit(SpackEckit):

    git = 'https://github.com/ecmwf/eckit.git'
    version('1.20.0', branch='1.20.0')
