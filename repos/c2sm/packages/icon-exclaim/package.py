from spack.pkg.c2sm.icon import Icon
import shutil
import os
import spack.error as error


def validate_variant_dsl(pkg, name, value):
    set_mutual_excl = set(["substitute", "verify", "serialize"])
    set_input_var = set(value)
    if len(set_mutual_excl.intersection(set_input_var)) > 1:
        raise error.SpecError(
            "Cannot have more than one of (substitute, verify, serialize) in the same build"
        )


class IconExclaim(Icon):
    git = "git@github.com:C2SM/icon-exclaim.git"

    maintainers("huppd", "leclairm", "stelliom")

    version("develop", branch="icon-dsl", submodules=True)
    version("0.3.0", commit="5c5b742a969af2bd491e26cd0a05a35838f121c4", submodules=True)

    # EXCLAIM-GT4Py specific features:
    dsl_values = ("substitute", "verify")
    variant(
        "dsl",
        default="none",
        validator=validate_variant_dsl,
        values=("none",) + dsl_values,
        description="Build with GT4Py dynamical core",
        multi=True,
    )
    variant("cuda-mempool", default=False, description="Enable cuda memory pool")

    depends_on("icon4py@0.0.15", when="@0.3.0")
    for x in dsl_values:
        depends_on("icon4py", type="build", when=f"dsl={x}")

    def configure_args(self):
        raw_args = super().configure_args()

        # Split into categories
        args_flags: list[str] = []
        icon_ldflags: list[str] = []
        icon_fcflags: list[str] = []
        ldflags: list[str] = []
        libs: list[str] = []

        for a in raw_args:
            if a.startswith("LIBS="):
                libs.append(a.split("=", 1)[1].strip())
            elif a.startswith("ICON_LDFLAGS="):
                icon_ldflags.append(a.split("=", 1)[1].strip())
            elif a.startswith("ICON_FCFLAGS="):
                icon_fcflags.append(a.split("=", 1)[1].strip())
            elif a.startswith("LDFLAGS="):
                ldflags.append(a.split("=", 1)[1].strip())
            else:
                args_flags.append(a)

        # Handle DSL variants
        dsl = self.spec.variants["dsl"].value
        if dsl != ("none",):
            if "substitute" in dsl:
                args_flags.append("--enable-py2f=substitute")
            elif "verify" in dsl:
                args_flags.append("--enable-py2f=verify")
            else:
                raise ValueError(
                    f"Unknown DSL variant '{dsl}'. "
                    f"Valid options are: {', '.join(('none',) + self.dsl_values)}"
                )

            # Add icon4py paths and libs
            icon4py_prefix = self.spec["icon4py"].prefix
            bindings_dir = os.path.join(icon4py_prefix, "src")

            ldflags.append(f"-L{bindings_dir} -Wl,-rpath,{bindings_dir}")
            libs.append("-licon4py_bindings")

        # enable cuda memory pool
        if self.spec.satisfies("+cuda-mempool"):
            icon_fcflags.append("-cuda")

        # Remove duplicates
        icon_ldflags = list(set(icon_ldflags))
        ldflags = list(set(ldflags))
        libs = list(set(libs))

        # Reconstruct final configure args
        final_args = args_flags
        if icon_ldflags:
            final_args.append("ICON_LDFLAGS=" + " ".join(icon_ldflags))
        if ldflags:
            final_args.append("LDFLAGS=" + " ".join(ldflags))
        if icon_fcflags:
            final_args.append("ICON_FCFLAGS=" + " ".join(icon_fcflags))
        if libs:
            final_args.append("LIBS=" + " ".join(libs))

        return final_args

    def build(self, spec, prefix):
        # Check the variant
        dsl = self.spec.variants["dsl"].value
        if dsl != ("none",):
            file = "icon4py_bindings.f90"

            bindings_dir = os.path.join(self.spec["icon4py"].prefix, "src")
            src_file = os.path.join(bindings_dir, file)

            build_py2f_dir = os.path.join(self.stage.source_path, "src", "build_py2f")
            os.makedirs(build_py2f_dir, exist_ok=True)
            dest_file = os.path.join(build_py2f_dir, file)

            shutil.copy2(src_file, dest_file)
            print(
                f"Copied {src_file} to build directory {dest_file} because +dsl is enabled"
            )

        # Proceed with the normal build
        super().build(spec, prefix)
