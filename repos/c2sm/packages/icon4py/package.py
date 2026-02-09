import json
import os
import pathlib

from spack.package import *
from spack_repo.builtin.build_systems.generic import Package


class Icon4py(Package):
    """ICON4Py Python interface package."""

    homepage = "https://github.com/C2SM/icon4py"
    git = "https://github.com/C2SM/icon4py.git"

    # --- Versions ---
    version("main", branch="main")

    def url_for_version(self, version):
        return f"https://github.com/C2SM/icon4py/archive/refs/tags/v{version}.zip"

    # --- Variants ---
    variant("cuda", default=True, description="Enable CUDA support")
    variant(
        "cuda_arch",
        default="none",
        description="CUDA architecture (e.g. 80 for A100, 90 for H100)",
        values=lambda x: True,  # accept any user-specified string
    )

    # --- Dependencies ---
    extends("python")
    depends_on("python@3.11:3.12")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("git")
    depends_on("uv@0.7:", type="build")
    depends_on("bzip2", type="build")
    depends_on("py-numpy")
    depends_on("py-cffi")
    depends_on("py-pybind11")
    depends_on("py-nanobind")
    depends_on("py-mpi4py")

    with when("+cuda"):
        depends_on("py-cupy +cuda")
        depends_on("ghex +python +cuda")

    with when("~cuda"):
        depends_on("ghex +python ~cuda")

    # --- Environment setup ---
    def setup_build_environment(self, env):
        """Propagate CUDA architecture to dependencies."""
        cuda_arch = self.spec.variants["cuda_arch"].value
        if "+cuda" in self.spec:
            if cuda_arch == "none":
                tty.warn(
                    "Building with +cuda but no cuda_arch set. "
                    "Consider specifying e.g. cuda_arch=80 or cuda_arch=90.")
            else:
                env.set("SPACK_CUDA_ARCH", cuda_arch)
                tty.msg(f"Building for CUDA architecture: {cuda_arch}")

    # --- Build/install logic ---
    def install(self, spec, prefix):
        uv = prepare_uv()
        python_spec = spec["python"]
        venv_path = prefix.share.venv

        tty.msg(
            f"Creating venv using Spack Python at: {python_spec.command.path}")
        uv(
            "venv",
            "--seed",
            "--relocatable",
            "--system-site-packages",
            str(venv_path),
            "--python",
            python_spec.command.path,
        )

        tty.msg("Grabbing Spack-installed packages (distributions)")
        pip = Executable(venv_path.bin.pip)
        spack_installed = get_installed_pkg(pip)
        tty.msg(f"Found spack_installed packages: {spack_installed}")

        # --- Handle CUDA vs non-CUDA extras ---
        extras = ["all"]
        no_install = [*spack_installed, "ghex"]

        if "+cuda" in spec:
            extras.append("cuda12")
            no_install.append("cupy-cuda12x")

        tty.msg("Installing missing packages via uv sync")
        uv(
            "sync",
            "--active",
            *sum([["--extra", e] for e in extras], []),
            "--inexact",
            "--no-editable",
            "--python",
            str(venv_path.bin.python),
            *no_install_options(no_install),
            extra_env={
                "VIRTUAL_ENV": str(venv_path),
                "CC": self.compiler.cc,
                "CXX": self.compiler.cxx,
            },
        )

        tty.msg("Linking Spack-installed packages into venv")
        pathlib.Path(
            f"{venv_path.lib.python}{python_spec.version.up_to(2)}/site-packages/spack_installed.pth"
        ).write_text(pythonpath_to_pth())

        tty.msg("Running py2fgen code generator")
        py2fgen = Executable(venv_path.bin.py2fgen)
        py2fgen(
            "icon4py.tools.py2fgen.wrappers.all_bindings",
            "diffusion_init,diffusion_run,grid_init,solve_nh_init,solve_nh_run",
            "icon4py_bindings",
            "-o",
            prefix.src,
            extra_env={
                "VIRTUAL_ENV": str(venv_path),
                "CC": self.compiler.cc,
                "CXX": self.compiler.cxx,
            },
        )


def prepare_uv():
    uv = which("uv")
    uv.add_default_env("UV_NO_CACHE", "true")
    uv.add_default_env("UV_NO_MANAGED_PYTHON", "true")
    uv.add_default_env("UV_PYTHON_DOWNLOADS", "never")
    return uv


def get_installed_pkg(pip):
    return [
        item["name"]
        for item in json.loads(pip("list", "--format", "json", output=str))
    ]


def no_install_options(installed):
    for name in installed:
        yield "--no-install-package"
        yield name


def pythonpath_to_pth():
    return "\n".join(os.environ.get("PYTHONPATH", "").split(":"))
