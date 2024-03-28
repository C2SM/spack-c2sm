# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *
import llnl.util.filesystem as fs
from spack.build_systems.cmake import CMakeBuilder
import os


class Infero(CMakePackage):
    '''
    Infero runs a pre-trained ML model for inference. It can be deployed on a HPC system 
    without the need for high-level python libraries (e.g. TensorFlow, PyTorch, etc..)
    '''

    homepage = "https://github.com/ecmwf-projects/infero.git"
    url = "https://github.com/ecmwf-projects/infero.git"

    version('0.1.2',
            git=url,
            commit='4c229a16ce75a249c83cbf43e0c953a7a42f2f83')

    maintainers = ['juckerj']

    variant('quiet', description='Disable calls to Log::info', default=False)
    variant('tf_c', description='Enable tensorflow-c backend', default=False)
    variant('onnx', description='Enable ONNX backend', default=False)

    depends_on('eckit@1.20.2')
    depends_on('fckit@0.9.0')
    depends_on('ecbuild', type=('build'))
    depends_on('tensorflowc', when='+tf_c')
    depends_on('onnx-runtime', when='+onnx')

    patch('comment_out_log-level_info.patch', when='@0.1.2 +quiet')

    @property
    def libs(self):
        libraries = ['libinfero', 'libinferof']

        libs = find_libraries(libraries,
                              root=self.prefix,
                              shared=True,
                              recursive=True)

        if libs and len(libs) == len(libraries):
            return libs

        msg = 'Unable to recursively locate shared {0} libraries in {1}'
        raise spack.error.NoLibrariesError(
            msg.format(self.spec.name, self.spec.prefix))


class CMakeBuilder(CMakeBuilder):

    def check(self):
        """Search the CMake-generated files for the targets ``test`` and ``check``,
        and runs them if found.
        """
        with fs.working_dir(self.build_directory):
            make.jobs = 1
            self.pkg._if_make_target_execute("test",
                                             jobs_env="CTEST_PARALLEL_LEVEL")
            self.pkg._if_make_target_execute("check")

    def cmake_args(self):
        args = [
            self.define('CMAKE_PREFIX_PATH',
                        f'{self.spec["ecbuild"].prefix}/share/ecbuild/cmake'),
            self.define('ENABLE_MPI', False),
            self.define('ENABLE_FCKIT', True),

            # enable Fortran interfaces
            self.define(f'FCKIT_ROOT', f'{self.spec["fckit"].prefix}')
        ]

        # enable TF-C backend
        if "+tf_c" in self.spec:
            args.extend([
                self.define('ENABLE_TF_C', True),
                self.define(f'TENSORFLOWC_ROOT',
                            f'{self.spec["tensorflowc"].prefix}')
            ])

        #enable ONNX backend
        if "+onnx" in self.spec:
            args.extend([
                self.define('ENABLE_ONNX', True),
                self.define(f'ONNX_ROOT',
                            f'{self.spec["onnx-runtime"].prefix}')
            ])
        return args

    @run_after('install')
    def link_fmod_into_include(self):
        mod = 'inferof.mod'
        src = os.path.join(self.prefix, 'module/infero', mod)
        dest = os.path.join(self.prefix.include, mod)
        os.symlink(src, dest)
