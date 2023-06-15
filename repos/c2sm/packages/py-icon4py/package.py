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
    git = 'ssh://git@github.com/C2SM/icon4py.git'

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

    @property
    def headers(self):
        '''Workaround to hide the details of the installation path, 
        i.e "lib/python3.10/site-packages/icon4py/atm_dyn_iconam"
        from upstream packages. It needs to be part of the "Spec" object,
        therefore choose the headers-function
        '''


        query_parameters = self.spec.last_query.extra_parameters

        if len(query_parameters) > 1:
            raise ValueError('Only one query parameter allowed')

        if (self.spec.version == ver('0.0.3') and len(query_parameters) == 1):
            msg = 'Not implemented for version {0}'.format(self.spec.version)
            raise spack.error.NoHeadersError(msg)

        if 'atm_dyn_iconam' in query_parameters:
            header = self._find_folder_and_add_dummy_header(self.prefix,'atm_dyn_iconam')
        elif 'tools' in query_parameters:
            header = self._find_folder_and_add_dummy_header(self.prefix,'icon4pytools')
        else:
            header = HeaderList([])

        return header
    
    def _find_folder_and_add_dummy_header(self,prefix,name):
        folder = find(prefix,name)
        headerlist = HeaderList(f'{folder[0]}/dummy.h')
        return headerlist




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

        if self.spec.version == ver('0.0.3'):
            build_dirs = [
                'common', 'pyutils', 'testutils', 'liskov', 'atm_dyn_iconam'
            ]
        else:
            build_dirs = ['common', 'atm_dyn_iconam', 'tools']

        for dir in build_dirs:
            with working_dir(os.path.join(self.stage.source_path, dir)):
                pip(*args)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '--cov',
               '--cov-append')
