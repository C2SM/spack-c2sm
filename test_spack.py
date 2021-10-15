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
        'spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=gpu +cppdycore', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        'spack installcosmo cosmo@master%pgi cosmo_target=cpu ~cppdycore', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
        'spack devbuildcosmo cosmo@dev-build%pgi cosmo_target=cpu ~cppdycore', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
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
        'spack dev-build -u build icon@dev-build%pgi config_dir=./.. icon_target=cpu', # Listed in https://c2sm.github.io/spack-c2sm/QuickStart.html
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
    'cosmo' : {'cuda', 'serialbox', 'libgrib1', 'cosmo-grib-api-definitions', 'cosmo-eccodes-definitions', 'omni-xmod-pool', 'claw', 'zlib_ng'},
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

# Maps commands to Set[packages]
commands_to_packages = {
    'all' : {
        'atlas', 'atlas_utilities', 'claw', 'cosmo', 'cosmo-dycore', 'cosmo-eccodes-definitions',
        'cosmo-grib-api', 'cosmo-grib-api-definitions', 'cuda', 'dawn', 'dawn4py', 'dusk',
        'dyicon_benchmarks', 'ecbuild', 'eccodes', 'eckit', 'gridtools', 'icon', 'icondusk-e2e',
        'icontools', 'int2lm', 'libgrib1', 'mpich', 'oasis', 'omnicompiler', 'omni-xmod-pool',
        'openmpi', 'serialbox', 'xcodeml-tools', 'zlib_ng'
    },
    'atlas' : {'atlas'},
    'atlas_utilities' : {'atlas_utilities'},
    'claw' : {'claw'},
    'cosmo' : {'cosmo'},
    'cosmo-dycore' : {'cosmo-dycore'},
    'cosmo-eccodes-definitions' : {'cosmo-eccodes-definitions'},
    'cosmo-grib-api' : {'cosmo-grib-api'},
    'cosmo-grib-api-definitions' : {'cosmo-grib-api-definitions'},
    'cuda' : {'cuda'},
    'dawn' : {'dawn'},
    'dawn4py' : {'dawn4py'},
    'dusk' : {'dusk'},
    'dyicon_benchmarks' : {'dyicon_benchmarks'},
    'ecbuild' : {'ecbuild'},
    'eccodes' : {'eccodes'},
    'eckit' : {'eckit'},
    'gridtools' : {'gridtools'},
    'icon' : {'icon'},
    'icondusk-e2e' : {'icondusk-e2e'},
    'icontools' : {'icontools'},
    'int2lm' : {'int2lm'},
    'libgrib1' : {'libgrib1'},
    'mpich' : {'mpich'},
    'oasis' : {'oasis'},
    'omnicompiler' : {'omnicompiler'},
    'omni-xmod-pool' : {'omni-xmod-pool'},
    'openmpi' : {'openmpi'},
    'serialbox' : {'serialbox'},
    'xcodeml-tools' : {'xcodeml-tools'},
    'zlib_ng' : {'zlib_ng'},
}

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


class Spack(unittest.TestCase):
    commands = ''

    def test_spack(self):        
        ntasks = 16

        upstream = 'ON'
        if '--no_upstream' in self.commands:
            upstream = 'OFF'
            self.commands.remove('--no_upstream')

        # with open('test_job', 'w') as f:
        #     f.writelines('#!/bin/sh')
        #     f.writelines('#SBATCH --time=02:00:00')

        #     f.writelines(f'module load python/3.7.4')
        #     f.writelines(f'python3 ./config.py -m {machine} -i . -r ./spack/etc/spack -p $PWD/spack -s $PWD/spack -u {upstream} -c ./spack-cache')
        #     f.writelines(f'. spack/share/spack/setup-env.sh')

        #     for case in CommandsToUseCases(commands):
        #         f.writelines(f'srun {case}')

        # input sanity check
        for c in self.commands:
            with self.subTest():
                self.assertTrue(c in commands_to_packages)

        for case in CommandsToUseCases(self.commands):
            with self.subTest():
                subprocess.run(case, check=True)


if __name__ == '__main__':
    Spack.commands = sys.argv[1:]
    Spack.commands.remove('launch')
    Spack.commands.remove('jenkins')
    sys.argv = [sys.argv[0]]
    
    unittest.main()