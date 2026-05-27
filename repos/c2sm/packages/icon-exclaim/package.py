import shutil
import os

import spack.error as error
from spack.package import *

from spack.pkg.c2sm.icon_nwp import IconNwp


def validate_variant_dsl(pkg, name, value):
    set_mutual_excl = set(["substitute", "verify", "serialize"])
    set_input_var = set(value)
    if len(set_mutual_excl.intersection(set_input_var)) > 1:
        raise error.SpecError(
            "Cannot have more than one of (substitute, verify, serialize) in the same build"
        )


class IconExclaim(IconNwp):
    """ICON - is a modeling framework for weather, climate, and environmental
    prediction.
    It solves the full three-dimensional non-hydrostatic and compressible
    Navier-Stokes equations on an icosahedral grid and allows seamless
    predictions from local to global scales.
    This is for additional options from the upstream ICON-NWP for exclaime
    specific features."""

    git = "git@github.com:C2SM/icon-exclaim.git"

    maintainers("leclairm", "stelliom", "huppd")

    version("develop", branch="icon-dsl", submodules=True)
    version("0.3.0", commit="a0be2c3e0448ec2dc92024e3b38ec635435ac0dd", submodules=True)

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

    def setup_build_environment(self, env):
        if self.spec.variants['dsl'].value != ('none', ):
            tty.msg(f"adding {self.spec['icon4py'].prefix.share.venv.bin} to PATH for icon4py bindings because +dsl is enabled")
            env.prepend_path("PATH", self.spec["icon4py"].prefix.share.venv.bin)

    def set_configure_args(self) -> None:
        super().set_configure_args()

        # Handle DSL variants
        dsl = self.spec.variants["dsl"].value
        if dsl != ("none",):
            if "substitute" in dsl:
                self.icon_configure_args.args.append("--enable-icon4py=substitute")
            elif "verify" in dsl:
                self.icon_configure_args.args.append("--enable-icon4py=verify")
            else:
                raise ValueError(
                    f"Unknown DSL variant '{dsl}'. "
                    f"Valid options are: {', '.join(('none',) + self.dsl_values)}"
                )

            # Add icon4py paths and libs 
            bindings_dir = os.path.join(self.spec["icon4py"].prefix, "src")
            self.icon_configure_args.flags["LDFLAGS"].append(f"-L{bindings_dir} -Wl,-rpath,{bindings_dir}")
            self.icon_configure_args.flags["LIBS"].append("-licon4py_bindings")

        # enable cuda memory pool
        if self.spec.satisfies("+cuda-mempool"):
            self.icon_configure_args.flags["ICON_FCFLAGS"].append("-cuda")
