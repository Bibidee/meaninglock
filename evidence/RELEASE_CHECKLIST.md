# Release checklist

- [ ] `contracts/` contains only `meaning_lock.py`.
- [x] `contracts/meaning_lock.py` is a single deployable candidate; no artificial line-count requirement is used.
- [ ] Lint, validate, schema and typecheck exit zero using the pinned SDK.
- [ ] Direct Mode tests include mocked web, screenshot and JSON LLM responses.
- [ ] Integration tests pass in the intended network environment.
- [ ] Explorer source is byte-identical to `contracts/meaning_lock.py`.
- [ ] A vision-capable, JSON-capable validator model is enabled.
- [ ] `scripts/run_release.ps1` completes with no failed command.
- [x] Deterministic category and safe-fallback unit tests pass where the SDK is available.
- [x] Lifecycle includes uncontested expiry, repeatable preserved rounds, bounded appeals, and timeout recovery that reopens monitoring.
- [x] Escrow components are tracked and payout ordering follows checks-effects-interactions.
- [x] Input bounds, HTTPS URL policy, digest format, evidence caps, and collision-safe storage keys are enforced.
- [ ] Direct Mode multimodal mocks pass on a supported non-Windows runner.
