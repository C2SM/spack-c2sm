from spack.pkg.builtin.icon import Icon as SpackIcon
import os
import re
import glob
from collections import defaultdict
from llnl.util import tty
from spack.util.environment import is_system_path
import spack.error as error


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


class Icon(SpackIcon):
    git = 'git@gitlab.dkrz.de:icon/icon.git'

    maintainers('jonasjucker', 'huppd')

    version('develop', submodules=True)
    version("2024.01-1", tag="icon-2024.01-1", submodules=True)
    version('2.6.6-mch2b', tag='icon-nwp/icon-2.6.6-mch2b', submodules=True)
    version('2.6.6-mch2a', tag='icon-nwp/icon-2.6.6-mch2a', submodules=True)
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
        'eccodes-definitions',
        default=False,
        description=
        'Enable extension of eccodes with center specific definition files')

    depends_on('cosmo-eccodes-definitions',
               type='run',
               when='+eccodes-definitions')

    with when('+emvorado'):
        depends_on('eccodes +fortran')
        depends_on('hdf5 +szip +hl +fortran')
        depends_on('zlib')
        # WORKAROUND: A build and link dependency should imply that the same compiler is used. This enforces it.
        depends_on('eccodes %nvhpc', when='%nvhpc')
        depends_on('eccodes %gcc', when='%gcc')

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. This enforces it.
    for __x in SpackIcon.serialization_values:
        with when("serialization={0}".format(__x)):
            depends_on('serialbox %nvhpc', when='%nvhpc')
            depends_on('serialbox %gcc', when='%gcc')

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. This enforces it.
    depends_on('netcdf-fortran %nvhpc', when='%nvhpc')
    depends_on('netcdf-fortran %gcc', when='%gcc')

    depends_on('hdf5 +szip', when='+sct')

    # patch_libtool is a function from Autotoolspackage.
    # For BB we cannot use it because it finds all files
    # named "libtool". spack-c2sm is cloned into icon-repo,
    # therefore this function detects not only "libtool" files, but
    # also the folder where libtool package itself is installed.
    patch_libtool = False

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

        fcgroup = self.spec.variants['fcgroup'].value
        # ('none',) is the values spack assign if fcgroup is not set
        if fcgroup != ('none', ):
            args.extend(self.fcgroup_to_config_arg())
            flags.update(self.fcgroup_to_config_var())

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

    @run_after('configure')
    def copy_runscript_related_input_files(self):
        with working_dir(self.build_directory):
            icon_dir = self.configure_directory
            # only synchronize if out-of-source build
            if os.path.abspath(icon_dir) != os.path.abspath(self.build_directory):
                Rsync = which('rsync', required=True)
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
