from spack.package import *


class Oomph(CMakePackage, CudaPackage, ROCmPackage):
    """Oomph is a non-blocking callback-based point-to-point communication library."""

    homepage = "https://github.com/ghex-org/oomph"
    url = "https://github.com/ghex-org/oomph/archive/refs/tags/v0.2.0.tar.gz"
    git = "https://github.com/ghex-org/oomph.git"
    maintainers = ["boeschf"]

    version("0.4.0", sha256="e342c872dfe4832be047f172dc55c12951950c79da2630b071c61607ef913144")
    version("0.3.0", sha256="61e346d1ba28a859745de47f37edce39c7f5c5e1aab716493dc964e158fd99ec")
    version("0.2.0", sha256="135cdb856aa817c053b6af1617869dbcd0ee97d34607e78874dd775ea389434e")
    version("0.1.0", sha256="0ff36db0a5f30ae1bb02f6db6d411ea72eadd89688c00f76b4e722bd5a9ba90b")
    version("main", branch="main")

    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran-bindings")

    generator("ninja")

    backends = ("mpi", "ucx", "libfabric")
    variant(
        "backend", default="mpi", description="Transport backend", values=backends, multi=False
    )

    variant("fortran-bindings", default=False, description="Build Fortran bindings")
    with when("+fortran-bindings"):
        variant(
            "fortran-fp",
            default="float",
            description="Floating point type",
            values=("float", "double"),
            multi=False,
        )
        variant("fortran-openmp", default=True, description="Compile with OpenMP")

    variant(
        "enable-barrier",
        default=True,
        description="Enable thread barrier (disable for task based runtime)",
    )

    depends_on("hwmalloc+cuda", when="+cuda")
    depends_on("hwmalloc+rocm", when="+rocm")
    depends_on("hwmalloc", when="~cuda~rocm")

    with when("backend=ucx"):
        depends_on("ucx+thread_multiple")
        depends_on("ucx+cuda", when="+cuda")
        depends_on("ucx+rocm", when="+rocm")
        variant("use-pmix", default="False", description="Use PMIx to establish out-of-band setup")
        variant("use-spin-lock", default="False", description="Use pthread spin locks")
        depends_on("pmix", when="+use-pmix")

    libfabric_providers = ("cxi", "efa", "gni", "psm2", "tcp", "verbs")
    with when("backend=libfabric"):
        variant(
            "libfabric-provider",
            default="tcp",
            description="fabric",
            values=libfabric_providers,
            multi=False,
        )
        for provider in libfabric_providers:
            depends_on(f"libfabric fabrics={provider}", when=f"libfabric-provider={provider}")

    depends_on("mpi")
    depends_on("boost+thread")

    depends_on("googletest", type=("build","test"))

    patch("install_0.2.patch", when="@:0.2.0", level=1)
    patch("install_0.3.patch", when="@0.3.0", level=1)

    def cmake_args(self):
        args = [
            self.define_from_variant("OOMPH_BUILD_FORTRAN", "fortran-bindings"),
            self.define_from_variant("OOMPH_FORTRAN_OPENMP", "fortran-openmp"),
            self.define_from_variant("OOMPH_UCX_USE_PMI", "use-pmix"),
            self.define_from_variant("OOMPH_UCX_USE_SPIN_LOCK", "use-spin-lock"),
            self.define_from_variant("OOMPH_ENABLE_BARRIER", "enable-barrier"),
            self.define("OOMPH_WITH_TESTING", self.run_tests),
            self.define("OOMPH_GIT_SUBMODULE", False),
            self.define("OOMPH_USE_BUNDLED_LIBS", False),
        ]

        if self.run_tests and self.spec.satisfies("^openmpi"):
            args.append(self.define("MPIEXEC_PREFLAGS", "--oversubscribe"))

        if self.spec.variants["fortran-bindings"].value == True:
            args.append(self.define("OOMPH_FORTRAN_FP", self.spec.variants["fortran-fp"].value))

        for backend in self.backends:
            args.append(
                self.define(
                    f"OOMPH_WITH_{backend.upper()}", self.spec.variants["backend"].value == backend
                )
            )

        if self.spec.satisfies("backend=libfabric"):
            args.append(
                self.define(
                    "OOMPH_LIBFABRIC_PROVIDER", self.spec.variants["libfabric-provider"].value
                )
            )

        return args
