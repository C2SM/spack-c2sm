# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestFactoryboy(PythonPackage):
    """factory_boy integration with the pytest runner"""

    homepage = "https://pytest-factoryboy.readthedocs.io/en/stable/"

    pypi = "pytest-factoryboy/pytest_factoryboy-2.5.1.tar.gz"

    maintainers = ['samkellerhals']

    version('2.5.1',
            sha256=
            '7275a52299b20c0f58b63fdf7326b3fd2b7cbefbdaa90fdcfc776bbe92197484')

    # TODO: These two deps had to be excluded, otherwise
    #       conretizer had problems with py-gt4py spec

    #depends_on('py-tox@4.0.8:', type=('build', 'run'))
    #depends_on('py-packaging@22.0:', type=('build', 'run'))

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-factory-boy@2.10.0:', type=('build', 'run'))
    depends_on('py-pytest@5.0.0:', type=('build', 'run'))
    depends_on('py-typing-extensions', type=('build', 'run'))
    depends_on('py-inflection', type=('build', 'run'))
    depends_on('py-mypy', type=('build', 'run'))
    depends_on('py-tox@3.14.2:', type=('build', 'run'))
    depends_on('py-packaging@21.3:', type=('build', 'run'))
    depends_on('py-importlib-metadata', type=('build', 'run'))
    depends_on('py-coverage +toml', type=('build', 'run'))

    patch('patches/2.5.1/group.patch', when='@2.5.1')

    depends_on('py-poetry-core@1.0.0:', type='build')
