# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install omnicompiler
#
# You can edit this file again by typing:
#
#     spack edit omnicompiler
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Omnicompiler(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://omni-compiler.org/download/stable/omnicompiler-1.3.2.tar.bz2"

    maintainers = ['elsagermann']

    version('1.3.2',
            sha256=
            '62e965edaf0217aeaf471664cb7af7ecbdd84239b98f962a6ce6a4d77668247d')
    version('1.3.1',
            sha256=
            '9fee60855a2c25a63168923be468fc9598e200897dfffec61494de6d38f001bd')
    version('1.3.0',
            sha256=
            'bbea9eb10277d4658edd4ea80ad727a299e9117bb470c7e637b36627a24b742d')
    version('1.2.3',
            sha256=
            'c211c9919579c6c0d7b13f22d3d46fa638c6158c06bee67880a34868f4dc3b95')

    variant('mod2xmod',
            default=False,
            description=
            "Build T_Module which can transform .mod files to .xmod files.")
    # FIXME: Add dependencies if required.
    depends_on('libxml2')
    depends_on('m4')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')
    depends_on('mpfr', when='+mod2xmod')
    depends_on('mpi')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('YACC', 'bison -y')

    def configure_args(self):
        args = []
        if '+mod2xmod' in self.spec:
            args = [
                '--enable-mod2xmod',
                '--with-gmp=/usr/..',
                '--with-mpfr-include={0}'.format(self.spec['mpfr'].prefix +
                                                 '/include'),
                '--with-mpfr-lib={0}'.format(self.spec['mpfr'].prefix +
                                             '/lib'),
                '--with-libxml2={0}'.format(spec['libxml2'].prefix),
            ]

        return args
