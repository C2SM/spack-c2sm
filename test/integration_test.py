import pytest
from spack_commands import ALL_PACKAGES, spack_info, spack_spec


@pytest.mark.parametrize("package", ALL_PACKAGES)
def test_info(package: str):
    "Tests that the command 'spack info <package>' works."
    spack_info(package)


@pytest.mark.parametrize("package", ALL_PACKAGES)
def test_spec(package: str):
    "Tests that the command 'spack spec <package>' works."
    spack_spec(package)


def test_icon_c2sm_serialization():
    spack_spec("icon-c2sm serialization=create")


def test_icon_c2sm_fcgroup():
    spack_spec("icon-c2sm fcgroup=DACE.externals/dace_icon.-O1")


def test_icon_extra_config_args():
    spack_spec(
        "icon-c2sm extra-config-args=--disable-new_feature,--enable-old_config_arg"
    )


def test_int2lm_parallel():
    spack_spec("int2lm +parallel")


def test_int2lm_no_parallel():
    spack_spec("int2lm ~parallel")
