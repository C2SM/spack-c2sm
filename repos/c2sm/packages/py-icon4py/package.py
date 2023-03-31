# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import inspect


class PyIcon4py(PythonPackage):
    """ICON4Py contains Python (GT4Py) implementations of ICON (inspired) 
    components for weather and climate models."""

    url = "git@github.com:C2SM/icon4py.git"

    homepage = "https://github.com/C2SM/icon4py"

    maintainers = ['samkellerhals']

    version('main', branch='main', git='ssh://git@github.com/C2SM/icon4py.git')

    depends_on('py-wheel', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-tabulate@0.8.9:', type=('build', 'run'))
    # TODO: push new version to Spack official
    depends_on('py-fprettify@0.3.7:', type=('build', 'run'))
    depends_on('py-gt4py', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))

    def install(self, spec, prefix):
        """Install everything from build directory."""

        args = PythonPackage._std_args(self) + ['--prefix=' + prefix]

        for option in self.install_options(spec, prefix):
            args.append('--install-option=' + option)
        for option in self.global_options(spec, prefix):
            args.append('--global-option=' + option)

        if self.stage.archive_file and self.stage.archive_file.endswith(
                '.whl'):
            args.append(self.stage.archive_file)
        else:
            args.append('.')

        pip = inspect.getmodule(self).pip
        build_dirs = ['common', 'pyutils', 'testutils', 'atm_dyn_iconam']
        for dir in build_dirs:
            with working_dir(os.path.join(self.stage.source_path, dir)):
                pip(*args)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '--cov',
               '--cov-append')
