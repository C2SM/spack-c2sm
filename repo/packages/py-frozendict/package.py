# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.py_frozendict import PyFrozendict as SpackPyFrozendict


class PyFrozendict(SpackPyFrozendict):

    version('2.4.0',
            sha256=
            'c26758198e403337933a92b01f417a8240c954f553e1d4b5e0f8e39d9c8e3f0a')

    # TODO: remove this extension once we have a more recent
    # version than v0.21.1
    def setup_build_environment(self, env):
        # C extension is not supported for 3.11+. See also
        # https://github.com/Marco-Sulla/python-frozendict/issues/68
        if self.spec.satisfies("^python@3.11:"):
            env.set("FROZENDICT_PURE_PY", "1")
