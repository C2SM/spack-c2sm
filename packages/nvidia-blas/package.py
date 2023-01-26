# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class NvidiaBlas(Package):
    """The Cray Scientific Libraries package, LibSci, is a collection of
    numerical routines optimized for best performance on Cray systems."""

    has_code = False    # Skip attempts to fetch source that is not available

    version("21.3")

    provides("blas")

    @property
    def libs(self):

        lib = ["libblas"]

        return find_libraries(
            lib,
            root='/opt/nvidia/hpc_sdk/Linux_x86_64/21.3/compilers/lib',
            shared=True,
            recursive=True)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format('{name} is not installable, you need to specify '
                             'it as an external package in packages.yaml'))

