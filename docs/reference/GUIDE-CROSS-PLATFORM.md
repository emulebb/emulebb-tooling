# Running eMuleBB On macOS And Linux

This guide explains how to run or use eMuleBB on macOS and Linux. For the normal
Windows desktop path, start with the [Setup Guide](GUIDE-SETUP.md) instead.

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
API and integrates with the aMuTorrent web controller and the Arr stack
(Prowlarr, Radarr, Sonarr, Lidarr), all of which are browser-based and
cross-platform.

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
WebUI; these are not eMuleBB controller compatibility surfaces. In this workspace,
`analysis/amule` is an upstream source/fixture reference, separate from the
optional eMuleBB Windows-build fork.

## Native Cross-Platform Future: emulebb-rust

`emulebb-rust` is a separate Rust-native eD2K/Kad client with a headless daemon,
local indexing, its own `/api/v1` contract, and an embedded SPA WebUI. It is not
a line-by-line MFC port or a shared-contract backend for the frozen aMuTorrent
controller. Windows, Linux, and macOS CI build artifacts exist, but platform
runtime and public-network transfer claims require their own proof. It is not
yet the stable MFC package replacement.

For the authoritative capability boundary, see the
[eMuleBB Rust release scope](../products/emulebb-rust/RELEASE-SCOPE.md).
