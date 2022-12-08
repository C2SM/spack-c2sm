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
#     spack install py-frozendict
#
# You can edit this file again by typing:
#
#     spack edit py-frozendict
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyFrozendict(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"

    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
    url = "https://pypi.org/project/frozendict"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    version('2.3.4',
            sha256=
            '15b4b18346259392b0d27598f240e9390fafbff882137a9c48a1e0104fb17f78')

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    depends_on('python@3.6:', type=('build', 'run'))

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    depends_on('py-setuptools', type='build')

    # FIXME: Add additional dependencies if required.
    # depends_on('py-foo', type=('build', 'run'))

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
