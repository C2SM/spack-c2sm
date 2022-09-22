# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os
import subprocess
import shutil

import llnl.util.tty as tty
import re

# same used by spack, comes with it
import ruamel.yaml as yaml

import spack.config
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
from spack.stage import DIYStage
from spack.spec import Spec
from spack.cmd.dev_build import dev_build
from spack.main import SpackCommand

description = "Install cosmo and dycore with or without testing using spec.yaml for key dependencies"
section = "scripting"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["jobs", "spec"])

    subparser.add_argument('--only',
                           default='package,dependencies',
                           dest='things_to_install',
                           choices=['package', 'dependencies'],
                           help="""select the mode of installation.
the default is to install the package along with all its dependencies.
alternatively one can decide to install only the package or only
the dependencies""")

    subparser.add_argument(
        '--keep-stage',
        action='store_true',
        help="don't remove the build stage if installation succeeds")

    subparser.add_argument(
        "--test",
        choices=['root', 'all'],
        dest="things_to_test",
        help="""If root is chosen, run COSMO testsuite before installation 
        (but skip tests for dependencies). If all is chosen, 
        run package tests during installation for all packages.""")

    subparser.add_argument("-v",
                           "--verbose",
                           dest="lverbose",
                           action="store_true",
                           help="""Verbose installation""")

    subparser.add_argument('--force_uninstall',
                           action='store_true',
                           help="force uninstall if package already installed")

    subparser.add_argument(
        '--dont-restage',
        action='store_false',
        dest="restage",
        help="if a partial install is detected, don’t delete prior state")

    subparser.add_argument('-u',
                           '--until',
                           dest='until',
                           default=None,
                           help="phase to stop after when installing")


def custom_install(spec, args):
    package = spack.repo.get(spec)

    if args.things_to_test == 'root':
        args.things_to_test = ['cosmo']
    elif args.things_to_test == 'all':
        args.things_to_test = True
    else:
        args.things_to_test = False

    kwargs = {
        'make_jobs': args.jobs,
        'install_deps': ('dependencies' in args.things_to_install),
        'install_package': ('package' in args.things_to_install),
        'keep_stage': args.keep_stage,
        'tests': args.things_to_test,
        'verbose': args.lverbose,
        'stop_at': args.until,
        'restage': args.restage
    }

    if args.things_to_install == 'dependencies':
        # If we want to only install dependencies and one of them fails,
        # spack doesn't return a failure exit code.
        # This fixes this issue:
        kwargs['fail_fast'] = True

    if args.force_uninstall:
        if package.installed:
            package.do_uninstall(force=True)
    package.do_install(**kwargs)


def installcosmo(self, args):
    # Extract and concretize cosmo_spec
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = specs[0]

    # Collect user-specified versions of dependencies before first concretization
    user_versioned_deps = set()
    for dep in cosmo_spec.traverse():
        if dep.name != "cosmo" and dep.versions and len(dep.versions) != 0:
            user_versioned_deps.add(dep.name)

    cosmo_spec.concretize()

    package = spack.repo.get(cosmo_spec)
    package.do_fetch()
    package.do_stage()

    # Load serialized yaml from inside cloned repo
    with open(package.stage.source_path + "/cosmo/ACC/spack/spec.yaml",
              "r") as f:
        try:
            data = yaml.load(f)
        except yaml.error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))

    # Read nodes out of list.  Root spec (cosmo) is the first element;
    # dependencies are the following elements.
    spec_list = [Spec.from_node_dict(node) for node in data["spec"]]
    if not spec_list:
        raise spack.error.SpecError("YAML spec contains no nodes.")

    # Take only the dependencies
    deps_serialized_dict = dict((spec.name, spec) for spec in spec_list)

    # Selectively substitute the dependencies' versions with those found in the deserialized list of specs
    # The order of precedence in the choice of a dependency's version becomes:
    # 1. the one provided by the user in the command,
    # 2. the one specified in spec.yaml,
    # 3. the default prescribed by the spack package.
    for dep in cosmo_spec.traverse():
        if dep.name in deps_serialized_dict and not dep.name in user_versioned_deps:
            dep.versions = deps_serialized_dict[dep.name].versions.copy()
        if dep.name == "cosmo-dycore":
            dep.versions = cosmo_spec.versions.copy()

    # re-concretize
    cosmo_spec = spack.cmd.parse_specs(str(cosmo_spec))[0]
    cosmo_spec.concretize()

    # Dev-build cosmo
    custom_install(cosmo_spec, args)
