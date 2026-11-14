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

After launch, open `http://127.0.0.1:20017/` on the daemon host and enter the
packaged starter key `change_me_123change_me_123change_me_123`. The listener
defaults to `0.0.0.0:20017`. The private `emulebb-rust-settings.toml` in the
selected profile owns bootstrap authentication; the
[first-launch guide](GUIDE-GETTING-STARTED.md#profile-and-control-plane-settings)
owns the common configuration and client workflow. The APK generates its own
key instead. Verify checksums using the [supporting-file instructions](#what-each-supporting-file-does)
before installing or launching any package.

## Windows x64 And ARM64

Choose `-windows-x64.zip` for Intel/AMD x64 or `-windows-arm64.zip` for native
Windows ARM64. Extract the complete ZIP into a writable application directory.
Keep `webui` and the packaged runtime files beside `emulebb-rust.exe`, then
double-click the executable or run this in that directory:

```powershell
.\emulebb-rust.exe
```

The default profile and `emulebb-rust-settings.toml` are beside the executable.
For a separate writable profile, run
`.\emulebb-rust.exe --profile <profile-directory>`. Open the browser console as
described above. Keep the daemon process running while using the client; use
WebUI shutdown or Ctrl+C in its console to stop gracefully. The ZIP does not
install a Windows service. The hosted runner version is not an established
oldest supported Windows version.

## Linux

Choose the matching native CPU package. `uname -m` normally reports `x86_64`
for x64 (`amd64`) or `aarch64` for ARM64. The variants below share the same daemon
and WebUI; choose according to the host's package and library requirements.

### Debian/Ubuntu DEB

Choose `-linux-amd64.deb` or `-linux-arm64.deb` and install the downloaded file
through the host package manager. Replace `<downloaded-file>` below:

```sh
sudo apt install ./<downloaded-file>.deb
emulebb-rust --profile "$HOME/.config/emulebb-rust"
```

The CLI command explicitly chooses a writable profile because the installed
binary lives under `/usr/lib/emulebb-rust`. Its bootstrap is
`$HOME/.config/emulebb-rust/emulebb-rust-settings.toml`. Alternatively, use the
desktop launcher, which chooses `$XDG_CONFIG_HOME/emulebb-rust` when set, or
`~/.config/emulebb-rust`, and opens the browser console. The daemon has no
implicit home-directory fallback when called directly.

The dated nightly below declares `libc6 (>= 2.38)`, `libgcc-s1 (>= 4.2)` and
`ca-certificates`. Inspect the chosen build's dependencies; these are not a
promise that every Debian/Ubuntu release can run it.

### Portable GNU AppImage

Choose `-linux-x86_64.AppImage` or `-linux-aarch64.AppImage`. Mark the downloaded
file executable, then launch it; replace `<downloaded-file>` below:

```sh
chmod +x ./<downloaded-file>.AppImage
./<downloaded-file>.AppImage
```

Its launcher opens the browser and selects `$XDG_CONFIG_HOME/emulebb-rust` or
`~/.config/emulebb-rust` for the profile and bootstrap. Pass
`--profile <profile-directory>` to select another writable location. This
packages the GNU daemon; host kernel, libraries and AppImage runtime/FUSE
compatibility still matter. An exact oldest distribution or FUSE requirement
has not been established here.

### Static musl Archive

Choose `-linux-amd64-musl.tar.zst` or `-linux-arm64-musl.tar.zst`. Use a
tar/zstd-capable extractor and preserve the complete layout. For example:

```sh
tar --zstd -xf ./<downloaded-file>.tar.zst
cd emulebb-rust
./emulebb-rust
```

Keep adjacent `webui` files. The writable extracted executable directory is the
default profile, including `emulebb-rust-settings.toml`; pass an explicit
`--profile <profile-directory>` to change it. A compatible CPU/kernel and system
CA certificates are still needed. No exact oldest kernel or minimum RAM/storage
guarantee is established. A Linux musl binary is not an Android binary.

For each Linux variant, keep the daemon or launcher process running and open
the console at `http://127.0.0.1:20017/`. Stop through WebUI shutdown or Ctrl+C
when launched from a terminal. These packages do not install a system service.
The DEB/AppImage browser opener uses port 20017; if you override the REST port,
open the matching URL manually.

## macOS Intel And Apple Silicon

Choose `-macos-x64.dmg` for Intel or `-macos-arm64.dmg` for Apple Silicon. Open
the DMG, copy **eMuleBB Rust.app** to Applications or another installation
location, and launch the copied app. The app is unsigned and not notarized;
follow the normal macOS Privacy & Security approval flow.

The launcher starts the daemon and browser console and selects
`~/Library/Application Support/emulebb-rust` for its writable profile. Its
`emulebb-rust-settings.toml` contains the API key. The app can therefore run from
an installation location that is not writable. Quit the app or use WebUI
shutdown to stop the daemon. The launcher opens port 20017; open the matching
browser URL manually if you choose another REST port.

Directly running `Contents/MacOS/emulebb-rust` instead uses the executable
directory unless `--profile` is supplied; use an explicit writable profile for
that CLI mode. The package declares macOS 12.0, while the retained native smoke
below ran on macOS 15. Treat those as different facts.

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
and keep persistent state when replacing the container. The s6 launcher selects
the profile at `/config/emulebb-rust` and completed downloads at `/data/ed2k`.

For example, in a Linux shell replace `VERSION_FROM_RELEASE` with a published
version and choose `ubuntu` or `alpine`. Set PUID/PGID to the intended volume
owner; Docker chooses the native CPU from the image's multiarchitecture index.

```sh
version='VERSION_FROM_RELEASE'
variant='ubuntu'
docker run --detach --name emulebb-rust \
  -e PUID="$(id -u)" -e PGID="$(id -g)" \
  -p 20017:20017/tcp -p 20019:20019/tcp -p 20020:20020/udp \
  -v emulebb-config:/config -v emulebb-data:/data \
  "ghcr.io/emulebb/emulebb-rust:${version}-${variant}"
```

Open `http://127.0.0.1:20017/` on the container host and enter the starter key
or your configured key from
`/config/emulebb-rust/emulebb-rust-settings.toml`. Both variants run the daemon
under s6 in the background, explicitly selecting `0.0.0.0:20017`, the profile
above and `/data/ed2k` for incoming files. Those launch arguments take precedence
over the corresponding persisted settings. Stop with `docker stop emulebb-rust`;
restart with `docker start emulebb-rust`. Preserve both volumes when replacing
the image and select restart policy through your container engine if desired.

The daemon serves plain HTTP; remote TLS belongs at a reverse proxy. P2P TCP/UDP
routing and reachability need deliberate host/router configuration in addition
to the port mappings. The
[optional Gluetun example](https://github.com/emulebb/emulebb-rust/blob/main/packaging/docker/compose.gluetun.example.yaml)
is an advanced deployment reference with its own pinned image version. Select
an actual published version for a new deployment; the example does not establish
general VPN-safety proof.

## Android: APK Or Native Shell

The nightly release contract keeps all three alternatives below. The native
archives remain public release assets alongside the signed APK; they are not
limited to developer artifacts in Actions. APK candidates currently await the
full runtime qualification and publication gate, so use only assets actually
present in the selected published release. The failed
[candidate run 43583500231](https://github.com/emulebb/emulebb-rust/actions/runs/43583500231)
did not publish an APK release.

| Alternative | CPU | Filename suffix |
| --- | --- | --- |
| Android application candidate, Android 12+ | ARM64 and x86_64 in one APK | `-android-universal.apk` |
| Experimental native shell, including Termux | ARM64 / aarch64 | `-android-arm64-v8a.tar.zst` |
| Experimental native shell, including Termux | x86_64 / amd64 | `-android-x86_64.tar.zst` |

The native binaries target API 28+ (Android 9+) with 16 KiB-compatible ELF
alignment. That binary floor does not establish runtime support on every Android
version. The new APK candidate minimum is API 31 (Android 12); its API 31-37
runtime qualification, including Android 12L, is separate from native archive
compilation. A bounded API 31 ARM64 phone smoke has passed for one signed local
APK, but the complete qualification and release publication remain pending. A
Linux musl archive cannot substitute for either Android archive. Fire OS, Termux
runtime and 24-hour continuous operation remain unqualified; see
[the owning feature](../active/items/RUST-FEAT-056.md).

### Android Application

Verify the APK checksum from the same release, then open the APK and allow
installation from that download source when Android asks. Open eMuleBB and:

1. Select **Grant all-files access** and enable the Android special access.
   Start requires it. On Android API 37, also select **Allow local network**;
   Android 12-16 do not require that newer prompt.
2. Select **Allow notifications** for the running-service notification and its
   Stop action. Android 12/12L opens app notification settings; Android 13+
   requests the notification permission. Select **Allow continuous background operation** for the Doze
   exemption, then review **App battery settings** and allow unrestricted
   operation. Notifications and battery exemption are recommended; their denial
   is shown in the shell and does not itself block Start.
3. Review the displayed folders, press **Start**, and wait for **Running**.
   A fresh profile uses `Download/eMuleBB/Incoming` for completed files and
   `Download/eMuleBB/Shared` as its additional shared folder. Incoming files are
   shared automatically. Incomplete files stay in app-managed storage. Change
   folders in WebUI Settings and Sharing; later starts preserve those choices.
4. Select **Copy API key**, then **Open WebUI** and enter that key. The APK
   generates its own first-run key. Its listener defaults to
   `0.0.0.0:20017`; the same phone's browser opens `http://127.0.0.1:20017/`.
   Client settings, search, sharing and transfers belong to this browser console.

The native shell follows Android's system light/dark setting. The browser
console separately offers **System**, **Light** and **Dark** appearance.

The intended default profile leaves the IP unset, interface empty and VPN Guard
disabled/off for automatic direct routing: the daemon selects a detected local
IPv4 address and lets the operating system route traffic with that source
address. Explicit IP, interface or VPN Guard choices remain strict bindings and
fail when unsupported. This routing change is in progress; older Android kernel
binding support and full Android qualification remain unproved. A bounded API
31 phone smoke passed for one signed local APK; see the
[evidence record](../active/items/RUST-FEAT-056.md#latest-api-31-phone-smoke).

After Start, a dedicated foreground service and partial wake lock keep the
daemon running independently of the shell and browser. This consumes battery
and network traffic; Android and device battery policies still control process
survival. Use the app's **Stop**, the notification's Stop action, or WebUI
shutdown to stop cleanly. After reboot, open the app and press Start again.
Automatic boot resume is deferred; there is no reboot-resume setting.

Completed-file name collisions preserve the existing file. For example,
`abc.mp3` becomes `abc_01.mp3`, up to `_99`, then `_001` through `_999` and
wider groups when necessary. Atomic rename is used where supported. On other
filesystems, the daemon exclusively creates a free candidate and copies into
it; that filename can appear in a file manager before copying finishes, but
eMuleBB does not share it until verification and durable completion succeed.
An interrupted copy may remain as an unshared partial; the original download
is retained and retry uses another free name.

The storage repair changes this beta's database schema. An older profile fails
with a fresh-profile instruction; no migration or automatic reset is performed.
Preserve any required data before clearing an old APK test profile. Native
shell users can select a new writable directory with `--profile`.

### Termux Native Shell

This is an experimental advanced-shell alternative, without the APK's native
service controls. Install Termux using its
[official installation instructions](https://github.com/termux/termux-app#installation).
Match the archive to the CPU running Termux: `uname -m` normally reports
`aarch64` for `arm64-v8a`, or `x86_64` for `x86_64`. No Rust compiler, root,
proot or Linux distribution is required.

Replace `VERSION_FROM_RELEASE` with the exact selected release version, and
choose one ABI below. Run these commands inside Termux:

```sh
pkg install curl coreutils tar zstd
version='VERSION_FROM_RELEASE'
abi='arm64-v8a' # Use x86_64 for an x86_64 Termux environment.
mkdir -p "$HOME/emulebb-native"
cd "$HOME/emulebb-native"
asset="emulebb-rust-v${version}-android-${abi}.tar.zst"
base="https://github.com/emulebb/emulebb-rust/releases/download/rust-v${version}"
curl --fail --location --remote-name "$base/$asset"
curl --fail --location --remote-name "$base/SHA256SUMS"
sha256sum --check --ignore-missing SHA256SUMS
```

Continue only when the exact archive reports `OK`. Extract into a fresh
directory for a new installation; preserve an existing stopped profile before
replacing program files.

```sh
tar --zstd -xf "$asset"
cd emulebb-rust
termux-wake-lock
./run-developer.sh
```

The tar contains an `emulebb-rust` directory with the executable, launcher,
bootstrap TOML, `webui`, licenses and SBOM. Keep them together and use the
launcher: it sets the library path for any bundled runtime dependencies. Without
`--profile`, profile state goes beside the executable, independently of the
shell's working directory. An explicit `--profile` selects a writable profile;
relative paths resolve from the shell working directory. Keep executables,
profile, database and secrets under Termux's private `$HOME`, with the archive's
private directory and bootstrap permissions intact.

Open `http://127.0.0.1:20017/` in the phone browser. The bundled bootstrap uses
`0.0.0.0:20017` and the ready key
`change_me_123change_me_123change_me_123`; see
[control-plane settings](GUIDE-GETTING-STARTED.md#profile-and-control-plane-settings)
to choose your own key. The adjacent `webui` supplies the console.

Shared Android storage, including `~/storage/shared`, is mounted `noexec` and
does not preserve the private profile permissions. Do not extract the program
there. For optional completed-file or shared folders, run `termux-setup-storage`,
grant the requested Android storage access, and create dedicated directories:

```sh
termux-setup-storage
mkdir -p "$HOME/storage/shared/Download/eMuleBB/Incoming"
mkdir -p "$HOME/storage/shared/Download/eMuleBB/Shared"
realpath "$HOME/storage/shared/Download/eMuleBB/Incoming"
realpath "$HOME/storage/shared/Download/eMuleBB/Shared"
```

Paste the printed absolute paths into WebUI Settings and Sharing. The daemon
does not expand shell `$HOME` or `~` in WebUI fields. Granting storage access
does not move a profile or automatically configure these folders. Review the
contents before sharing; the incoming directory is shared automatically.

Keep the Termux session running and allow unrestricted battery use in Android's
Termux app settings. `termux-wake-lock` prevents CPU sleep while held; it does not
guarantee process survival or network availability. Stop gracefully with
**Ctrl+C** and wait for the daemon to exit, then run `termux-wake-unlock`.
Android 12+ can still kill Termux child processes; see the official
[Termux process notice](https://github.com/termux/termux-app#termux-application)
and [execution/storage restrictions](https://github.com/termux/termux-packages/wiki/Termux-execution-environment).

Archive `*-compile-elf.json` evidence covers compilation, test linking and ELF
inspection. It does not claim target test execution, Termux UID/runtime
qualification or a 24-hour soak. Separate APK/ADB phone transfer and rendered
WebUI proofs do not qualify execution inside Termux.

## What Each Supporting File Does

| Asset family | Purpose |
| --- | --- |
| ZIP, DEB, AppImage, DMG, musl tar/zstd | Runnable native packages |
| Android universal APK | Signed Android application candidate/release |
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
universal Android device operation or Termux runtime support.
