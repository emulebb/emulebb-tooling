# Downloads And Platforms

Use the [newest dated nightly prerelease](https://github.com/emulebb/emulebb-rust/releases)
for current public beta testing. Choose your operating system and CPU, then
download a runnable package rather than a manifest or source archive. Rust or a
compiler is not required to use the native packages.

**Active beta.** Beta 3 is the next development target, without a release date.
See [first launch](GUIDE-GETTING-STARTED.md) before starting the daemon, and the
[release scope](../RELEASE-SCOPE.md) for the current holds and compatibility rules.

## Choose A Native Package

The filenames below are suffixes following `emulebb-rust-v<VERSION>`. `x64`,
`x86_64` and `amd64` refer to the same CPU family; `ARM64` and `aarch64` refer to
the other native family. Match the package to the system running the daemon,
which can differ from the computer displaying its browser console.

| System | CPU | Runnable package |
| --- | --- | --- |
| Windows | x64 / ARM64 | `-windows-x64.zip` / `-windows-arm64.zip` |
| Linux, package-managed | x64 / ARM64 | `-linux-amd64.deb` / `-linux-arm64.deb` |
| Linux, portable GNU | x64 / ARM64 | `-linux-x86_64.AppImage` / `-linux-aarch64.AppImage` |
| Linux, static musl | x64 / ARM64 | `-linux-amd64-musl.tar.zst` / `-linux-arm64-musl.tar.zst` |
| macOS | Intel / Apple Silicon | `-macos-x64.dmg` / `-macos-arm64.dmg` |

**Windows:** extract the complete ZIP into a writable application directory.
Keep `webui` beside `emulebb-rust.exe`, then run the executable. The hosted runner
version is not an established oldest supported Windows version.

**Linux DEB:** install the matching file through the host package manager, for
example `sudo apt install ./<downloaded-file>.deb`. Use its desktop launcher,
or run `emulebb-rust --profile "$HOME/.config/emulebb-rust"` for an explicit
writable CLI profile. The daemon itself defaults to its executable directory
and never silently falls back from a read-only installation.
The dated nightly below declares `libc6 (>= 2.38)`, `libgcc-s1 (>= 4.2)` and
`ca-certificates`. Inspect the chosen build's package dependencies; these are not
a promise that every Debian/Ubuntu release can run it.

**Linux AppImage:** mark the matching file executable and run it. This packages
the GNU daemon; it is not libc-independent. Host kernel, library and AppImage
runtime/FUSE compatibility still matter. An exact oldest distribution or FUSE
requirement has not been established here.

**Linux musl:** use a tar/zstd-capable extractor, enter the extracted
`emulebb-rust` directory and run `./emulebb-rust`, keeping adjacent `webui` files.
A compatible CPU/kernel and system CA certificates are still needed. No exact
oldest kernel or minimum RAM/storage guarantee is established. A Linux musl
binary is not an Android binary.

**macOS:** open the matching DMG and copy the app to a writable installation
location. The app is unsigned and not notarized; follow the normal macOS
Privacy & Security approval flow. Launching the app starts the daemon/browser
console; quitting stops it. The package declares macOS 12.0, while the retained
native smoke below ran on macOS 15. Treat those as different facts. GUI users
can recover the API key from their private profile bootstrap file.

## Containers

Pull runnable images from
[`ghcr.io/emulebb/emulebb-rust`](https://github.com/emulebb/emulebb-rust/pkgs/container/emulebb-rust).
Both Ubuntu and Alpine variants publish Linux `amd64` and `arm64` manifests.

| Tag | Meaning |
| --- | --- |
| `<VERSION>-ubuntu`, `<VERSION>` | Versioned Ubuntu variant; Ubuntu is the default |
| `<VERSION>-alpine` | Versioned Alpine variant |
| `nightly-ubuntu`, `nightly` | Moving nightly Ubuntu aliases |
| `nightly-alpine` | Moving nightly Alpine alias |

There is no published `latest` alias. Use a verified `@sha256:<digest>` reference
for an exact deployment; moving nightly tags can change. An `.oci.tar.manifest.json`
release attachment is publication evidence, not a runnable container archive.

A container engine must support the selected CPU. Provide writable `/config`
and `/data` mounts, configure `PUID`/`PGID` as appropriate for their ownership,
and keep persistent state when replacing the container. The s6 image places the
implicit profile at `/config/emulebb-rust` and completed downloads at `/data/ed2k`.

For local control, bind host REST port 20017 to loopback. The daemon speaks plain
HTTP; remote TLS belongs at a trusted reverse proxy. Restrict access and keep the
API key private. P2P TCP/UDP routing and reachability need their own deliberate
container/network configuration; opening REST does not open P2P ports.
The [optional Gluetun example](https://github.com/emulebb/emulebb-rust/blob/main/packaging/docker/compose.gluetun.example.yaml)
is an advanced deployment reference, not a requirement or general VPN-safety proof.

## Experimental Android Developer Bundles

`-android-arm64-v8a.tar.zst` and `-android-x86_64.tar.zst` contain native CLI
developer builds targeting API 28+ with 16KB-compatible ELF alignment. Follow the
bundled developer README/launcher for controlled ADB work.

These remain **experimental native CLI developer bundles**. Compilation/test
linking and ELF audit cover the selected archive; its compile/ELF report does not
claim runtime execution. Separately, an API 37/x86_64/16 KiB KVM emulator
[run](https://github.com/emulebb/emulebb-build/actions/runs/43369243640)
using a source-built release-mode daemon on the development channel from
[Rust source `6429b952`](https://github.com/emulebb/emulebb-rust/commit/6429b952eac6f19ee9bf084d3a84d5649dfba0c2)
verified six TLS cases, fresh EXE-directory profile creation from a different
working directory, authenticated REST startup and graceful shutdown.

Published Android archive execution, physical devices, ARM runtime, APK/JNI,
WebUI, completed-file delivery, transfers and VPN behavior remain unqualified.
APK signing and app-store installation are separate work.

## What Each Supporting File Does

| Asset family | Purpose |
| --- | --- |
| ZIP, DEB, AppImage, DMG, musl tar/zstd | Runnable native packages |
| Android tar/zstd | Experimental CLI developer packages |
| `SHA256SUMS` | Compare downloaded bytes before launch |
| `*.manifest.json` | Package version/source/CPU, payload hashes or OCI publication metadata |
| `*-candidate-manifest.json` | Whole candidate inventory and source/evidence binding |
| `*.sbom.spdx.json` | Component/license inventory |
| `*-package-smoke-*.json` | Exact-source native execution scope and results |
| `*-compile-elf.json` | Android compile/ELF evidence, not runtime proof |
| `*-security.json`, `*.vulnerabilities.txt`, `*-scanner.txt` | Image policy results and scanner identity |
| `*-security-SHA256SUMS`, `*.oci.digest` | Image evidence checksums and published digests |
| Release notes | Changes, provenance context and profile/schema warnings |
| GitHub Source code ZIP/tar.gz | Source snapshots; not runnable client packages |

GitHub provenance attestations bind subjects to workflow/source identity. They
are separate from ordinary release downloads. Native packages can be unsigned
while their build provenance is attested. A checksum alone verifies byte equality,
not the identity or trustworthiness of its publisher.

Download `SHA256SUMS` from the same release as your package. In PowerShell,
`Get-FileHash -Algorithm SHA256 -LiteralPath <downloaded-file>` prints the hash;
compare it to the exact filename's entry. On Linux, `sha256sum <downloaded-file>`
provides the corresponding comparison; on macOS use `shasum -a 256 <downloaded-file>`.
Do not launch a file whose hash differs. Advanced users can verify published
attestations with `gh attestation verify <downloaded-file> --repo emulebb/emulebb-rust`.

## Dated Proof, Not A Blanket Support Claim

Published nightly
[`0.1.0-beta.2.nightly.20261110.g78f74541`](https://github.com/emulebb/emulebb-rust/releases/tag/rust-v0.1.0-beta.2.nightly.20261110.g78f74541)
binds product and workflow source `78f74541ad9985ccc5cfe6987e1c2e3b41134249`.
[Run 42761216405, attempt 2](https://github.com/emulebb/emulebb-rust/actions/runs/42761216405/attempts/2)
completed 31 jobs and published 81 assets, including the experimental Android
bundles. GitHub's automatic source archives are additional, separate files.

Eight native/musl package reports cover startup, API/WebUI assets, a synthetic
local transfer, partial restart and shutdown on their native hosted CPU/OS.
Public discovery was disabled for those local tests. Rendered-browser proof is
recorded for Windows x64; asset checks on other platforms are not equivalent.
Native OCI smoke/security evidence covers Ubuntu/Alpine on both CPUs under its
configured policy, not a zero-vulnerability guarantee.

Independent publication verification checked small metadata/hashes and registry
objects; it did not locally execute the large packages or pull image layers.
Later main revisions need their own publication evidence. Deep public-network
evidence is concentrated on Windows/Linux x64. None of this proves current-head
100k-file performance, long-soak reliability, universal minimum-OS support or
Android device operation.
