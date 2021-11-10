#!/usr/bin/python

import copy
import inspect
import sys
import subprocess
import unittest

def run(command: str):
    setup = ''
    if command.startswith('spack'):
        setup = 'source spack/share/spack/setup-env.sh && '
    
    subprocess.run(setup + command, check=True, shell=True)

# For each spack test there should be at least one line of comment stating
# why this spack command is tested and/or where this spack command is used.
# Otherwise this may apply:
# “All Your Tests are Terrible..." - Titus Winters & Hyrum Wright
# https://www.youtube.com/watch?v=u5senBJUkPc&ab_channel=CppCon


class AtlasTest(unittest.TestCase):
    package_name = 'atlas'
    depends_on = {'ecbuild', 'eckit'}


class AtlasUtilityTest(unittest.TestCase):
    package_name = 'atlas_utilities'
    depends_on = {'atlas', 'eckit'}


class ClawTest(unittest.TestCase):
    package_name = 'claw'
    depends_on = {}


class CosmoTest(unittest.TestCase):
    package_name = 'cosmo'
    depends_on = {'cuda', 'serialbox', 'libgrib1', 'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'omni-xmod-pool', 'claw', 'zlib_ng', 'cosmo-dycore'}

    def test_install_master_gpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore')

    def test_install_master_cpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack installcosmo cosmo@master%pgi cosmo_target=cpu ~cppdycore')

    # def test_install_test(self):
    #     # TODO! From https://github.com/C2SM/spack-c2sm/pull/289
    #     run('spack installcosmo --test=root cosmo@master%pgi')

    # def test_install_test_claw(self):
    #     # TODO! From https://github.com/C2SM/spack-c2sm/pull/289
    #     run('spack installcosmo --test=root cosmo@master%pgi +claw')

    def test_devbuild(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('git clone git@github.com:MeteoSwiss-APN/cosmo.git')
        run('cd cosmo')

        with self.subTest(case='gpu'):
            run('spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=gpu +cppdycore')
        with self.subTest(case='gpu'):
            run('spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=cpu ~cppdycore')

        # run('cd ..')
        # run('rm -rf cosmo')


class CosmoDycoreTest(unittest.TestCase):
    package_name = 'cosmo-dycore'
    depends_on = {'gridtools', 'serialbox', 'cuda'}


class CosmoEccodesDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-eccodes-definitions'
    depends_on = {'eccodes'}


class CosmoGribApiTest(unittest.TestCase):
    package_name = 'cosmo-grib-api'
    depends_on = {}


class CosmoGribApiDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-grib-api-definitions'
    depends_on = {'cosmo-grib-api'}


class CudaTest(unittest.TestCase):
    package_name = 'cuda'
    depends_on = {}


class DawnTest(unittest.TestCase):
    package_name = 'dawn'
    depends_on = {}


class Dawn4PyTest(unittest.TestCase):
    package_name = 'dawn4py'
    depends_on = {}


class DuskTest(unittest.TestCase):
    package_name = 'dusk'
    depends_on = {'dawn4py'}


class DyiconBenchmarksTest(unittest.TestCase):
    package_name = 'dyicon_benchmarks'
    depends_on = {'atlas_utilities', 'atlas', 'cuda'}


class EcbuildTest(unittest.TestCase):
    package_name = 'ecbuild'
    depends_on = {}


class EccodesTest(unittest.TestCase):
    package_name = 'eccodes'
    depends_on = {}


class EckitTest(unittest.TestCase):
    package_name = 'eckit'
    depends_on = {'ecbuild'}


class GridToolsTest(unittest.TestCase):
    package_name = 'gridtools'
    depends_on = {'cuda'}


class IconTest(unittest.TestCase):
    package_name = 'icon'
    depends_on = {'serialbox', 'eccodes', 'claw'}

    # def test_install(self):
    #     # TODO! From https://github.com/C2SM/spack-c2sm/pull/289
    #     run('spack install icon@nwp%pgi icon_target=gpu +claw')

    # TODO: Reactivate once the test works!
    # def test_devbuild_cpu(self):
    #     # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
    #     run('git clone --recursive git@gitlab.dkrz.de:icon/icon-cscs.git')
    #     run('cd icon-cscs')
    #     run('mkdir -p pgi_cpu')
    #     run('cd pgi_cpu')
    #     run('touch a_fake_file.f90')
        
    #     try:
    #         run('spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=cpu')
    #     finally:
    #         run('cd ../..')
    #         run('rm -rf icon-cscs')

    # TODO: Reactivate once the test works!
    # def test_devbuild_gpu(self):
    #     # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
    #     run('git clone --recursive git@gitlab.dkrz.de:icon/icon-cscs.git')
    #     run('cd icon-cscs')
    #     run('mkdir -p pgi_gpu')
    #     run('cd pgi_gpu')
    #     run('touch a_fake_file.f90')

    #     try:
    #         run('spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=gpu')
    #     finally:
    #         run('cd ../..')
    #         run('rm -rf icon-cscs')


class Int2lmTest(unittest.TestCase):
    package_name = 'int2lm'
    depends_on = {'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'libgrib1'}

    def test_install(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack install int2lm@c2sm_master%pgi')

    # def test_install_test(self):
    #     # TODO! From https://github.com/C2SM/spack-c2sm/pull/319
    #     run('spack install --test=root int2lm@c2sm_master%gcc')

    def test_install_no_pollen(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack install int2lm@org_master%pgi pollen=False')


class IconDuskE2ETest(unittest.TestCase):
    package_name = 'icondusk-e2e'
    depends_on = {'atlas_utilities', 'dawn4py', 'dusk', 'atlas', 'cuda'}


class IconToolsTest(unittest.TestCase):
    package_name = 'icontools'
    depends_on = {'eccodes', 'cosmo-grib-api'}


class LibGrib1Test(unittest.TestCase):
    package_name = 'libgrib1'
    depends_on = {}


class LogTest(unittest.TestCase):
    package_name = 'log'
    depends_on = {}


class MpichTest(unittest.TestCase):
    package_name = 'mpich'
    depends_on = {}


class OasisTest(unittest.TestCase):
    package_name = 'oasis'
    depends_on = {}


class OmniCompilerTest(unittest.TestCase):
    package_name = 'omnicompiler'
    depends_on = {}


class OmniXmodPoolest(unittest.TestCase):
    package_name = 'omni-xmod-pool'
    depends_on = {}


class OpenMPITest(unittest.TestCase):
    package_name = 'openmpi'
    depends_on = {}


class SerialBoxTest(unittest.TestCase):
    package_name = 'serialbox'
    depends_on = {}


class XcodeMLToolsTest(unittest.TestCase):
    package_name = 'xcodeml-tools'
    depends_on = {}


class ZLibNGTest(unittest.TestCase):
    package_name = 'zlib_ng'
    depends_on = {}


# A set of all test case classes
all_test_cases = {c for _,c in inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and issubclass(member, unittest.TestCase))}

# Maps all packages in this repo to the set of packages they depend on. Must form a DAG.
dependencies = {case.package_name: case.depends_on for case in all_test_cases}

# Maps commands to a set of commands or packages. Must form a DAG.
# The keys can't be package names.
expansions = {
    'all': {case.package_name for case in all_test_cases}
}

def Self_and_up(origin: set, DAG: map) -> set:
    reachers = copy.deepcopy(origin)
    while True:
        old_size = len(reachers)
        # add elements up the DAG
        reachers |= {parent for parent, children in DAG.items() if any(child in reachers for child in children)}
        new_size = len(reachers)
        if old_size == new_size:
            return reachers

def Has_cycle(directed_graph: map) -> bool:
    return False # TODO!


class DAG_Algorithm_Test(unittest.TestCase):

    def test_direction(self):
        # a -> b -> c
        DAG = {'a': {'b'}, 'b': {'c'}}
        reachers = Self_and_up({'b'}, DAG)
        self.assertTrue('a' in reachers)

    def test_transitivity(self):
        # a -> b -> c -> d
        DAG = {'a': {'b'}, 'b': {'c'}, 'c': {'d'}}
        reachers = Self_and_up({'c'}, DAG)
        self.assertEqual(reachers, {'a','b','c'})

    def test_diamon(self):
        # a -> b+c -> d
        DAG = {'a': {'b','c'}, 'b': {'d'}, 'c': {'d'}}
        b_reachers = Self_and_up({'b'}, DAG)
        c_reachers = Self_and_up({'c'}, DAG)
        d_reachers = Self_and_up({'d'}, DAG)
        self.assertEqual(b_reachers, {'a','b'})
        self.assertEqual(c_reachers, {'a','c'})
        self.assertEqual(d_reachers, {'a','b','c','d'})

    # def test_cycle(self): TODO!
    #     # a <-> b
    #     graph = {'a': {'b'}, 'b': {'a'}}
    #     self.assertTrue(Has_cycle(graph))

    def test_no_cycle(self):
        # a -> b
        graph = {'a': {'b'}}
        self.assertFalse(Has_cycle(graph))

    def test_diamon_is_acyclic(self):
        # a -> b+c -> d
        DAG = {'a': {'b','c'}, 'b': {'d'}, 'c': {'d'}}
        self.assertFalse(Has_cycle(DAG))


class SelfTest(unittest.TestCase):

    def test_expansions(self):
        """Tests that expandable commands are not package names"""
        for exp in expansions.keys():
            self.assertTrue(exp not in dependencies)

    def test_dependencies_is_acyclic(self):
        self.assertFalse(Has_cycle(dependencies))

    def test_expansions_is_acyclic(self):
        self.assertFalse(Has_cycle(expansions))

    def test_all_dependencies_are_packages(self):
        all_package_names = {case.package_name for case in all_test_cases}
        for _, deps in dependencies.items():
            for dep in deps:
                self.assertTrue(dep in all_package_names)


if __name__ == '__main__':
    test_loader = unittest.TestLoader()

    # Do self test first to fail fast
    suite = unittest.TestSuite([
        test_loader.loadTestsFromTestCase(DAG_Algorithm_Test),
        test_loader.loadTestsFromTestCase(SelfTest)
    ])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        sys.exit(False)

    commands = sys.argv[1:]
    sys.argv = [sys.argv[0]] # unittest needs this

    commands.remove('launch')
    commands.remove('jenkins')

    upstream = 'OFF'
    if '--upstream' in commands:
        upstream = 'ON'
        commands.remove('--upstream')

    if '--daint' in commands:
        machine = 'daint'
        commands.remove('--daint')
    if '--tsa' in commands:
        machine = 'tsa'
        commands.remove('--tsa')

    # configure spack
    subprocess.run(f'python ./config.py -m {machine} -i . -r ./spack/etc/spack -p ./spack -s ./spack -u {upstream} -c ./spack-cache', check=True, shell=True)

    known_commands = dependencies.keys() | expansions.keys()

    # handles backward compatibility to run any command
    if any(c not in known_commands for c in commands):
        print('Input contains unknown command.')
        run(' '.join(commands))
        sys.exit()

    commands = set(commands)

    # expand expandable commands
    while any(c in expansions for c in commands):
        for c in commands:
            if c in expansions:
                commands |= expansions[c]
                commands.remove(c)
                break

    # all commands are packages now!

    packages_to_test = Self_and_up(commands, dependencies)

    # collect tests from all packages to test
    suite = unittest.TestSuite([
        test_loader.loadTestsFromTestCase(case)
        for case in all_test_cases if case.package_name in packages_to_test
    ])
    
    # run tests
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())