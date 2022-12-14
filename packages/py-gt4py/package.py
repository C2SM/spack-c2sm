# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-gt4py
#
# You can edit this file again by typing:
#
#     spack edit py-gt4py
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGt4py(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"

    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
    url = "ssh://git@github.com/GridTools/gt4py.git"

    version('functional', branch='functional', git=url)

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    depends_on('python@3.10:', type=('build', 'run'))
    depends_on('py-attrs@20.3:', type=('build', 'run'))

    depends_on('py-black@22.3.0:', type=('build', 'run'))

    depends_on('py-boltons@20.0.0:', type=('build', 'run'))
    depends_on('py-click@7.1:', type=('build', 'run'))
    depends_on('cmake@3.18:', type=('build', 'run'))

    depends_on('py-devtools@0.5:', type=('build', 'run'))
    depends_on('py-frozendict@2.3:', type=('build', 'run'))
    depends_on('py-cytoolz@0.11: +cython', type=('build', 'run'))

    # TODO: update version to 5.8
    depends_on('py-deepdiff@5.6:', type=('build', 'run'))

    depends_on('py-jinja2@2.10:', type=('build', 'run'))
    depends_on('py-lark@1.1.2:', type=('build', 'run'))

    depends_on('py-mako@1.1:', type=('build', 'run'))
    depends_on('py-networkx@2.4:', type=('build', 'run'))
    depends_on('py-ninja@1.10:', type=('build', 'run'))
    depends_on('py-numpy@1.21: ~blas ~lapack', type=('build', 'run'))
    depends_on('py-packaging@20.0:', type=('build', 'run'))
    depends_on('py-pybind11@2.5:', type=('build', 'run'))
    depends_on('py-toolz@0.12.0:', type=('build', 'run'))
    depends_on('py-typing-extensions@4.2:', type=('build', 'run'))
    depends_on('py-xxhash@1.4.4:', type=('build', 'run'))

    # test-only dep does not work for dev-build
    depends_on('py-pytest@6.1:', type=('build', 'run'))

    # deps from requirements-dev.txt
    depends_on('py-check-manifest@0.40:', type=('build', 'run'))
    depends_on('py-coverage@5.0:', type=('build', 'run'))
    depends_on('py-darglint@1.6:', type=('build', 'run'))
    depends_on('py-devtools@0.6:', type=('build', 'run'))
    depends_on('py-factory-boy@3.1:', type=('build', 'run'))

    #depends_on('py-flake8@5.0.4:', type=('build', 'run'))
    depends_on('py-flake8', type=('build', 'run'))

    # isort~=5.10
    depends_on('py-isort', type=('build', 'run'))

    # jupytext>=1.14
    depends_on('py-jupytext', type=('build', 'run'))

    # mypy>=0.990
    depends_on('py-mypy', type=('build', 'run'))

    depends_on('py-psutil@5.0:', type=('build', 'run'))

    depends_on('py-pygments@2.7:', type=('build', 'run'))
    depends_on('py-pytest-cache@1.0:', type=('build', 'run'))
    depends_on('py-pytest-cov@2.8:', type=('build', 'run'))
    depends_on('py-pytest-factoryboy@2.0:', type=('build', 'run'))

    # avoid problems with py-pluggy dep
    depends_on('py-tox@3.14:', type=('build', 'run'))

    # pytest-xdist[psutil]>=2.2
    depends_on('py-pytest-xdist', type=('build', 'run'))

    depends_on('py-sphinx@3.1:', type=('build', 'run'))
    depends_on('py-sphinx-rtd-theme@0.4:', type=('build', 'run'))

    depends_on('py-wheel', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-setuptools@40.8.0:', type='build')

    # pytest fails with:
    #__main__.py: error: unrecognized arguments: --cov-config=setup.cfg
    patch('patches/functional/rm_cov_config_arg.patch', when='@functional')

    def global_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py
        # FIXME: If not needed, delete this function
        options = []
        return options

    def install_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py install
        # FIXME: If not needed, delete this function
        options = []
        return options

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('spack-test', create=True):
            python('-m', 'pytest', '-v', '../tests')
