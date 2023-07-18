# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gridtools(Package):
    """The GridTools framework is a set of libraries and utilities to develop performance portable applications in the area of weather and climate."""

    homepage = "https://github.com/GridTools/gridtools.git"
    git = "git@github.com:GridTools/gridtools.git"

    maintainers = ['elsagermann']

    version('master', branch='master')
    version('1.1.3', commit='d33fa6fecee0a7bd9e080212c1038f0dbd31fe97')
    version('1.1.2', commit='685880444d4599cc0871e4ec8032e7cccd1755e0')
    version('1.1.0', commit='12ee09103bcd46edb978259b59e90d611f32ed01')
    version('1.0.3', commit='8468d2000ccec95d3a1c481664e6b41a0b038413')
    version('1.0.2', commit='2d42ea7d7639de1b52a2106e049a21cfea7192ea')
    version('1.0.1', commit='11053321adac080abee0c6d8399ed6a63479bb48')
    version('1.0.0', commit='5dfeace6f20eefa6633102533d5a0e1564361ecf')

    variant('build_type',
            default='Release',
            description='Build type',
            values=('Debug', 'Release', 'DebugRelease'))
    variant('shared_libs',
            default=False,
            description="Build shared librairies")
    variant('install_examples',
            default=False,
            description="Build with examples")
    variant('build_testing', default=False, description="Build with tests")
    variant('use_mpi', default=True, description="Build with using mpi")
    variant('no_boost_cmake',
            default=True,
            description="Build with no boost for CMake")
    variant('export_no_package_registery',
            default=True,
            description="Build with export no package registery")
    variant('enable_bindings_gerneration',
            default=True,
            description="Build with bindings generation")
    variant('cuda_arch',
            default='none',
            description='Build with cuda_arch',
            values=('80', '70', '60', '37'),
            multi=False)
    variant('cuda', default=True, description='Build with cuda or target gpu')

    depends_on('ncurses')
    depends_on('cmake@3.14.5:')
    depends_on('boost@1.67.0:')
    depends_on('mpi', type=('build', 'link', 'run'), when='~cuda')
    depends_on('mpi +cuda', type=('build', 'link', 'run'), when='+cuda')
    depends_on('cuda', type=('build', 'link', 'run'), when='+cuda')

    conflicts('%pgi@20:')
    conflicts('%pgi@:17')

    phases = ['install']

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
