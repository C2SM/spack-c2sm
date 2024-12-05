from spack.pkg.c2sm.icon import Icon as IconC2sm

import os
import re
from collections import defaultdict
import spack.error as error


def validate_variant_dsl(pkg, name, value):
    set_mutual_excl = set(['substitute', 'verify', 'serialize'])
    set_input_var = set(value)
    if len(set_mutual_excl.intersection(set_input_var)) > 1:
        raise error.SpecError(
            'Cannot have more than one of (substitute, verify, serialize) in the same build'
        )


class IconExclaim(IconC2sm):
    git = 'git@gitlab.dkrz.de:icon/icon.git'

    maintainers('jonasjucker', 'huppd')

    version('exclaim-master',
            branch='master',
            git='git@github.com:C2SM/icon-exclaim.git',
            submodules=True)
    version('exclaim',
            branch='icon-dsl',
            git='git@github.com:C2SM/icon-exclaim.git',
            submodules=True)

    # The variants' default follow those of ICON
    # as described here
    # https://gitlab.dkrz.de/icon/icon/-/blob/icon-2024.01/configure?ref_type=tags#L1492-1638

    # EXCLAIM-GT4Py specific features:
    dsl_values = ('substitute', 'verify', 'serialize', 'fused', 'nvtx', 'lam')
    variant('dsl',
            default='none',
            validator=validate_variant_dsl,
            values=('none', ) + dsl_values,
            description='Build with GT4Py dynamical core',
            multi=True)

    for x in dsl_values:
        depends_on('py-icon4py', when='dsl={0}'.format(x))
        depends_on('py-gridtools-cpp', when='dsl={0}'.format(x))
        depends_on('boost', when='dsl={0}'.format(x))
        conflicts('^python@:3.9,3.11:', when='dsl={0}'.format(x))

    depends_on('cosmo-eccodes-definitions',
               type='run',
               when='+eccodes-definitions')

    def setup_build_environment(self, env):
        super().set_build_envirionment(self, env)
        # help cmake to build dsl-stencils
        if 'none' not in self.spec.variants['dsl'].value:
            env.set("CUDAARCHS", self.spec.variants['cuda_arch'].value[0])
            env.unset("CUDAHOSTCXX")
            env.set("BOOST_ROOT", self.spec['boost'].prefix)

    def configure_args(self):
        args = super().configure_args()
        super_libs = args.pop()

        libs = LibraryList([])
        flags = defaultdict(list)

        # Check for DSL variants and set corresponding Liskov options
        dsl = self.spec.variants['dsl'].value
        if dsl != ('none', ):
            if 'substitute' in dsl:
                args.append('--enable-liskov=substitute')
            elif 'verify' in dsl:
                args.append('--enable-liskov=verify')
            elif 'serialize' in dsl:
                raise error.UnsupportedPlatformError(
                    'serialize mode is not supported yet by icon-liskov')

            if 'lam' in dsl:
                args.append('--enable-dsl-local')
            if 'nvtx' in dsl:
                args.append('--enable-nvtx')
            if 'fused' in dsl:
                raise error.UnsupportedPlatformError(
                    'liskov does not support fusing just yet')

            flags['LOC_GT4PY'].append(self.spec['py-gt4py'].prefix)
            flags['LOC_ICON4PY_BIN'].append(self.spec['py-icon4py'].prefix)

            flags['LOC_ICON4PY_ATM_DYN_ICONAM'].append(
                self.spec['py-icon4py:atm_dyn_iconam'].headers.directories[0])

            if self.spec['py-icon4py'].version < Version("0.0.4"):
                flags['LOC_ICON4PY_UTILS'].append(
                    os.path.dirname(
                        self.spec['py-icon4py:utils'].headers.directories[0]))
            else:
                flags['LOC_ICON4PY_TOOLS'].append(
                    self.spec['py-icon4py:tools'].headers.directories[0])
                if self.spec['py-icon4py'].version > Version("0.0.7"):
                    flags['LOC_ICON4PY_DIFFUSION'].append(
                        self.spec['py-icon4py:diffusion'].headers.
                        directories[0])
                    flags['LOC_ICON4PY_INTERPOLATION'].append(
                        self.spec['py-icon4py:interpolation'].headers.
                        directories[0])
                if self.spec['py-icon4py'].version > Version("0.0.8"):
                    flags['LOC_ICON4PY_ADVECTION'].append(
                        self.spec['py-icon4py:advection'].headers.
                        directories[0])
            flags['LOC_GRIDTOOLS'].append(
                self.spec['py-gridtools-cpp:data'].headers.directories[0])
            flags['GT4PYNVCFLAGS'] = flags['NVCFLAGS']

        args.extend([
            "{0}={1}".format(name, " ".join(value))
            for name, value in flags.items()
        ])
        args.append(f"{super_libs} {libs.link_flags}")
        return args
