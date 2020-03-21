##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class CosmoDycore(CMakePackage):
    """FIXME: Put a proper description of your package here."""
    
    homepage = "https://github.com/COSMO-ORG/cosmo/tree/master/dycore"
    git      = "git@github.com:COSMO-ORG/cosmo.git"
    maintainers = ['elsagermann']
    
    version('master', branch='master')

    variant('build_tests', default=True, description="Compile Dycore unittests & regressiontests")
    variant('cosmo_target', default='gpu', description='Build target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('cuda_arch', default='none', description='Build with cuda_arch', values=('sm_70', 'sm_60', 'sm_37'), multi=False)
    variant('slave', default='tsa', description='Build on slave tsa or daint', multi=False)
    variant('data_path', default='.', description='Serialization data path', multi=False)
    
    depends_on('gridtools@1.1.3 cosmo_target=gpu', when='cosmo_target=gpu')
    depends_on('gridtools@1.1.3 cosmo_target=cpu', when='cosmo_target=cpu')
    depends_on('boost@1.67.0')
    depends_on('serialbox@2.6.0', when='+build_tests')
    depends_on('mpi', type=('build', 'run'))
    depends_on('cuda', type=('build', 'run'))
    depends_on('slurm', type='run')
    depends_on('cmake@3.12:%gcc', type='build')

    root_cmakelists_dir='dycore'
    
    def setup_environment(self, spack_env, run_env):
        if self.spec.variants['slave'].value == 'daint':
            spack_env.set('MPICH_RDMA_ENABLED_CUDA', '1')
            spack_env.set('MPICH_G2G_PIPELINE', '64')
        spack_env.set('UCX_MEMTYPE_CACHE', 'n')
        spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cuda_copy,cuda_ipc,cma')
        spack_env.set('GRIDTOOLS_ROOT', self.spec['gridtools'].prefix)
        if self.spec.variants['build_tests'].value:
          spack_env.set('SERIALBOX_ROOT', self.spec['serialbox'].prefix)

    def cmake_args(self):
      spec = self.spec

      args = []

      GridToolsDir = spec['gridtools'].prefix + '/lib/cmake'
      
      args.append('-DGridTools_DIR={0}'.format(GridToolsDir))  
      args.append('-DCMAKE_BUILD_TYPE=Release')
      args.append('-DCMAKE_INSTALL_PREFIX={0}'.format(self.prefix))
      args.append('-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON')
      args.append('-DBoost_USE_STATIC_LIBS=ON')
      args.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))
      args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=OFF')
      args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
    
      if spec.variants['real_type'].value == 'float':
        args.append('-DPRECISION=float')
      else:
        args.append('-DPRECISION=double')
      
      if not spec.variants['build_tests'].value:
          args.append('-DBUILD_TESTING=OFF')
      else:
          args.append('-DBUILD_TESTING=ON')
          SerialBoxRoot = spec['serialbox'].prefix + '/cmake'
          args.append('-DSerialbox_DIR={0}'.format(SerialBoxRoot))

      # target=gpu
      if self.spec.variants['cosmo_target'].value == 'gpu':
        args.append('-DENABLE_CUDA=ON')
        args.append('-DCUDA_ARCH={0}'.format(self.spec.variants['cuda_arch'].value))
        args.append('-DDYCORE_TARGET_ARCHITECTURE=CUDA')
      # target=cpu
      else:
        args.append('-DENABLE_CUDA=OFF')
        args.append('-DDYCORE_TARGET_ARCHITECTURE=x86')

      return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        if '+build_tests' in self.spec:
            with working_dir(self.build_directory + '/src'):
                mkdir(prefix.tests)
                install_tree('tests', prefix.tests)
            with working_dir(prefix + '/tests/unittests'):
                if self.spec.variants['slave'].value == 'tsa':
                    run_unittests = Executable('srun -n 1 -p normal --gres=gpu:1 ./unittests  --gtest_filter=-TracerBindings.TracerVariable')
                if self.spec.variants['slave'].value == 'daint':
                    run_unittests = Executable('srun --time=00:05:00 -C gpu -p normal -A g110 -N 1 ./unittests  --gtest_filter=-TracerBindings.TracerVariable')
                run_unittests()
            with working_dir(prefix + '/tests/unittests/gcl_fortran'):
                if self.spec.variants['slave'].value == 'tsa':
                    run_unitests_gcl_bindings = Executable('srun -n 4 -p normal --gres=gpu:4 ./unittests_gcl_bindings')
                if self.spec.variants['slave'].value == 'daint':
                    run_unitests_gcl_bindings = Executable('srun --time=00:05:00 -C gpu -p normal -A g110 -N 4 ./unittests_gcl_bindings')
                run_unitests_gcl_bindings()
            with working_dir(prefix + '/tests/regression'):
                testlist=['cosmo1_cp_test1', 'cosmo1_test3', 'cosmo1_test3_all_off', 'cosmo1_test3_coldpool_uv', 'cosmo1_test3_non_default', 'cosmo1_test3_vdiffm1', 'cosmo7_test_3', 'cosmo7_test_namelist_irunge_kutta2', 'cosmoe_test_sppt', 'cosmoe_test_sppt_coldpools', 'cosmoe_test_sppt_bechtold']
                for test in testlist:
                    if self.spec.variants['slave'].value == 'tsa':
                        run_regression_test = Executable('srun -n 1 -p debug --gres=gpu:1 ./regression_tests -p ' + self.spec.variants['data_path'].value + self.spec.variants['real_type'].value + '/' + test + ' --gtest_filter=-DycoreUnittest.Performance')
                    if self.spec.variants['slave'].value == 'daint':
                        run_regression_test = Executable('srun --time=00:05:00 -C gpu -p normal -A g110 -N 1 ./regression_tests -p ' + self.spec.variants['data_path'].value + self.spec.variants['real_type'].value + '/' + test + ' --gtest_filter=-DycoreUnittest.Performance')
                    run_regression_test()
                     


