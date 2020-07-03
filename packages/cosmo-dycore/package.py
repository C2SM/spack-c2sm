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
import subprocess, re

def get_releases(repo):
        git_obj = subprocess.run(["git","ls-remote",repo], stdout=subprocess.PIPE)
        git_tags = [re.match('refs/tags/(.*)', x.decode('utf-8')).group(1) for x in git_obj.stdout.split() if re.match('refs/tags/(.*)', x.decode('utf-8'))]
        return git_tags
def dycore_tags(repo):
    tags = get_releases(repo)
    for tag in tags:
        version(tag, git=repo, tag=tag)

class CosmoDycore(CMakePackage):
    """C++ dycore of cosmo based on GridTools library"""
    
    homepage = "https://github.com/COSMO-ORG/cosmo/tree/master/dycore"
    git      = "git@github.com:COSMO-ORG/cosmo.git"
    maintainers = ['elsagermann']
    
    version('master', branch='master')
    version('dev-build', branch='master')
    version('mch', git='git@github.com:MeteoSwiss-APN/cosmo.git', branch='mch')
    version('gt2', git='git@github.com:havogt/cosmo.git', branch='gt2')

    dycore_tags("git@github.com:MeteoSwiss-APN/cosmo.git")

    variant('build_type', default='Release', description='Build type', values=('Debug', 'Release', 'DebugRelease'))
    variant('build_tests', default=True, description="Compile Dycore unittests & regressiontests")
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('slave', default='tsa', description='Build on slave tsa or daint', multi=False)
    variant('pmeters', default=False, description="Enable the performance meters for the dycore stencils")
    variant('data_path', default='.', description='Serialization data path', multi=False)
    variant('production', default=False, description='Force all variants to be the ones used in production')
    variant('cuda_arch', default='none', description='Build with cuda_arch', values=('70', '60', '37'), multi=False)
    variant('cuda', default=True, description='Build with cuda or target gpu')
    variant('slurm_args', default='"-p debug -n {0} --gres=gpu:{0}"', description='Slurm arguments for testing')

    depends_on('gridtools@1.1.3 +cuda', when='+cuda')
    depends_on('gridtools@1.1.3 ~cuda cuda_arch=none', when='~cuda')
    depends_on('boost@1.67.0')
    depends_on('serialbox@2.6.0', when='+build_tests')
    depends_on('mpi', type=('build', 'run'))
    depends_on('slurm', type='run')
    depends_on('cmake@3.12:%gcc', type='build')
    depends_on('cuda', when='+cuda', type=('build', 'run'))

    conflicts('+production', when='build_type=Debug')
    conflicts('+production', when='cosmo_target=cpu')
    conflicts('+production', when='+pmeters')

    root_cmakelists_dir='dycore'
    
    def setup_environment(self, spack_env, run_env):
        if self.spec['mpi'].name == 'mpich':
            spack_env.set('MPICH_G2G_PIPELINE', '64')
            if '+cuda' in self.spec:
                spack_env.set('MPICH_RDMA_ENABLED_CUDA', '1')
        spack_env.set('UCX_MEMTYPE_CACHE', 'n')
        if '+cuda' in self.spec:
            spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cuda_copy,cuda_ipc,cma')
        else:
            spack_env.set('UCX_TLS', 'rc_x,ud_x,mm,shm,cma')

    def cmake_args(self):
      spec = self.spec

      args = []
      
      if not '@gt2' in spec:
          GridToolsDir = spec['gridtools'].prefix + '/lib/cmake'
          args.append('-DGridTools_DIR={0}'.format(GridToolsDir))

      args.append('-DCMAKE_BUILD_TYPE={0}'.format(self.spec.variants['build_type'].value))
      args.append('-DCMAKE_INSTALL_PREFIX={0}'.format(self.prefix))
      args.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))
      args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
      args.append('-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON')
      args.append('-DBoost_USE_STATIC_LIBS=ON')

      if spec.variants['pmeters'].value:
          args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=ON')
      else:
          args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=OFF')
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
      if '+cuda' in spec:
          args.append('-DENABLE_CUDA=ON')
          cuda_arch = spec.variants['cuda_arch'].value
          if cuda_arch is not None:
              args.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch))
          if '@gt2' in spec:
              args.append('-DDYCORE_TARGET_ARCHITECTURE=gpu')
          else:
              args.append('-DDYCORE_TARGET_ARCHITECTURE=CUDA')
      # target=cpu
      else:
        args.append('-DENABLE_CUDA=OFF')
        if '@gt2' in spec:
            args.append('-DDYCORE_TARGET_ARCHITECTURE=cpu_ifirst')
        else:
            args.append('-DDYCORE_TARGET_ARCHITECTURE=x86')

      return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
      if '+build_tests' in self.spec: 
            subprocess.run(['./test_dycore.py',  str(self.spec),  self.build_directory], cwd = self.root_cmakelists_dir + '/test/tools')
