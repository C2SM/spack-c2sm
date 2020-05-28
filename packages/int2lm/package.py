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
#     spack install int2lm
#
# You can edit this file again by typing:
#
#     spack edit int2lm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Int2lm(MakefilePackage):
    """INT2LM performs the interpolation from coarse grid model data to initial
    and/or boundary data for the COSMO-Model."""

    homepage = "http://www.cosmo-model.org/content/model/"
    url      = "https://github.com/MeteoSwiss-APN/int2lm/archive/v2.7.2.tar.gz"
    git      = 'git@github.com:MeteoSwiss-APN/int2lm.git'

    maintainers = ['egermann']
    
    version('master', branch='master')
    version('v2.7.2', commit='7a460906e826142be1fb9338d2210ccf7566d5a2')
    version('v2.7.1', commit='ee0780f86ecc676a9650170f361b92ff93379071')
    version('v2.6.2', commit='07690dab05c931ba02c947ec32c988eea65898f8')

    depends_on('cosmo-grib-api-definitions')
    depends_on('libgrib1 slave=tsa', when='slave=tsa')
    depends_on('libgrib1 slave=daint', when='slave=daint')
    depends_on('libgrib1 slave=kesch', when='slave=kesch')
    depends_on('mpi', type=('build', 'run'), when='+parallel')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    
    variant('debug', default=False, description='Build debug INT2LM')
    variant('parallel', default=True, description='Build parallel INT2LM')
    variant('pollen', default=False, description='Build with pollen enabled')
    variant('slave', default='tsa', description='Build on slave tsa, daint or kesch', multi=False)
    variant('verbose', default=False, description='Build with verbose enabled')


    @property
    def build_targets(self):
        build = []
        if self.spec.variants['verbose'].value:
            build.append('VERBOSE=1')
        if self.spec.variants['pollen'].value:
            build.append('ART=1')
        MakeFileTarget = ''
        if '+parallel' in self.spec:
            MakeFileTarget += 'par'
        else:
            MakeFileTarget += 'seq'
        if '+debug' in self.spec:
            MakeFileTarget += 'debug'
        else:
            MakeFileTarget += 'opt'
                                                                                                        build.append(MakeFileTarget)
        return build

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        OptionsFileName= 'Options'
        if self.compiler.name == 'gcc':
            OptionsFileName += '.gnu'
        elif self.compiler.name == 'pgi':
            OptionsFileName += '.pgi'
        elif self.compiler.name == 'cce':
            OptionsFileName += '.cray'
         makefile.filter('/Options.*', '/' + OptionsFileName)
