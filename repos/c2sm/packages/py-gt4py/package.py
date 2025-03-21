# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from spack import *


class PyGt4py(PythonPackage):
    """Python library for generating high-performance implementations 
    of stencil kernels for weather and climate modeling from a 
    domain-specific language (DSL). """

    homepage = "https://gridtools.github.io/gt4py/latest/index.html"

    url = "git@github.com:GridTools/gt4py.git"

    version('main', branch='main', git=url)
    version('1.0.3.3', tag='icon4py_20240229', git=url)
    version('1.0.3.7', tag='icon4py_20240521', git=url)
    version('1.0.3.9', tag='icon4py_20240912', git=url)
    version('1.0.3.10', tag='icon4py_20241113', git=url)

    maintainers = ['samkellerhals']

    # Build dependencies
    depends_on('py-wheel', type='build')
    depends_on('py-cython', type='build')

    # downgrade to from 65 to 63 because of py-numpy
    depends_on('py-setuptools@63:', type='build')

    depends_on('cmake@3.22:', type=('build', 'run'))
    depends_on('boost@1.73.0:', type=('build', 'run'))
    depends_on('clang-format@9:', type=('build', 'run'))

    # Python dependencies from setup.cfg
    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-attrs@21.3:', type=('build', 'run'))
    depends_on('py-black@22.3.0:', type=('build', 'run'))
    depends_on('py-boltons@20.1:', type=('build', 'run'))
    depends_on('py-cached-property@1.5.1:', type=('build', 'run'))
    depends_on('py-click@8.0.0:', type=('build', 'run'))
    depends_on('py-cytoolz@0.12:', type=('build', 'run'))
    depends_on('py-deepdiff@5.6.0:', type=('build', 'run'))
    depends_on('py-devtools@0.6:', type=('build', 'run'))
    depends_on('py-frozendict@2.3:', type=('build', 'run'))
    depends_on('py-gridtools-cpp@2.3.6:', type=(
        'build', 'run'
    ))  #gridtools-cpp is backwards compatible with older gt4py versions
    depends_on('py-jinja2@3.0.0:', type=('build', 'run'))
    depends_on('py-lark@1.1.2:', type=('build', 'run'))
    depends_on('py-mako@1.1:', type=('build', 'run'))
    depends_on('py-ninja@1.10:', type=('build', 'run'))
    depends_on('py-numpy@1.24.2:', type=('build', 'run'))
    depends_on('py-packaging@20.0:', type=('build', 'run'))
    depends_on('py-pybind11@2.10.1:', type=('build', 'run'))
    depends_on('py-nanobind@1.4.0:', when="@1.0.1.3:", type=('build', 'run'))
    depends_on('py-tabulate@0.8.10:', type=('build', 'run'))
    depends_on('py-typing-extensions@4.5.0',
               when="@:1.0.3.5",
               type=('build', 'run'))
    depends_on('py-typing-extensions@4.10.0',
               when="@1.0.3.6:",
               type=('build', 'run'))
    depends_on('py-toolz@0.12.0:', type=('build', 'run'))
    depends_on('py-xxhash@1.4.4:3.0.9', type=('build', 'run'))
    depends_on('py-hypothesis@6.0.0:', type=('build', 'run'))

    # Python dependencies from requirements-dev.txt
    # Convert to type=('test') ?
    depends_on('py-coverage@5.0:', type=('build', 'run'))
    depends_on('py-devtools@0.6:', type=('build', 'run'))
    depends_on('py-factory-boy@3.1:', type=('build', 'run'))
    depends_on('py-psutil@5.0:', type=('build', 'run'))
    depends_on('py-pytest-cache@1.0:', type=('build', 'run'))
    depends_on('py-pytest-cov@2.8:', type=('build', 'run'))
    depends_on('py-pytest-factoryboy@2.0.3:', type=('build', 'run'))
    depends_on('py-pytest@7.0:', type=('build', 'run'))
    depends_on('py-diskcache@5.2:', type=('build', 'run'))
    # setup.cfg requires newer version, but not available yet
    depends_on('py-tox@3.14:', type=('build', 'run'))

    # missing version constraint: pytest-xdist[psutil]>=2.4
    depends_on('py-pytest-xdist', type=('build', 'run'))

    def test(self):
        # workaround for not finding own python module
        python_spec = self.spec['python']
        python_version = python_spec.version.up_to(2)
        install_path = join_path(self.prefix, 'lib', f"python{python_version}",
                                 'site-packages')
        os.environ[
            'PYTHONPATH'] = f"{install_path}:{os.environ.get('PYTHONPATH', '')}"

        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '-k', '.run_gtfn]',
               'tests/next_tests', 'tests/eve_tests')
