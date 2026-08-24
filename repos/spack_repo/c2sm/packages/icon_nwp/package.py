import os
import re
import glob
from collections import defaultdict
from itertools import chain

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *
from spack.spec import Spec


def check_variant_fcgroup(fcgroup):
    pattern = re.compile(r"^[A-Z]+\..+\..")
    # fcgroup is False as default
    if pattern.match(fcgroup) or fcgroup == "none":
        return True
    else:
        tty.warn("Variant fcgroup needs format GROUP.files.flag")
        return False


def check_variant_extra_config_args(extra_config_arg):
    pattern = re.compile(r"--(enable|disable)-\S+")
    if pattern.match(extra_config_arg) or extra_config_arg == "none":
        return True
    else:
        tty.warn(
            f'The value "{extra_config_arg}" for the extra_config_args variant must follow the format "--enable-arg" or "--disable-arg"'
        )
        return False


class BaseIcon(AutotoolsPackage):
    """ICON - is a modeling framework for weather, climate, and environmental prediction. It solves
    the full three-dimensional non-hydrostatic and compressible Navier-Stokes equations on an
    icosahedral grid and allows seamless predictions from local to global scales."""

    homepage = "https://www.icon-model.org"
    url = "https://gitlab.dkrz.de/icon/icon-model/-/archive/icon-2024.01-public/icon-model-icon-2024.01-public.tar.gz"
    git = "https://gitlab.dkrz.de/icon/icon-model.git"
    submodules = True

    maintainers("skosukhin", "Try2Code")

    license("BSD-3-Clause", checked_by="skosukhin")

    version(
        "2025.10-2", tag="icon-2025.10-2-public", commit="69ef5cda9b81f5947e30d1016f41e7b37012f5de"
    )
    version(
        "2025.04", tag="icon-2025.04-public", commit="1be2ca66ea0de149971d2e77e88a9f11c764bd22"
    )
    version("2024.10", sha256="5c461c783eb577c97accd632b18140c3da91c1853d836ca2385f376532e9bad1")
    version("2024.07", sha256="f53043ba1b36b8c19d0d2617ab601c3b9138b90f8ff8ca6db0fd079665eb5efa")
    version("2024.01-1", sha256="3e57608b7e1e3cf2f4cb318cfe2fdb39678bd53ca093955d99570bd6d7544184")
    version("2024.01", sha256="d9408fdd6a9ebf5990298e9a09c826e8c15b1e79b45be228f7a5670a3091a613")

    # Model Features:
    variant("atmo", default=True, description="Enable the atmosphere component")
    variant("les", default=True, description="Enable the Large-Eddy Simulation component")
    variant("upatmo", default=True, description="Enable the upper atmosphere component")
    variant("ocean", default=True, description="Enable the ocean component")
    variant("jsbach", default=True, description="Enable the land component JSBACH")
    variant("waves", default=True, description="Enable the ocean surface wave component")
    variant("coupling", default=True, description="Enable the coupling")
    variant("aes", default=True, description="Enable the AES physics package")
    variant("nwp", default=True, description="Enable the NWP physics package")
    variant(
        "ecrad", default=False, description="Enable usage of the ECMWF radiation scheme (ECRAD)"
    )
    variant(
        "rte-rrtmgp",
        default=True,
        description="Enable usage of the RTE+RRTMGP toolbox for radiation calculations",
    )
    variant(
        "art", default=False, description="Enable the aerosols and reactive trace component ART"
    )

    # Infrastructural Features:
    variant("mpi", default=True, description="Enable MPI (parallelization) support")
    variant("openmp", default=False, description="Enable OpenMP support")

    nvidia_targets = {"nvidia-{0}".format(cc): cc for cc in CudaPackage.cuda_arch_values}
    # TODO: add AMD GPU support

    variant(
        "gpu",
        default="none",
        values=("none",) + tuple(nvidia_targets.keys()),
        description="Enable GPU support for the specified architecture",
    )
    for __x in nvidia_targets.keys():
        # Other compilers are not yet tested or supported, older NVHPC versions are not supported:
        requires("%nvhpc@21.3:", when="gpu={0}".format(__x))

    variant("mpi-gpu", default=True, description="Enable usage of the GPU-aware MPI features")
    requires("+mpi", when="+mpi-gpu")
    conflicts("gpu=none", when="+mpi-gpu")

    variant("grib2", default=False, description="Enable GRIB2 I/O")

    variant(
        "parallel-netcdf",
        default=False,
        description="Enable usage of the parallel features of NetCDF",
    )
    requires("+mpi", when="+parallel-netcdf")

    variant("cdi-pio", default=False, description="Enable usage of the parallel features of CDI")
    requires("+mpi", when="+cdi-pio")

    variant("yaxt", default=False, description="Enable the YAXT data exchange")
    requires("+mpi", when="+yaxt")

    serialization_values = ("read", "perturb", "create")
    variant(
        "serialization",
        default="none",
        values=("none",) + serialization_values,
        description="Enable the Serialbox2 serialization",
    )

    variant("comin", default=False, description="Enable the ICON community interfaces")

    # Optimization Features:
    variant("mixed-precision", default=False, description="Enable mixed-precision dynamical core")

    variant("single-precision", default=False, description="Enable single-precision")
    conflicts(
        "+single-precision",
        when="@:2025.03",
        msg="+single-precision requires icon version 2025.04 or newer",
    )

    variant(
        "single-precision-ecrad", default=False, description="Enable single-precision for ecRad"
    )
    conflicts(
        "+single-precision-ecrad",
        when="@:2025.09",
        msg="+single-precision-ecrad requires icon version 2025.10 or newer",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("python", type="build")
    depends_on("perl", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("gmake@3.81:", type="build")
    depends_on("findutils", type="build")

    depends_on("libxml2", when="+art")
    depends_on("libfyaml@0.6:", when="+coupling")
    for __x in serialization_values:
        depends_on("serialbox+fortran", when="serialization={0}".format(__x))
    depends_on("eccodes", when="+grib2")
    depends_on("lapack")
    depends_on("blas")
    depends_on("netcdf-fortran")
    depends_on("netcdf-c")
    depends_on("netcdf-c+mpi", when="+parallel-netcdf")
    depends_on("mpi", when="+mpi")

    for __x in nvidia_targets.keys():
        depends_on("cuda", when="gpu={0}".format(__x))

    def __init__(self, spec: Spec) -> None:
        super().__init__(spec)
        self.single_args: list[str] = []
        self.flags: dict(str, list[str]) = defaultdict(list)
        self.libs: LibraryList = LibraryList([])

    def set_configure_args(self) -> None:
        self.single_args.append("--disable-rpaths")

        for x in [
            "atmo",
            "les",
            "upatmo",
            "ocean",
            "jsbach",
            "waves",
            "aes",
            "nwp",
            "ecrad",
            "rte-rrtmgp",
            "openmp",
            "mpi-gpu",
            "parallel-netcdf",
            "cdi-pio",
            "yaxt",
            "mixed-precision",
            "single-precision",
            "single-precision-ecrad",
            "comin",
        ]:
            self.single_args.extend(self.enable_or_disable(x))

        if self.spec.satisfies("+art"):
            self.single_args.append("--enable-art")
            self.libs += self.spec["libxml2"].libs
        else:
            self.single_args.append("--disable-art")

        if self.spec.satisfies("+coupling"):
            self.single_args.append("--enable-coupling")
            self.libs += self.spec["libfyaml"].libs
        else:
            self.single_args.append("--disable-coupling")

        serialization = self.spec.variants["serialization"].value
        if serialization == "none":
            self.single_args.append("--disable-serialization")
        else:
            self.single_args.extend(
                [
                    "--enable-serialization={0}".format(serialization),
                    "SB2PP={0}".format(self.spec["serialbox"].pp_ser),
                ]
            )
            self.libs += self.spec["serialbox:fortran"].libs

        if self.spec.satisfies("+grib2"):
            self.single_args.append("--enable-grib2")
            self.libs += self.spec["eccodes:c"].libs
        else:
            self.single_args.append("--disable-grib2")

        self.libs += self.spec["lapack:fortran"].libs
        self.libs += self.spec["blas:fortran"].libs
        self.libs += self.spec["netcdf-fortran"].libs
        self.libs += self.spec["netcdf-c"].libs

        if self.spec.satisfies("+mpi"):
            self.single_args.extend(
                [
                    "--enable-mpi",
                    # We cannot provide a universal value for MPI_LAUNCH, therefore we have to
                    # disable the MPI checks:
                    "--disable-mpi-checks",
                    "CC=" + self.spec["mpi"].mpicc,
                    "FC=" + self.spec["mpi"].mpifc,
                ]
            )
        else:
            self.single_args.append("--disable-mpi")

        gpu = self.spec.variants["gpu"].value

        if gpu in self.nvidia_targets:
            self.single_args.append("--enable-gpu=openacc+cuda")
            self.flags["CUDAFLAGS"] = [
                "-g",
                "-O3",
                "-arch=sm_{0}".format(self.nvidia_targets[gpu]),
                "-ccbin={0}".format(spack_cxx),
            ]
            self.libs += self.spec["cuda"].libs
        else:
            self.single_args.append("--disable-gpu")

        if gpu in self.nvidia_targets or self.spec.satisfies("+comin"):
            self.flags["ICON_LDFLAGS"].extend(self.compiler.stdcxx_libs)

        if self.compiler.name == "gcc":
            self.flags["CFLAGS"].append("-g")
            self.flags["ICON_CFLAGS"].append("-O3")
            self.flags["ICON_BUNDLED_CFLAGS"].append("-O2")
            self.flags["FCFLAGS"].append("-g")
            self.flags["ICON_FCFLAGS"].append("-O2")
            if self.spec.satisfies("+ocean"):
                self.flags["ICON_OCEAN_FCFLAGS"].extend(["-O3", "-fno-tree-loop-vectorize"])
                self.single_args.extend(
                    ["--enable-fcgroup-OCEAN", "ICON_OCEAN_PATH=src/hamocc:src/ocean:src/sea_ice"]
                )

        elif self.compiler.name in ["intel", "oneapi"]:
            self.single_args.append("--enable-intel-consistency")

            self.flags["CFLAGS"].extend(["-g", "-ftz", "-fma", "-ip", "-qno-opt-dynamic-align"])
            self.flags["ICON_CFLAGS"].append("-O3")
            self.flags["ICON_BUNDLED_CFLAGS"].append("-O2")
            self.flags["FCFLAGS"].extend(["-g", "-fp-model source"])
            self.flags["ICON_FCFLAGS"].extend(
                [
                    "-O3",
                    "-ftz",
                    "-qoverride-limits",
                    "-assume realloc_lhs",
                    "-align array64byte",
                    "-fma",
                    "-ip",
                ]
            )

            if self.spec.satisfies("+coupling%oneapi"):
                self.flags["ICON_YAC_CFLAGS"].extend(["-O2", "-fp-model precise"])

            if self.spec.satisfies("+ocean"):
                self.flags["ICON_OCEAN_FCFLAGS"].extend(
                    ["-O3", "-assume norealloc_lhs", "-reentrancy threaded"]
                )
                self.single_args.extend(
                    ["--enable-fcgroup-OCEAN", "ICON_OCEAN_PATH=src/hamocc:src/ocean:src/sea_ice"]
                )

                if self.spec.satisfies("+openmp"):
                    self.flags["ICON_OCEAN_FCFLAGS"].extend(["-DOCE_SOLVE_OMP"])

            if self.spec.satisfies("+ecrad"):
                self.flags["ICON_ECRAD_FCFLAGS"].extend(["-qno-opt-dynamic-align", "-no-fma", "-fpe0"])

        elif self.compiler.name == "nvhpc":
            self.flags["CFLAGS"].extend(["-g", "-O2"])
            self.flags["FCFLAGS"].extend(
                ["-g", "-O2", "-Mrecursive", "-Mallocatable=03", "-Mstack_arrays"]
            )

            if gpu in self.nvidia_targets:
                self.flags["FCFLAGS"].extend(
                    ["-acc=gpu", "-gpu=cc{0}".format(self.nvidia_targets[gpu])]
                )

            if self.spec.satisfies("+coupling%nvhpc@:23.9"):
                self.single_args.append("yac_cv_fc_is_contiguous_works=yes")

        else:
            self.flags["CFLAGS"].extend(["-g", "-O2"])
            self.flags["FCFLAGS"].extend(["-g", "-O2"])

    def configure_args(self) -> list[str]:
        # Populate self.single_args and self.flags
        self.set_configure_args()
        self.flags["LIBS"].append(libs.link_flags)
        # Remove duplicates while keeping the original order
        self.single_args = list(dict.fromkeys(self.single_args))
        for key, values in self.flags.items():
            self.flags[key] = list(dict.fromkeys(values))
        # Return final list
        return [
            *chain(
                self.single_args,
                (
                    "{0}={1}".format(name, " ".join(values))
                    for name, values in self.flags.items()
                ),
            )
        ]
    

class IconNwp(BaseIcon):
    """ICON - is a modeling framework for weather, climate, and environmental
    prediction.
    It solves the full three-dimensional non-hydrostatic and compressible
    Navier-Stokes equations on an icosahedral grid and allows seamless
    predictions from local to global scales.
    This is for additional options from the upstream ICON for NWP specific features."""

    homepage = "https://gitlab.dkrz.de/icon/icon-nwp"
    git = "git@gitlab.dkrz.de:icon/icon-nwp.git"
    submodules = True

    maintainers("leclairm", "stelliom", "huppd")

    version("develop", branch="master")
    version("main", branch="master")

    version("2024.10-mch-1.0", tag="icon-2024.10-mch-1.0", preferred=True)
    version("2024.01-mch-2.1", tag="icon-2024.01-mch-2.1")
    version("2024.01-mch-2.0", tag="icon-2024.01-mch-2.0")
    version("2.6.6-mch2b", tag="icon-nwp/icon-2.6.6-mch2b")
    version("2.6.6-mch2a", tag="icon-nwp/icon-2.6.6-mch2a")

    # Model Features:
    variant(
        "dace",
        default=False,
        description="Enable the DACE modules for data assimilation",
    )
    requires("+mpi", when="+dace")

    variant(
        "emvorado",
        default=False,
        description="Enable the radar forward operator EMVORADO",
    )
    requires("+mpi", when="+emvorado")

    variant(
        "art-gpl",
        default=False,
        description="Enable GPL-licensed code parts of the ART component",
    )
    variant(
        "acm-license",
        default=False,
        description="Enable code parts that require accepting the ACM Software License",
    )

    # Infrastructural Features:
    variant(
        "active-target-sync",
        default=False,
        description="Enable MPI active target mode (otherwise, passive target mode is used)",
    )
    variant(
        "async-io-rma",
        default=True,
        description="Enable remote memory access (RMA) for async I/O",
    )
    variant(
        "realloc-buf",
        default=False,
        description="Enable reallocatable communication buffer",
    )
    variant("sct", default=False, description="Enable the SCT timer")
    variant(
        "extra-config-args",
        default="none",
        multi=True,
        values=check_variant_extra_config_args,
        description="Inject any configure argument not yet available as variant\nUse this feature cautiously, as injecting non-variant configure arguments may potentially disrupt the build process",
    )

    # Optimization Features:
    variant("loop-exchange", default=False, description="Enable loop exchange")
    variant(
        "vectorized-lrtm",
        default=False,
        description="Enable the parallelization-invariant version of LRTM",
    )
    variant(
        "pgi-inlib",
        default=False,
        description="Enable PGI/NVIDIA cross-file function inlining via an inline library",
    )
    variant("nccl", default=False, description="Enable NCCL for communication")

    variant("cuda-graphs", default=False, description="Enable CUDA graphs.")
    requires("%nvhpc@23.3:", when="+cuda-graphs")

    variant(
        "fcgroup",
        default="none",
        multi=True,
        values=check_variant_fcgroup,
        description="Create a Fortran compile group: GROUP;files;flag \nNote: flag can only be one single value, i.e. -O1",
    )

    variant("nvtx", default=False, description="Enable NVTX for profiling")
    requires("%nvhpc", when="+nvtx")  # NVTX is only supported for nvhpc

    # verbosity
    variant(
        "silent-rules",
        default=True,
        description="Enable silent-rules for build-process",
    )

    variant(
        "eccodes-definitions",
        default=False,
        description="Enable extension of eccodes with center specific definition files",
    )

    variant("cuda-mempool", default=False, description="Enable cuda memory pool")
    requires("+realloc-buf", when="+cuda-mempool")

    variant("icon4py", default=False, description="Build with ICON4Py granules")
    with when("+icon4py"):
        extends("python")
        depends_on("python@3.12:")
        depends_on("cmake", type="build")

    depends_on("eccodes-cosmo-resources", type="run", when="+eccodes-definitions")

    with when("+emvorado"):
        depends_on("eccodes +fortran")
        depends_on("hdf5 +szip +hl +fortran")
        depends_on("zlib-ng")
        # WORKAROUND: A build and link dependency should imply that the same compiler is used. This enforces it.
        depends_on("eccodes %nvhpc", when="%nvhpc")
        depends_on("eccodes %gcc", when="%gcc")

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. This enforces it.
    for __x in BaseIcon.serialization_values:
        depends_on(
            "serialbox+fortran %nvhpc", when="serialization={0} %nvhpc".format(__x)
        )
        depends_on("serialbox+fortran %gcc", when="serialization={0} %gcc".format(__x))

    # WORKAROUND: A build and link dependency should imply that the same compiler is used. This enforces it.
    depends_on("netcdf-fortran %nvhpc", when="%nvhpc")
    depends_on("netcdf-fortran %gcc", when="%gcc")

    depends_on("hdf5 +szip", when="+sct")

    # patch_libtool is a function from Autotoolspackage.
    # For BB we cannot use it because it finds all files
    # named "libtool". spack-c2sm is cloned into icon-repo,
    # therefore this function detects not only "libtool" files, but
    # also the folder where libtool package itself is installed.
    patch_libtool = False

    # patches
    patch("mo_nh_stepping_null_pointer.patch", when="%fortran=nvhpc@26.1")

    # TODO: install icon4py from within the icon package recipe
    #       following a similar strategy as the icon4py package.
    #       Also make sure to point to the uv found as dependency
    #       with `uv=Executable(spec["uv"].prefix.bin.uv)` rather than
    #       uv = which("uv"), potentially leading to another location
    def setup_build_environment(self, env):
        if self.spec.satisfies("+icon4py"):
            env.set("CMAKE", join_path(self.spec["cmake"].prefix.bin, "cmake"))
            icon4py_bin_dir = f"{self.configure_directory}/externals/icon4py/.venv/bin"
            if not os.path.exists(icon4py_bin_dir):
                msg = f"icon4py bin dir not found at {icon4py_bin_dir}"
                tty.error(msg)
                raise RuntimeError(msg)
            env.prepend_path("PATH", icon4py_bin_dir)

    def set_configure_args(self) -> None:
        super().set_configure_args()

        # The base class hardcodes FCFLAGS per compiler vendor and never
        # consults self.spec.compiler_flags. On top of that, FC is forced
        # to the MPI compiler wrapper, which bypasses Spack's own
        # compiler-wrapper flag injection (SPACK_FFLAGS). Without this,
        # any `fflags=...` set on the spec (e.g. via spack.yaml) would be
        # silently dropped instead of reaching the Fortran compiler.
        self.flags["FCFLAGS"].extend(self.spec.compiler_flags["fflags"])

        for x in (
            "dace",
            "emvorado",
            "art-gpl",
            "acm-license",
            "active-target-sync",
            "async-io-rma",
            "realloc-buf",
            "parallel-netcdf",
            "sct",
            "loop-exchange",
            "vectorized-lrtm",
            "pgi-inlib",
            "nccl",
            "cuda-graphs",
            "silent-rules",
            "icon4py",
        ):
            self.single_args.extend(self.enable_or_disable(x))

        if "+emvorado" in self.spec:
            self.libs += self.spec["eccodes:fortran"].libs
            self.libs += self.spec["hdf5:fortran,hl"].libs
            self.libs += self.spec["zlib-ng"].libs

        if "+sct" in self.spec:
            self.libs += self.spec["hdf5"].libs

        if "+nvtx" in self.spec:
            self.flags["FCFLAGS"].append("-D_USE_NVTX")
            self.libs += LibraryList(["nvhpcwrapnvtx"])

        if "+icon4py" in self.spec:
            self.libs += self.spec["python"].libs

        fcgroup = self.spec.variants["fcgroup"].value
        if fcgroup != ("none",):
            # ('none',) is the values spack assigns if fcgroup is not set
            for group in fcgroup:
                name, files, flag = group.split(".")
                self.single_args.append(f"--enable-fcgroup-{name}={files}")
                self.flags[f"ICON_{name}_FCFLAGS"].append(flag)

        # add configure arguments not yet available as variant
        extra_config_args = self.spec.variants["extra-config-args"].value
        if extra_config_args != ("none",):
            for x in extra_config_args:
                # prevent configure-args already available as variant
                # to be set through variant extra_config_args
                self.validate_extra_config_args(x)
                self.single_args.append(x)
            tty.warn(
                "You use variant extra-config-args. Injecting non-variant configure arguments may potentially disrupt the build process!"
            )

        if self.spec.satisfies("+cuda-mempool"):
            self.flags["ICON_FCFLAGS"].append("-cuda")

        # Help the libtool scripts of the bundled libraries find the correct
        # paths to the external libraries. Specify the library search (-L) flags
        # in the reversed order
        # (see https://gitlab.dkrz.de/icon/icon#icon-dependencies):
        # and for non-system directories only:
        non_system_reversed_lib_dirs = [
            f"-L{d}" for d in reversed(self.libs.directories) if not is_system_path(d)
        ]
        if non_system_reversed_lib_dirs:
            self.flags["LDFLAGS"].extend(non_system_reversed_lib_dirs)

    def strip_variant_prefix(self, variant_string):
        prefixes = ["--enable-", "--disable-"]

        for prefix in prefixes:
            if variant_string.startswith(prefix):
                return variant_string[len(prefix) :]

        raise ValueError

    def validate_extra_config_args(self, arg):
        variant_from_arg = self.strip_variant_prefix(arg)
        if variant_from_arg in self.spec.variants:
            raise error.SpecError(
                f'The value "{arg}" for the extra_config_args variant conflicts '
                f"with the existing variant {variant_from_arg}. Set this variant instead."
            )

    def configure(self, spec, prefix):
        if (
            os.path.exists(os.path.join(self.build_directory, "icon.mk"))
            and self.build_uses_same_spec()
        ):
            tty.warn(
                "icon.mk already present -> skip configure stage",
                '\t delete "icon.mk" or run "make distclean" to not skip configure',
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

        previous_spec = os.path.join(self.build_directory, ".previous_spec.yaml")

        # not the first build in self.build_directory
        if os.path.exists(previous_spec):
            with open(previous_spec, mode="r") as f:
                if self.spec == Spec.from_yaml(f):
                    is_same_spec = True
                else:
                    is_same_spec = False
                    tty.warn("Cannot skip configure phase because spec changed")

        # first build in self.build_directory, no worries
        else:
            is_same_spec = False

        # dump spec of new build
        with open(previous_spec, mode="w") as f:
            f.write(self.spec.to_yaml())

        return is_same_spec

    @run_after("configure")
    def copy_runscript_related_input_files(self):
        with working_dir(self.build_directory):
            icon_dir = self.configure_directory
            # only synchronize if out-of-source build
            if os.path.abspath(icon_dir) != os.path.abspath(self.build_directory):
                Rsync = which("rsync", required=True)
                Rsync(
                    "-uavz",
                    f"{icon_dir}/run",
                    ".",
                    "--exclude=*.in",
                    "--exclude=.*",
                    "--exclude=standard_*",
                )
                Rsync(
                    "-uavz",
                    f"{icon_dir}/externals",
                    ".",
                    "--exclude=.git",
                    "--exclude=*.f90",
                    "--exclude=*.F90",
                    "--exclude=*.c",
                    "--exclude=*.h",
                    "--exclude=*.Po",
                    "--exclude=tests",
                    "--exclude=*.mod",
                    "--exclude=*.o",
                    "--exclude=externals/icon4py/.venv/",
                )
                Rsync("-uavz", f"{icon_dir}/make_runscripts", ".")

                Ln = which("ln", required=True)
                dirs = glob.glob(f"{icon_dir}/run/standard_*")
                for dir in dirs:
                    Ln("-sf", "-t", "run/", f"{dir}")
                Ln("-sf", f"{icon_dir}/data")
                Ln("-sf", f"{icon_dir}/vertical_coord_tables")
                Ln("-sf", f"{icon_dir}/scripts")
                if self.spec.satisfies("+icon4py"):
                    icon4py_base = f"{icon_dir}/externals/icon4py"
                    icon4py_target = os.path.join(
                        self.build_directory, "externals/icon4py"
                    )
                    with working_dir(icon4py_target):
                        Ln(
                            "-sf",
                            os.path.join(
                                os.path.relpath(icon4py_base, icon4py_target), ".venv"
                            ),
                        )
