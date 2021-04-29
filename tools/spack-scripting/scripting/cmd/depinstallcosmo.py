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
    arguments.add_common_arguments(subparser, ["spec"])


def custom_devbuild(spec, jobs):
    package = spack.repo.get(spec)

    if package.installed:
        package.do_uninstall(force=True)

    package.do_install(verbose=True, make_jobs=jobs)


def depinstallcosmo(self, args):
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
    with open(package.stage.source_path + "/cosmo/ACC/spack/spec.yaml", "r") as f:
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

    # re-concretize
    cosmo_spec = spack.cmd.parse_specs(cosmo_spec.__str__())[0]
    cosmo_spec.concretize()

    print("[DEBUG] Full spec: ", cosmo_spec)  # TODO: debug, remove

    # Dev-build cosmo
    custom_devbuild(cosmo_spec, args.jobs)
