import unittest
import sys
import os
from pathlib import Path
from context import needs_testing, if_context_includes, skip_machines

spack_c2sm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '..')

sys.path.append(os.path.normpath(spack_c2sm_path))
from src import machine_name, log_with_spack


def test_with_spack(command: str, log_name: str = None):
    if log_name is None:
        log_name = command.replace('--show-log-on-error ', '') \
            .replace('--test=root ', '') \
            .replace('-v ', '') \
            .replace(' ', '_') \
            .replace('%', '')

    log = Path(
        f'{spack_c2sm_path}/log/{machine_name()}/system_test/{log_name}.log')
    ret = log_with_spack(command, log)
    ret.check_returncode()


def spack_installcosmo_and_test(command: str, log_name: str = None):
    test_with_spack(f'spack installcosmo -v {command}', log_name)


def spack_install_and_test(command: str, log_name: str = None):
    test_with_spack(f'spack install --show-log-on-error --test=root {command}',
                    log_name)


@if_context_includes('cosmo')
class CosmoTest(unittest.TestCase):
    package_name = 'cosmo'

    def test_install_version_6_0_cpu(self):
        spack_installcosmo_and_test(
            'cosmo @6.0 %nvhpc cosmo_target=cpu ~cppdycore')

    def test_install_version_6_0_gpu(self):
        spack_installcosmo_and_test(
            'cosmo @6.0 %nvhpc cosmo_target=gpu +cppdycore')

    def test_devbuild_version_6_0_cpu(self):
        #spack_install_and_test('cosmo @6.0 %nvhpc cosmo_target=cpu ~cppdycore')
        pass  #TODO

    def test_devbuild_version_6_0_gpu(self):
        #spack_install_and_test('cosmo @6.0 %nvhpc cosmo_target=gpu +cppdycore')
        pass  #TODO

    def test_install_version_5_09_mch_1_2_p2(self):
        spack_installcosmo_and_test(
            'cosmo @5.09a.mch1.2.p2 %nvhpc cosmo_target=gpu +cppdycore')


@if_context_includes('cosmo-dycore')
class CosmoDycoreTest(unittest.TestCase):
    package_name = 'cosmo-dycore'

    def test_install_version_6_0_cuda(self):
        spack_install_and_test('cosmo-dycore @6.0 +cuda')

    def test_install_version_6_0_no_cuda(self):
        spack_install_and_test('cosmo-dycore @6.0 ~cuda')


@if_context_includes('cosmo-eccodes-definitions')
class CosmoEccodesDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-eccodes-definitions'

    def test_install_version_2_19_0_7(self):
        spack_install_and_test('cosmo-eccodes-definitions @2.19.0.7')


@if_context_includes('cosmo-grib-api')
class CosmoGribApiTest(unittest.TestCase):
    package_name = 'cosmo-grib-api'

    def test_install_version_1_20_0_3(self):
        spack_install_and_test('cosmo-grib-api @1.20.0.2')


@if_context_includes('cosmo-grib-api-definitions')
class CosmoGribApiDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-grib-api-definitions'


@if_context_includes('dawn')
class DawnTest(unittest.TestCase):
    package_name = 'dawn'


@if_context_includes('dawn4py')
class Dawn4PyTest(unittest.TestCase):
    package_name = 'dawn4py'


@if_context_includes('dusk')
class DuskTest(unittest.TestCase):
    package_name = 'dusk'


@if_context_includes('icon')
class GridToolsTest(unittest.TestCase):
    package_name = 'gridtools'

    def test_install_version_1_1_3(self):
        spack_install_and_test('gridtools @1.1.3')


@if_context_includes('icon')
@skip_machines('tsa')  # config file does not exist for these machines
class IconTest(unittest.TestCase):
    package_name = 'icon'

    def test_install_nwp_gpu(self):
        spack_install_and_test(
            'icon @nwp %nvhpc icon_target=gpu +claw +eccodes +ocean')

    def test_install_nwp_cpu(self):
        spack_install_and_test(
            'icon @nwp %nvhpc icon_target=cpu serialize_mode=create +eccodes +ocean'
        )

    def test_devbuild_nwp_gpu(self):
        spack_install_and_test(
            'icon @develop %nvhpc config_dir=./.. icon_target=gpu')

    def test_devbuild_nwp_cpu(self):
        spack_install_and_test(
            'icon @develop %nvhpc config_dir=./.. icon_target=cpu')

    def test_install_exclaim_cpu(self):
        spack_install_and_test(
            'icon @exclaim-master %nvhpc icon_target=cpu +eccodes +ocean')

    def test_install_exclaim_cpu_gcc(self):
        spack_install_and_test(
            'icon @exclaim-master %gcc icon_target=gpu +eccodes +ocean +claw')

    def test_install_exclaim_gpu(self):
        spack_install_and_test(
            'icon @exclaim-master %nvhpc icon_target=gpu +eccodes +ocean +claw'
        )


@if_context_includes('int2lm')
class Int2lmTest(unittest.TestCase):
    package_name = 'int2lm'

    def test_install_nvhpc(self):
        spack_install_and_test('int2lm @int2lm-3.00 %nvhpc')

    def test_install_gcc(self):
        spack_install_and_test('int2lm @c2sm-master %gcc')

    def test_install_nvhpc(self):
        spack_install_and_test('int2lm @c2sm-master %nvhpc')


@if_context_includes('icontools')
class IconToolsTest(unittest.TestCase):
    package_name = 'icontools'

    def test_install(self):
        spack_install_and_test('icontools @c2sm-master %gcc')


@if_context_includes('libgrib1')
class LibGrib1Test(unittest.TestCase):
    package_name = 'libgrib1'

    def test_install_version_22_01_2020(self):
        spack_install_and_test('libgrib1 @22-01-2020')


@if_context_includes('oasis')
class OasisTest(unittest.TestCase):
    package_name = 'oasis'


@if_context_includes('omni-xmod-pool')
class OmniXmodPoolTest(unittest.TestCase):
    package_name = 'omni-xmod-pool'

    def test_install_version_0_1(self):
        spack_install_and_test('omni-xmod-pool @0.1')


@if_context_includes('omnicompiler')
class OmniCompilerTest(unittest.TestCase):
    package_name = 'omnicompiler'

    def test_install_version_1_3_2(self):
        spack_install_and_test('omnicompiler @1.3.2')


@if_context_includes('xcodeml-tools')
class XcodeMLToolsTest(unittest.TestCase):
    package_name = 'xcodeml-tools'

    def test_install_version_92a35f9(self):
        spack_install_and_test('xcodeml-tools @92a35f9')


@if_context_includes('zlib_ng')
class ZLibNGTest(unittest.TestCase):
    package_name = 'zlib_ng'

    def test_install_version_2_0_0(self):
        spack_install_and_test('xcodeml-tools @2.0.0')


if __name__ == '__main__':
    commands = sys.argv[1:]
    sys.argv = [sys.argv[0]]  # unittest needs this
    unittest.main(verbosity=2)
