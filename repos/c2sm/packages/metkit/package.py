from spack.package import *

from spack.pkg.builtin.metkit import Metkit as SpackMetkit


class Metkit(SpackMetkit):

    # This file can be removed when this PR https://github.com/spack/spack/pull/42871
    # is included in a release on spack and this is used by spack-c2sm.
    depends_on("eckit@:1.21", when="@:1.10")
