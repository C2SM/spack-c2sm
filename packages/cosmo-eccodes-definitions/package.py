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
#     spack install cosmo-eccodes-definitions
#
# You can edit this file again by typing:
#
#     spack edit cosmo-eccodes-definitions
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class CosmoEccodesDefinitions(Package):
    """To simplify the usage of the GRIB 2 format within the COSMO Consortium, a COSMO GRIB 2 Policy has been defined. One element of this policy is to define a unified ecCodes system for the COSMO community, which is compatible with all COSMO software. This unified system is split into two parts, the vendor distribution of the ecCodes, available from ECMWF and the modified samples and definitions used by the COSMO consortium, available in the current repository."""

    homepage = "https://github.com/COSMO-ORG/eccodes-cosmo-resources.git"
    url      = "git@github.com:COSMO-ORG/eccodes-cosmo-resources.git"
    git      = 'git@github.com:COSMO-ORG/eccodes-cosmo-resources.git'

    maintainers = ['egermann']

    version('2.14.1.2', commit='15f3a862d0349f4fc332e383c69acbed71b7804d')
    version('2.14.1.1', commit='708d7a4590964c094b6df7fec4a9ccb2981de9fa')

    variant('aec', default=True, description='Enable Adaptive Entropy Coding for decoding/encoding')

    depends_on('eccodes@2.14.1 ~aec', when='~aec', type='build')

    def setup_run_environment(self, env):
        eccodes_definition_path = self.spec['cosmo-eccodes-definitions'].prefix + '/cosmoDefinitions/definitions/:' + self.spec['eccodes'].prefix + '/share/eccodes/definitions/'
        env.prepend_path('GRIB_DEFINITION_PATH', eccodes_definition_path)
        eccodes_samples_path = self.spec['cosmo-eccodes-definitions'].prefix + '/cosmoDefinitions/samples/'
        env.prepend_path('GRIB_SAMPLES_PATH', eccodes_samples_path)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def install(self, spec, prefix):
        mkdir(prefix.cosmoDefinitions)
        mkdir(prefix.cosmoDefinitions + '/definitions')
        mkdir(prefix.cosmoDefinitions + '/samples')
        install_tree('definitions', prefix.cosmoDefinitions + '/definitions')
        install_tree('samples', prefix.cosmoDefinitions + '/samples')
