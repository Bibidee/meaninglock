# Release checklist

- [ ] `contracts/` contains only `meaning_lock.py`.
- [ ] `contracts/meaning_lock.py` is at least 1000 substantive lines and remains one deployable candidate.
- [ ] Lint, validate, schema and typecheck exit zero using the pinned SDK.
- [ ] Direct Mode tests include mocked web, screenshot and JSON LLM responses.
- [ ] Integration tests pass in the intended network environment.
- [ ] Explorer source is byte-identical to `contracts/meaning_lock.py`.
- [ ] A vision-capable, JSON-capable validator model is enabled.
- [ ] `scripts/run_release.ps1` completes with no failed command.
- [ ] Deterministic category and safe-fallback unit tests pass.
- [ ] Direct Mode multimodal mocks pass on a supported non-Windows runner.
