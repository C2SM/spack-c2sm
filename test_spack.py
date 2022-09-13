#!/usr/bin/python

import copy
import inspect
import sys
import subprocess
import unittest
import asyncio
from random import randint

all_machines = {'daint', 'tsa'}

# For each spack test there should be at least one line of comment stating
# why this spack command is tested and/or where this spack command is used.
# Otherwise this may apply:
# “All Your Tests are Terrible..." - Titus Winters & Hyrum Wright
# https://www.youtube.com/watch?v=u5senBJUkPc&ab_channel=CppCon


class TestCase(unittest.TestCase):

    def Run(self, command: str, cwd='.', parallel=False):
        setup = ''
        if command.startswith('spack'):
            setup = f'source spack/share/spack/setup-env.sh ; '

        srun = ''
        if parallel:
            if machine == 'tsa':
                srun = 'srun -c 16 -t 01:00:00'
            if machine == 'daint':
                srun = 'srun -C gpu -A g110 -t 01:00:00'

        # randomly delay start of installation to avoid write-locks
        delay = randint(5, 20)

        # 2>&1 redirects stderr to stdout
        subprocess.run(
            f'{setup} (cd {cwd} ; {srun} sleep {delay} && {command}) >> {machine}_{self.package_name}_{self._testMethodName}.log 2>&1',
            check=True,
            shell=True)

    def Srun(self, command: str, cwd='.'):
        return self.Run(command, cwd, parallel=True)

    def spack_install_and_test(self, command: str, cwd='.'):
        if 'cosmo' in command and 'cosmo-dycore' not in command:
            spack_install = 'spack installcosmo -v'
        else:
            spack_install = 'spack install --show-log-on-error'

        cmd_build = spack_install + ' --until build ' + command
        self.Srun(cmd_build, cwd)

        cmd_root = spack_install + ' --dont-restage --test=root ' + command
        self.Run(cmd_root, cwd)

    def spack_devbuild_and_test(self, command: str, cwd='.'):
        cmd_build = 'spack devbuildcosmo --until build ' + command
        self.Srun(cmd_build, cwd)

        cmd_root = 'spack devbuildcosmo --dont-restage --test=root ' + command
        self.Run(cmd_root, cwd)


class AtlasUtilityTest(TestCase):
    package_name = 'atlas_utilities'
    depends_on = {}
    machines = all_machines


class ClawTest(TestCase):
    package_name = 'claw'
    depends_on = {}
    machines = all_machines


class CosmoTest(TestCase):
    package_name = 'cosmo'
    depends_on = {
        'cuda', 'serialbox', 'libgrib1', 'cosmo-grib-api-definitions',
        'cosmo-eccodes-definitions', 'omni-xmod-pool', 'claw', 'zlib_ng',
        'cosmo-dycore'
    }
    machines = all_machines

    def test_install_master_gpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        if machine == 'tsa':
            self.spack_install_and_test(
                'cosmo@org-master%pgi cosmo_target=gpu +cppdycore')
        else:
            self.spack_install_and_test(
                'cosmo@org-master%nvhpc cosmo_target=gpu +cppdycore')

    def test_install_master_cpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        if machine == 'tsa':
            self.spack_install_and_test(
                'cosmo@org-master%pgi cosmo_target=cpu ~cppdycore')
        else:
            self.spack_install_and_test(
                'cosmo@org-master%nvhpc cosmo_target=cpu ~cppdycore')

    # def test_install_test(self):
    #     # TODO: Decide if we want to integrate this test or not. It has been used lately here: From https://github.com/C2SM/spack-c2sm/pull/289
    #     self.Srun('spack installcosmo --test=root cosmo@master%pgi')

    # def test_install_test_claw(self):
    #     # TODO: Decide if we want to integrate this test or not. It has been used lately here: From https://github.com/C2SM/spack-c2sm/pull/289
    #     self.Srun('spack installcosmo --test=root cosmo@master%pgi +claw')

    def test_devbuild_cpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        self.Run('git clone ssh://git@github.com/MeteoSwiss-APN/cosmo.git')
        try:
            if machine == 'tsa':
                self.spack_devbuild_and_test(
                    'cosmo@dev-build%pgi cosmo_target=cpu ~cppdycore',
                    cwd='cosmo')
            else:
                self.spack_devbuild_and_test(
                    'cosmo@dev-build%nvhpc cosmo_target=cpu ~cppdycore',
                    cwd='cosmo')
        finally:
            self.Run('rm -rf cosmo')

    def test_devbuild_gpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        self.Run('git clone ssh://git@github.com/MeteoSwiss-APN/cosmo.git')
        try:
            if machine == 'tsa':
                self.spack_devbuild_and_test(
                    'cosmo@dev-build%pgi cosmo_target=gpu +cppdycore',
                    cwd='cosmo')
            else:
                self.Srun(
                    'spack devbuildcosmo cosmo@dev-build%nvhpc cosmo_target=gpu +cppdycore',
                    cwd='cosmo')
        finally:
            self.Run('rm -rf cosmo')

    def test_install_old_version(self):
        # So we can reproduce results from old versions.
        if machine == 'tsa':
            self.spack_install_and_test(
                'cosmo@apn_5.08.mch.1.0.p3%pgi cosmo_target=cpu ~cppdycore')


class CosmoDycoreTest(TestCase):
    package_name = 'cosmo-dycore'
    depends_on = {'gridtools', 'serialbox', 'cuda'}
    machines = all_machines

    def test_install_float_cpu(self):
        # The dycore team's PR testing relies on this.
        # The dycore tests launch an srun, therefore the spack command can't be launched in an srun aswell, because sruns don't nest!
        self.spack_install_and_test(
            'cosmo-dycore@master%gcc real_type=float build_type=Release ~cuda')

    def test_install_float_gpu(self):
        # The dycore team's PR testing relies on this.
        # The dycore tests launch an srun, therefore the spack command can't be launched in an srun aswell, because sruns don't nest!
        self.spack_install_and_test(
            'cosmo-dycore@master%gcc real_type=float build_type=Release +cuda')

    def test_install_double_cpu(self):
        # The dycore team's PR testing relies on this.
        # The dycore tests launch an srun, therefore the spack command can't be launched in an srun aswell, because sruns don't nest!
        self.spack_install_and_test(
            'cosmo-dycore@master%gcc real_type=double build_type=Release ~cuda'
        )

    def test_install_double_gpu(self):
        # The dycore team's PR testing relies on this.
        # The dycore tests launch an srun, therefore the spack command can't be launched in an srun aswell, because sruns don't nest!
        self.spack_install_and_test(
            'cosmo-dycore@master%gcc real_type=double build_type=Release +cuda'
        )


class CosmoEccodesDefinitionsTest(TestCase):
    package_name = 'cosmo-eccodes-definitions'
    depends_on = {'eccodes'}
    machines = all_machines


class CosmoGribApiTest(TestCase):
    package_name = 'cosmo-grib-api'
    depends_on = {}
    machines = all_machines


class CosmoGribApiDefinitionsTest(TestCase):
    package_name = 'cosmo-grib-api-definitions'
    depends_on = {'cosmo-grib-api'}
    machines = all_machines


class CudaTest(TestCase):
    package_name = 'cuda'
    depends_on = {}
    machines = all_machines


class DawnTest(TestCase):
    package_name = 'dawn'
    depends_on = {}
    machines = all_machines


class Dawn4PyTest(TestCase):
    package_name = 'dawn4py'
    depends_on = {}
    machines = all_machines


class DuskTest(TestCase):
    package_name = 'dusk'
    depends_on = {'dawn4py'}
    machines = all_machines


class EccodesTest(TestCase):
    package_name = 'eccodes'
    depends_on = {}
    machines = all_machines


class GridToolsTest(TestCase):
    package_name = 'gridtools'
    depends_on = {'cuda'}
    machines = all_machines


class IconTest(TestCase):
    package_name = 'icon'
    depends_on = {'serialbox', 'eccodes', 'claw'}
    machines = {'daint'}

    def test_install_nwp_gpu_nvidia(self):
        # So we can make sure ICON-NWP (OpenACC) devs can compile (mimicks Buildbot for Tsa)
        self.Srun(
            'spack install --show-log-on-error icon@nwp%nvhpc icon_target=gpu +claw +eccodes +ocean'
        )

    def test_install_nwp_cpu_nvidia(self):
        # So we can make sure ICON-NWP (OpenACC) devs can compile (mimicks Buildbot for Tsa)
        self.Srun(
            'spack install --show-log-on-error icon@nwp%nvhpc icon_target=cpu serialize_mode=create +eccodes +ocean'
        )

    def test_devbuild_cpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        self.Run(
            'git clone --recursive ssh://git@gitlab.dkrz.de/icon/icon-nwp.git')
        self.Run('mkdir -p icon-nwp/cpu')
        self.Run('touch .dummy_file', cwd='icon-nwp/cpu')
        try:
            self.Srun(
                'spack dev-build -u build icon@dev-build%nvhpc config_dir=./.. icon_target=cpu',
                cwd='icon-nwp/cpu')
        finally:
            self.Run('rm -rf icon-nwp')

    def test_devbuild_gpu(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        self.Run(
            'git clone --recursive ssh://git@gitlab.dkrz.de/icon/icon-nwp.git')
        self.Run('mkdir -p icon-nwp/gpu')
        self.Run('touch .dummy_file', cwd='icon-nwp/gpu')
        try:
            self.Srun(
                'spack dev-build -u build icon@dev-build%nvhpc config_dir=./.. icon_target=gpu',
                cwd='icon-nwp/gpu')
        finally:
            self.Run('rm -rf icon-nwp')


class IconTestExclaim(TestCase):
    package_name = 'icon'
    depends_on = {'serialbox', 'eccodes', 'claw'}
    machines = 'daint'

    def test_install_exclaim_cpu_nvidia(self):
        self.spack_install_and_test(
            'icon@exclaim-master%nvhpc icon_target=cpu +eccodes +ocean')

    def test_install_exclaim_gpu_nvidia(self):
        self.spack_install_and_test(
            'icon@exclaim-master%nvhpc icon_target=gpu +eccodes +ocean +claw')

    def test_install_exclaim_cpu_gcc(self):
        self.spack_install_and_test(
            'icon@exclaim-master%gcc icon_target=cpu +eccodes +ocean')


class Int2lmTest(TestCase):
    package_name = 'int2lm'
    depends_on = {
        'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'libgrib1'
    }
    machines = all_machines

    def test_install_pgi(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        if machine == 'tsa':
            self.spack_install_and_test('int2lm@c2sm-master%pgi')

    def test_install_no_pollen(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        if machine == 'tsa':
            self.spack_install_and_test('int2lm@org-master%pgi pollen=False')

    def test_install_gcc(self):
        # So our quick start tutorial works: https://c2sm.github.io/spack-c2sm/QuickStart.html
        self.spack_install_and_test('int2lm@c2sm-master%gcc')

    def test_install_nvhpc(self):
        # Replacement of PGI after upgrade of Daint Feb 22
        if machine == 'daint':
            self.spack_install_and_test('int2lm@c2sm-master%nvhpc')

    def test_install_nvhpc_features(self):
        # c2sm-features contains some additional functionalities
        if machine == 'daint':
            self.spack_install_and_test('int2lm@c2sm-features%nvhpc')


class IconToolsTest(TestCase):
    package_name = 'icontools'
    depends_on = {'eccodes', 'cosmo-grib-api'}
    machines = all_machines

    # C2SM supported version
    def test_install(self):
        self.spack_install_and_test('icontools@c2sm-master%gcc')


class LibGrib1Test(TestCase):
    package_name = 'libgrib1'
    depends_on = {}
    machines = all_machines


class LogTest(TestCase):
    package_name = 'log'
    depends_on = {}
    machines = all_machines


class MpichTest(TestCase):
    package_name = 'mpich'
    depends_on = {}
    machines = all_machines


class OasisTest(TestCase):
    package_name = 'oasis'
    depends_on = {}
    machines = all_machines


class OmniCompilerTest(TestCase):
    package_name = 'omnicompiler'
    depends_on = {}
    machines = all_machines


class OmniXmodPoolTest(TestCase):
    package_name = 'omni-xmod-pool'
    depends_on = {}
    machines = all_machines


class OpenMPITest(TestCase):
    package_name = 'openmpi'
    depends_on = {}
    machines = all_machines


class SerialBoxTest(TestCase):
    package_name = 'serialbox'
    depends_on = {}
    machines = all_machines


class XcodeMLToolsTest(TestCase):
    package_name = 'xcodeml-tools'
    depends_on = {}
    machines = all_machines


class ZLibNGTest(TestCase):
    package_name = 'zlib_ng'
    depends_on = {}
    machines = all_machines


# A set of all test case classes
all_test_cases = {
    c
    for _, c in inspect.getmembers(
        sys.modules[__name__], lambda member: inspect.isclass(member) and
        issubclass(member, TestCase) and member != TestCase)
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


class CustomTestSuite(unittest.TestSuite):

    def run(self, result, debug=False):
        """
        We override the 'run' routine to support the execution of unittest in parallel
        :param result:
        :param debug:
        :return:
        """
        topLevel = False
        if getattr(result, '_testRunEntered', False) is False:
            result._testRunEntered = topLevel = True
        asyncMethod = []
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for index, test in enumerate(self):
            asyncMethod.append(self.startRunCase(index, test, result))
        if asyncMethod:
            loop.run_until_complete(asyncio.wait(asyncMethod))
        loop.close()
        if topLevel:
            self._tearDownPreviousClass(None, result)
            self._handleModuleTearDown(result)
            result._testRunEntered = False
        return result

    async def startRunCase(self, index, test, result):

        def _isnotsuite(test):
            "A crude way to tell apart testcases and suites with duck-typing"
            try:
                iter(test)
            except TypeError:
                return True
            return False

        loop = asyncio.get_event_loop()
        if result.shouldStop:
            return False

        if _isnotsuite(test):
            self._tearDownPreviousClass(test, result)
            self._handleModuleFixture(test, result)
            self._handleClassSetUp(test, result)
            result._previousTestClass = test.__class__

            if (getattr(test.__class__, '_classSetupFailed', False)
                    or getattr(result, '_moduleSetUpFailed', False)):
                return True

        await loop.run_in_executor(None, test, result)

        if self._cleanup:
            self._removeTestAtIndex(index)


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

    if 'launch' in commands:
        commands.remove('launch')
    if 'jenkins' in commands:
        commands.remove('jenkins')

    upstream = 'OFF'
    if '--upstream' in commands:
        upstream = 'ON'
        commands.remove('--upstream')

    exclusive = False
    if '--exclusive' in commands:
        exclusive = True
        commands.remove('--exclusive')

    machine_count = 0
    if '--daint' in commands:
        machine = 'daint'
        spack_machine = machine
        commands = [x for x in commands if x != '--daint']
        machine_count += 1
    if '--dom' in commands:
        machine = 'daint'
        spack_machine = 'dom'
        commands = [x for x in commands if x != '--dom']
        machine_count += 1
    if '--tsa' in commands:
        machine = 'tsa'
        spack_machine = machine
        commands = [x for x in commands if x != '--tsa']
        machine_count += 1

    if machine_count != 1:
        sys.exit()

    known_commands = dependencies.keys() | expansions.keys()

    # handles backward compatibility to run an arbitrary command
    is_arbitrary_command = any(c not in known_commands for c in commands)

    print('Test plan:', flush=True)
    print('====================================', flush=True)
    print(
        f'Configuring spack with upstream {upstream} on machine {spack_machine}.',
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
        f'python ./config.py -m {spack_machine} -i . -r ./spack/etc/spack -p ./spack -s ./spack -u {upstream} -c ./spack-cache',
        check=True,
        shell=True)

    if is_arbitrary_command:
        setup = ''
        if joined_command.startswith('spack'):
            setup = f'source spack/share/spack/setup-env.sh &&'
        subprocess.run(f'{setup} {joined_command} >> {machine}.log',
                       check=True,
                       shell=True)
        sys.exit()
    else:
        # collect and run tests from all packages selected
        suite = CustomTestSuite([
            test_loader.loadTestsFromTestCase(case) for case in all_test_cases
            if case.package_name in packages_to_test
            and machine in case.machines
        ])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit(not result.wasSuccessful())
