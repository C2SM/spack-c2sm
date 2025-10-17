from spack.package import *


def translate_platform(platform_name: str) -> str:
    if platform_name == "darwin":
        return "apple-darwin"
    elif platform_name == "linux":
        return "unknown-linux-gnu"
    return platform_name


def translate_arch(arch_name: str) -> str:
    if arch_name in ["m1", "m2", "neoverse_v2"]:
        return "aarch64"
    if arch_name in ["zen3"]:
        return "x86_64"
    return arch_name


class Uv(Package):
    """Install UV from binary releases"""

    url = "https://github.com/astral-sh/uv/releases/download/0.7.12/uv-aarch64-apple-darwin.tar.gz"

    version(
        "0.7.12",
        sha256=
        "189108cd026c25d40fb086eaaf320aac52c3f7aab63e185bac51305a1576fc7e",
        extension=".tar.gz",
    )
    version(
        "0.7.20",
        sha256=
        "675165f879d6833aa313ecb25ac44781e131933a984727e180b3218d2cd6c1e9",
        extension=".tar.gz",
    )

    def url_for_version(self, version):
        arch = translate_arch(self.spec.target)
        platform = translate_platform(self.spec.platform)
        return f"https://github.com/astral-sh/uv/releases/download/{version}/uv-{arch}-{platform}.tar.gz"

    def do_stage(self, mirror_only=False):
        checksums = {
            ("0.7.12", "apple-darwin", "aarch64"):
            ("189108cd026c25d40fb086eaaf320aac52c3f7aab63e185bac51305a1576fc7e"
             ),
            ("0.7.20", "unknown-linux-gnu", "aarch64"):
            ("675165f879d6833aa313ecb25ac44781e131933a984727e180b3218d2cd6c1e9"
             ),
            ("0.7.20", "unknown-linux-gnu", "x86_64"):
            ("10f204426ff188925d22a53c1d0310d190a8d4d24513712e1b8e2ca9873f0666"
             ),
        }
        version = str(self.spec.version)
        arch = translate_arch(self.spec.target)
        platform = translate_platform(self.spec.platform)
        key = (version, platform, arch)

        if key not in checksums:
            msg = f"Unsupported platform/arch for version {version}: {platform}-{arch}."
            raise InstallError(msg)

        self.fetcher.digest = checksums[key]
        super().do_stage(mirror_only)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("uv", prefix.bin.uv)
        install("uvx", prefix.bin.uvx)
