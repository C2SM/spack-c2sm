# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import os


class PytorchFortran(CMakePackage):
    '''
    Pytorch Fortran bindings - Fortran Frontend

    The goal of this code is to provide Fortran HPC codes with a simple way to use 
    Pytorch deep learning framework. We want Fortran developers to take advantage 
    of rich and optimized Torch ecosystem from within their existing codes.
    '''

    homepage = "https://github.com/alexeedm/pytorch-fortran"
    url = "https://github.com/alexeedm/pytorch-fortran.git"

    version('0.4', git=url, tag='v0.4')

    maintainers = ['juckerj']

    depends_on('pytorch-fortran-proxy')

    root_cmakelists_dir = 'src/f90_bindings'

    def cmake_args(self):
        args = [self.define('OPENACC', 1)]

        return args

    @property
    def libs(self):
        libraries = ['libpytorch_fort_proxy']

        libs = find_libraries(libraries,
                              root=self.prefix,
                              shared=True,
                              recursive=True)

        if libs and len(libs) == len(libraries):
            return libs

        msg = 'Unable to recursively locate shared {0} libraries in {1}'
        raise spack.error.NoLibrariesError(
            msg.format(self.spec.name, self.spec.prefix))

    @run_after('install')
    def link_fmod_into_include(self):
        mod = 'torch_ftn.mod'
        src = os.path.join(self.prefix.include, 'mod_files', mod)
        dest = os.path.join(self.prefix.include, mod)
        os.symlink(src, dest)
