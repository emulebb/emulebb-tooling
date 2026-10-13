# emulebb-rust API And UI Policy

This task-routed annex applies only to `/api/v1`, REST routes, DTOs, OpenAPI,
controllers, or the embedded SPA WebUI.

- The forward `/api/v1` contract under `docs\products\emulebb-rust\api` is
  authoritative. The frozen MFC REST contract is not a forward-compatibility
  constraint.
- Route or DTO changes evolve daemon code, OpenAPI, validators, embedded SPA
  models, and tests together. Do not add speculative aliases or legacy shapes.
- Do not bump `apiVersion` or REST `contractVersion` without a deliberate API
  freeze or release-boundary decision.
