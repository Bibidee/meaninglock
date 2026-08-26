# MeaningLock

MeaningLock is a standalone GenLayer Intelligent Contract primitive for locking GEN behind a public covenant whose material meaning must remain intact. It is a reusable primitive, not a frontend product. Correctness, deterministic settlement, and auditable lifecycle rules take priority over source length.

## Design

Deterministic state holds the parties, escrow ledger, lifecycle, evidence references, immutable audit sequence, policy thresholds, appeal windows, settlement basis points, and canonical verdict. Verification performs web fetch/render, screenshot inspection and optional image evidence inside a GenLayer consensus block. Validators compare only compact categorical fields, never raw HTML, screenshots, prose, or timestamps. This minimizes — but cannot guarantee elimination of — nondeterministic `UNDETERMINED` outcomes.

The implementation separates registration and frozen terms, multimodal evidence acquisition, round-based challenge/appeal/recovery transitions, and deterministic escrow settlement with append-only audit records. Publisher collateral and challenger collateral are tracked independently; terminal actions can only return each component to its owner or route the publisher security deposit to the beneficiary after final adverse settlement.

## Lifecycle

`ACTIVE → PENDING (review round) → ACTIVE (preserved/timeout) → PENDING ... → RESOLVED (adverse appeal window) → CLOSED`.
Uncontested expiry is claimable by the publisher. Preserved reviews do not terminate monitoring. Appeals replace the canonical evidence context and keep adverse settlement locked until the appeal deadline.

Payout uses one helper, `_send_gen`, which zeroes its ledger and marks the covenant paid before emitting its single finalized GEN transfer.

## Layout

- `contracts/meaning_lock.py` is the only deployable source.
- `tests/direct/` and `tests/integration/` are outside `contracts/` so lint/schema extraction cannot mistake them for contracts.
- `scripts/release_check.ps1` verifies source isolation and the single-transfer invariant.

## Verify

```powershell
genvm-lint check contracts/meaning_lock.py
genvm-lint schema contracts/meaning_lock.py --output evidence/meaning_lock.schema.json
genvm-lint typecheck contracts/meaning_lock.py
pytest tests/direct -v
pytest tests/integration -v
powershell -ExecutionPolicy Bypass -File scripts/release_check.ps1
```

No deploy command is included. Publish the exact same source to Explorer after the full release checklist passes. A fresh deployment is required whenever `contracts/meaning_lock.py` changes; historical deployment addresses are evidence only.

The Studio deployment history and current closure deployment are in
`evidence/DEPLOYMENT.md`. Historical addresses are explicitly superseded; use
only the fresh address recorded in the closure section after independently
checking Explorer source parity.
