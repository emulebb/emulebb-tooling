# Windows Hyper-V Suite Isolation Guide

This guide shows how to run eMuleBB package and suite checks inside local
Windows Hyper-V guests. Use this path when you want a clean Windows environment
that is isolated from the host machine's daily eMuleBB profile, downloads,
controllers, and runtime state.

Hyper-V is useful for release testing, package smoke testing, and cautious
suite experimentation. It is not the normal first install path. For normal use,
start with the [Setup Guide](GUIDE-SETUP.md).

This guide is host-side Windows test isolation. To run or use eMuleBB on macOS
or Linux, see [Running on macOS and Linux](GUIDE-CROSS-PLATFORM.md) instead.

## What Hyper-V Isolation Provides

The workspace VM lab treats each guest as a clean install target:

- The host builds or selects release packages.
- The host copies only the package and test payload into the guest.
- eMuleBB, profiles, suite state, controller state, temp files, and logs live
  inside the guest run root.
- The guest is restored from the clean checkpoint before each run.
- Reports are copied back under the workspace test report directory.

This protects the host from accidental reuse of the host's live profile or
download directories. It also keeps package tests repeatable because each run
starts from the same checkpointed Windows image.

Hyper-V is not a security boundary for secrets or untrusted files. Do not copy
private host profiles, private download roots, credentials, or sensitive shared
directories into the guest unless you deliberately want that data in the VM.

## Network Model

The default lab uses separate Hyper-V networks:

| Network | Default name | Purpose |
|---|---|---|
| Test switch | `emulebb-vm-private` | Isolated guest test traffic after preparation |
| Provisioning NAT | `emulebb-vm-nat` | Temporary internet access while preparing the guest image |
| VPN switch | `emulebb-vm-external` | Optional live-wire profiles that require a VPN-oriented path |

Most introductory runs are offline or LAN-scoped inside the lab. They should not
contact the public eD2K/Kad network. Public-network or VPN live-wire profiles
are separate advanced runs and should only be used after the local package and
suite checks are healthy.

## Host Requirements

Use a host that can run local Hyper-V:

- Windows Pro, Enterprise, or Server with Hyper-V available.
- An elevated PowerShell session for VM preparation and execution.
- Enough local resources for two Windows guests when using the default matrix:
  at least 8 GB available RAM is a practical minimum, with more preferred.
- Enough disk for the generated VHDX files; the default disk setting is 64 GB
  per target.
- A materialized eMuleBB workspace with `repos/emulebb-build` and
  `repos/emulebb-build-tests`.
- Your own legal Windows ISO files and licenses.

Do not download Windows ISO images from unofficial sources. The lab consumes
the ISO path you provide; it does not bundle, mirror, or authorize Windows
installation media.

## Manual User VM Path

Use this path when you want to try the eMuleBB suite in a VM without using the
workspace test harness.

1. Create a Generation 2 Hyper-V VM.
2. Install Windows from your own legal ISO.
3. Give the VM enough local resources for the suite, for example 4 GB RAM, two
   virtual processors, and a 64 GB virtual disk.
4. Use a private or internal virtual switch for isolation whenever the guest
   does not need internet access.
5. Use a NAT/default switch only when the guest needs to download release
   assets, then return to the isolated switch before experiments that should
   not touch the public network.
6. Disable shared host folders, drive redirection, and clipboard sharing unless
   you intentionally need them for a short transfer.
7. Take a clean checkpoint before installing eMuleBB.
8. Download the eMuleBB suite bootstrapper inside the guest.
9. Install the suite inside the guest.
10. Run `Get-SuiteInfo.ps1` inside the guest.

Inside the guest, use the same full suite bootstrap pattern as the setup guide:
replace the version with a release or nightly that is actually published on
GitHub Releases.

```powershell
$version = '0.7.3-rc.3'
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

After installation, run the generated suite check from the install root:

```powershell
.\scripts\Get-SuiteInfo.ps1
```

Keep all eMuleBB incoming, temp, profile, controller, and suite data inside the
guest unless you deliberately export a report. Revert to the clean checkpoint
when you want to discard the run.

## Configure The Lab

Run these commands from the build repo:

```powershell
cd $env:EMULEBB_WORKSPACE_ROOT\repos\emulebb-build
Copy-Item .\vm-lab.example.json .\vm-lab.local.json
```

Edit `vm-lab.local.json`. That file is intentionally ignored by Git. Keep
machine-local values there, not in tracked docs or scripts.

Use the example as the shape:

```json
{
  "schema": "emulebb.windows-vm-lab.v1",
  "hyperv": {
    "switch_name": "emulebb-vm-private",
    "checkpoint_name": "emulebb-clean",
    "memory_mb": 4096,
    "disk_gb": 64,
    "processor_count": 2
  },
  "guest": {
    "username": "emulebbtest",
    "password_env": "EMULEBB_VM_TEST_PASSWORD"
  },
  "targets": {
    "win10": {
      "vm_name": "emulebb-win10",
      "iso_path": "D:\\path\\to\\Win10.iso",
      "edition": "Windows 10 Pro"
    },
    "win11": {
      "vm_name": "emulebb-win11",
      "iso_path": "D:\\path\\to\\Win11.iso",
      "edition": "Windows 11 Pro"
    }
  }
}
```

Use VM names and switch names that do not collide with other local Hyper-V work.
The `edition` value must match an edition available inside the ISO.

Set the guest password environment variable in the elevated shell:

```powershell
$env:EMULEBB_VM_TEST_PASSWORD = '<guest-password>'
```

Use a password that is only for this disposable VM account.

## Prepare Clean Guests

Start with a dry run:

```powershell
python -m emule_workspace vm-lab prepare --dry-run
```

Then prepare the images and clean checkpoints:

```powershell
python -m emule_workspace vm-lab prepare --matrix win10,win11
```

Preparation is slow the first time. It creates VHDX images, installs Windows
from the configured ISOs, installs the guest tooling needed by the harness, and
creates the clean checkpoint named in `vm-lab.local.json`.

Repeat runs are designed to restore the clean checkpoint instead of rebuilding
the image. Use `--rebuild-images` only when you intentionally want to discard
the prepared guests and start over:

```powershell
python -m emule_workspace vm-lab prepare --matrix win10,win11 --rebuild-images
```

## Run A Safe Suite Installer Smoke

Use `package-helper-install` when you want the safest first check of the
packaged PowerShell helpers and suite installer path inside isolated guests:

```powershell
python -m emule_workspace test windows-vm `
  --profile package-helper-install `
  --release-version 0.7.3-rc.3
```

This builds or refreshes the release package through the workspace
orchestration, restores the clean guests, expands the eMuleBB package inside
the guests, parses packaged PowerShell scripts, dry-runs
`Install-eMuleBBSuite.ps1`, and checks the packaged firewall helper.

If the matching release package already exists under the workspace release
state, use `--skip-build` to prove the package path without rebuilding:

```powershell
python -m emule_workspace test windows-vm `
  --profile package-helper-install `
  --release-version 0.7.3-rc.3 `
  --skip-build
```

Current VM profiles expect the supported matrix, `win10,win11`. Do not narrow
the command to only one target unless the profile catalog has changed to
support that matrix.

## Run A Reusable Local/VM Suite Scenario

After the package helper smoke passes, use a reusable campaign scenario when
you want to exercise the suite path with the local swarm harness inside clean
guests:

```powershell
python -m emule_workspace test campaign-scenario `
  --scenario emulebb.flow.controller.installer-swarm.v1 `
  --mode vm `
  --release-version 0.7.3-rc.3 `
  --skip-build `
  --swarm-tier 1 `
  --local-swarm-mode execute
```

This is a stronger end-to-end check than the package helper smoke. It uses the
shared local/VM campaign catalog, restores the Hyper-V guests, stages the
release package, uses the suite installer path, and runs the selected local
swarm scenario in the guest.

Use `--local-swarm-mode plan` when you only want to verify command planning and
payload staging:

```powershell
python -m emule_workspace test campaign-scenario `
  --scenario emulebb.flow.controller.installer-swarm.v1 `
  --mode vm `
  --release-version 0.7.3-rc.3 `
  --skip-build `
  --swarm-tier 1 `
  --local-swarm-mode plan `
  --dry-run
```

## Debugging A Failed Guest

By default, the harness restores the clean checkpoint and stops the guest when
the run finishes. To inspect a failure interactively, add `--keep-running`:

```powershell
python -m emule_workspace test windows-vm `
  --profile package-helper-install `
  --release-version 0.7.3-rc.3 `
  --skip-build `
  --keep-running
```

Use this only for debugging. After inspection, stop the VM and run the normal
command again so the harness restores the clean checkpoint.

Reports are written under:

```text
EMULEBB_WORKSPACE_ROOT\workspaces\workspace\state\test-reports\windows-vm
```

The `latest` folder points at the most recent VM run. Each target also writes a
target-specific result JSON under the timestamped run directory.

## Safe Operating Rules

- Do not attach host download directories to the guest.
- Do not import the host's daily eMuleBB profile into the guest.
- Do not reuse the same guest profile for unrelated experiments; use clean
  checkpoint restores.
- Prefer `package-helper-install` before any live or local-swarm profile.
- Keep public-network profiles separate from offline and LAN-scoped checks.
- Use `--skip-build` only when the matching package assets already exist.
- Keep VM credentials local and disposable.
- Treat `--keep-running` as a temporary debugging mode.

## Troubleshooting

- `Missing Hyper-V/Windows imaging command`: Hyper-V or Windows imaging tooling
  is unavailable. Enable Hyper-V on a supported Windows edition and run from an
  elevated shell.
- Windows Home host: the local Hyper-V VM lab expects a Windows edition with
  Hyper-V support. Use Windows Pro, Enterprise, or Server for this path.
- `Windows VM lab requires an elevated PowerShell host`: the shell is not
  elevated. Reopen PowerShell as Administrator.
- `Windows ISO is missing`: `iso_path` points at a missing file. Edit
  `vm-lab.local.json` and use a valid local ISO path.
- Edition selection fails during preparation: the configured edition does not
  exist in the ISO. Change `edition` to the exact ISO edition name.
- Guest password variable is required: `EMULEBB_VM_TEST_PASSWORD` is not set.
  Set the environment variable in the elevated shell before running commands.
- `--skip-build` reports a missing package: the release package was not built
  yet. Drop `--skip-build` or build/package the matching release first.
- The profile rejects the matrix: the selected profile requires the supported
  target set. Use `--matrix win10,win11` unless the profile catalog says
  otherwise.
- Checkpoint restore fails: the clean checkpoint is missing or damaged. Re-run
  `vm-lab prepare`, or use `--rebuild-images` if the image must be recreated.
- Provisioning network conflicts: the default NAT prefix collides with local
  networking. Change `provisioning_nat_prefix`, `provisioning_gateway`, and
  guest IPs in `vm-lab.local.json`.

## What To Report

When filing an issue for a Hyper-V run, include:

- eMuleBB package version and architecture.
- Host Windows version and whether Hyper-V was enabled locally.
- VM target matrix.
- VM profile or campaign scenario.
- Exact command line.
- Whether `--skip-build` was used.
- The relevant run directory under `state\test-reports\windows-vm`.
- Any target-specific result JSON and captured stdout/stderr files.

Do not include private guest passwords, VPN credentials, private Windows product
keys, or personal profile data in public reports.
