import os, subprocess, glob, re
from collections import defaultdict

from llnl.util import lang, filesystem, tty
from spack.util.environment import is_system_path, dump_environment
from spack.util.executable import which_string, which
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


class Icon(AutotoolsPackage, CudaPackage):
    """Icosahedral Nonhydrostatic Weather and Climate Model."""

    homepage = "https://www.icon-model.org"
    url = "https://gitlab.dkrz.de/icon/icon-model/-/archive/icon-2024.01-public/icon-model-icon-2024.01-public.tar.gz"
    git = 'git@gitlab.dkrz.de:icon/icon.git'

    maintainers = ['jonasjucker', 'dominichofer']

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
    variant('atmo',
            default=True,
            description='Enable the atmosphere component')
    variant('les',
            default=True,
            description='Enable the Large-Eddy Simulation component')
    variant('upatmo',
            default=True,
            description='Enable the upper atmosphere component')
    variant('ocean', default=True, description='Enable the ocean component')
    variant('jsbach', default=True, description='Enable the land component')
    variant('waves',
            default=False,
            description='Enable the surface wave component')
    variant('coupling', default=True, description='Enable the coupling')
    variant('aes', default=True, description='Enable the AES physics package')
    variant('nwp', default=True, description='Enable the NWP physics package')
    variant('ecrad',
            default=False,
            description='Enable usage of the ECMWF radiation scheme')
    variant('rte-rrtmgp',
            default=True,
            description='Enable usage of the RTE+RRTMGP toolbox '
            'for radiation calculations')
    variant(
        'rttov',
        default=False,
        description='Enable usage of the radiative transfer model for TOVS')
    variant('dace',
            default=False,
            description='Enable the DACE modules for data assimilation')
    variant('emvorado',
            default=False,
            description='Enable the radar forward operator EMVORADO')
    variant('art',
            default=False,
            description='Enable the aerosols and reactive trace component ART')
    variant('art-gpl',
            default=False,
            description='Enable GPL-licensed code parts of the ART component')
    variant('comin',
            default=False,
            description='Enable the ICON community interfaces')
    variant(
        'acm-license',
        default=False,
        description=
        'Enable code parts that require accepting the ACM Software License')

    # Infrastructural Features:
    variant('mpi',
            default=True,
            description='Enable MPI (parallelization) support')
    variant(
        'active-target-sync',
        default=False,
        description=
        'Enable MPI active target mode (otherwise, passive target mode is used)'
    )
    variant('async-io-rma',
            default=True,
            description='Enable remote memory access (RMA) for async I/O')
    variant('mpi-gpu',
            default=False,
            description='Enable usage of the GPU-aware MPI features')
    variant('openmp', default=False, description='Enable OpenMP support')
    variant('gpu',
            default='no',
            values=('openacc+cuda', 'no'),
            description='Enable GPU support')
    variant('realloc-buf',
            default=False,
            description='Enable reallocatable communication buffer')
    variant('grib2', default=False, description='Enable GRIB2 I/O')
    variant('parallel-netcdf',
            default=False,
            description='Enable usage of the parallel features of NetCDF')
    variant('cdi-pio',
            default=False,
            description='Enable usage of the parallel features of CDI')
    variant('sct', default=False, description='Enable the SCT timer')
    variant('yaxt', default=False, description='Enable the YAXT data exchange')

    serialization_values = ('read', 'perturb', 'create')
    variant('serialization',
            default='none',
            values=('none', ) + serialization_values,
            description='Enable the Serialbox2 serialization')
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
    variant('comin',
            default=False,
            description='Enable usage of ComIn toolbox '
            'for building plugins.')

    # Optimization Features:
    variant('loop-exchange', default=True, description='Enable loop exchange')
    variant('vectorized-lrtm',
            default=False,
            description='Enable the parallelization-invariant version of LRTM')
    variant('mixed-precision',
            default=False,
            description='Enable mixed precision dycore')
    variant(
        'pgi-inlib',
        default=False,
        description=
        'Enable PGI/NVIDIA cross-file function inlining via an inline library')
    variant('nccl', default=False, description='Enable NCCL for communication')
    variant('cuda-graphs', default=False, description='Enable CUDA graphs.')
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

    # C2SM specific Features:
    variant(
        'infero',
        default=False,
        description=
        'Build with infero for inference with machine-learning models. Experimental, needs non-standard codebase!'
    )
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

    depends_on('infero +quiet +tf_c +onnx', when='+infero')
    depends_on('pytorch-fortran', when='+pytorch')

    depends_on('libfyaml', when='+coupling')
    depends_on('libxml2', when='+coupling')
    depends_on('libxml2', when='+art')

    depends_on('rttov+hdf5', when='+rttov')
    depends_on('rttov~openmp', when='~openmp+rttov')

    for x in serialization_values:
        depends_on('serialbox+fortran', when='serialization={0}'.format(x))

    depends_on('libcdi-pio+fortran+netcdf', when='+cdi-pio')
    depends_on('libcdi-pio grib2=eccodes', when='+cdi-pio+grib2')
    depends_on('libcdi-pio+mpi', when='+cdi-pio+mpi')

    depends_on('eccodes +fortran', when='+emvorado')
    depends_on('eccodes', when='+grib2 ~cdi-pio')
    depends_on('cosmo-eccodes-definitions',
               type=('build', 'run'),
               when='+eccodes-definitions')

    depends_on('yaxt+fortran', when='+cdi-pio')
    depends_on('lapack')
    depends_on('blas')
    depends_on('netcdf-fortran')

    depends_on('netcdf-c', when='~cdi-pio')
    depends_on('netcdf-c', when='+coupling')
    depends_on('netcdf-c+mpi', when='+parallel-netcdf~cdi-pio')

    depends_on('hdf5 +szip +hl +fortran', when='+emvorado')
    depends_on('hdf5 +szip', when='+sct')

    depends_on('zlib', when='+emvorado')
    depends_on('mpi', when='+mpi')

    depends_on('python', type='build')
    depends_on('perl', type='build')
    depends_on('cmake@3.18:', type='build')

    conflicts('+dace', when='~mpi')
    conflicts('+emvorado', when='~mpi')
    conflicts('+cuda', when='%gcc')
    conflicts('~infero', when='+pytorch')

    # The gpu=openacc+cuda relies on the cuda variant
    conflicts('~cuda', when='gpu=openacc+cuda')
    conflicts('+cuda', when='gpu=no')

    conflicts('+cuda-graphs', when='%cce')
    conflicts('+cuda-graphs', when='%gcc')
    conflicts('+cuda-graphs', when='%intel')
    conflicts('+cuda-graphs', when='%pgi')
    conflicts('+cuda-graphs', when='%nvhpc@:23.2')

    conflicts('+loop-exchange', when='gpu=openacc+cuda')

    # Flag to mark if we build out-of-source
    # Needed to trigger sync of input files for experiments
    out_of_source_build = False
    out_of_source_configure_directory = ''

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
        args = ['--disable-rpaths']
        flags = defaultdict(list)
        libs = LibraryList([])

        for x in [
                'atmo',
                'les',
                'upatmo',
                'ocean',
                'jsbach',
                'waves',
                'coupling',
                'aes',
                'nwp',
                'ecrad',
                'rte-rrtmgp',
                'rttov',
                'dace',
                'emvorado',
                'art',
                'art-gpl',
                'comin',
                'acm-license',
                'mpi',
                'active-target-sync',
                'async-io-rma',
                'mpi-gpu',
                'openmp',
                'realloc-buf',
                'grib2',
                'parallel-netcdf',
                'sct',
                'yaxt',
                'testbed',
                'loop-exchange',
                'vectorized-lrtm',
                'mixed-precision',
                'pgi-inlib',
                'nccl',
                'cuda-graphs',
                'silent-rules',
                'comin',
        ]:
            args += self.enable_or_disable(x)

        if '+cdi-pio' in self.spec:
            args.extend([
                '--enable-cdi-pio', '--with-external-cdi',
                '--with-external-yaxt'
            ])

        if self.compiler.name == 'gcc':
            flags['CFLAGS'].append('-g')
            flags['ICON_CFLAGS'].append('-O3')
            flags['ICON_BUNDLED_CFLAGS'].append('-O2')
            flags['FCFLAGS'].extend([
                '-g',
                '-fmodule-private',
                '-fimplicit-none',
                '-fmax-identifier-length=63',
                '-Wall',
                '-Wcharacter-truncation',
                '-Wconversion',
                '-Wunderflow',
                '-Wunused-parameter',
                '-Wno-surprising',
                '-fall-intrinsics',
            ])
            flags['ICON_FCFLAGS'].extend([
                '-O2', '-fbacktrace', '-fbounds-check',
                '-fstack-protector-all', '-finit-real=nan',
                '-finit-integer=-2147483648', '-finit-character=127'
            ])
            flags['ICON_OCEAN_FCFLAGS'].append('-O3')

            # Version-specific workarounds:
            fc_version = self.compiler.version
            if fc_version >= ver(10):
                flags['ICON_FCFLAGS'].append('-fallow-argument-mismatch')
                flags['ICON_OCEAN_FCFLAGS'].append('-fallow-argument-mismatch')
                if '+ecrad' in self.spec:
                    # For externals/ecrad/ifsaux/random_numbers_mix.F90:
                    flags['ICON_ECRAD_FCFLAGS'].append('-fallow-invalid-boz')
        elif self.compiler.name == 'intel':
            flags['CFLAGS'].extend(
                ['-g', '-gdwarf-4', '-O3', '-qno-opt-dynamic-align', '-ftz'])
            flags['FCFLAGS'].extend(
                ['-g', '-gdwarf-4', '-traceback', '-fp-model source'])
            flags['ICON_FCFLAGS'].extend(
                ['-O2', '-assume realloc_lhs', '-ftz'])
            flags['ICON_OCEAN_FCFLAGS'].extend([
                '-O3', '-assume norealloc_lhs', '-reentrancy threaded',
                '-qopt-report-file=stdout', '-qopt-report=0',
                '-qopt-report-phase=vec'
            ])
            args.append('--enable-intel-consistency')
        elif self.compiler.name == 'nag':
            flags['CFLAGS'].append('-g')
            flags['ICON_CFLAGS'].append('-O3')
            flags['ICON_BUNDLED_CFLAGS'].append('-O2')
            flags['FCFLAGS'].extend([
                '-g', '-Wc,-g', '-O0', '-colour', '-f2008', '-w=uep',
                '-float-store', '-nan'
            ])
            if '~openmp' in self.spec:
                # The -openmp option is incompatible with the -gline option:
                flags['FCFLAGS'].append('-gline')
            flags['ICON_FCFLAGS'].extend([
                '-Wc,-pipe',
                '-Wc,--param,max-vartrack-size=200000000',
                '-Wc,-mno-fma',
                # Spack compiler wrapper (see the respective compilers.yaml)
                # injects '-mismatch', which is incompatible with '-C=calls'
                # Therefore, we specify the following flags instead of a single
                # '-C=all', which implies '-C=calls'.
                '-C=alias',
                '-C=array',
                '-C=bits',
                '-C=dangling',
                '-C=do',
                '-C=intovf',
                '-C=present',
                '-C=pointer',
                '-C=recursion'
            ])
            flags['ICON_BUNDLED_FCFLAGS'] = []
        elif self.compiler.name in ['pgi', 'nvhpc']:
            flags['CFLAGS'].extend(['-g', '-O2'])
            flags['FCFLAGS'].extend(
                ['-g', '-O', '-Mrecursive', '-Mallocatable=03', '-Mbackslash'])

            if self.spec.variants['gpu'].value == 'openacc+cuda':
                flags['FCFLAGS'].extend([
                    '-acc=verystrict', '-Minfo=accel,inline',
                    '-gpu=cc{0}'.format(
                        self.spec.variants['cuda_arch'].value[0])
                ])
        elif self.compiler.name == 'cce':
            flags['CFLAGS'].append('-g')
            flags['ICON_CFLAGS'].append('-O3')
            if self.spec.satisfies('%cce@13.0.0+coupling'):
                # For externals/yac/tests/test_interpolation_method_conserv.c:
                flags['ICON_YAC_CFLAGS'].append('-O2')
            flags['FCFLAGS'].extend([
                '-hadd_paren', '-r am', '-Ktrap=divz,ovf,inv',
                '-hflex_mp=intolerant', '-hfp0', '-O0'
            ])
            if self.spec.variants['gpu'].value == 'openacc+cuda':
                flags['FCFLAGS'].extend(['-hacc'])
        elif self.compiler.name == 'aocc':
            flags['CFLAGS'].extend(['-g', '-O2'])
            flags['FCFLAGS'].extend(['-g', '-O2'])
            if self.spec.satisfies('~cdi-pio+yaxt'):
                # Enable the PGI/Cray (NO_2D_PARAM) workaround for the test
                # suite of the bundled YAXT (apply also when not self.run_tests
                # to make sure we get identical installations):
                flags['ICON_YAXT_FCFLAGS'].append('-DNO_2D_PARAM')
        else:
            flags['CFLAGS'].extend(['-g', '-O2'])
            flags['FCFLAGS'].extend(['-g', '-O2'])

        if '+coupling' in self.spec or '+art' in self.spec:
            xml2_spec = self.spec['libxml2']
            libs += xml2_spec.libs
            # Account for the case when libxml2 is an external package installed
            # to a system directory, which means that Spack will not inject the
            # required -I flag with the compiler wrapper:
            if is_system_path(xml2_spec.prefix):
                xml2_headers = xml2_spec.headers
                # We, however, should filter the pure system directories out:
                xml2_headers.directories = [
                    d for d in xml2_headers.directories
                    if not is_system_path(d)
                ]
                flags['CPPFLAGS'].append(xml2_headers.include_flags)

        if '+coupling' in self.spec:
            libs += self.spec['libfyaml'].libs

        serialization = self.spec.variants['serialization'].value
        if serialization == 'none':
            args.append('--disable-serialization')
        else:
            args.extend([
                '--enable-serialization={0}'.format(serialization),
                'SB2PP={0}'.format(self.spec['serialbox'].pp_ser)
            ])
            libs += self.spec['serialbox:fortran'].libs

        if '+cdi-pio' in self.spec:
            libs += self.spec['libcdi-pio:fortran'].libs

        if '+emvorado' in self.spec:
            libs += self.spec['eccodes:fortran'].libs

        if '+grib2~cdi-pio' in self.spec:
            libs += self.spec['eccodes:c'].libs

        if '+cdi-pio' in self.spec:
            libs += self.spec['yaxt:fortran'].libs

        if '+rttov' in self.spec:
            libs += self.spec['rttov'].libs

        libs += self.spec['lapack:fortran'].libs
        libs += self.spec['blas:fortran'].libs
        libs += self.spec['netcdf-fortran'].libs

        if '+coupling' in self.spec or '~cdi-pio' in self.spec:
            libs += self.spec['netcdf-c'].libs

        if '+emvorado' in self.spec or '+rttov' in self.spec:
            libs += self.spec['hdf5:fortran,hl'].libs
        elif '+sct' in self.spec:
            libs += self.spec['hdf5'].libs

        if '+emvorado' in self.spec:
            libs += self.spec['zlib'].libs

        if '+mpi' in self.spec:
            args.extend([
                'CC=' + self.spec['mpi'].mpicc,
                'FC=' + self.spec['mpi'].mpifc,
                # We cannot provide a universal value for MPI_LAUNCH, therefore
                # we have to disable the MPI checks:
                '--disable-mpi-checks'
            ])

        if '+pytorch' in self.spec:
            libs += self.spec['pytorch-fortran'].libs
        if '+infero' in self.spec:
            libs += self.spec['infero'].libs

        fcgroup = self.spec.variants['fcgroup'].value
        # ('none',) is the values spack assign if fcgroup is not set
        if fcgroup != ('none', ):
            args.extend(self.fcgroup_to_config_arg())
            flags.update(self.fcgroup_to_config_var())

        gpu = self.spec.variants['gpu'].value
        if gpu == 'no':
            args.append('--disable-gpu')
        else:
            args.extend([
                '--enable-gpu={0}'.format(gpu),
                'NVCC={0}'.format(self.spec['cuda'].prefix.bin.nvcc)
            ])

            libs += self.spec['cuda'].libs

            cuda_host_compiler = self.compiler.cxx
            cuda_host_compiler_stdcxx_libs = self.compiler.stdcxx_libs

            if 'none' in self.spec.variants['dsl'].value:
                flags['NVCFLAGS'].extend(
                    ['-ccbin {0}'.format(cuda_host_compiler)])

            flags['NVCFLAGS'].extend([
                '-g', '-O3',
                '-arch=sm_{0}'.format(self.spec.variants['cuda_arch'].value[0])
            ])
            # cuda_host_compiler_stdcxx_libs might contain compiler-specific
            # flags (i.e. not the linker -l<library> flags), therefore we put
            # the value to the config_flags directly.
            flags['LIBS'].extend(cuda_host_compiler_stdcxx_libs)

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
            '{0}={1}'.format(var, ' '.join(val)) for var, val in flags.items()
        ])

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

    @run_after('configure')
    def adjust_rttov_macro(self):
        if '+rttov' in self.spec:
            rttov_major_version = self.spec['rttov'].version.up_to(1)
            if rttov_major_version != ver(13):
                filter_file('_RTTOV_VERSION=13',
                            '_RTTOV_VERSION={0}'.format(rttov_major_version),
                            'icon.mk',
                            string=True,
                            backup=False)

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

    @property
    def archive_files(self):
        # Archive files that are normally archived for AutotoolsPackage:
        archive = list(super(Icon, self).archive_files)
        # Archive makefiles:
        archive.extend(
            [join_path(self.build_directory, f) for f in ['Makefile', '*.mk']])
        return archive

    @property
    def build_directory(self):
        """Overrides function from spack.build_system.autotools
        
        By default build_directory is identical as configure_directory
        To enable out-of-source builds this is not the case anymore
        """

        return self.stage.source_path

    @property
    def configure_directory(self):
        """Returns the directory where 'configure' resides.

        Overides function from spack.build_systems.autotools

        """

        source_path = self.build_directory

        # dev_path is indicator for dev-build or develop
        # only case when out-of-source build are possible
        if "dev_path" in self.spec.variants:
            Git = which('git', required=True)
            git_root = Git('rev-parse',
                           '--show-toplevel',
                           output=str,
                           fail_on_error=True).replace("\n", "")
            if git_root != source_path:
                # mark out-of-source build for function
                # copy_runscript_related_input_files
                self.out_of_source_build = True
                self.out_of_source_configure_directory = git_root
                return git_root

        return source_path

    @run_before('configure')
    def report_out_of_source_directories(self):
        if self.out_of_source_build:
            tty.info(f'build-directory: {self.build_directory}')
            tty.info(
                f'configure-directory: {self.out_of_source_configure_directory}'
            )

    def configure(self, spec, prefix):
        if os.path.exists(
                os.path.join(self.build_directory,
                             'icon.mk')) and self.build_uses_same_spec():
            tty.warn(
                'icon.mk already present -> skip configure stage',
                '\t delete "icon.mk" or run "make distclean" to not skip configure'
            )
            return

        # Call configure of Autotools
        super().configure(spec, prefix)

    def build_uses_same_spec(self):
        """
        Ensure that configure is rerun in case spec has changed,
        otherwise for the case below

            $ spack dev-build icon @develop ~dace
            $ spack dev-build icon @develop +dace
        
        configure is skipped for the latter.
        """

        is_same_spec = False

        previous_spec = os.path.join(self.build_directory,
                                     '.previous_spec.yaml')

        # not the first build in self.build_directory
        if os.path.exists(previous_spec):
            with open(previous_spec, mode='r') as f:
                if self.spec == Spec.from_yaml(f):
                    is_same_spec = True
                else:
                    is_same_spec = False
                    tty.warn(
                        'Cannot skip configure phase because spec changed')

        # first build in self.build_directory, no worries
        else:
            is_same_spec = True

        # dump spec of new build
        with open(previous_spec, mode='w') as f:
            f.write(self.spec.to_yaml())

        return is_same_spec

    @run_after('configure')
    def copy_runscript_related_input_files(self):
        if self.out_of_source_build:
            with working_dir(self.build_directory):
                Rsync = which('rsync', required=True)
                icon_dir = self.configure_directory
                Rsync("-uavz", f"{icon_dir}/run", ".", "--exclude=*.in",
                      "--exclude=.*", "--exclude=standard_*")
                Rsync("-uavz", f"{icon_dir}/externals", ".", "--exclude=.git",
                      "--exclude=*.f90", "--exclude=*.F90", "--exclude=*.c",
                      "--exclude=*.h", "--exclude=*.Po", "--exclude=tests",
                      "--exclude=*.mod", "--exclude=*.o")
                Rsync("-uavz", f"{icon_dir}/make_runscripts", ".")

                Ln = which('ln', required=True)
                dirs = glob.glob(f"{icon_dir}/run/standard_*")
                for dir in dirs:
                    Ln("-sf", "-t", "run/", f"{dir}")
                Ln("-sf", f"{icon_dir}/data")
                Ln("-sf", f"{icon_dir}/vertical_coord_tables")
