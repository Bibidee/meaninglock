# Release checklist

- [ ] `contracts/` contains only `meaning_lock.py`.
- [x] `contracts/meaning_lock.py` is a single deployable candidate; no artificial line-count requirement is used.
- [x] Lint, validate, schema and typecheck exit zero using the pinned SDK.
- [x] Direct Mode tests include mocked web, screenshot and JSON LLM responses (`gltest tests/direct` passes on Windows with the documented loader compatibility shim).
- [x] Integration smoke tests pass locally; payable and consensus flows are recorded in `evidence/DEPLOYMENT.md`.
- [x] Final canonical-address payable registration/challenge/verification proof recorded in `evidence/DEPLOYMENT.md`.
- [x] Explorer source is byte-identical to `contracts/meaning_lock.py`.
- [ ] A vision-capable, JSON-capable validator model is enabled.
- [ ] `scripts/run_release.ps1` completes with no failed command.
- [x] Deterministic category and safe-fallback unit tests pass where the SDK is available.
- [x] Lifecycle includes uncontested expiry, repeatable preserved rounds, bounded appeals, and timeout recovery that reopens monitoring.
- [x] Escrow components are tracked and payout ordering follows checks-effects-interactions.
- [x] Input bounds, HTTPS URL policy, digest format, evidence caps, and collision-safe storage keys are enforced.
- [x] Direct Mode multimodal mocks pass through the official `genlayer-test` runner; the shim only compensates for its Windows temporary-file and empty-screenshot mock defects.
