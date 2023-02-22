from spack.package import *
from spack.pkg.builtin.py_poetry_core import PyPoetryCore as SpackPyPoetryCore


class PyPoetryCore(SpackPyPoetryCore):
    """Poetry PEP 517 Build Backend."""

    # https://github.com/python-poetry/poetry/issues/5547
    def setup_build_environment(self, env):
        env.set("GIT_DIR", join_path(self.stage.source_path, ".git"))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("GIT_DIR", join_path(dependent_spec.package.stage.source_path, ".git"))
