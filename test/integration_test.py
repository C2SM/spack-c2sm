import unittest
import sys
import os
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack


def spack_info(command: str, log_filename: str = None):
    """
    Tests 'spack info' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    ret = log_with_spack(f'spack info {command}', 'integration_test',
                         log_filename)
    ret.check_returncode()


def spack_spec(command: str, log_filename: str = None):
    """
    Tests 'spack info' of the given command and writes the output into the log file.
    If log_filename is None, command is used to create one.
    """
    ret = log_with_spack(f'spack spec {command}', 'integration_test',
                         log_filename)
    ret.check_returncode()


class InfoTest(unittest.TestCase):
    """Tests that 'spack spec <spec>' works for all conditional dependencies of all packages in spack-c2sm."""

    def test_cosmo(self):
        spack_info('cosmo')

    def test_cosmo_dycore(self):
        spack_info('cosmo-dycore')

    def test_cosmo_eccodes_definitions(self):
        spack_info('cosmo-eccodes-definitions')

    def test_cosmo_grib_api(self):
        spack_info('cosmo-grib-api')

    def test_cosmo_grib_api_definitions(self):
        spack_info('cosmo-grib-api-definitions')

    def test_dawn(self):
        spack_info('dawn')

    def test_dawn4py(self):
        spack_info('dawn4py')

    def test_dusk(self):
        spack_info('dusk')

    def test_flexpart_ifs(self):
        spack_info('flexpart-ifs')

    def test_gridtools(self):
        spack_info('gridtools')

    def test_icon(self):
        spack_info('icon')

    def test_icontools(self):
        spack_info('icontools')

    def test_int2lm(self):
        spack_info('int2lm')

    def test_libgrib1(self):
        spack_info('libgrib1')

    def test_oasis(self):
        spack_info('oasis')

    def test_omni_xmod_pool(self):
        spack_info('omni-xmod-pool')

    def test_omnicompiler(self):
        spack_info('omnicompiler')

    def test_xcodeml_tools(self):
        spack_info('xcodeml-tools')

    def test_zlib_ng(self):
        spack_info('zlib_ng')


class PlainSpecTest(unittest.TestCase):
    """Tests that the command 'spack spec <package>' works for all spack-c2sm packages."""

    def test_cosmo(self):
        spack_spec('cosmo')
        spack_spec('cosmo ~eccodes')
        spack_spec('cosmo cosmo_target=gpu ~cppdycore')
        spack_spec(
            'cosmo cosmo_target=gpu +serialize +eccodes +claw +zlib_ng +oasis')

    def test_cosmo_dycore(self):
        spack_spec('cosmo-dycore')
        spack_spec('cosmo-dycore ~cuda +gt1')
        spack_spec('cosmo-dycore +cuda +gt1 +build_tests')

    def test_cosmo_eccodes_definitions(self):
        spack_spec('cosmo-eccodes-definitions')

    def test_cosmo_grib_api(self):
        spack_spec('cosmo-grib-api')

    def test_cosmo_grib_api_definitions(self):
        spack_spec('cosmo-grib-api-definitions')

    def test_dawn(self):
        spack_spec('dawn')

    def test_dawn4py(self):
        spack_spec('dawn4py')

    def test_dusk(self):
        spack_spec('dusk')

    def test_flexpart_ifs(self):
        spack_spec('flexpart-ifs')

    def test_gridtools(self):
        spack_spec('gridtools')
        spack_spec('gridtools ~cuda')
        spack_spec('gridtools +cuda')

    def test_icon(self):
        spack_spec('icon')
        spack_spec('icon serialize_mode=create +eccodes +claw icon_target=gpu')

    def test_icontools(self):
        spack_spec('icontools')

    def test_int2lm(self):
        spack_spec('int2lm')
        spack_spec('int2lm ~eccodes')
        spack_spec('int2lm +eccodes +parallel')

    def test_libgrib1(self):
        spack_spec('libgrib1')

    def test_oasis(self):
        spack_spec('oasis')

    def test_omni_xmod_pool(self):
        spack_spec('omni-xmod-pool')

    def test_omnicompiler(self):
        spack_spec('omnicompiler')
        spack_spec('omnicompiler +mod2xmod')

    def test_xcodeml_tools(self):
        spack_spec('xcodeml-tools')

    def test_zlib_ng(self):
        spack_spec('zlib_ng')


if __name__ == '__main__':
    unittest.main(verbosity=2)
