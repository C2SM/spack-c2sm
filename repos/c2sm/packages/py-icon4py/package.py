# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import inspect

from spack import *
from spack.build_systems.python import PythonPipBuilder

import llnl.util.filesystem as fs


class PyIcon4py(PythonPackage):
    """ICON4Py contains Python (GT4Py) implementations of ICON (inspired) 
    components for weather and climate models."""

    url = "git@github.com:C2SM/icon4py.git"
    git = 'git@github.com:C2SM/icon4py.git'

    homepage = "https://github.com/C2SM/icon4py"

    maintainers = ['samkellerhals']

    version('main', branch='main', git=git)
    version('0.0.3', tag='v0.0.3', git=git)
    version('0.0.4', tag='v0.0.4', git=git)

    depends_on('py-wheel', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-tabulate@0.8.9:', type=('build', 'run'))
    # TODO: push new version to Spack official
    depends_on('py-fprettify@0.3.7:', type=('build', 'run'))
    depends_on('py-gt4py', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('boost@1.65.1:', type=('build', 'run'))

    # cmake in unit-tests needs this path
    def setup_build_environment(self, env):
        env.set("CMAKE_INCLUDE_PATH", self.spec['boost'].prefix.include)

    def test(self):
        # check if all installed module can be imported
        super().test()

        # unit tests
        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '--cov',
               '--cov-append')


class PythonPipBuilder(PythonPipBuilder):

    def install(self, pkg, spec, prefix):
        """Install everything from build directory."""

        args = PythonPipBuilder.std_args(pkg) + ["--prefix=" + prefix]

        for key, value in self.config_settings(spec, prefix).items():
            if spec["py-pip"].version < Version("22.1"):
                raise SpecError(
                    "'{}' package uses 'config_settings' which is only supported by "
                    "pip 22.1+. Add the following line to the package to fix this:\n\n"
                    '    depends_on("py-pip@22.1:", type="build")'.format(
                        spec.name))

            args.append("--config-settings={}={}".format(key, value))

        for option in self.install_options(spec, prefix):
            args.append("--install-option=" + option)
        for option in self.global_options(spec, prefix):
            args.append("--global-option=" + option)

        if pkg.stage.archive_file and pkg.stage.archive_file.endswith(".whl"):
            args.append(pkg.stage.archive_file)
        else:
            args.append(".")

        pip = inspect.getmodule(pkg).pip

        if self.spec.version == ver('0.0.3'):
            build_dirs = [
                'common', 'pyutils', 'testutils', 'liskov', 'atm_dyn_iconam'
            ]
        else:
            build_dirs = ['common', 'atm_dyn_iconam', 'tools']

        for dir in build_dirs:
            with fs.working_dir(os.path.join(self.build_directory, dir)):
                pip(*args)
