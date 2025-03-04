import pytest
from spack_commands import spack_install


def test_install_py_tabulate_0_8_10():
    spack_install('py-tabulate@0.8.10')
