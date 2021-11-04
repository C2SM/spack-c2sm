#!/usr/bin/python

import unittest
import sys
import subprocess

# Maps packages to Set[use cases].
# The comment after each use case states why this use case exists or where it appears.
use_cases = {
    'atlas' : {},
    'atlas_utilities' : {},
    'claw' : {},
    'cosmo' : {
        'spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        'spack installcosmo cosmo@master%pgi cosmo_target=cpu ~cppdycore', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        'git clone git@github.com:MeteoSwiss-APN/cosmo.git \
            && cd cosmo \
            && spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=gpu +cppdycore \
            && cd .. && rm -rf cosmo', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html 
        'git clone git@github.com:MeteoSwiss-APN/cosmo.git \
            && cd cosmo \
            && spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=cpu ~cppdycore \
            && cd .. && rm -rf cosmo', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        # 'spack installcosmo cosmo@master%pgi cosmo_target=gpu +cppdycore ^eccodes +aec +build_shared_libs',
    },
    'cosmo-dycore' : {},
    'cosmo-eccodes-definitions' : {},
    'cosmo-grib-api' : {},
    'cosmo-grib-api-definitions' : {},
    'cuda' : {},
    'dawn' : {},
    'dawn4py' : {},
    'dusk' : {},
    'dyicon_benchmarks' : {},
    'ecbuild' : {},
    'eccodes' : {},
    'eckit' : {},
    'gridtools' : {},
    'icon' : {
        'git clone --recursive git@gitlab.dkrz.de:icon/icon-cscs.git \
            && cd icon-cscs \
            && mkdir pgi_cpu \
            && cd pgi_cpu \
            && touch a_fake_file.f90 \
            && spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=cpu \
            && cd ../.. && rm -rf icon-cscs', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        'git clone --recursive git@gitlab.dkrz.de:icon/icon-cscs.git \
            && cd icon-cscs \
            && mkdir pgi_gpu \
            && cd pgi_gpu \
            && touch a_fake_file.f90 \
            && spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=gpu \
            && cd ../.. && rm -rf icon-cscs', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
    },
    'icondusk-e2e' : {},
    'icontools' : {},
    'int2lm' : {
        'spack install int2lm@c2sm_master%pgi', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        'spack install int2lm@org_master%pgi pollen=False', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
    },
    'libgrib1' : {},
    'mpich' : {},
    'oasis' : {},
    'omnicompiler' : {},
    'omni-xmod-pool' : {},
    'openmpi' : {},
    'serialbox' : {},
    'xcodeml-tools' : {},
    'zlib_ng' : {},
}

def UseCases(packages : set):
    return {case for p in packages for case in use_cases[p]}

# Maps packages to Set[packages it depends on].
dependencies = {
    'atlas' : {'ecbuild', 'eckit'},
    'atlas_utilities' : {'atlas', 'eckit'},
    'claw' : {},
    'cosmo' : {'cuda', 'serialbox', 'libgrib1', 'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'omni-xmod-pool', 'claw', 'zlib_ng', 'cosmo-dycore'},
    'cosmo-dycore' : {'gridtools', 'serialbox', 'cuda'},
    'cosmo-eccodes-definitions' : {'eccodes'},
    'cosmo-grib-api' : {},
    'cosmo-grib-api-definitions' : {'cosmo-grib-api'},
    'cuda' : {},
    'dawn' : {},
    'dawn4py' : {},
    'dusk' : {'dawn4py'},
    'dyicon_benchmarks' : {'atlas_utilities', 'atlas', 'cuda'},
    'ecbuild' : {},
    'eccodes' : {},
    'eckit' : {'ecbuild'},
    'gridtools' : {'cuda'},
    'icon' : {'serialbox', 'eccodes', 'claw'},
    'icondusk-e2e' : {'atlas_utilities', 'dawn4py', 'dusk', 'atlas', 'cuda'},
    'icontools' : {'eccodes', 'cosmo-grib-api'},
    'int2lm' : {'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'libgrib1'},
    'libgrib1' : {},
    'log' : {},
    'mpich' : {},
    'oasis' : {},
    'omnicompiler' : {},
    'omni-xmod-pool' : {},
    'openmpi' : {},
    'serialbox' : {},
    'xcodeml-tools' : {},
    'zlib_ng' : {},
}

def Dependents(packages : set):
    return {parent for parent, children in dependencies.items() if not packages.isdisjoint(children)}

# All packages that are configured by this repo
packages = {
    'atlas', 'atlas_utilities', 'claw', 'cosmo', 'cosmo-dycore', 'cosmo-eccodes-definitions',
    'cosmo-grib-api', 'cosmo-grib-api-definitions', 'cuda', 'dawn', 'dawn4py', 'dusk',
    'dyicon_benchmarks', 'ecbuild', 'eccodes', 'eckit', 'gridtools', 'icon', 'icondusk-e2e',
    'icontools', 'int2lm', 'libgrib1', 'mpich', 'oasis', 'omnicompiler', 'omni-xmod-pool',
    'openmpi', 'serialbox', 'xcodeml-tools', 'zlib_ng'
}

# Maps commands to Set[packages]
commands_to_packages = {p:{p} for p in packages}
commands_to_packages.update({'all': packages})

def Packages(commands : set):
    return {package for c in commands for package in commands_to_packages[c]}

def CommandsToUseCases(commands : set):
    p = Packages(commands)
    return UseCases(p | Dependents(p))


class SelfTest(unittest.TestCase):

    def test_empty_command(self):
        no_commands = set()
        cases = CommandsToUseCases(no_commands)
        self.assertFalse(cases)

    def test_command_all(self):
        cases = CommandsToUseCases({'all'})
        self.assertTrue(cases)

    def test_data_integrity(self):
        every_command = commands_to_packages.keys()
        every_case = {c for cases in use_cases.values() for c in cases}

        cases = CommandsToUseCases(every_command)

        self.assertEqual(cases, every_case)


class SpackTest(unittest.TestCase):
    commands = ''

    def test_spack(self):
        upstream = 'OFF'
        if '--upstream' in self.commands:
            upstream = 'ON'
            self.commands.remove('--upstream')

        if '--daint' in self.commands:
            machine = 'daint'
            self.commands.remove('--daint')
        if '--tsa' in self.commands:
            machine = 'tsa'
            self.commands.remove('--tsa')

        # config spack
        subprocess.run(f'python ./config.py -m {machine} -i . -r ./spack/etc/spack -p ./spack -s ./spack -u {upstream} -c ./spack-cache', check=True, shell=True)

        setup = 'source spack/share/spack/setup-env.sh && '
        if all(c in commands_to_packages for c in self.commands): # if commands are all in list of known commands
            for case in CommandsToUseCases(self.commands):
                with self.subTest(case=case):
                    subprocess.run(setup + case, check=True, shell=True)
        else: # if arbitrary commands
            subprocess.run(setup + ' '.join(self.commands), check=True, shell=True)


if __name__ == '__main__':
    SpackTest.commands = sys.argv[1:]
    SpackTest.commands.remove('launch')
    SpackTest.commands.remove('jenkins')
    sys.argv = [sys.argv[0]] # unittest needs this

    suite1 = unittest.TestLoader().loadTestsFromTestCase(SelfTest)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(SpackTest)
    suite = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner(verbosity=2).run(suite)
