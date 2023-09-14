# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install omni-xmod-pool
#
# You can edit this file again by typing:
#
#     spack edit omni-xmod-pool
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class OmniXmodPool(Package):
    """Sets of generic xmod file for OMNI Compiler"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "omni-xmod-pool"

    git = 'git@github.com:claw-project/omni-xmod-pool.git'

    maintainers = ['elsagermann']

    version('0.1', commit='9f6a713fcf6f8004ce15a149f1d819a1f18bfb30')

    def install(self, spec, prefix):
        mkdir(prefix.omniXmodPool)
        pool_list = ['grib_api', 'mpi', 'netcdf', 'serialbox']
        for pckg in pool_list:
            mkdir(prefix.omniXmodPool + '/' + pckg)
            install_tree(pckg, prefix.omniXmodPool + '/' + pckg)
