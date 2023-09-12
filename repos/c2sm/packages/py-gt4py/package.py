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

    url = "git@github.com:GridTools/gt4py.git"

    version('main', branch='main', git=url)
    version('1.1.1', tag='icon4py_20230413', git=url)
    version('1.1.2', tag='icon4py_20230621', git=url)
    version('1.1.3', tag='icon4py_20230817', git=url)

    maintainers = ['samkellerhals']

    # Build dependencies
    depends_on('py-wheel', type='build')
    depends_on('py-cython', type='build')

    # downgrade to from 65 to 63 because of py-numpy
    depends_on('py-setuptools@63:', type='build')

    depends_on('cmake@3.22:', type=('build', 'run'))
    depends_on('boost@1.65.1:', type=('build', 'run'))
    depends_on('clang-format@9:', type=('build', 'run'))

    # Python dependencies from setup.cfg
    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-attrs@21.3:', type=('build', 'run'))
    depends_on('py-black@22.3.0:', type=('build', 'run'))
    depends_on('py-boltons@20.0.0:', type=('build', 'run'))
    depends_on('py-cached-property@1.5:', type=('build', 'run'))
    depends_on('py-click@8.0.0:', type=('build', 'run'))
    depends_on('py-cytoolz@0.12:', type=('build', 'run'))
    depends_on('py-deepdiff@5.6:', type=('build', 'run'))
    depends_on('py-devtools@0.6:', type=('build', 'run'))
    depends_on('py-frozendict@2.3:', type=('build', 'run'))
    depends_on('py-gridtools-cpp@2.3.1:', type=(
        'build', 'run'
    ))  #gridtools-cpp is backwards compatible with older gt4py versions
    depends_on('py-jinja2@3.0.0:', type=('build', 'run'))
    depends_on('py-lark@1.1.2:', type=('build', 'run'))
    depends_on('py-mako@1.1:', type=('build', 'run'))
    depends_on('py-ninja@1.10:', type=('build', 'run'))
    depends_on('py-numpy@1.24.2: ~blas ~lapack', type=('build', 'run'))
    depends_on('py-packaging@20.0:', type=('build', 'run'))

    # versions later than 2.9.2 fail to pick to right Python version
    # for compiled modules.
    # See: https://github.com/C2SM/spack-c2sm/issues/803
    depends_on('py-pybind11@2.5:2.9.2', type=('build', 'run'))

    depends_on('py-nanobind@1.4.0:', when="@1.1.3:", type=('build', 'run'))
    depends_on('py-tabulate@0.8:', type=('build', 'run'))
    depends_on('py-typing-extensions@4.5:', type=('build', 'run'))
    depends_on('py-toolz@0.12.0:', type=('build', 'run'))
    depends_on('py-xxhash@1.4.4:', type=('build', 'run'))
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
    # setup.cfg requires newer version, but not available yet
    depends_on('py-tox@3.14:', type=('build', 'run'))

    # missing version constraint: pytest-xdist[psutil]>=2.4
    depends_on('py-pytest-xdist', type=('build', 'run'))

    def test(self):
        python('-m', 'pytest', '-v', '-s', '-n', 'auto', '--cov',
               '--cov-append', 'tests/next_tests', 'tests/eve_tests')
