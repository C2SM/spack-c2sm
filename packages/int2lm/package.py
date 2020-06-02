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

import os

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

    depends_on('cosmo-grib-api-definitions', when='~eccodes')
    depends_on('cosmo-eccodes-definitions@2.14.1.2 ~aec', when='+eccodes')
    depends_on('libgrib1@master slave=tsa', when='slave=tsa')
    depends_on('libgrib1@master slave=daint', when='slave=daint')
    depends_on('libgrib1@master slave=kesch', when='slave=kesch')
    depends_on('mpi', type=('build', 'run'), when='+parallel')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    
    variant('debug', default=False, description='Build debug INT2LM')
    variant('eccodes', default=False, description='Build with eccodes instead of grib-api')
    variant('parallel', default=True, description='Build parallel INT2LM')
    variant('pollen', default=False, description='Build with pollen enabled')
    variant('slave', default='tsa', description='Build on slave tsa, daint or kesch', multi=False)
    variant('verbose', default=False, description='Build with verbose enabled')

    def setup_environment(self, spack_env, run_env):
        # Grib-api. eccodes library
        if '~eccodes' in self.spec:
            grib_prefix = self.spec['cosmo-grib-api'].prefix
            grib_definition_prefix = self.spec['cosmo-grib-api-definitions'].prefix
            spack_env.set('GRIBAPIL', '-L' + grib_prefix + '/lib -lgrib_api_f90 -lgrib_api -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
        else:
            grib_prefix = self.spec['eccodes'].prefix
            grib_definition_prefix = self.spec['cosmo-grib-api-definitions'].prefix
            spack_env.set('GRIBAPIL', '-L' + grib_prefix + '/lib -leccodes_f90 -leccodes -L' + self.spec['jasper'].prefix + '/lib64 -ljasper')
        spack_env.set('GRIBAPII', '-I' + grib_prefix + '/include')
        spack_env.set('GRIB_DEFINITION_PATH', grib_definition_prefix + '/cosmoDefinitions/definitions/:' + grib_prefix + '/share/grib_api/definitions/')
        spack_env.set('GRIB_SAMPLES_PATH', grib_definition_prefix + '/cosmoDefinitions/samples/')

        # Netcdf library
        if self.spec.variants['slave'].value == 'daint':
            spack_env.set('NETCDFL', '-L$(NETCDF_DIR)/lib -lnetcdff -lnetcdf')
            spack_env.set('NETCDFI', '-I$(NETCDF_DIR)/include')
        else:
            spack_env.set('NETCDFL', '-L' + self.spec['netcdf-fortran'].prefix + '/lib -lnetcdff -L' + self.spec['netcdf-c'].prefix + '/lib64 -lnetcdf')
            spack_env.set('NETCDFI', '-I' + self.spec['netcdf-fortran'].prefix + '/include')

        # Grib1 library
        if self.compiler.name == 'gcc':
            spack_env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_gnu')
        elif self.compiler.name == 'cce':
            spack_env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_cray')
        else:
            spack_env.set('GRIBDWDL', '-L' + self.spec['libgrib1'].prefix + '/lib -lgrib1_' + self.compiler.name)

        # MPI library
        if self.spec['mpi'].name == 'openmpi':
            spack_env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpi_mpifh')
            spack_env.set('MPII', '-I'+ self.spec['mpi'].prefix + '/include')
        else:
            if self.compiler.name == 'gcc':
                spack_env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpich_gnu')
            elif self.compiler.name == 'cce':
                spack_env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpich_cray')
            else:
                spack_env.set('MPIL', '-L' + self.spec['mpi'].prefix + ' -lmpich_' + self.compiler.name)
            spack_env.set('MPII', '-I'+ self.spec['mpi'].prefix + '/include')

        # Compiler & linker variables
        if self.compiler.name == 'pgi':
            spack_env.set('F90', 'pgf90 -D__PGI_FORTRAN__')
            spack_env.set('LD', 'pgf90 -D__PGI_FORTRAN__')
        elif self.compiler.name == 'cce':
            spack_env.set('F90', 'ftn -D__CRAY_FORTRAN__')
            spack_env.set('LD', 'ftn -D__CRAY_FORTRAN__')
        else:
            spack_env.set('F90', self.spec['mpi'].mpifc)
            spack_env.set('LD', self.spec['mpi'].mpifc)

        # set runtime variables
        run_env_variables = {}
        run_env_variables['UCX_MEMTYPE_CACHE'] = 'n'
        run_env_variables['UCX_TLS'] = 'rc_x,ud_x,mm,shm,cma'
        for key in run_env_variables:
            spack_env.set(key, run_env_variables[key])

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

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.test)
        install('int2lm', prefix.bin)
        install_tree('test', prefix.test)
        install('int2lm', prefix.test + '/testsuite')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        with working_dir(prefix.test + '/testsuite/data'):
            get_test_data = './get_data.sh'
            os.system(get_test_data)
        with working_dir(prefix.test + '/testsuite'):
            if '+eccodes' in self.spec:
                run_testsuite = 'sbatch -W submit.' + self.spec.variants['slave'].value + '.slurm.eccodes'
            else:
                run_testsuite = 'sbatch -W submit.' + self.spec.variants['slave'].value + '.slurm'
            os.system(run_testsuite)
            cat_testsuite = 'cat testsuite.out'
            os.system(cat_testsuite)
