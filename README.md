# MeaningLock

MeaningLock is a standalone GenLayer Intelligent Contract primitive for locking GEN behind a public covenant whose material meaning must remain intact. It is a reusable primitive, not a frontend product. The deployable source is deliberately production-scale: 1000 lines with explicit lifecycle, policy, evidence, audit, recovery, and settlement logic.

## Design

Deterministic state holds the parties, escrow ledger, lifecycle, evidence references, immutable audit sequence, policy thresholds, appeal windows, settlement basis points, and canonical verdict. Verification performs web fetch/render, screenshot inspection and optional image evidence inside a GenLayer consensus block. Validators compare only compact categorical fields, never raw HTML, screenshots, prose, or timestamps. This minimizes — but cannot guarantee elimination of — nondeterministic `UNDETERMINED` outcomes.

The expanded implementation separates four concerns: (1) covenant registration and immutable baseline references, (2) multimodal evidence acquisition and canonicalization, (3) challenge/appeal/recovery state transitions, and (4) deterministic escrow settlement with append-only audit records. Internal policy predicates are intentionally explicit so reviewers can inspect every acceptance and failure path.

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

No deploy command is included. Publish the exact same source to Explorer after the full release checklist passes.

The corrected Studio deployment record is in `evidence/DEPLOYMENT.md`. The first
deployment attempt is explicitly superseded because its constructor exposed a
runtime storage-allocation defect; only the corrected address in that record is
usable.
