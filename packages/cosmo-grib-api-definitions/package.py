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
#     spack install cosmo-grib-api-definitions
#
# You can edit this file again by typing:
#
#     spack edit cosmo-grib-api-definitions
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class CosmoGribApiDefinitions(Package):
    """To simplify the usage of the GRIB 2 format within the COSMO Consortium, a COSMO GRIB 2 Policy has been defined. One element of this policy is to define a unified GRIB API system for the COSMO community, which is compatible with all COSMO software. This unified system is split into two parts, the vendor distribution of the GRIB API, available from ECMWF or from the repository libgrib-api-vendor, and the modified samples and definitions used by the COSMO consortium, available in the current repository."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/elsagermann/libgrib-api-cosmo-resources.git"
    url      = "git@github.com:elsagermann/libgrib-api-cosmo-resources.git"

    git      = 'git@github.com:elsagermann/libgrib-api-cosmo-resources.git'
    maintainers = ['elsagermann']

    version('1.20.0.2', commit='06f61f95ca2f5f0ddea668d82429331927ce81dc')
    
    depends_on('cosmo-grib-api@1.20.0.2', when='@1.20.0.2')

    def install(self, spec, prefix):
        mkdir(prefix.cosmoDefinitions)
        mkdir(prefix.cosmoDefinitions + '/definitions')
        mkdir(prefix.cosmoDefinitions + '/samples')
        install_tree('definitions', prefix.cosmoDefinitions + '/definitions')
        install_tree('samples', prefix.cosmoDefinitions + '/samples')
