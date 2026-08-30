# Release checklist

- [x] `contracts/` contains only `meaning_lock.py`.
- [x] `contracts/meaning_lock.py` is a single deployable candidate; no artificial line-count requirement is used.
- [x] Lint, validate, schema and typecheck exit zero using the pinned SDK.
- [x] Direct Mode tests include mocked web, screenshot and JSON LLM responses (`gltest tests/direct` passes on Windows with the documented loader compatibility shim).
- [ ] Environment-gated integration smoke test requires a configured live RPC/address; canonical payable and consensus flows are independently recorded in `evidence/DEPLOYMENT.md`.
- [x] Fresh canonical-address payable proof for the final source is recorded for `0x7ef7f667ceC8DB0d68b6E0c11263c97Af0238109` (registration, activation, challenge, and verification all finalized successfully; verification safely resolved `UNVERIFIABLE`).
- [x] Explorer source parity for the final source is confirmed on the canonical address; Explorer exposes 26 read and 22 write methods.
- [ ] A vision-capable, JSON-capable validator model is enabled.
- [x] `scripts/run_release.ps1` completes with no failed command.
- [x] Deterministic category and safe-fallback unit tests pass where the SDK is available.
- [x] Lifecycle includes uncontested expiry, repeatable preserved rounds, bounded appeals, and timeout recovery that reopens monitoring.
- [x] Escrow components are tracked and payout ordering follows checks-effects-interactions.
- [x] Input bounds, HTTPS URL policy, digest format, evidence caps, and collision-safe storage keys are enforced.
- [x] Direct Mode multimodal mocks pass through the official `genlayer-test` runner; the shim only compensates for its Windows temporary-file and empty-screenshot mock defects.
- [x] Semantic-verdict equivalence tests cover same verdict/different metadata, distinct verdict rejection, UNVERIFIABLE equivalence, CHANGED versus REMOVED, policy sensitivity, and malformed-record fallback.
