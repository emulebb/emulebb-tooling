# MFC 0.8.0 — Lean line (frozen-surface removal) lane spec

Status: proposal (no code yet). `0.8.x` MFC lane content (operator decision 2026-06-24).
**Not** a `0.7.3` gate; opens on `main` only after stable `0.7.3` and the `0.7.x` LTSC split.

Governs: [FROZEN-SURFACES](../FROZEN-SURFACES.md) (the canonical frozen-surface register),
[FUTURE-ROADMAP](../FUTURE-ROADMAP.md). Companion lane:
[Performance & Async](MFC-0.8.0-PERF-ASYNC-PLAN.md). Backlog items:
`REF-025` (#91), `REF-043` (#99), `REF-051` (#105), `REF-052` (#106), `REF-055`, `REF-058`.

## Context

When `0.7.3` final ships, `0.7.x` becomes the **LTSC** (long-term servicing) line — stable,
compatibility-preserving, compile-keeping its legacy baggage — and `main` opens for the
revived `0.8.x` modernization. The operator wants `0.8.x` **lean**: delete the dead/legacy
subsystems rather than carry them forward. This lane defines and schedules that removal.

This is **not new backlog** — the removals already exist as tracked items. The operator's
named targets map directly onto them:

| Operator target | Item | State |
|---|---|---|
| IRC, Scheduler, first-start wizard, legacy splash, legacy update-checker | `REF-025` (#91) | IN_PROGRESS |
| SMTP / email notifications | `REF-025` (#91) | IN_PROGRESS |
| Legacy Web Interface HTML templates (keep REST) | `REF-043` (#99) | OPEN |
| SOCKS / proxy support | `REF-051` (#105) | OPEN |
| Archive preview + recovery | `REF-052` (#106) | OPEN |
| Async known/shared startup load (perf, related) | `REF-058` | OPEN (0.8.0) |

The work is to **consolidate these into one scheduled "Lean 0.8.0" lane**, record the
keep-list precisely, and apply the two operator decisions below. Outcome: a smaller, clearer
`0.8.x` codebase with the supported controller/protocol surface intact and LTSC unaffected.

## Locked decisions (operator, 2026-06-24)

1. **Drop mbedTLS entirely; REST serves plaintext HTTP only.** This *flips* the prior
   `FROZEN-SURFACES.md` / `REF-043` decision that kept HTTPS/TLS because it "carries the
   controller API." Rationale: the control plane is local over `X_LOCAL_IP`, so HTTPS is
   unnecessary. **Keep** the web-server listener, allowed-IP checks, and REST
   `/api/v1`+`/api/v2` routing — now HTTP-only. Removal surface: TLS paths in `WebSocket.cpp`,
   `TLSthreading.*`, `WebServerCertificate.*`, `WebSocketTlsSeams.h`, SMTP's mbedTLS use, and
   the `mbedtls`/`mbedx509`/`tfpsacrypto` link+include in `emule.vcxproj`.
   - **Safety requirement (non-negotiable):** plaintext REST — which carries session
     tokens/credentials — must **bind to the local control-plane address only**
     (`X_LOCAL_IP` / loopback-equivalent), never a public or VPN-tunnel interface. This is a
     hard bind rule, consistent with the existing control-plane binding policy. The
     allowed-IP check stays as defense-in-depth.
2. **Extra removals included:** 3D preview control (`3DPreviewControl.*`), id3lib
   (third-party MP3 ID3 metadata; drops MP3-tag display in file details), and
   TextToSpeech / SAPI (`TextToSpeech.*`) — the last *flips* the `FROZEN-SURFACES.md`
   "keep SAPI best-effort" line.

## Keep-list (do NOT remove — supported boundaries)

Confirmed against `FROZEN-SURFACES.md` "Supported Boundaries" + code inventory:

- **Web-server listener + REST `/api/v1`+`/api/v2` + Torznab + aMuTorrent/Arr.** Only the
  legacy **HTML template page UI** is removed (REF-043); the API stays (now HTTP-only).
- **MiniMule** (`MiniMuleDlg.*`) — a **native eMuleBB feature**, explicitly *not* in the
  legacy MiniMule/IE-host removal bucket. Keep it.
- **`LifecycleProgressDlg`** — the modern startup-progress dialog the
  [startup slice](MFC-0.8.0-STARTUP-TIME-TO-INTERACTIVE.md) (REF-058) relies on. REF-025's
  "splash screen" removal targets the *legacy* splash behavior only and must **not** take
  `LifecycleProgressDlg`. No standalone `CSplashScreen` file exists in the tree — confirm
  during REF-025 execution that "splash" is the legacy bitmap path, not the lifecycle loader.
- **UPnP / interface-binding / VPN-guard** (`UPnPImpl*`, `BindAddressResolver`, VPN-guard
  seams); **CaptchaGenerator** (chat anti-spam, entangled with `BaseClient`);
  **HttpDownloadLog** (GeoIP / IP-filter / nodes.dat / server.met fetches); **Crypto++ /
  zlib / miniupnpc** core deps.

## Removal table

LOC are rough, from the eMuleBB `srchybrid` inventory. "Entanglement" flags anything that
needs care beyond a file delete.

| Subsystem | Item | Files (srchybrid) | ~LOC | Entanglement |
|---|---|---|---|---|
| Archive preview + recovery | REF-052 | `ArchivePreviewDlg.*`, `ArchiveRecovery.*` | ~3.4k | Self-contained UI; file-detail preview tab + `IDD_ARCHPREV` resource + context menu. |
| IRC | REF-025 | `Irc*.cpp/h` (6 pairs), `PPgIRC.*` | ~6.4k | Tab/window in `EmuleDlg`, toolbar button, prefs page, `ChatSelector`, context menus; uses proxy layer (also being removed). |
| SMTP / email | REF-025 | `SendMail.*`, `SMTPdialog.*`, `PPgNotify.*` | ~2k | `EmailSettings` in `Preferences`; uses mbedTLS (removed with TLS). |
| Scheduler | REF-025 | `Scheduler.*`, `PPgScheduler.*`, `SchedulerPolicySeams.h` | — | Scheduler tick in the timer; prefs page + keys. |
| First-start wizard | REF-025 | `Wizard.*` | — | First-run flow in `InitInstance`/`EmuleDlg`. |
| Legacy splash + update-checker | REF-025 | (legacy splash path), update-check | — | **Keep `LifecycleProgressDlg`.** |
| Proxy / SOCKS | REF-051 | `AsyncProxySocketLayer.*`, `PPgProxy.*` | ~1.7k | Proxy layer in `EMSocket.cpp`; `ProxySettings` in `Preferences`. Synergy with WSAPoll port. |
| Web Interface HTML templates | REF-043 | template/page UI in `CWebServer` (keep listener+REST) | — | Split HTML page UI from REST routing; **keep REST**. |
| mbedTLS / TLS → REST plaintext | **REF-060 (new)** | `WebSocket.cpp` TLS, `TLSthreading.*`, `WebServerCertificate.*`, `WebSocketTlsSeams.h`, `emule.vcxproj` deps | — | REST goes plaintext HTTP, bound local-only; decouple SMTP's TLS (SMTP removed anyway). |
| 3D preview control | REF-055 (fold) | `3DPreviewControl.*` | ~71 | Member of `PPgDisplay`. |
| id3lib MP3 metadata (**confirmed** 2026-06-24) | REF-055 (fold) | `KnownFile.cpp:61` `ID3_GetStringW`, `FileInfoDialog.cpp:34-35` id3 includes; `id3lib.lib`+`ID3LIB_LINKOPTION` in `emule.vcxproj` | — | **MediaInfo DLL is now the sole MP3-metadata path** — migrate `KnownFile.cpp:61` to it; `third_party/emulebb-id3lib` no longer built. Without MediaInfo.dll, MP3 tag display is gone (accepted). |
| TextToSpeech / SAPI | REF-025 (extend) | `TextToSpeech.*` | — | Voice notifications; flips the FROZEN-SURFACES "keep SAPI" line. |
| Sound / WAV event notifications (**added** 2026-06-24) | REF-025 (extend) | `PlaySound`/`sndPlaySound` call sites in `EmuleDlg.cpp` (+ IRC paths already going), `PPgMessages.cpp` sound checkbox, sound prefs keys in `Preferences.*` | ~0.2–0.3k | Shares paths with IRC (also removed). **Keep peer chat** — only the audio alerts go. |
| PeerCache dead resource-strings (**added** 2026-06-24) | REF-055 (fold) | commented `IDS_PEERCACHE_*` strings across `lang/*.rc` (~41 files) | trivial | PeerCache code/opcodes already gone; pure dead-string hygiene. |

### Item mapping
- **Schedule** `REF-025`, `REF-043`, `REF-051`, `REF-052` to milestone `0.8.0`.
- **New `REF-060`** for the mbedTLS/TLS removal + REST-plaintext switch (distinct surface:
  WebSocket TLS, cert, SMTP-TLS decouple, dep+vcxproj). Number is proposed; mint the
  `emulebb/emulebb` issue at promotion.
- **Extend `REF-025`** scope to add TextToSpeech/SAPI **and Sound/WAV event notifications**.
- **Fold** 3D-preview-control + id3lib + PeerCache dead-string cleanup into `REF-055`
  (code-quality/modernization), or split to small items at promotion.

### Evaluated and kept (2026-06-24)

These were inventoried as lean candidates and **deliberately kept** — recorded so they are
not re-proposed:

| Kept | Why |
|---|---|
| eD2K peer chat (`ChatWnd.*`, `ChatSelector.*`, `SmileySelector.*`) + `CaptchaGenerator` | Operator chose to keep peer messaging. Stays *retained-but-unsupported* (FROZEN-SURFACES already marks chat UI unsupported); not removed. Captcha protects it, so it stays too. |
| Internal video thumbnail/preview (`Preview.*`, `PreviewDlg.*`, FFmpeg pipeline, thumbnail column, search frame-grid) | Operator kept it. (External-player "preview" + REST preview endpoint are unaffected either way.) |
| WebServices external-lookup menus (`WebServices.*`, `webservices.dat`) | Kept. Isolated `ShellExecute` URL launcher. |
| Pinger raw-ICMP latency (`Pinger.*`) | Kept. Diagnostic readout in client/stats dialogs. |
| Skin/color profiles, ZIP/GZIP (`ZIPFile.*`/`GZipFile.*`), Collections, Statistics, MediaInfo | Skin is too deeply wired for the ROI; ZIP/GZIP is needed by Collections + IP-filter/GeoIP gz; Collections is the suite bridge; Statistics is core monitoring; MediaInfo is the kept metadata path. |
| `ReleaseUpdateCheck.*` (modern GitHub-release checker) | **Confirm before removing.** REF-025 lists a "legacy update checker"; this modern GitHub checker is likely kept (packaging uses GitHub releases). Do not remove without confirming which one REF-025 means. |

## Sequencing & synergies

- **Low-risk deletions first** (archive, IRC, SMTP, 3D-preview, id3lib, TextToSpeech,
  web-HTML-templates): isolated, shrink the surface with little risk.
- **Proxy removal (REF-051) interleaves with the WSAPoll network-core-thread port** and
  simplifies it — the reference `v0.72a` tree removed proxy *during* its WSAPoll migration.
  Preserve only the VPN-bind/egress-pin path; the proxy layer goes.
- **SMTP + TLS removal share the mbedTLS decouple** — do them together (`REF-025` SMTP +
  `REF-060` TLS).
- **REST-plaintext removes TLS state**, which *simplifies* the off-UI-thread REST
  read-locking in the [Performance & Async lane](MFC-0.8.0-PERF-ASYNC-PLAN.md).

## Definition of Done (per removal slice)

- Subsystem files deleted; all wiring (menus, toolbar, prefs pages, context menus, resource
  IDs, `Preferences` keys, `emule.vcxproj` entries) removed; build green `Debug|x64` +
  `Release|x64`.
- **No eD2K/Kad wire change:** the protocol-oracle packet diff (`packet_trace_diff.py`, key
  `(protocol_marker, opcode, payload_hex)`) shows no regression vs the `0.7.3` baseline.
  (Every removal here is UI/auxiliary; none may touch protocol.)
- For REF-043/REF-060: REST `/api/v1`+`/api/v2` contract tests pass over **plaintext HTTP**;
  the listener **binds local-only** (assert: no public/VPN-interface bind); allowed-IP check
  intact.
- For REF-051: VPN-guard + leak posture unchanged after proxy removal.
- `0.7.x` LTSC untouched.

## Out of scope

- Removing anything on the keep-list (REST/listener, MiniMule, LifecycleProgressDlg, UPnP/
  VPN-guard, CaptchaGenerator, HttpDownloadLog, Crypto++/zlib/miniupnpc).
- Any protocol/opcode/Kad change.
- Landing removals on the `0.7.x` LTSC line.

## Verification

Documentation task — verification is review-and-consistency plus the code-time gates above:
- Lean lane ↔ `FROZEN-SURFACES.md` ↔ REF items ↔ Performance & Async docs are consistent;
  `FROZEN-SURFACES.md` has no leftover contradiction (TLS + SAPI boundaries flipped
  coherently; MiniMule + LifecycleProgressDlg keeps explicit).
- Every code claim cites a real file on `main`.
- Per WORKSPACE-POLICY: one removal-slice per commit (per REF item / subsystem),
  English-only, no AI attribution, on `main`.
