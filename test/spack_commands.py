import os
import subprocess
import time
from pathlib import Path

REPO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PACKAGES_DIR = os.path.join(REPO_DIR, "repos", "c2sm", "packages")
ALL_PACKAGES = [
    name for name in os.listdir(PACKAGES_DIR)
    if os.path.isdir(os.path.join(PACKAGES_DIR, name))
]


def time_format(seconds) -> str:
    "Returns a string formatted as 'XXh YYm ZZ.ZZs'."

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h:
        parts.append(f"{h:.0f}h")
    if m:
        parts.append(f"{m:.0f}m")
    if s:
        parts.append(f"{s:.2f}s")
    return " ".join(parts)


def log_file(command: str) -> Path:
    # Filter out flags
    # and join by underscore, because spaces cause problems in bash.
    command = "_".join([x for x in command.split() if not x.startswith("-")])

    # Remove % because they cause problems in web browsers
    command = command.replace("%", "")

    # Remove . because they cause problems in shell commands
    command = command.replace("%", "")

    return Path(REPO_DIR) / "log" / (command + ".log")


def run_with_spack(command: str, log: Path) -> None:
    log.parent.mkdir(exist_ok=True, parents=True)
    with log.open("a") as f:
        f.write(f"{command}\n\n")

    # setup-env.sh may define SPACK_UENV_PATH.
    if "SPACK_UENV_PATH" in os.environ:
        uenv = os.environ["SPACK_UENV_PATH"]
    else:
        uenv = ""

    start = time.time()
    # Direct stream to avoid buffering.
    # 'env -i' clears the environment.
    # 'bash -l' makes it a login shell.
    # 'bash -c' reads commands from string.
    # '2>&1' redirects stderr to stdout.
    ret = subprocess.run(
        f'env -i bash -l -c "(. {REPO_DIR}/setup-env.sh {uenv}; {command}) >> {log} 2>&1"',
        check=False,
        shell=True,
    )
    end = time.time()

    # Log time and success
    duration = time_format(end - start)
    success = "OK" if ret.returncode == 0 else "FAILED"
    with log.open("a") as f:
        f.write(f"\n\n{duration}\n{success}\n")

    ret.check_returncode()


def spack_info(spec: str):
    log = log_file(f"info {spec}")
    run_with_spack(f"spack info {spec}", log)


def spack_spec(spec: str):
    log = log_file(f"spec {spec}")
    run_with_spack(f"spack spec {spec}", log)


def spack_install(spec: str, test_root: bool = True):
    log = log_file(f"install {spec}")

    # A spec at the top of a log helps debugging.
    run_with_spack(f"spack spec {spec}", log)

    test_arg = "--test=root" if test_root else ""
    run_with_spack(f"spack install --verbose {test_arg} {spec}", log)
