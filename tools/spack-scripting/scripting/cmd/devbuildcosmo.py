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

description = "Dev-build cosmo and dycore with or without testing."
section = "scripting"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["jobs", "spec"])

    subparser.add_argument("--no_specyaml",
                           action="store_true",
                           help="Ignore spec.yaml")
    subparser.add_argument(
        "--test",
        choices=['root', 'dycore', 'all'],
        dest="things_to_test",
        help="""If root is chosen, run COSMO testsuite before installation 
        (but skip tests for dependencies). If dycore is chosen, 
        run test for Dycore and COSMO testsuite.
        If all is chosen, 
        run package tests during installation for all packages.""")
    subparser.add_argument("-c",
                           "--clean_build",
                           action="store_true",
                           help="Clean dev-build")

    subparser.add_argument(
        '--dont-restage',
        action='store_false',
        dest="restage",
        help="if a partial install is detected, don’t delete prior state")

    subparser.add_argument(
        '-u',
        '--until',
        dest='until',
        default=None,
        help="phase to stop after when installing (only applies to COSMO)")


def custom_devbuild(source_path, spec, args):
    package = spack.repo.get(spec)
    package.stage = DIYStage(source_path)

    if package.installed:
        package.do_uninstall(force=True)

    if args.things_to_test == 'root':
        args.things_to_test = ['cosmo']

    elif args.things_to_test == 'dycore':
        args.things_to_test = ['cosmo', 'cosmo-dycore']

    elif args.things_to_test == 'all':
        args.things_to_test = True

    # Bugfix: somehow args are changed outside of function when changed inside here
    # Therefore, at second call of this function things_to_test is a list
    elif isinstance(args.things_to_test, list):
        if args.things_to_test[0] != 'cosmo':
            tty.die("unknown entry in devbuildcosmo for argument '--test' ")

    else:
        args.things_to_test = False

    kwargs = {
        'make_jobs': args.jobs,
        'restage': args.restage,
        'tests': args.things_to_test
    }

    # for testing purposes we want to split build and install phase for COSMO
    if package.name == 'cosmo':
        kwargs['stop_at'] = args.until

    package.do_install(verbose=True, **kwargs)


def devbuildcosmo(self, args):
    # Extract and concretize cosmo_spec
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    # validate specs
    specs = spack.cmd.parse_specs(args.spec)

    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = spack.cmd.parse_specs(args.spec)[0]

    # Collect user-specified versions of dependencies before first concretization
    user_versioned_deps = set()
    for dep in cosmo_spec.traverse():
        if dep.name != "cosmo" and dep.versions and len(dep.versions) != 0:
            user_versioned_deps.add(dep.name)

    cosmo_spec.concretize()

    # Setting source_path to current working directory
    source_path = os.getcwd()
    source_path = os.path.abspath(source_path)

    if not args.no_specyaml:
        # Load serialized yaml from inside cloned repo
        with open(source_path + "/cosmo/ACC/spack/spec.yaml", "r") as f:
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
        # 1. the one specified in spec.yaml,
        # 2. the one provided by the user in the command,
        # 3. the default prescribed by the spack package.
        for dep in cosmo_spec.traverse():
            if dep.name in deps_serialized_dict and not dep.name in user_versioned_deps:
                dep.versions = deps_serialized_dict[dep.name].versions.copy()
            if dep.name == "cosmo-dycore":
                dep.versions = cosmo_spec.versions.copy()

        # Re-concretize Spec: to enforce checking of constraints after update of versions.
        # Note: unfortunately there is no better way to re-concretize a Spec (e.g. via API).
        #       The only solution seems to be going via string representation and then back
        #       into a Spec object. It's not elegant but it seems to work very well.
        cosmo_spec = spack.cmd.parse_specs(str(cosmo_spec))[0]
        cosmo_spec.concretize()

    # Clean if needed
    if args.clean_build:
        print("\033[92m" + "==> " + "\033[0m" +
              "cosmo: Cleaning build directory")

        # set F90 to prevent abort defined in Makefile
        os.environ["F90"] = "NOTSET"
        subprocess.run(["make", "clean"], cwd=source_path + "/cosmo/ACC")
        os.environ.pop("F90")

        if os.path.exists(source_path + "/spack-build"):
            print("\033[92m" + "==> " + "\033[0m" +
                  "dycore: Cleaning build directory")
            shutil.rmtree(source_path + "/spack-build")

    if cosmo_spec.satisfies("+cppdycore"):

        dycore_spec = cosmo_spec.get_dependency("cosmo-dycore").spec

        custom_devbuild(source_path, dycore_spec, args)

    # Dev-build cosmo
    custom_devbuild(source_path, cosmo_spec, args)
