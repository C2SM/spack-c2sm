from spack.pkg.builtin.icon import Icon as SpackIcon
import os, glob, re
from collections import defaultdict

from llnl.util import tty
from spack.util.environment import is_system_path
from spack.util.executable import which
import spack.error as error


def validate_variant_dsl(pkg, name, value):
    set_mutual_excl = set(['substitute', 'verify', 'serialize'])
    set_input_var = set(value)
    if len(set_mutual_excl.intersection(set_input_var)) > 1:
        raise error.SpecError(
            'Cannot have more than one of (substitute, verify, serialize) in the same build'
        )


def check_variant_fcgroup(fcgroup):
    pattern = re.compile(r"^[A-Z]+\..+\..")
    # fcgroup is False as default
    if pattern.match(fcgroup) or fcgroup == 'none':
        return True
    else:
        tty.warn('Variant fcgroup needs format GROUP.files.flag')
        return False


def check_variant_extra_config_args(extra_config_arg):
    pattern = re.compile(r'--(enable|disable)-\S+')
    if pattern.match(extra_config_arg) or extra_config_arg == 'none':
        return True
    else:
        tty.warn(
            f'The value "{extra_config_arg}" for the extra_config_args variant must follow the format "--enable-arg" or "--disable-arg"'
        )
        return False


class IconC2sm(SpackIcon):
    git = 'git@gitlab.dkrz.de:icon/icon.git'

    maintainers('jonasjucker', 'huppd')

    version('develop', submodules=True)
    version("2024.01-1", tag="icon-2024.01-1", submodules=True)
    version('exclaim-master',
            branch='master',
            git='git@github.com:C2SM/icon-exclaim.git',
            submodules=True)
    version('exclaim',
            branch='icon-dsl',
            git='git@github.com:C2SM/icon-exclaim.git',
            submodules=True)
    version('nwp-master',
            git='git@gitlab.dkrz.de:icon/icon-nwp.git',
            submodules=True)

    # The variants' default follow those of ICON
    # as described here
    # https://gitlab.dkrz.de/icon/icon/-/blob/icon-2024.01/configure?ref_type=tags#L1492-1638

    # Model Features:
    variant('dace',
            default=False,
            description='Enable the DACE modules for data assimilation')
    requires("+mpi", when="+dace")

    variant('emvorado',
            default=False,
            description='Enable the radar forward operator EMVORADO')
    requires("+mpi", when="+emvorado")

    variant('art-gpl',
            default=False,
            description='Enable GPL-licensed code parts of the ART component')
    variant(
        'acm-license',
        default=False,
        description=
        'Enable code parts that require accepting the ACM Software License')

    # Infrastructural Features:
    variant(
        'active-target-sync',
        default=False,
        description=
        'Enable MPI active target mode (otherwise, passive target mode is used)'
    )
    variant('async-io-rma',
            default=True,
            description='Enable remote memory access (RMA) for async I/O')
    variant('realloc-buf',
            default=False,
            description='Enable reallocatable communication buffer')
    variant('sct', default=False, description='Enable the SCT timer')
    variant('testbed',
            default=False,
            description='Enable ICON Testbed infrastructure')

    variant(
        'extra-config-args',
        default='none',
        multi=True,
        values=check_variant_extra_config_args,
        description=
        'Inject any configure argument not yet available as variant\nUse this feature cautiously, as injecting non-variant configure arguments may potentially disrupt the build process'
    )

    # Optimization Features:
    variant('loop-exchange', default=True, description='Enable loop exchange')
    variant('vectorized-lrtm',
            default=False,
            description='Enable the parallelization-invariant version of LRTM')
    variant(
        'pgi-inlib',
        default=False,
        description=
        'Enable PGI/NVIDIA cross-file function inlining via an inline library')
    variant('nccl', default=False, description='Enable NCCL for communication')

    variant('cuda-graphs', default=False, description='Enable CUDA graphs.')
    requires('%nvhpc@23.3:', when='+cuda-graphs')

    variant(
        'fcgroup',
        default='none',
        multi=True,
        values=check_variant_fcgroup,
        description=
        'Create a Fortran compile group: GROUP;files;flag \nNote: flag can only be one single value, i.e. -O1'
    )

    # verbosity
    variant('silent-rules',
            default=True,
            description='Enable silent-rules for build-process')
    variant(
        'pytorch',
        default=False,
        description=
        'Build with pytorch for inference with machine-learning models. Experimental, needs non-standard codebase!'
    )
    variant(
        'eccodes-definitions',
        default=False,
        description=
        'Enable extension of eccodes with center specific definition files')

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

    with when('+emvorado'):
        depends_on('eccodes +fortran')
        depends_on('hdf5 +szip +hl +fortran')
        depends_on('zlib')

    depends_on('pytorch-fortran', when='+pytorch')
    depends_on('hdf5 +szip', when='+sct')

    # patch_libtool is a function from Autotoolspackage.
    # For BB we cannot use it because it finds all files
    # named "libtool". spack-c2sm is cloned into icon-repo,
    # therefore this function detects not only "libtool" files, but
    # also the folder where libtool package itself is installed.
    patch_libtool = False

    def setup_build_environment(self, env):
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

        for x in [
                'dace',
                'emvorado',
                'art-gpl',
                'acm-license',
                'active-target-sync',
                'async-io-rma',
                'realloc-buf',
                'parallel-netcdf',
                'sct',
                'testbed',
                'loop-exchange',
                'vectorized-lrtm',
                'pgi-inlib',
                'nccl',
                'cuda-graphs',
                'silent-rules',
        ]:
            args += self.enable_or_disable(x)

        if '+emvorado' in self.spec:
            libs += self.spec['eccodes:fortran'].libs
            libs += self.spec['hdf5:fortran,hl'].libs
            libs += self.spec['zlib'].libs

        if '+sct' in self.spec:
            libs += self.spec['hdf5'].libs

        if '+pytorch' in self.spec:
            libs += self.spec['pytorch-fortran'].libs

        fcgroup = self.spec.variants['fcgroup'].value
        # ('none',) is the values spack assign if fcgroup is not set
        if fcgroup != ('none', ):
            args.extend(self.fcgroup_to_config_arg())
            flags.update(self.fcgroup_to_config_var())

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

        # add configure arguments not yet available as variant
        extra_config_args = self.spec.variants['extra-config-args'].value
        if extra_config_args != ('none', ):
            for x in extra_config_args:
                # prevent configure-args already available as variant
                # to be set through variant extra_config_args
                self.validate_extra_config_args(x)
                args.append(x)
            tty.warn(
                'You use variant extra-config-args. Injecting non-variant configure arguments may potentially disrupt the build process!'
            )

        # Finalize the LIBS variable (we always put the real collected
        # libraries to the front):
        flags['LIBS'].insert(0, libs.link_flags)

        # Help the libtool scripts of the bundled libraries find the correct
        # paths to the external libraries. Specify the library search (-L) flags
        # in the reversed order
        # (see https://gitlab.dkrz.de/icon/icon#icon-dependencies):
        # and for non-system directories only:
        flags['LDFLAGS'].extend([
            '-L{0}'.format(d) for d in reversed(libs.directories)
            if not is_system_path(d)
        ])

        args.extend([
            "{0}={1}".format(name, " ".join(value))
            for name, value in flags.items()
        ])
        args.append(f"{super_libs} {libs.link_flags}")
        return args

    def fcgroup_to_config_arg(self):
        arg = []
        for group in self.spec.variants['fcgroup'].value:
            name = group.split('.')[0]
            files = group.split('.')[1]
            arg.append(f'--enable-fcgroup-{name}={files}')
        return arg

    def fcgroup_to_config_var(self):
        var = {}
        for group in self.spec.variants['fcgroup'].value:
            name = group.split('.')[0]
            flag = group.split('.')[2]
            # Note: flag needs to be a list
            var[f'ICON_{name}_FCFLAGS'] = [flag]
        return var

    def strip_variant_prefix(self, variant_string):
        prefixes = ["--enable-", "--disable-"]

        for prefix in prefixes:
            if variant_string.startswith(prefix):
                return variant_string[len(prefix):]

        raise ValueError

    def validate_extra_config_args(self, arg):
        variant_from_arg = self.strip_variant_prefix(arg)
        if variant_from_arg in self.spec.variants:
            raise error.SpecError(
                f'The value "{arg}" for the extra_config_args variant conflicts '
                f'with the existing variant {variant_from_arg}. Set this variant instead.'
            )

    def check(self):
        # By default "check" calls make with targets "check" and "test".
        # This testing is beyond the scope of BuildBot test at CSCS.
        # Therefore override this function, saves a lot of time too.
        pass

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def checksuite(self):
        # script needs cdo to work, but not listed as dep of ICON
        test_script = 'scripts/spack/test.py'
        if os.path.exists(test_script):
            test_py = Executable(test_script)

            # test.py fails if PYTHONHOME has any value,
            # even '' or ' ' is failing, therefore delete
            # it temporary from env
            if 'PYTHONHOME' in os.environ:
                PYTHONHOME = os.environ['PYTHONHOME']
                os.environ.pop('PYTHONHOME')
                pythonhome_is_set = True
            else:
                pythonhome_is_set = False

            with open('spec.yaml', mode='w') as f:
                f.write(self.spec.to_yaml())
            test_py('--spec', 'spec.yaml', fail_on_error=True)

            # restore PYTHONHOME after test.py
            if pythonhome_is_set:
                os.environ['PYTHONHOME'] = PYTHONHOME
        else:
            tty.warn('Cannot find test.py -> skipping tests')
