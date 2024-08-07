import pytest
import sys
import os

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import log_with_spack, sanitized_filename, all_packages, machine_name


def drop(unsupported_packages: list) -> list:
    try:
        exclude = unsupported_packages[machine_name()]
        return [p for p in all_packages if p not in exclude]
    except KeyError:
        return all_packages


def spack_info(spec: str, log_filename: str = None):
    """
    Tests 'spack info' of the given spec and writes the output into the log file.
    """

    if log_filename is None:
        log_filename = sanitized_filename(f'{spec}-spack_info')
    log_with_spack(f'spack info {spec}', 'integration_test', log_filename)


def spack_spec(spec: str, log_filename: str = None):
    """
    Tests 'spack info' of the given spec and writes the output into the log file.
    """

    if log_filename is None:
        log_filename = sanitized_filename(f'{spec}-spack_spec')
    log_with_spack(f'spack spec {spec}', 'integration_test', log_filename)


@pytest.mark.parametrize('package', all_packages)
def test_spack_info(package: str):
    spack_info(package)


unsupported_packages = {
    'tsa': [
        'cosmo',  # irrelevant
        'flexpart-cosmo',  # No compatible compiler available
    ]
}


@pytest.mark.parametrize('package', drop(unsupported_packages))
def test_spack_spec(package: str):
    spack_spec(package)


@pytest.mark.icon
@pytest.mark.parametrize('variant', [
    'serialization=create', 'fcgroup=DACE.externals/dace_icon.-O1',
    'extra-config-args=--disable-new_feature,--enable-old_config_arg'
])
def test_icon_spec_with_variant(variant: str):
    spack_spec(f'icon {variant}')


@pytest.mark.int2lm
@pytest.mark.parametrize('variant', ['+parallel', '~parallel'])
def test_int2lm_spec_with_variant(variant: str):
    spack_spec(f'int2lm {variant}')
