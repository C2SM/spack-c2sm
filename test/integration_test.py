import unittest
import sys
import os
from pathlib import Path

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack


def spack_info(spec: str, log_filename: str = None):
    """
    Tests 'spack info' of the given spec and writes the output into the log file.
    If log_filename is None, spec is used to create one.
    """
    ret = log_with_spack(f'spack info {spec}', 'integration_test',
                         log_filename)


def spack_spec(spec: str, log_filename: str = None):
    """
    Tests 'spack info' of the given spec and writes the output into the log file.
    If log_filename is None, spec is used to create one.
    """
    ret = log_with_spack(f'spack spec {spec}', 'integration_test',
                         log_filename)


class InfoTest(unittest.TestCase):
    """Tests that 'spack spec <spec>' works for all conditional dependencies of all packages in spack-c2sm."""

    def test_clang_format(self):
        spack_info('clang-format')

    def test_claw(self):
        spack_info('claw')

    def test_cosmo(self):
        spack_info('cosmo')

    def test_cosmo_dycore(self):
        spack_info('cosmo-dycore')

    def test_cosmo_eccodes_definitions(self):
        spack_info('cosmo-eccodes-definitions')

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

    def test_py_black(self):
        spack_info('py-black')

    def test_py_boltons(self):
        spack_info('py-boltons')

    def test_py_cytoolz(self):
        spack_info('py-cytoolz')

    def test_py_devtools(self):
        spack_info('py-devtools')

    def test_py_editables(self):
        spack_info('py-editables')

    def test_py_factory_boy(self):
        spack_info('py-factory-boy')

    def test_py_fprettify(self):
        spack_info('py-fprettify')

    def test_py_frozendict(self):
        spack_info('py-frozendict')

    def test_py_gridtools_cpp(self):
        spack_info('py-gridtools-cpp')

    def test_py_gt4py(self):
        spack_info('py-gt4py')

    def test_py_hatchling(self):
        spack_info('py-hatchling')

    def test_py_icon4py(self):
        spack_info('py-icon4py')

    def test_py_inflection(self):
        spack_info('py-inflection')

    def test_py_lark(self):
        spack_info('py-lark')

    def test_py_pathspec(self):
        spack_info('py-pathspec')

    def test_py_pytest_factoryboy(self):
        spack_info('py-pytest-factoryboy')

    def test_py_toolz(self):
        spack_info('py-toolz')

    def test_py_typing_extensions(self):
        spack_info('py-typing')

    def test_xcodeml_tools(self):
        spack_info('xcodeml-tools')

    def test_zlib_ng(self):
        spack_info('zlib_ng')


class PlainSpecTest(unittest.TestCase):
    """Tests that the command 'spack spec <package>' works for all spack-c2sm packages."""

    def test_clang_format(self):
        spack_spec('clang-format')

    def test_claw(self):
        spack_spec('claw')

    def test_cosmo(self):
        spack_spec('cosmo')
        spack_spec('cosmo cosmo_target=gpu ~cppdycore')
        spack_spec('cosmo cosmo_target=gpu +serialize +claw +zlib_ng +oasis')

    def test_cosmo_dycore(self):
        spack_spec('cosmo-dycore')
        spack_spec('cosmo-dycore ~cuda +gt1')
        spack_spec('cosmo-dycore +cuda +gt1 +build_tests')

    def test_cosmo_eccodes_definitions(self):
        spack_spec('cosmo-eccodes-definitions')

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
        spack_spec('int2lm +parallel')

    def test_libgrib1(self):
        spack_spec('libgrib1')

    def test_oasis(self):
        spack_spec('oasis')

    def test_omni_xmod_pool(self):
        spack_spec('omni-xmod-pool')

    def test_py_black(self):
        spack_spec('py-black')

    def test_py_boltons(self):
        spack_spec('py-boltons')

    def test_py_cytoolz(self):
        spack_spec('py-cytoolz')

    def test_py_devtools(self):
        spack_spec('py-devtools')

    def test_py_editables(self):
        spack_spec('py-editables')

    def test_py_factory_boy(self):
        spack_spec('py-factory-boy')

    def test_py_fprettify(self):
        spack_spec('py-fprettify')

    def test_py_frozendict(self):
        spack_spec('py-frozendict')

    def test_py_gridtools_cpp(self):
        spack_spec('py-gridtools-cpp')

    def test_py_gt4py(self):
        spack_spec('py-gt4py')

    def test_py_hatchling(self):
        spack_spec('py-hatchling')

    def test_py_icon4py(self):
        spack_spec('py-icon4py')

    def test_py_inflection(self):
        spack_spec('py-inflection')

    def test_py_lark(self):
        spack_spec('py-lark')

    def test_py_pathspec(self):
        spack_spec('py-pathspec')

    def test_py_pytest_factoryboy(self):
        spack_spec('py-pytest-factoryboy')

    def test_py_toolz(self):
        spack_spec('py-toolz')

    def test_py_typing_extensions(self):
        spack_spec('py-typing')

    def test_xcodeml_tools(self):
        spack_spec('xcodeml-tools')

    def test_zlib_ng(self):
        spack_spec('zlib_ng')


if __name__ == '__main__':
    unittest.main(verbosity=2)
