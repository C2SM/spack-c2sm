"""Exercise the DACE fetch hook with Spack and local, executable fetch scripts."""

from pathlib import Path

import pytest
import spack.repo
from spack.spec import Spec
from spack.util.executable import ProcessError


@pytest.fixture(params=[False, True], ids=["in-source", "out-of-source"])
def package(request, tmp_path, monkeypatch):
    package_cls = spack.repo.PATH.get_pkg_class("c2sm.icon-nwp")
    pkg = package_cls(Spec("icon-nwp +dace"))
    source = tmp_path / "source"
    source.mkdir()
    build = tmp_path / "build" if request.param else source
    build.mkdir(exist_ok=True)
    pkg.configure_directory = str(source)
    pkg.build_directory = str(build)
    # Configure may be invoked from a directory other than the source tree.
    monkeypatch.chdir(build)
    return pkg


def write_fetch(package, body):
    dace = Path(package.configure_directory) / "externals" / "dace"
    dace.mkdir(parents=True, exist_ok=True)
    script = dace / "fetch.sh"
    script.write_text("#!/bin/sh\nset -eu\n" + body + "\n")
    script.chmod(0o755)
    return dace


def test_fetch_and_repeat(package, monkeypatch):
    monkeypatch.setenv("DACE_TEST_VALUE", "inherited")
    dace = write_fetch(
        package,
        'mkdir src\nprintf "%s" "$DACE_TEST_VALUE" > src/renamed-source.f90',
    )
    package.fetch_dace_sources()
    assert (dace / "src/renamed-source.f90").read_text() == "inherited"
    assert not (dace / ".spack-fetch-in-progress").exists()
    # A second invocation would fail at mkdir if it tried fetching again.
    package.fetch_dace_sources()
    assert Path.cwd() == Path(package.build_directory)
    if package.build_directory != package.configure_directory:
        assert not (Path(package.build_directory) / "externals").exists()


def test_disabled_dace(package):
    dace = write_fetch(package, "exit 99")
    package.spec = Spec("icon-nwp ~dace")
    package.fetch_dace_sources()
    assert {p.name for p in dace.iterdir()} == {"fetch.sh"}


@pytest.mark.parametrize("with_fetch", [False, True])
def test_existing_checkout(package, with_fetch):
    dace = write_fetch(package, "exit 99")
    (dace / "some-other-source.f90").write_text("preserve me")
    if not with_fetch:
        (dace / "fetch.sh").unlink()
    package.fetch_dace_sources()
    assert (dace / "some-other-source.f90").read_text() == "preserve me"
    assert not (dace / ".spack-fetch-in-progress").exists()


def test_absent_dace_directory(package):
    package.fetch_dace_sources()


def test_retry_failed_fetch(package, tmp_path):
    dace = write_fetch(package, "mkdir partial\ntouch partial/incomplete\nexit 1")
    with pytest.raises(ProcessError):
        package.fetch_dace_sources()
    assert (dace / ".spack-fetch-in-progress").is_file()
    assert Path.cwd() == Path(package.build_directory)

    # Retry must remove partial output, including links without touching targets.
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "keep").write_text("untouched")
    (dace / "link").symlink_to(outside, target_is_directory=True)
    write_fetch(
        package, "test ! -e partial\ntest ! -L link\nmkdir src\ntouch src/new.f90"
    )
    package.fetch_dace_sources()
    assert (dace / "src/new.f90").is_file()
    assert (outside / "keep").read_text() == "untouched"
    assert not (dace / ".spack-fetch-in-progress").exists()


def test_success_without_sources_can_be_retried(package):
    dace = write_fetch(package, "exit 0")
    with pytest.raises(RuntimeError, match="empty tree"):
        package.fetch_dace_sources()
    assert (dace / ".spack-fetch-in-progress").is_file()
    write_fetch(package, "mkdir src\ntouch src/new.f90")
    package.fetch_dace_sources()
    assert (dace / "src/new.f90").is_file()
    assert not (dace / ".spack-fetch-in-progress").exists()
