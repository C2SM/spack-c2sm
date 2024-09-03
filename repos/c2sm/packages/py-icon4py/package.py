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

    maintainers = ['agopal', 'samkellerhals']

    version('main', branch='main', git=git)
    version('0.0.10', tag='v0.0.10', git=git)
    version('0.0.11', tag='v0.0.11', git=git)
    version('0.0.12', tag='v0.0.12', git=git)
    version('0.0.13', tag='v0.0.13', git=git)

    depends_on('py-wheel', type='build')
    depends_on('py-setuptools', type='build')

    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-tabulate@0.8.9:', type=('build', 'run'))
    # TODO: push new version to Spack official
    depends_on('py-fprettify@0.3.7:', type=('build', 'run'))
    depends_on('py-gt4py', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))
    depends_on('boost@1.73.0:', type=('build', 'run'))

    def patch(self):
        spack_pytest_ini = 'jenkins/spack/pytest.ini'
        if os.path.exists(spack_pytest_ini):
            fs.install(spack_pytest_ini, '.')

    # cmake in unit-tests needs this path
    def setup_build_environment(self, env):
        env.set("CMAKE_INCLUDE_PATH", self.spec['boost'].prefix.include)

    def test(self):
        # check if all installed module can be imported
        super().test()
        # unit tests

        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '-m',
               'not slow_tests')

    @property
    def headers(self):
        '''Workaround to hide the details of the installation path,
        i.e "lib/python3.10/site-packages/icon4py/atm_dyn_iconam"
        from upstream packages. It needs to be part of the "Spec" object,
        therefore choose the headers-function
        '''
        query_parameters = self.spec.last_query.extra_parameters
        version = self.spec.version

        folder_mapping = {
            ver('=0.0.3.1'): {
                'atm_dyn_iconam': 'atm_dyn_iconam',
                'utils':
                'liskov'  #utils will eventually map to parent directory of liskov
            },
            ver('=0.0.9'): {
                'atm_dyn_iconam': 'dycore',
                'tools': 'icon4pytools',
                'diffusion': 'diffusion/stencils',
                'interpolation': 'interpolation/stencils',
                'advection': 'advection',
            },
            ver('=0.0.10'): {
                'atm_dyn_iconam': 'dycore',
                'tools': 'icon4pytools',
                'diffusion': 'diffusion/stencils',
                'interpolation': 'interpolation/stencils',
                'advection': 'advection',
            },
            ver('=0.0.11'): {
                'atm_dyn_iconam': 'dycore',
                'tools': 'icon4pytools',
                'diffusion': 'diffusion/stencils',
                'interpolation': 'interpolation/stencils',
                'advection': 'advection',
            },
            ver('=main'): {
                'atm_dyn_iconam': 'dycore',
                'tools': 'icon4pytools',
                'diffusion': 'diffusion/stencils',
                'interpolation': 'interpolation/stencils',
                'advection': 'advection',
            },
        }

        if len(query_parameters) > 1:
            raise ValueError('Only one query parameter allowed')

        folder_name = folder_mapping.get(version, {})

        if not folder_name:
            return HeaderList([])

        for param, folder in folder_name.items():
            if param in query_parameters:
                return self._find_folder_and_add_dummy_header(
                    self.prefix, folder)

        return HeaderList([])

    def _find_folder_and_add_dummy_header(self, prefix, name):
        folder = find(prefix, name)
        headerlist = HeaderList(f'{folder[0]}/dummy.h')
        return headerlist


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

        if self.spec.version == ver('=0.0.3.1'):
            build_dirs = [
                'common', 'pyutils', 'testutils', 'liskov', 'atm_dyn_iconam'
            ]
        else:
            build_dirs = [
                'tools', 'model/atmosphere/dycore',
                'model/atmosphere/diffusion', 'model/atmosphere/advection',
                'model/common/'
            ]

        for dir in build_dirs:
            with fs.working_dir(os.path.join(self.build_directory, dir)):
                pip(*args)
