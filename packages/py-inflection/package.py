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


class PyInflection(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"

    # FIXME: ensure the package is not available through PyPI. If it is,
    # re-run `spack create --force` with the PyPI URL.
    pypi = "inflection/inflection-0.5.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions here.
    version('0.5.1',
            sha256=
            '1a29730d366e996aaacffb2f1f1cb9593dc38e2ddd30c91250c6dde09ea9b417')

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-isort', type=('build', 'run'))
    depends_on('py-flake8', type=('build', 'run'))
    depends_on('py-pytest', type=('build', 'run'))

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    depends_on('py-setuptools', type='build')
