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
#     spack install py-hatchling
#
# You can edit this file again by typing:
#
#     spack edit py-hatchling
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPytestFactoryboy(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"

    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
    pypi = "pytest-factoryboy/pytest_factoryboy-2.5.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions here.
    version('2.5.1',
            sha256=
            '7275a52299b20c0f58b63fdf7326b3fd2b7cbefbdaa90fdcfc776bbe92197484')

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-factory-boy@2.10.0:', type=('build', 'run'))
    depends_on('py-pytest@5.0.0:', type=('build', 'run'))
    depends_on('py-typing-extensions', type=('build', 'run'))
    depends_on('py-inflection', type=('build', 'run'))
    depends_on('py-mypy', type=('build', 'run'))
    #depends_on('py-tox@4.0.8:', type=('build', 'run'))
    depends_on('py-tox@3.14.2:', type=('build', 'run'))
    #depends_on('py-packaging@22.0:', type=('build', 'run'))
    depends_on('py-packaging@21.3:', type=('build', 'run'))
    depends_on('py-importlib-metadata', type=('build', 'run'))
    depends_on('py-coverage +toml', type=('build', 'run'))

    patch('patches/2.5.1/group.patch',when='@2.5.1')

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    depends_on('py-poetry-core@1.0.0:', type='build')

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
