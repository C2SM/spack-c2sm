import pytest
from spack_commands import (
    ALL_PACKAGES,
    spack_info,
    spack_spec,
    run_with_spack,
    log_file,
)


@pytest.mark.parametrize("package", ALL_PACKAGES)
def test_info(package: str):
    "Tests that the command 'spack info <package>' works."
    spack_info(package)


@pytest.mark.parametrize("package", ALL_PACKAGES)
def test_spec(package: str):
    "Tests that the command 'spack spec <package>' works."
    spack_spec(package)


def test_icon_serialization():
    spack_spec("icon serialization=create")


def test_icon_fcgroup():
    spack_spec("icon fcgroup=DACE.externals/dace_icon.-O1")


def test_icon_extra_config_args():
    spack_spec(
        "icon extra-config-args=--disable-new_feature,--enable-old_config_arg")


def test_compilers():
    run_with_spack("spack compilers", log=log_file("compilers"))


def test_find():
    run_with_spack("spack find", log=log_file("find"))
