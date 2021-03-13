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

import spack.config
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo
from spack.stage import DIYStage
from spack.spec import Spec
from spack.cmd.dev_build import dev_build
from spack.main import SpackCommand

from buildyamlconf import DepsYamlConf

description = "Dev-build cosmo and dycore with or without testing."
section = "scripting"
level = "long"

def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['jobs'])

    subparser.add_argument(
        '-t', '--test', action='store_true', help="Dev-build with testing")
    arguments.add_common_arguments(subparser, ['spec'])

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
    cosmo_spec.concretize()

    package = spack.repo.get(cosmo_spec)
    package.do_fetch()
    package.do_stage() 

    depsconf = DepsYamlConf(package.stage.source_path)

    for aspec in depsconf.dependency_spec.split():
        args.spec.append(aspec)

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    cosmo_spec = specs[0]

    print("Full spec: ",cosmo_spec)
    cosmo_spec.concretize()


     # Dev-build cosmo
    custom_devbuild(cosmo_spec, args.jobs)

