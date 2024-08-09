from spack.package import *

from spack.pkg.builtin.fdb import Fdb as SpackFdb


class Fdb(SpackFdb):

    # This section can be removed when the following commit
    # https://github.com/spack/spack/commit/8871bd5ba5c58562b8c20baa00f125aeccba586f
    # is included in a release on spack and this is used by spack-c2sm.
    depends_on("eckit@1.24.4:", when="@5.11.22:")

    # This section can be removed when the following PR
    # https://github.com/spack/spack/pull/42874
    # is included in a release on spack and this is used by spack-c2sm.
    @property
    def libs(self):
        return find_libraries("libfdb5",
                              root=self.prefix,
                              shared=True,
                              recursive=True)
