import unittest
import sys
import os
from pathlib import Path
from context import needs_testing

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

    @unittest.skipUnless(needs_testing('cosmo'), 'irrelevant')
    def test_cosmo(self):
        spack_info('cosmo')

    @unittest.skipUnless(needs_testing('cosmo-dycore'), 'irrelevant')
    def test_cosmo_dycore(self):
        spack_info('cosmo-dycore')

    @unittest.skipUnless(needs_testing('cosmo-eccodes-definitions'),
                         'irrelevant')
    def test_cosmo_eccodes_definitions(self):
        spack_info('cosmo-eccodes-definitions')

    @unittest.skipUnless(needs_testing('cosmo-grib-api'), 'irrelevant')
    def test_cosmo_grib_api(self):
        spack_info('cosmo-grib-api')

    @unittest.skipUnless(needs_testing('cosmo-grib-api-definitions'),
                         'irrelevant')
    def test_cosmo_grib_api_definitions(self):
        spack_info('cosmo-grib-api-definitions')

    @unittest.skipUnless(needs_testing('dawn'), 'irrelevant')
    def test_dawn(self):
        spack_info('dawn')

    @unittest.skipUnless(needs_testing('dawn4py'), 'irrelevant')
    def test_dawn4py(self):
        spack_info('dawn4py')

    @unittest.skipUnless(needs_testing('dusk'), 'irrelevant')
    def test_dusk(self):
        spack_info('dusk')

    @unittest.skipUnless(needs_testing('flexpart-ifs'), 'irrelevant')
    def test_flexpart_ifs(self):
        spack_info('flexpart-ifs')

    @unittest.skipUnless(needs_testing('gridtools'), 'irrelevant')
    def test_gridtools(self):
        spack_info('gridtools')

    @unittest.skipUnless(needs_testing('icon'), 'irrelevant')
    def test_icon(self):
        spack_info('icon')

    @unittest.skipUnless(needs_testing('icontools'), 'irrelevant')
    def test_icontools(self):
        spack_info('icontools')

    @unittest.skipUnless(needs_testing('int2lm'), 'irrelevant')
    def test_int2lm(self):
        spack_info('int2lm')

    @unittest.skipUnless(needs_testing('libgrib1'), 'irrelevant')
    def test_libgrib1(self):
        spack_info('libgrib1')

    @unittest.skipUnless(needs_testing('oasis'), 'irrelevant')
    def test_oasis(self):
        spack_info('oasis')

    @unittest.skipUnless(needs_testing('omni-xmod-pool'), 'irrelevant')
    def test_omni_xmod_pool(self):
        spack_info('omni-xmod-pool')

    @unittest.skipUnless(needs_testing('omnicompiler'), 'irrelevant')
    def test_omnicompiler(self):
        spack_info('omnicompiler')

    @unittest.skipUnless(needs_testing('xcodeml-tools'), 'irrelevant')
    def test_xcodeml_tools(self):
        spack_info('xcodeml-tools')

    @unittest.skipUnless(needs_testing('zlib_ng'), 'irrelevant')
    def test_zlib_ng(self):
        spack_info('zlib_ng')


class PlainSpecTest(unittest.TestCase):
    """Tests that the command 'spack spec <package>' works for all spack-c2sm packages."""

    @unittest.skipUnless(needs_testing('cosmo'), 'irrelevant')
    @unittest.skipIf(machine_name() in [
        'balfrin', 'manali'
    ], 'cosmo-dycore has no suitable cuda backend parameters implemented for cuda_arch=80'
                     )
    def test_cosmo(self):
        spack_spec('cosmo')
        spack_spec('cosmo ~eccodes')
        spack_spec('cosmo cosmo_target=gpu ~cppdycore')
        spack_spec(
            'cosmo cosmo_target=gpu +serialize +eccodes +claw +zlib_ng +oasis')

    @unittest.skipUnless(needs_testing('cosmo-dycore'), 'irrelevant')
    @unittest.skipIf(machine_name() in [
        'balfrin', 'manali'
    ], 'cosmo-dycore has no suitable cuda backend parameters implemented for cuda_arch=80'
                     )
    def test_cosmo_dycore(self):
        spack_spec('cosmo-dycore')
        spack_spec('cosmo-dycore ~cuda +gt1')
        spack_spec('cosmo-dycore +cuda +gt1 +build_tests')

    @unittest.skipUnless(needs_testing('cosmo-eccodes-definitions'),
                         'irrelevant')
    def test_cosmo_eccodes_definitions(self):
        spack_spec('cosmo-eccodes-definitions')

    @unittest.skipUnless(needs_testing('cosmo-grib-api'), 'irrelevant')
    def test_cosmo_grib_api(self):
        spack_spec('cosmo-grib-api')

    @unittest.skipUnless(needs_testing('cosmo-grib-api-definitions'),
                         'irrelevant')
    def test_cosmo_grib_api_definitions(self):
        spack_spec('cosmo-grib-api-definitions')

    @unittest.skipUnless(needs_testing('dawn'), 'irrelevant')
    def test_dawn(self):
        spack_spec('dawn')

    @unittest.skipUnless(needs_testing('dawn4py'), 'irrelevant')
    def test_dawn4py(self):
        spack_spec('dawn4py')

    @unittest.skipUnless(needs_testing('dusk'), 'irrelevant')
    def test_dusk(self):
        spack_spec('dusk')

    @unittest.skipUnless(needs_testing('flexpart-ifs'), 'irrelevant')
    def test_flexpart_ifs(self):
        spack_spec('flexpart-ifs')

    @unittest.skipUnless(needs_testing('gridtools'), 'irrelevant')
    def test_gridtools(self):
        spack_spec('gridtools')
        spack_spec('gridtools ~cuda')
        spack_spec('gridtools +cuda')

    @unittest.skipUnless(needs_testing('icon'), 'irrelevant')
    def test_icon(self):
        spack_spec('icon')
        spack_spec('icon serialize_mode=create +eccodes +claw icon_target=gpu')

    @unittest.skipUnless(needs_testing('icontools'), 'irrelevant')
    def test_icontools(self):
        spack_spec('icontools')

    @unittest.skipUnless(needs_testing('int2lm'), 'irrelevant')
    def test_int2lm(self):
        spack_spec('int2lm')
        spack_spec('int2lm ~eccodes')
        spack_spec('int2lm +eccodes +parallel')

    @unittest.skipUnless(needs_testing('libgrib1'), 'irrelevant')
    def test_libgrib1(self):
        spack_spec('libgrib1')

    @unittest.skipUnless(needs_testing('oasis'), 'irrelevant')
    def test_oasis(self):
        spack_spec('oasis')

    @unittest.skipUnless(needs_testing('omni-xmod-pool'), 'irrelevant')
    def test_omni_xmod_pool(self):
        spack_spec('omni-xmod-pool')

    @unittest.skipUnless(needs_testing('omnicompiler'), 'irrelevant')
    def test_omnicompiler(self):
        spack_spec('omnicompiler')
        spack_spec('omnicompiler +mod2xmod')

    @unittest.skipUnless(needs_testing('xcodeml-tools'), 'irrelevant')
    def test_xcodeml_tools(self):
        spack_spec('xcodeml-tools')

    @unittest.skipUnless(needs_testing('zlib_ng'), 'irrelevant')
    def test_zlib_ng(self):
        spack_spec('zlib_ng')


if __name__ == '__main__':
    commands = sys.argv[1:]
    sys.argv = [sys.argv[0]]  # unittest needs this
    unittest.main(verbosity=2)
