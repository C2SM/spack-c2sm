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

    url = "https://github.com/astral-sh/uv/releases/download/0.0.0/uv-ARCH-PLATFORM.tar.gz"

    version("0.7.12", sha256="dummy")
    version("0.7.20", sha256="dummy")
    version("0.9.3", sha256="dummy")
    version("0.9.4", sha256="dummy")

    # Platform-specific checksums
    checksums = {
        ("0.7.12", "apple-darwin", "aarch64"): "189108cd026c25d40fb086eaaf320aac52c3f7aab63e185bac51305a1576fc7e",
        ("0.7.12", "unknown-linux-gnu", "aarch64"): "23233d2e950ed8187858350da5c6803b14cbbeaef780382093bb2f2bc4ba1200",
        ("0.7.20", "unknown-linux-gnu", "aarch64"): "675165f879d6833aa313ecb25ac44781e131933a984727e180b3218d2cd6c1e9",
        ("0.7.20", "unknown-linux-gnu", "x86_64"): "10f204426ff188925d22a53c1d0310d190a8d4d24513712e1b8e2ca9873f0666",
        ("0.9.3", "unknown-linux-gnu", "aarch64"): "2094a3ead5a026a2f6894c4d3f71026129c8878939a57f17f0c8246a737bed1d",
        ("0.9.3", "unknown-linux-gnu", "x86_64"): "4d6f84490da4b21bb6075ffc1c6b22e0cf37bc98d7cca8aff9fbb759093cdc23",
        ("0.9.4", "unknown-linux-gnu", "aarch64"): "c507e8cc4df18ed16533364013d93c2ace2c7f81a2a0d892a0dc833915b02e8b",
        ("0.9.4", "unknown-linux-gnu", "x86_64"): "e02f7fc102d6a1ebfa3b260b788e9adf35802be28c8d85640e83246e61519c1e",
    }

    def url_for_version(self, version):
        arch = translate_arch(self.spec.target)
        platform = translate_platform(self.spec.platform)
        return f"https://github.com/astral-sh/uv/releases/download/{version}/uv-{arch}-{platform}.tar.gz"

    def do_stage(self, mirror_only=False):
        version = str(self.spec.version)
        arch = translate_arch(self.spec.target)
        platform = translate_platform(self.spec.platform)
        key = (version, platform, arch)

        if key not in self.checksums:
            raise InstallError(f"Unsupported platform/arch for version {version}: {platform}-{arch}.")

        # Override fetcher digest with the correct checksum
        self.fetcher.digest = self.checksums[key]
        super().do_stage(mirror_only)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("uv", prefix.bin.uv)
        install("uvx", prefix.bin.uvx)
