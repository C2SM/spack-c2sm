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

def git_config():
    git_config_count = os.getenv('GIT_CONFIG_COUNT')
    if git_config_count is None:
        return

    try:
        git_config_count = int(git_config_count)
    except ValueError:
        return

    var_export = []
    for i in range(git_config_count):
        key_var = f'GIT_CONFIG_KEY_{i}'
        value_var = f'GIT_CONFIG_VALUE_{i}'

        key = os.getenv(key_var)
        value = os.getenv(value_var)

        if key is None or value is None:
            continue

        var_export.append(f'export {key_var}="{key}"')
        var_export.append(f' export {value_var}="{value}"')
    return ";".join(var_export)

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
        f'env -i bash -l -c "(. {REPO_DIR}/setup-env.sh {uenv}; {git_config()}; {command}) >> {log} 2>&1"',
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
    run_with_spack(f"spack -dd install --verbose {test_arg} {spec}", log)
