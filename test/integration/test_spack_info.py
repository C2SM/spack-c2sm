#!/usr/bin/python3

from .spack_commands import spack_info
import unittest


class InfoTest(unittest.TestCase):
    """Tests that the command 'spack info <package>' works for all spack-c2sm packages."""

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


if __name__ == '__main__':
    unittest.main()
