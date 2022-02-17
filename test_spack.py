#!/usr/bin/python

import copy
import inspect
import sys
import subprocess
import unittest

all_machines = {'daint', 'tsa'}


def run(command: str, cwd='.'):
    setup = ''
    if command.startswith('spack'):
        setup = f'source spack/share/spack/setup-env.sh &&'

    subprocess.run(f'{setup} cd {cwd} && {command}', check=True, shell=True)


# For each spack test there should be at least one line of comment stating
# why this spack command is tested and/or where this spack command is used.
# Otherwise this may apply:
# “All Your Tests are Terrible..." - Titus Winters & Hyrum Wright
# https://www.youtube.com/watch?v=u5senBJUkPc&ab_channel=CppCon


class AtlasTest(unittest.TestCase):
    package_name = 'atlas'
    depends_on = {'ecbuild', 'eckit'}
    machines = all_machines


class AtlasUtilityTest(unittest.TestCase):
    package_name = 'atlas_utilities'
    depends_on = {'atlas', 'eckit'}
    machines = all_machines


class ClawTest(unittest.TestCase):
    package_name = 'claw'
    depends_on = {}
    machines = all_machines


class CosmoTest(unittest.TestCase):
    package_name = 'cosmo'
    depends_on = {
        'cuda', 'serialbox', 'libgrib1', 'cosmo-grib-api-definitions',
        'cosmo-eccodes-definitions', 'omni-xmod-pool', 'claw', 'zlib_ng',
        'cosmo-dycore'
    }
    machines = all_machines

    def test_install_master_gpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack installcosmo cosmo@org-master%pgi cosmo_target=gpu +cppdycore'
            )

    def test_install_master_cpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack installcosmo cosmo@org-master%pgi cosmo_target=cpu ~cppdycore'
            )

    # def test_install_test(self):
    #     # TODO: Decide if we want to integrate this test or not. It has been used lately here: From https://github.com/C2SM/spack-c2sm/pull/289
    #     run('spack installcosmo --test=root cosmo@master%pgi')

    # def test_install_test_claw(self):
    #     # TODO: Decide if we want to integrate this test or not. It has been used lately here: From https://github.com/C2SM/spack-c2sm/pull/289
    #     run('spack installcosmo --test=root cosmo@master%pgi +claw')

    def test_devbuild_cpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('git clone git@github.com:MeteoSwiss-APN/cosmo.git')
        try:
            run('spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=cpu ~cppdycore',
                cwd='cosmo')
        finally:
            run('rm -rf cosmo')

    def test_devbuild_gpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('git clone git@github.com:MeteoSwiss-APN/cosmo.git')
        try:
            run('spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=gpu +cppdycore',
                cwd='cosmo')
        finally:
            run('rm -rf cosmo')

    def test_install_old_version(self):
        # So we can reproduce results from old versions.
        run('spack installcosmo cosmo@apn_5.08.mch.1.0.p3%pgi cosmo_target=cpu ~cppdycore'
            )


class CosmoDycoreTest(unittest.TestCase):
    package_name = 'cosmo-dycore'
    depends_on = {'gridtools', 'serialbox', 'cuda'}
    machines = all_machines


class CosmoEccodesDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-eccodes-definitions'
    depends_on = {'eccodes'}
    machines = all_machines


class CosmoGribApiTest(unittest.TestCase):
    package_name = 'cosmo-grib-api'
    depends_on = {}
    machines = all_machines


class CosmoGribApiDefinitionsTest(unittest.TestCase):
    package_name = 'cosmo-grib-api-definitions'
    depends_on = {'cosmo-grib-api'}
    machines = all_machines


class CudaTest(unittest.TestCase):
    package_name = 'cuda'
    depends_on = {}
    machines = all_machines


class DawnTest(unittest.TestCase):
    package_name = 'dawn'
    depends_on = {}
    machines = all_machines


class Dawn4PyTest(unittest.TestCase):
    package_name = 'dawn4py'
    depends_on = {}
    machines = all_machines


class DuskTest(unittest.TestCase):
    package_name = 'dusk'
    depends_on = {'dawn4py'}
    machines = all_machines


class DyiconBenchmarksTest(unittest.TestCase):
    package_name = 'dyicon_benchmarks'
    depends_on = {'atlas_utilities', 'atlas', 'cuda'}
    machines = all_machines


class EcbuildTest(unittest.TestCase):
    package_name = 'ecbuild'
    depends_on = {}
    machines = all_machines


class EccodesTest(unittest.TestCase):
    package_name = 'eccodes'
    depends_on = {}
    machines = all_machines


class EckitTest(unittest.TestCase):
    package_name = 'eckit'
    depends_on = {'ecbuild'}
    machines = all_machines


class GridToolsTest(unittest.TestCase):
    package_name = 'gridtools'
    depends_on = {'cuda'}
    machines = all_machines


class IconTest(unittest.TestCase):
    package_name = 'icon'
    depends_on = {'serialbox', 'eccodes', 'claw'}
    machines = {'daint'}

    def test_install_nwp_gpu_nvidia(self):
        # So we can make sure ICON-NWP (OpenACC) devs can compile (mimick Buildbot for Tsa)
        run('spack install icon@nwp%nvhpc icon_target=gpu +claw +eccodes +ocean'
            )

    def test_install_nwp_cpu_nvidia(self):
        # So we can make sure ICON-NWP (OpenACC) devs can compile (mimick Buildbot for Tsa)
        run('spack install icon@nwp%nvhpc icon_target=cpu serialize_mode=create +eccodes +ocean'
            )

    # TODO: Reactivate once the test works!
    # def test_devbuild_cpu(self):
    #     # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
    #     run('git clone --recursive git@gitlab.dkrz.de:icon/icon-cscs.git')
    #     run('mkdir -p icon-cscs/pgi_cpu')
    #     run('touch a_fake_file.f90', cwd='icon-cscs/pgi_cpu')

    #     try:
    #         run('spack dev-build -i -u build icon@dev-build%pgi config_dir=./.. icon_target=cpu', cwd='icon-cscs/pgi_cpu')
    #     finally:
    #         run('rm -rf icon-cscs')

    # TODO: Reactivate once the test works!
    # def test_devbuild_gpu(self):
    #     # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
    #     run('git clone --recursive git@gitlab.dkrz.de:icon/icon-cscs.git')
    #     run('mkdir -p icon-cscs/pgi_gpu')
    #     run('touch a_fake_file.f90', cwd='icon-cscs/pgi_gpu')

    #     try:
    #         run('spack dev-build -i -u build icon@dev-build%pgi config_dir=./.. icon_target=gpu', cwd='icon-cscs/pgi_gpu')
    #     finally:
    #         run('rm -rf icon-cscs')


class Int2lmTest(unittest.TestCase):
    package_name = 'int2lm'
    depends_on = {
        'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'libgrib1'
    }
    machines = all_machines

    def test_install_pgi(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack install --test=root int2lm@c2sm-master%pgi')

    def test_install_gcc(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack install --test=root int2lm@c2sm-master%gcc')

    def test_install_no_pollen(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        run('spack install --test=root int2lm@org-master%pgi pollen=False')


class IconDuskE2ETest(unittest.TestCase):
    package_name = 'icondusk-e2e'
    depends_on = {'atlas_utilities', 'dawn4py', 'dusk', 'atlas', 'cuda'}
    machines = all_machines


class IconToolsTest(unittest.TestCase):
    package_name = 'icontools'
    depends_on = {'eccodes', 'cosmo-grib-api'}
    machines = all_machines

    # C2SM supported version
    def test_install(self):
        run('spack install --test=root icontools@c2sm-master%gcc')


class LibGrib1Test(unittest.TestCase):
    package_name = 'libgrib1'
    depends_on = {}
    machines = all_machines


class LogTest(unittest.TestCase):
    package_name = 'log'
    depends_on = {}
    machines = all_machines


class MpichTest(unittest.TestCase):
    package_name = 'mpich'
    depends_on = {}
    machines = all_machines


class OasisTest(unittest.TestCase):
    package_name = 'oasis'
    depends_on = {}
    machines = all_machines


class OmniCompilerTest(unittest.TestCase):
    package_name = 'omnicompiler'
    depends_on = {}
    machines = all_machines


class OmniXmodPoolTest(unittest.TestCase):
    package_name = 'omni-xmod-pool'
    depends_on = {}
    machines = all_machines


class OpenMPITest(unittest.TestCase):
    package_name = 'openmpi'
    depends_on = {}
    machines = all_machines


class SerialBoxTest(unittest.TestCase):
    package_name = 'serialbox'
    depends_on = {}
    machines = all_machines


class XcodeMLToolsTest(unittest.TestCase):
    package_name = 'xcodeml-tools'
    depends_on = {}
    machines = all_machines


class ZLibNGTest(unittest.TestCase):
    package_name = 'zlib_ng'
    depends_on = {}
    machines = all_machines


# A set of all test case classes
all_test_cases = {
    c
    for _, c in inspect.getmembers(
        sys.modules[__name__], lambda member: inspect.isclass(member) and
        issubclass(member, unittest.TestCase))
}

# Maps all packages in this repo to the set of packages they depend on. Must form a DAG.
dependencies = {case.package_name: case.depends_on for case in all_test_cases}

# Maps commands to a set of commands or packages. Must form a DAG.
# The keys can't be package names.
expansions = {'all': {case.package_name for case in all_test_cases}}


def Self_and_up(origin: set, DAG: map) -> set:
    reachers = copy.deepcopy(origin)
    while True:
        old_size = len(reachers)
        # add elements up the DAG
        reachers |= {
            parent
            for parent, children in DAG.items()
            if any(child in reachers for child in children)
        }
        new_size = len(reachers)
        if old_size == new_size:
            return reachers


def Has_cycle(directed_graph: map, visited=None, vertex=None) -> bool:
    if visited is None and vertex is None:
        return any(
            Has_cycle(directed_graph, set(), element)
            for element in directed_graph)

    if vertex not in directed_graph:
        return False
    for next in directed_graph[vertex]:
        if next in visited:
            return True
        if Has_cycle(directed_graph, visited | set(next), next):
            return True
    return False


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
        self.assertEqual(reachers, {'a', 'b', 'c'})

    def test_diamond(self):
        # a -> b+c -> d
        DAG = {'a': {'b', 'c'}, 'b': {'d'}, 'c': {'d'}, 'd': {}}
        b_reachers = Self_and_up({'b'}, DAG)
        c_reachers = Self_and_up({'c'}, DAG)
        d_reachers = Self_and_up({'d'}, DAG)
        self.assertEqual(b_reachers, {'a', 'b'})
        self.assertEqual(c_reachers, {'a', 'c'})
        self.assertEqual(d_reachers, {'a', 'b', 'c', 'd'})

    def test_cycle(self):
        # a <-> b
        graph = {'a': {'b'}, 'b': {'a'}}
        self.assertTrue(Has_cycle(graph))

    def test_no_cycle(self):
        # a -> b
        graph = {'a': {'b'}, 'b': {}}
        self.assertFalse(Has_cycle(graph))

    def test_diamond_is_acyclic(self):
        # a -> b+c -> d
        DAG = {'a': {'b', 'c'}, 'b': {'d'}, 'c': {'d'}, 'd': {}}
        self.assertFalse(Has_cycle(DAG))


class SelfTest(unittest.TestCase):

    def test_expansions(self):
        """Tests that expandable commands are not package names"""
        for exp in expansions.keys():
            self.assertTrue(exp not in dependencies)

    def test_dependencies_is_acyclic(self):
        self.assertFalse(Has_cycle(dependencies))

    def test_expansions_is_acyclic(self):
        self.assertFalse(Has_cycle({**dependencies, **expansions}))

    def test_all_dependencies_are_packages(self):
        all_package_names = {case.package_name for case in all_test_cases}
        for _, deps in dependencies.items():
            for dep in deps:
                self.assertTrue(dep in all_package_names)


if __name__ == '__main__':
    test_loader = unittest.TestLoader()

    # Do self-test first to fail fast
    print('====================================', flush=True)
    print('Self-tests:', flush=True)
    print('====================================', flush=True)
    suite = unittest.TestSuite([
        test_loader.loadTestsFromTestCase(DAG_Algorithm_Test),
        test_loader.loadTestsFromTestCase(SelfTest)
    ])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print('====================================', flush=True)
    if not result.wasSuccessful():
        sys.exit(1)

    commands = sys.argv[1:]
    sys.argv = [sys.argv[0]]  # unittest needs this

    commands.remove('launch')
    commands.remove('jenkins')

    upstream = 'OFF'
    if '--upstream' in commands:
        upstream = 'ON'
        commands.remove('--upstream')

    exclusive = False
    if '--exclusive' in commands:
        exclusive = True
        commands.remove('--exclusive')

    if '--daint' in commands:
        machine = 'daint'
        commands.remove('--daint')
    if '--tsa' in commands:
        machine = 'tsa'
        commands.remove('--tsa')

    known_commands = dependencies.keys() | expansions.keys()

    # handles backward compatibility to run an arbitrary command
    is_arbitrary_command = any(c not in known_commands for c in commands)

    print('Test plan:', flush=True)
    print('====================================', flush=True)
    print(f'Configuring spack with upstream {upstream} on machine {machine}.',
          flush=True)

    if is_arbitrary_command:
        joined_command = ' '.join(commands)
        print(f'Executing: {joined_command}', flush=True)
    else:
        commands = set(commands)

        # expand expandable commands
        while any(c in expansions for c in commands):
            for c in commands:
                if c in expansions:
                    commands |= expansions[c]
                    commands.remove(c)
                    break

        # all commands are packages now!

        if exclusive:
            packages_to_test = commands
        else:
            packages_to_test = Self_and_up(commands, dependencies)

        # run tests
        print(f'Testing packages: {packages_to_test}', flush=True)

    print('====================================', flush=True)
    print('Testing now...', flush=True)

    # configure spack
    subprocess.run(
        f'python ./config.py -m {machine} -i . -r ./spack/etc/spack -p ./spack -s ./spack -u {upstream} -c ./spack-cache',
        check=True,
        shell=True)

    if is_arbitrary_command:
        run(joined_command)
        sys.exit()
    else:
        # collect and run tests from all packages selected
        suite = unittest.TestSuite([
            test_loader.loadTestsFromTestCase(case) for case in all_test_cases
            if case.package_name in packages_to_test and machine in case.machines
        ])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(not result.wasSuccessful())
