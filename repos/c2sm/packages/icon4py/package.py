import json
import os
import pathlib

import llnl
from llnl.util import tty
from spack import *


class Icon4py(Package):
    extends("python")
    depends_on("python@3.11:")

    depends_on("git")
    depends_on("boost@1.85:+mpi+python", type=("build", "run"))
    depends_on("uv@0.7:", type="build")
    depends_on("bzip2", type="build")
    depends_on("py-numpy")
    depends_on("py-cffi")
    depends_on("py-pybind11")
    depends_on("py-nanobind")
    depends_on("py-mpi4py")
    depends_on("py-cupy +cuda")
    depends_on("ghex +python +cuda")

    version(
        "icon_20250328",
        sha256=
        "8573ef031d207438f549511e859f522c60163ea660aafea93ef4991b9010739a",
        extension="zip",
    )

    def url_for_version(self, version):
        return f"https://github.com/c2sm/icon4py/archive/refs/heads/{version}.zip"

    def install(self, spec, prefix):
        uv = prepare_uv()
        python_spec = spec["python"]
        venv_path = prefix.share.venv

        tty.msg(
            f"creating venv using spack python at: {python_spec.command.path}")
        uv(
            "venv",
            "--seed",
            "--relocatable",
            "--system-site-packages",
            str(venv_path),
            "--python",
            python_spec.command.path,
        )

        tty.msg(f"grabbing spack installed packages (distributions)")
        pip = Executable(venv_path.bin.pip)
        spack_installed = get_installed_pkg(pip)

        tty.msg(f"installing missing packages")
        uv(
            "sync",
            "--active",
            "--extra",
            "all",
            "--extra",
            "cuda12",
            "--inexact",
            "--no-editable",
            "--python",
            str(venv_path.bin.python),
            *no_install_options([*spack_installed, "cupy-cuda12x", "ghex"]),
            extra_env={"VIRTUAL_ENV": str(venv_path)},
        )

        tty.msg(f"linking spack installed packages into venv")
        pathlib.Path(
            f"{venv_path.lib.python}{python_spec.version.up_to(2)}/site-packages/spack_installed.pth"
        ).write_text(pythonpath_to_pth())

        tty.msg(f"running py2fgen")
        py2fgen = Executable(venv_path.bin.py2fgen)
        py2fgen(
            "icon4py.tools.py2fgen.wrappers.all_bindings",
            "diffusion_init,diffusion_run,grid_init,solve_nh_init,solve_nh_run",
            "icon4py_bindings",
            "-o",
            prefix.src,
            extra_env={"VIRTUAL_ENV": str(venv_path)},
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
    return "\n".join(os.environ["PYTHONPATH"].split(":"))
