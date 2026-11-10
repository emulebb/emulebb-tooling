# Running eMuleBB On macOS And Linux

For the current Rust beta, use the native Windows/Linux/macOS
[downloads and platforms guide](../products/emulebb-rust/reference/GUIDE-DOWNLOADS-PLATFORMS.md)
and [first-launch journey](../products/emulebb-rust/reference/GUIDE-GETTING-STARTED.md).
It includes Linux musl, container and experimental Android distinctions and
dated proof limits. You do not need a Windows VM for the native Rust packages.

The remaining VM/Wine/remote-Windows options document the maintained MFC
desktop client. For its normal Windows path, start with the
[Setup Guide](GUIDE-SETUP.md). Existing maintenance headings are retained.

## Why The MFC Desktop Client Has No Native macOS Or Linux Build

The eMuleBB MFC desktop client is a Windows application built on MFC and the
Win32 API. MFC is a Microsoft-proprietary, Windows-only framework, and its
source is not redistributable, so that client cannot be recompiled natively for
macOS or Linux the way a portable toolkit app could.

Running the MFC client on those systems therefore means one of four things:

- run a Windows guest in a virtual machine (highest fidelity),
- run the Windows binary on a compatibility layer such as Wine (community,
  best-effort, unsupported),
- run the core on Windows and drive it from a macOS/Linux browser through the
  REST API and controllers, or
- use a different client that is natively cross-platform.

The separate `emulebb-rust` client is the native cross-platform direction for
the eMuleBB family, summarized at the end of this guide.

## Option A: Windows Virtual Machine (Recommended)

A Windows guest runs the unmodified, official `emulebb.exe`, so behavior matches
a real Windows install.

### Apple Silicon Macs (M-series)

Run a Windows 11 **ARM64** guest and install the project's native **ARM64**
package. Because the guest and the binary are both ARM64, the app itself is not
translated.

- Hypervisors: Parallels Desktop, VMware Fusion, UTM, or QEMU.
- Use the ARM64 release ZIP, not the x64 ZIP.

### Intel Macs And Linux

Run an x64 Windows guest and install the x64 package.

- Hypervisors: VMware Workstation/Fusion, VirtualBox, or KVM/QEMU.
- Use the x64 release ZIP.

### Networking

Give the guest a **bridged** network adapter so eD2K and Kad can open a reachable
listening port and obtain High ID. A guest behind the host's NAT will typically
get Low ID and reduced connectivity. See the [Network Guide](GUIDE-NETWORK.md)
for port, bind, and UPnP details.

### Installing Inside The Guest

Use the same SHA-256-verified bootstrap pattern as the Setup Guide. Replace the
version with a release or nightly that is actually published on GitHub Releases.

```powershell
$version = '0.7.3'
$releaseUrl = "https://github.com/emulebb/emulebb/releases/download/emulebb-v$version"
$workRoot = Join-Path $env:TEMP "emulebb-suite-$version"
New-Item -ItemType Directory -Force -Path $workRoot | Out-Null
$scriptPath = Join-Path $workRoot 'Bootstrap-eMuleBBSuite.ps1'
iwr -UseBasicParsing "$releaseUrl/Bootstrap-eMuleBBSuite.ps1" -OutFile $scriptPath
$expected = ((irm "$releaseUrl/Bootstrap-eMuleBBSuite.ps1.sha256") -split '\s+')[0]
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $scriptPath).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "Bootstrapper SHA256 mismatch: $actual" }
& $scriptPath -Version $version -Bundle Full -NonInteractive -NoStart
```

For the standalone desktop app only, download and extract the matching
`emulebb-<version>-<arch>.zip` and run `emulebb.exe`, exactly as on a physical
Windows machine.

### Windows-Host Hyper-V Test Lab

If your host is already Windows and you want isolated, repeatable package and
suite checks (not the macOS/Linux path above), use the
[Hyper-V Suite Isolation Guide](GUIDE-HYPERV-WINDOWS.md). That guide is host-side
test isolation, not a way to run eMuleBB on macOS or Linux.

## Option B: Wine And CrossOver (Community, Unsupported)

> The project does not test or support Wine. This path is community, best-effort
> only. Use a virtual machine (Option A) when you need reliable behavior.

eMuleBB is relatively Wine-friendly: the package is a single statically linked
`emulebb.exe` plus `lang\*.dll` resource DLLs. The main prerequisite is the
MFC/Visual C++ runtime inside the Wine prefix.

- Linux: stock Wine, or CrossOver for a better-supported commercial Wine.
- macOS: CrossOver, Whisky, or the Game Porting Toolkit. On Apple Silicon the x64
  Windows binary is translated, which is more fragile than the native ARM64 VM in
  Option A.

Typical preparation in a fresh prefix:

```bash
winetricks vcrun2022
```

Then extract the x64 ZIP into the prefix and launch `emulebb.exe` with Wine.

### Known-Broken Or Unverified Under Wine

These surfaces depend on Windows behavior and are not validated under Wine:

- **Long-path support** is a Windows-only capability in eMuleBB and is not
  expected to work under Wine. See the [Long Paths Guide](GUIDE-LONGPATHS.md).
- System tray, the MiniMule popup, and some shell/COM integration.
- UPnP port mapping and related NAT behavior.
- Crash-dump capture and diagnostics output.

Core P2P networking (Winsock) maps to host sockets and generally works, but treat
the whole path as experimental.

## Option C: Windows-Hosted Core With A Cross-Platform Controller

You can keep the eMuleBB engine on a Windows host, VM, or Wine instance and
control it from any macOS or Linux browser. eMuleBB exposes an authenticated REST
API and integrates with the Arr stack (Prowlarr, Radarr, Sonarr, Lidarr), whose
management interfaces are browser-based and cross-platform.

This gives you cross-platform *use* without running the desktop UI locally. The
P2P engine still runs on Windows; only the control plane is remote. See
[Controllers And REST](GUIDE-CONTROLLERS-REST.md) and the
[Stack Integration Guide](GUIDE-STACK-INTEGRATIONS.md).

## Option D: aMule (Native, Different Client)

If your goal is to use the eD2K and Kad network natively on macOS or Linux
today, aMule is a maintained, cross-platform wxWidgets client for exactly that.
Because eMuleBB stays stock-compatible at the eD2K and Kad wire layer, aMule
and eMuleBB peers interoperate normally.

The trade-off is that aMule is a different client: you do not get eMuleBB-specific
features such as the broadband upload-slot controller or the eMuleBB MFC/Rust
REST contracts and integrations. Current upstream aMule has its own REST API and
WebUI; these are not eMuleBB controller compatibility surfaces. In this
workspace, `repos/amule-stable` is the frozen aMule 3.0.1 protocol-parity
authority at commit `02db0d7faecfc377694ff6242bc23346185990ed`.
Diagnostics-only patches must be separate exact revisions recorded with their
pinned base. `repos/amule` follows upstream HEAD for analysis and future
interoperability only and is never a current parity gate.

## Native Cross-Platform Future: emulebb-rust

The historical heading above is retained for inbound links. `emulebb-rust` is
now an active beta with native Windows/Linux/macOS packages, its own REST API
and a browser console. It is separate from the maintained MFC client. Follow the
[platform guide](../products/emulebb-rust/reference/GUIDE-DOWNLOADS-PLATFORMS.md)
for published packages and dated native smoke versus deeper network evidence.

For the authoritative capability boundary, see the
[eMuleBB Rust release scope](../products/emulebb-rust/RELEASE-SCOPE.md).
