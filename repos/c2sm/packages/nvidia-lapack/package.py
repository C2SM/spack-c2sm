# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class NvidiaLapack(Package):
    """
    There is no module 'cray-libsci' available for Nvidia on Daint to
    provide blas/lapack. Instead Nvidia comes with its own implementation.
    This package helps Spack to detect the libraries and prevents it
    from building blas/lapack from i.e. netlib-lapack instead
    """

    homepage = ""
    maintainers = ['juckerj']

    has_code = False  # Skip attempts to fetch source that is not available

    version("dummy-version")

    provides("lapack")

    @property
    def libs(self):

        lib = ["liblapack"]

        return find_libraries(lib,
                              root=self.prefix,
                              shared=True,
                              recursive=True)

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format('{name} is not installable, you need to specify '
                             'it as an external package in packages.yaml'))
