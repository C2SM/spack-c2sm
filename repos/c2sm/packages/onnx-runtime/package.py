# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil


class OnnxRuntime(Package):
    '''

    ONNX Runtime is a cross-platform inference and training machine-learning accelerator.

    ONNX Runtime inference can enable faster customer experiences and lower costs, 
    supporting models from deep learning frameworks such as PyTorch and TensorFlow/Keras 
    as well as classical machine learning libraries such as scikit-learn, LightGBM, XGBoost, etc. 
    ONNX Runtime is compatible with different hardware, drivers, and operating systems, 
    and provides optimal performance by leveraging hardware accelerators where applicable alongside graph optimizations and transforms
    '''

    homepage = "https://github.com/microsoft/onnxruntime"
    url = "https://github.com/microsoft/onnxruntime/releases/download/v1.10.0/onnxruntime-linux-x64-1.10.0.tgz"

    version('1.10.0',
            sha256=
            'cc1753424114b3f7490be8b4f79e3b1aa205c57811c011fefa68c6577d634c63')

    maintainers = ['juckerj']

    phases = ['install']

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
