# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class AtlasUtilities(CMakePackage):
    """This repoistory contains some utilities to transform Atlas meshes as well as the first ICON stencil prototype computing a Laplacian."""

    homepage = 'https://github.com/mroethlin/AtlasUtilities'
    url      = "https://github.com/mroethlin/AtlasUtilities"
    git      = 'https://github.com/mroethlin/AtlasUtilities'
    maintainers = ['cosunae']

    version('master', branch='master')

    depends_on('atlas@0.22.0')
    depends_on('eckit')
    depends_on('netcdf-cxx4')
    depends_on('netcdf-c')

    variant('build_type', default='Release', description='Build type', values=('Debug', 'Release', 'DebugRelease'))

    def cmake_args(self):
        args = []
        spec = self.spec
        args.append('-DCMAKE_MODULE_PATH={0}/share/ecbuild/cmake'.
                    format(spec['ecbuild'].prefix))
        args.append('-Deckit_DIR={0}'.format(spec['eckit'].prefix))
        args.append('-Datlas_DIR={0}'.format(spec['atlas'].prefix))
        args.append('-Dnetcdfcxx4_DIR={0}'.format(spec['netcdf-cxx4'].prefix))
        args.append('-Dnetcdf_DIR={0}'.format(spec['netcdf-c'].prefix))
        args.append('-DCMAKE_BUILD_TYPE={0}'.format(self.spec.variants['build_type'].value))

        return args

