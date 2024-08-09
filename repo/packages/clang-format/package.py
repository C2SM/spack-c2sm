# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ClangFormat(Package):
    """Clang-Format is a widely-used C++ code formatter."""

    homepage = "https://llvm.org/"
    url = "https://github.com/llvm/llvm-project/releases/download/llvmorg-15.0.6/clang+llvm-15.0.6-x86_64-linux-gnu-ubuntu-18.04.tar.xz"

    maintainers = ['juckerj']

    version('15.0.6',
            sha256=
            '38bc7f5563642e73e69ac5626724e206d6d539fbef653541b34cae0ba9c3f036')

    phases = ['install']

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('bin/clang-format', f'{prefix.bin}/clang-format')
