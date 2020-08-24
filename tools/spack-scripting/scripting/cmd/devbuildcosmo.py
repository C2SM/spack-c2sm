# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os
import subprocess
import shutil

import llnl.util.tty as tty

import spack.config
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
from spack.stage import DIYStage
from spack.spec import Spec
from spack.cmd.dev_build import dev_build
from spack.main import SpackCommand

description = "Dev-build cosmo and dycore with or without testing."
section = "scripting"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['jobs'])
    subparser.add_argument(
        '-d', '--source-path', dest='source_path', default=None,
        help="path to source directory. defaults to the current directory")
    subparser.add_argument(
        '-i', '--ignore-dependencies', action='store_true', dest='ignore_deps',
        help="don't try to install dependencies of requested packages")
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '--keep-prefix', action='store_true',
        help="do not remove the install prefix if installation fails")
    subparser.add_argument(
        '--skip-patch', action='store_true',
        help="skip patching for the developer build")
    subparser.add_argument(
        '-q', '--quiet', action='store_true', dest='quiet',
        help="do not display verbose build output while installing")
    subparser.add_argument(
        '--drop-in', type=str, dest='shell', default=None,
        help="drop into a build environment in a new shell, e.g. bash, zsh")

    subparser.add_argument(
        '-t', '--test', action='store_true', help="Dev-build with testing")
    subparser.add_argument(
        '-c', '--clean_build', action='store_true', help="Clean dev-build")
    subparser.add_argument(
        '-w', '--without_dycore', action='store_true', help="Dev-build cosmo but not dycore")

    arguments.add_common_arguments(subparser, ['spec'])

    stop_group = subparser.add_mutually_exclusive_group()
    stop_group.add_argument(
        '-b', '--before', type=str, dest='before', default=None,
        help="phase to stop before when installing (default None)")
    stop_group.add_argument(
        '-u', '--until', type=str, dest='until', default=None,
        help="phase to stop after when installing (default None)")

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ['clean', 'dirty'])


def devbuildcosmo(self, args):
    # Extract and concretize cosmo_spec
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = specs[0]
    temp_cosmo_spec = str(cosmo_spec)
    cosmo_spec.concretize()

    # Set dycore_spec
    if not args.without_dycore:
        dycore_spec = 'cosmo-dycore@dev-build '
    else:
        dycore_spec = 'cosmo-dycore@master '

    # extracting dycore variants
    dycore_spec += cosmo_spec.format('{^cosmo-dycore.variants}')

    # extracting correct mpi variant
    dycore_spec += ' ^' + cosmo_spec.format('{^mpi.name}') + '%' + cosmo_spec.compiler.name

    # remove the slurm_args variant causing troubles to the concretizer
    dycore_spec = dycore_spec.replace(cosmo_spec.format('{^cosmo-dycore.variants.slurm_args}'), ' ')

    base_directory = os.getcwd()

    # Clean if needed
    if args.clean_build:
        print('\033[92m' + '==> ' + '\033[0m' + 'cosmo: Cleaning build directory')
        subprocess.run(["make", "clean"], cwd = base_directory + '/cosmo/ACC')

        if not args.without_dycore:
          print('\033[92m' + '==> ' + '\033[0m' + 'dycore: Cleaning build directory')
          if os.path.exists(base_directory + '/spack-build'):
              shutil.rmtree(base_directory + '/spack-build')

    if cosmo_spec.satisfies('+cppdycore') and not args.without_dycore:
        # Concretize dycore spec and cosmo_serialize spec
        dycore_spec = Spec(dycore_spec)
        dycore_spec.concretize()

        args.spec = str(dycore_spec)

        if args.until == 'build':
            shutil.rmtree(dycore_spec.prefix)
            args.until = None

        # Dev-build dycore
        dev_build(self, args)
        # Launch dycore tests
        if args.test:
            print('\033[92m' + '==> ' + '\033[0m' + 'cosmo-dycore: Launching dycore tests')
            subprocess.run(['./dycore/test/tools/test_dycore.py', str(dycore_spec), base_directory + '/spack-build'])

        find_cmd = SpackCommand('find')
        dycore_hash = find_cmd('--format', '{hash}', 'cosmo-dycore@dev-build', 'real_type=' + cosmo_spec.variants['real_type'].value, ' ^' + cosmo_spec.format('{^mpi.name}') + '%' + cosmo_spec.compiler.name)

        temp_cosmo_spec = temp_cosmo_spec + ' ^/' + dycore_hash
        args.spec = temp_cosmo_spec
        args.ignore_deps = True

    # Dev-build cosmo
    dev_build(self, args)

    # Launch cosmo tests
    if args.test and '~serialize' in cosmo_spec:
        print('\033[92m' + '==> ' + '\033[0m' + 'cosmo: Launching cosmo tests')
        subprocess.run(["./cosmo/ACC/test/tools/test_cosmo.py", str(cosmo_spec), base_directory])

    # Serialize data
    if '+serialize' in cosmo_spec:
        print('\033[92m' + '==> ' + '\033[0m' + 'cosmo: Serializing data')
        subprocess.run(["./cosmo/ACC/test/tools/serialize_cosmo.py", str(cosmo_spec), base_directory])
