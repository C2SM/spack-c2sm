#!/usr/bin/python3

from .spack_commands import spack_spec
import unittest


class PlainSpecTest(unittest.TestCase):
    """Tests that the command 'spack spec <package>' works for all spack-c2sm packages."""

    def test_cosmo(self):
        spack_spec('cosmo')

    def test_cosmo_dycore(self):
        spack_spec('cosmo-dycore')

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

    def test_icon(self):
        spack_spec('icon')

    def test_icontools(self):
        spack_spec('icontools')

    def test_int2lm(self):
        spack_spec('int2lm')

    def test_libgrib1(self):
        spack_spec('libgrib1')

    def test_oasis(self):
        spack_spec('oasis')

    def test_omni_xmod_pool(self):
        spack_spec('omni-xmod-pool')

    def test_omnicompiler(self):
        spack_spec('omnicompiler')

    def test_xcodeml_tools(self):
        spack_spec('xcodeml-tools')

    def test_zlib_ng(self):
        spack_spec('zlib_ng')


class ConditionalDependenciesSpecTest(unittest.TestCase):
    """Tests that 'spack spec <spec>' works for all conditional dependencies of all packages in spack-c2sm."""

    def test_cosmo(self):
        spack_spec('cosmo ~eccodes')
        spack_spec('cosmo cosmo_target=gpu ~cppdycore')
        spack_spec(
            'cosmo cosmo_target=gpu +serialize +eccodes +claw +zlib_ng +oasis')

    def test_cosmo_dycore(self):
        spack_spec('cosmo-dycore ~cuda +gt1')
        spack_spec('cosmo-dycore +cuda +gt1 +build_tests')

    def test_gridtools(self):
        spack_spec('gridtools ~cuda')
        spack_spec('gridtools +cuda')

    def test_icon(self):
        spack_spec('icon serialize_mode=create +eccodes +claw icon_target=gpu')

    def test_int2lm(self):
        spack_spec('int2lm ~eccodes')
        spack_spec('int2lm +eccodes +parallel')

    def test_omnicompiler(self):
        spack_spec('omnicompiler +mod2xmod')


if __name__ == '__main__':
    unittest.main()
