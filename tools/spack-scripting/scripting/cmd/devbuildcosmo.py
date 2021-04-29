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
    arguments.add_common_arguments(subparser, ["jobs"])

    subparser.add_argument(
        "-t", "--test", action="store_true", help="Dev-build with testing"
    )
    subparser.add_argument(
        "-c", "--clean_build", action="store_true", help="Clean dev-build"
    )
    arguments.add_common_arguments(subparser, ["spec"])


def custom_devbuild(source_path, spec, jobs):
    package = spack.repo.get(spec)
    package.stage = DIYStage(source_path)

    if package.installed:
        package.do_uninstall(force=True)

    package.do_install(verbose=True, make_jobs=jobs)


def devbuildcosmo(self, args):
    # Extract and concretize cosmo_spec
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    # validate specs
    specs = spack.cmd.parse_specs(args.spec)

    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = spack.cmd.parse_specs(args.spec)[0]
    cosmo_spec.concretize()

    # Setting source_path to current working directory
    source_path = os.getcwd()
    source_path = os.path.abspath(source_path)

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
        if dep.name in deps_serialized_dict:
            dep.versions = deps_serialized_dict[dep.name].versions.copy()
        if dep.name == "cosmo-dycore":
            dep.versions = cosmo_spec.versions.copy()

    # re-concretize
    cosmo_spec = spack.cmd.parse_specs(cosmo_spec.__str__())[0]
    cosmo_spec.concretize()

    print("[DEBUG] Cosmo full spec", cosmo_spec)  # TODO: debug, remove

    # Clean if needed
    if args.clean_build:
        print("\033[92m" + "==> " + "\033[0m" + "cosmo: Cleaning build directory")
        subprocess.run(["make", "clean"], cwd=source_path + "/cosmo/ACC")

        if os.path.exists(base_directory + "/spack-build"):
            print("\033[92m" + "==> " + "\033[0m" + "dycore: Cleaning build directory")
            shutil.rmtree(source_path + "/spack-build")

    if cosmo_spec.satisfies("+cppdycore"):
        # Extracting dycore variants
        dycore_spec = (
            cosmo_spec.format("{^cosmo-dycore.name}")
            + cosmo_spec.format("{^cosmo-dycore.@version}")
            + cosmo_spec.format("{^cosmo-dycore.%compiler}")
            + cosmo_spec.format("{^cosmo-dycore.variants}")
        )

        # Extracting correct mpi variant
        dycore_spec += (
            " ^"
            + cosmo_spec.format("{^mpi.name}")
            + cosmo_spec.format("{^mpi.@version}")
            + cosmo_spec.format("{^mpi.%compiler}")
            + cosmo_spec.format("{^mpi.variants}")
        )

        # Remove the slurm_args variant causing troubles to the concretizer
        dycore_spec = dycore_spec.replace(
            cosmo_spec.format("{^cosmo-dycore.variants.slurm_args}"), " "
        )

        dycore_spec = Spec(dycore_spec).concretized()

        print("[DEBUG] Dycore full spec", dycore_spec)  # TODO: debug, remove
        custom_devbuild(source_path, dycore_spec, args.jobs)

        # Launch dycore tests
        if args.test:
            print(
                "\033[92m" + "==> " + "\033[0m" + "cosmo-dycore: Launching dycore tests"
            )
            subprocess.run(
                [
                    "./dycore/test/tools/test_dycore.py",
                    str(dycore_spec),
                    source_path + "/spack-build",
                ]
            )

    # Dev-build cosmo
    custom_devbuild(source_path, cosmo_spec, args.jobs)

    # Launch cosmo tests
    if args.test:
        print("\033[92m" + "==> " + "\033[0m" + "cosmo: Launching cosmo tests")
        subprocess.run(
            ["./cosmo/ACC/test/tools/test_cosmo.py", str(cosmo_spec), source_path]
        )

    # Serialize data
    if "+serialize" in cosmo_spec:
        print("\033[92m" + "==> " + "\033[0m" + "cosmo: Serializing data")
        subprocess.run(
            ["./cosmo/ACC/test/tools/serialize_cosmo.py", str(cosmo_spec), source_path]
        )
