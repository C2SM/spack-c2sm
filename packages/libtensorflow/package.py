# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtensorflow(Package):
    '''
    Tensorflow-C for GPU's
    '''

    homepage = "https://www.tensorflow.org/install/lang_c"
    url = "https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-gpu-linux-x86_64-2.6.0.tar.gz"

    maintainers = ['juckerj']

    version('2.6.0',
            sha256=
            '1a93057baa9f831a00a5935132c8e7438ee4ddfc166779dca51aae8c4a40870b')

    phases = ['install']

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
