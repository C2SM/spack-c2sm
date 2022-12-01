import unittest
import sys
import os
from pathlib import Path
from context import needs_testing, if_context_includes

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack


def test_with_spack(command: str, log_name: str = None):
    if log_name is None:
        log_name = command.replace(' ', '_').replace('%', '')

    log = Path(
        f'{spack_c2sm_path}/log/{machine_name()}/integration_test/{log_name}.log'
    )
    ret = log_with_spack(command, log)
    ret.check_returncode()


def spack_info(command: str, log_name: str = None):
    test_with_spack(f'spack info {command}', log_name)


def spack_spec(command: str, log_name: str = None):
    test_with_spack(f'spack spec {command}', log_name)


class InfoTest(unittest.TestCase):
    """Tests that 'spack spec <spec>' works for all conditional dependencies of all packages in spack-c2sm."""

    @if_context_includes('cosmo')
    def test_cosmo(self):
        spack_info('cosmo')

    @if_context_includes('cosmo-dycore')
    def test_cosmo_dycore(self):
        spack_info('cosmo-dycore')

    @if_context_includes('cosmo-eccodes-definitions')
    def test_cosmo_eccodes_definitions(self):
        spack_info('cosmo-eccodes-definitions')

    @if_context_includes('cosmo-grib-api')
    def test_cosmo_grib_api(self):
        spack_info('cosmo-grib-api')

    @if_context_includes('cosmo-grib-api-definitions')
    def test_cosmo_grib_api_definitions(self):
        spack_info('cosmo-grib-api-definitions')

    @if_context_includes('dawn')
    def test_dawn(self):
        spack_info('dawn')

    @if_context_includes('dawn4py')
    def test_dawn4py(self):
        spack_info('dawn4py')

    @if_context_includes('dusk')
    def test_dusk(self):
        spack_info('dusk')

    @if_context_includes('flexpart-ifs')
    def test_flexpart_ifs(self):
        spack_info('flexpart-ifs')

    @if_context_includes('gridtools')
    def test_gridtools(self):
        spack_info('gridtools')

    @if_context_includes('icon')
    def test_icon(self):
        spack_info('icon')

    @if_context_includes('icontools')
    def test_icontools(self):
        spack_info('icontools')

    @if_context_includes('int2lm')
    def test_int2lm(self):
        spack_info('int2lm')

    @if_context_includes('libgrib1')
    def test_libgrib1(self):
        spack_info('libgrib1')

    @if_context_includes('oasis')
    def test_oasis(self):
        spack_info('oasis')

    @if_context_includes('omni-xmod-pool')
    def test_omni_xmod_pool(self):
        spack_info('omni-xmod-pool')

    @if_context_includes('omnicompiler')
    def test_omnicompiler(self):
        spack_info('omnicompiler')

    @if_context_includes('xcodeml-tools')
    def test_xcodeml_tools(self):
        spack_info('xcodeml-tools')

    @if_context_includes('zlib_ng')
    def test_zlib_ng(self):
        spack_info('zlib_ng')


class PlainSpecTest(unittest.TestCase):
    """Tests that the command 'spack spec <package>' works for all spack-c2sm packages."""

    @if_context_includes('cosmo')
    def test_cosmo(self):
        spack_spec('cosmo')
        spack_spec('cosmo ~eccodes')
        spack_spec('cosmo cosmo_target=gpu ~cppdycore')
        spack_spec(
            'cosmo cosmo_target=gpu +serialize +eccodes +claw +zlib_ng +oasis')

    @if_context_includes('cosmo-dycore')
    def test_cosmo_dycore(self):
        spack_spec('cosmo-dycore')
        spack_spec('cosmo-dycore ~cuda +gt1')
        spack_spec('cosmo-dycore +cuda +gt1 +build_tests')

    @if_context_includes('cosmo-eccodes-definitions')
    def test_cosmo_eccodes_definitions(self):
        spack_spec('cosmo-eccodes-definitions')

    @if_context_includes('cosmo-grib-api')
    def test_cosmo_grib_api(self):
        spack_spec('cosmo-grib-api')

    @if_context_includes('cosmo-grib-api-definitions')
    def test_cosmo_grib_api_definitions(self):
        spack_spec('cosmo-grib-api-definitions')

    @if_context_includes('dawn')
    def test_dawn(self):
        spack_spec('dawn')

    @if_context_includes('dawn4py')
    def test_dawn4py(self):
        spack_spec('dawn4py')

    @if_context_includes('dusk')
    def test_dusk(self):
        spack_spec('dusk')

    @if_context_includes('flexpart-ifs')
    def test_flexpart_ifs(self):
        spack_spec('flexpart-ifs')

    @if_context_includes('gridtools')
    def test_gridtools(self):
        spack_spec('gridtools')
        spack_spec('gridtools ~cuda')
        spack_spec('gridtools +cuda')

    @if_context_includes('icon')
    def test_icon(self):
        spack_spec('icon')
        spack_spec('icon serialize_mode=create +eccodes +claw icon_target=gpu')

    @if_context_includes('icontools')
    def test_icontools(self):
        spack_spec('icontools')

    @if_context_includes('int2lm')
    def test_int2lm(self):
        spack_spec('int2lm')
        spack_spec('int2lm ~eccodes')
        spack_spec('int2lm +eccodes +parallel')

    @if_context_includes('libgrib1')
    def test_libgrib1(self):
        spack_spec('libgrib1')

    @if_context_includes('oasis')
    def test_oasis(self):
        spack_spec('oasis')

    @if_context_includes('omni-xmod-pool')
    def test_omni_xmod_pool(self):
        spack_spec('omni-xmod-pool')

    @if_context_includes('omnicompiler')
    def test_omnicompiler(self):
        spack_spec('omnicompiler')
        spack_spec('omnicompiler +mod2xmod')

    @if_context_includes('xcodeml-tools')
    def test_xcodeml_tools(self):
        spack_spec('xcodeml-tools')

    @if_context_includes('zlib_ng')
    def test_zlib_ng(self):
        spack_spec('zlib_ng')


if __name__ == '__main__':
    commands = sys.argv[1:]
    sys.argv = [sys.argv[0]]  # unittest needs this
    unittest.main(verbosity=2)
