# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil


class Libtorch(Package):
    '''
    '''

    homepage = "https://www.tensorflow.org/install/lang_c"
    url = "https://download.pytorch.org/libtorch/cu117/libtorch-cxx11-abi-shared-with-deps-2.0.1%2Bcu117.zip"

    maintainers = ['juckerj']

    version('1.0')

    phases = ['install']

    manual_download = True

    def install(self, spec, prefix):
        # can't use Spack convenience-function 'install_tree' because it uses
        # shutil.copy2 under the hood. For an unknown reason installing from
        # the unzipped tarbal only works using shutil.copy.
        shutil.copytree('lib',
                        prefix.lib,
                        symlinks=True,
                        copy_function=shutil.copy)
        shutil.copytree('include',
                        prefix.include,
                        symlinks=True,
                        copy_function=shutil.copy)
        shutil.copytree('share',
                        prefix.share,
                        symlinks=True,
                        copy_function=shutil.copy)
        shutil.copytree('bin',
                        prefix.bin,
                        symlinks=True,
                        copy_function=shutil.copy)
