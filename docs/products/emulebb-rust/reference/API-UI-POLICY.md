# emulebb-rust API And UI Policy

This task-routed annex applies only to `/api/v1`, REST routes, DTOs, OpenAPI,
controllers, or the embedded SPA WebUI.

- The forward `/api/v1` contract under `docs\products\emulebb-rust\api` is
  authoritative. The frozen MFC REST contract is not a forward-compatibility
  constraint.
- The accepted [Public Foundation](../design/PUBLIC-FOUNDATION.md) owns the
  round-one native contract and its coordinated REST/OpenAPI/SPA redesign.
  Implement future consumers later against that foundation; do not postpone
  contract design until Arr or preserve superseded beta shapes.
- Route or DTO changes evolve daemon code, OpenAPI, validators, embedded SPA
  models, and tests together. Do not add speculative aliases or legacy shapes.
- Organize the first-party contract around durable system/settings, network,
  unified search/result, transfer, library/sharing, and index domains. Live,
  indexed, and hybrid results share one provenance-bearing canonical model.
- Future Torznab and qBittorrent routes use their native paths on the same HTTP
  listener but translate through canonical services. They do not own parallel
  transfer or index state. The qBittorrent adapter implements only the subset
  required by supported Arr workflows.
- The embedded SPA is an operations console. Do not grow a desktop-GUI mirror
  or an internal automation-rule engine; external controllers own selection,
  scheduling, and post-processing.
- The supported listener default is `0.0.0.0:20017` on every product platform
  and package. Explicit listener settings remain authoritative. Every first-party and compatibility
  route family requires authentication and bounded request handling appropriate
  to that protocol.
- Do not bump `apiVersion` or REST `contractVersion` without a deliberate
  contract-freeze or release-boundary decision.
