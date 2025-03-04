import pytest
from spack_commands import spack_install


def test_install_clang_format():
    spack_install('clang-format')


def test_install_cosmo_eccodes_definitions():
    spack_install('cosmo-eccodes-definitions')


def test_install_ecbuild():
    # Tests are disabled because they fail with:
    # The following tests FAILED:
    # 	  1 - ECBUILD-359 (Failed)
    # 	  2 - ECBUILD-401 (Failed)
    # 	  8 - ECBUILD-511 (Failed)
    # 	 11 - bundle-subdir-std (Failed)
    # 	 12 - bundle-subdir-ecbfind (Failed)
    # 	 17 - test_ecbuild_find_package (Failed)
    spack_install('ecbuild @3.7.2', test_root=False)



def test_install_makedepf90():
    # Tests are disabled because they fail with:
    # test1.sh: No such file or directory
    spack_install('makedepf90', test_root=False)


def test_install_py_cytoolz():
    spack_install('py-cytoolz')


def test_install_py_devtools():
    spack_install('py-devtools')


def test_install_py_factory_boy():
    spack_install('py-factory-boy')


def test_install_py_gridtools_cpp():
    spack_install('py-gridtools-cpp')


def test_install_py_hatchling():
    spack_install('py-hatchling')


def test_install_py_inflection():
    spack_install('py-inflection')


def test_install_py_pytest_factoryboy():
    spack_install('py-pytest-factoryboy')


def test_install_py_tabulate():
    spack_install('py-tabulate')


def test_install_py_typing_extensions():
    spack_install('py-typing-extensions')


