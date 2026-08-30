# Release checklist

- [x] `contracts/` contains only `meaning_lock.py`.
- [x] `contracts/meaning_lock.py` is a single deployable candidate; no artificial line-count requirement is used.
- [x] Lint, validate, schema and typecheck exit zero using the pinned SDK.
- [x] Direct Mode tests include mocked web, screenshot and JSON LLM responses; final CI run `33335456689` reports `35 passed, 2 skipped` with the documented loader compatibility shim.
- [ ] Environment-gated integration smoke test requires a configured live RPC/address; canonical payable and consensus flows are independently recorded in `evidence/DEPLOYMENT.md`.
- [x] Fresh canonical-address payable proof is recorded for `0x74FB9B259a3BC0d8852de0c2597952360903294e` (registration, activation, challenge, and verification finalized; final state `ACTIVE/PRESERVED/ROUND_NONE`; challenger refunded and publisher principal locked).
- [x] Explorer source parity for the corrected source was confirmed during fresh Studio deployment; schema exposes the corrected source methods.
- [ ] A vision-capable, JSON-capable validator model is enabled.
- [x] `scripts/run_release.ps1` completed with no failed command in the pinned
  release environment (the current Windows shell lacks `python`/`genvm-lint`,
  so a direct rerun here is environment-blocked).
- [x] Deterministic category and safe-fallback unit tests pass where the SDK is available.
- [x] Lifecycle includes uncontested expiry, repeatable preserved rounds, bounded appeals, and timeout recovery that reopens monitoring.
- [x] Escrow components are tracked and payout ordering follows checks-effects-interactions.
- [x] Input bounds, HTTPS URL policy, digest format, evidence caps, and collision-safe storage keys are enforced.
- [x] Direct Mode multimodal mocks pass through the official `genlayer-test` runner; the shim only compensates for its Windows temporary-file and empty-screenshot mock defects.
- [x] Semantic-verdict equivalence tests cover same verdict/different metadata, distinct verdict rejection, UNVERIFIABLE equivalence, CHANGED versus REMOVED, policy sensitivity, and malformed-record fallback.

Historical note: Studio rejected one follow-up registration before contract
execution while loading a stale unrelated `ClaimVerifier` artifact. It was not
part of the canonical deployment. The canonical live proof is the successful
registration/activation/challenge/verification sequence documented in
`evidence/DEPLOYMENT.md`.
