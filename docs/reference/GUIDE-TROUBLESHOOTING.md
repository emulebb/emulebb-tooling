# eMule BB Troubleshooting Guide

Troubleshooting should start by collecting evidence, then changing the smallest
setting that explains the symptom. eMule BB keeps the classic desktop app model:
the live state belongs to the app, while REST and companion tools observe or
request native state changes.

## Evidence First

Collect the support artifact that matches the problem:

| Problem area | Useful evidence |
|---|---|
| Network and Low ID | normal logs, verbose logs, port test output, firewall state, bind target |
| Kad | Kad state, UDP port state, bootstrap source, firewall and UPnP evidence |
| Sharing and startup | shared-cache state, hash queue, share roots, long-path state |
| Upload performance | upload cap, slot target, slow-slot state, queue and IO diagnostics |
| REST/controllers | WebServer state, bind/port, API key, OpenAPI route, controller logs |
| Crashes or hangs | mini dump for crashes, full dump for hangs or memory growth |

Prefer redacted diagnostic snapshots for support. Use raw snapshots only when
the recipient is trusted and the data sensitivity is understood.

## Common Symptoms

| Symptom | First checks |
|---|---|
| Low ID | TCP port, firewall, router/NAT, bind target, port test |
| Kad firewalled | UDP port, Kad bootstrap, firewall, UPnP/router, bind target |
| No search results | selected network, server/Kad state, query shape, search method |
| Slow startup | shared cache state, broad share roots, hash queue, long paths |
| Slow upload | finite upload cap, slot target, slow-slot state, IO/timer diagnostics |
| REST fails | WebServer enabled, bind/port, API key, lifecycle, OpenAPI route |
| IP filter ineffective | enabled flag, rule count, filter level, reload/update logs |

## Testing And Performance Context

Do not diagnose performance from one isolated observation. eMule BB performance
work is tied to concrete operating surfaces: broadband upload slot policy,
queue/source limits, socket and file buffers, startup caches, long paths, and
controller responsiveness. When a problem appears, compare the observed symptom
with those surfaces before changing unrelated network or profile settings.

For release confidence, distinguish quick hosted CI from full release proof.
The hosted fast lane covers the shared non-live harness. Broader release proof
adds native tests, REST/controller checks, UI/resource coverage, live eD2K/Kad
scenarios, language smoke, and package provenance. Current release status lives
in the [Beta 0.7.3 dashboard](../active/RELEASE-0.7.3.md).

## Related Guides

- [Product Guide](GUIDE-EMULEBB.md)
- [Network Guide](GUIDE-NETWORK.md)
- [Sharing Guide](GUIDE-SHARING.md)
- [Downloads and Search Guide](GUIDE-DOWNLOADS-SEARCH.md)
- [Controllers and REST Guide](GUIDE-CONTROLLERS-REST.md)
- [IP Filter Guide](GUIDE-IP-FILTERS.md)
- [Long Path Guide](GUIDE-LONGPATHS.md)
