# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGt4py(PythonPackage):
    """Python library for generating high-performance implementations 
    of stencil kernels for weather and climate modeling from a 
    domain-specific language (DSL). """

    homepage = "https://gridtools.github.io/gt4py/latest/index.html"

    url = "ssh://git@github.com/GridTools/gt4py.git"

    version('main', branch='main', git=url)
    version('1.0.1', tag='v1.0.1', git=url)

    maintainers = ['samkellerhals']

    # Build dependencies
    depends_on('py-wheel', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-setuptools@59.4:', type='build')

    depends_on('cmake@3.22:', type=('build', 'run'))
    depends_on('boost@1.65.1:', type=('build', 'run'))
    depends_on('clang-format@9:', type=('build', 'run'))

    # Python dependencies from setup.cfg
    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-attrs@21.3:', type=('build', 'run'))
    depends_on('py-black@22.3.0:', type=('build', 'run'))
    depends_on('py-boltons@20.0.0:', type=('build', 'run'))
    depends_on('py-cached-property@1.5:', type=('build', 'run'))
    depends_on('py-click@7.1:', type=('build', 'run'))
    depends_on('py-cytoolz@0.11: +cython', type=('build', 'run'))
    depends_on('py-deepdiff', type=('build', 'run'))
    depends_on('py-devtools@0.6:', type=('build', 'run'))
    depends_on('py-frozendict@2.3:', type=('build', 'run'))
    depends_on('py-gridtools-cpp@2.2.3:', type=('build', 'run'))
    depends_on('py-jinja2@2.10:', type=('build', 'run'))
    depends_on('py-lark@1.1.2:', type=('build', 'run'))
    depends_on('py-mako@1.1:', type=('build', 'run'))
    depends_on('py-networkx@2.4:', type=('build', 'run'))
    depends_on('py-ninja@1.10:', type=('build', 'run'))
    depends_on('py-numpy@1.22.2: +blas +lapack', type=('build', 'run'))
    depends_on('py-packaging@20.0:', type=('build', 'run'))
    depends_on('py-pybind11@2.5:', type=('build', 'run'))
    depends_on('py-scipy@1.4:', type=('build', 'run'))
    depends_on('py-tabulate@0.8:', type=('build', 'run'))
    depends_on('py-typing-extensions@4.2:', type=('build', 'run'))
    depends_on('py-astunparse@1.6.3:', type=('build', 'run'))
    depends_on('py-toolz@0.12.0:', type=('build', 'run'))
    depends_on('py-xxhash@1.4.4:', type=('build', 'run'))
    depends_on('py-hypothesis@4.14:', type=('build', 'run'))

    # Python dependencies from requirements-dev.txt
    # Convert to type=('test') ?
    depends_on('py-coverage@5.0:', type=('build', 'run'))
    depends_on('py-devtools@0.6:', type=('build', 'run'))
    depends_on('py-factory-boy@3.1:', type=('build', 'run'))
    depends_on('py-psutil@5.0:', type=('build', 'run'))
    depends_on('py-pytest-cache@1.0:', type=('build', 'run'))
    depends_on('py-pytest-cov@2.8:', type=('build', 'run'))
    depends_on('py-pytest-factoryboy@2.0:', type=('build', 'run'))
    depends_on('py-pytest@6.1:', type=('build', 'run'))
    # setup.cfg requires newer version, but not available yet
    depends_on('py-tox@3.14:', type=('build', 'run'))

    # missing version constraint: pytest-xdist[psutil]>=2.2
    depends_on('py-pytest-xdist', type=('build', 'run'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '--cov',
               '--cov-append', 'tests/next_tests', 'tests/eve_tests')
