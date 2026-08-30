# MeaningLock

MeaningLock is a standalone GenLayer Intelligent Contract primitive for locking GEN behind a public covenant whose material meaning must remain intact. It is a reusable primitive, not a frontend product. Correctness, deterministic settlement, and auditable lifecycle rules take priority over source length.

## Design

Deterministic state holds the parties, escrow ledger, lifecycle, evidence references, immutable audit sequence, policy thresholds, appeal windows, settlement basis points, and canonical verdict. Verification performs web fetch/render, screenshot inspection and optional image evidence inside a GenLayer consensus block. Validators compare only compact categorical fields, never raw HTML, screenshots, prose, or timestamps. This minimizes — but cannot guarantee elimination of — nondeterministic `UNDETERMINED` outcomes.

MeaningLock defines validator equivalence over the final covenant-specific verdict
after deterministic policy reduction. Impact, confidence, and topic-mask fields
are diagnostic metadata from the accepted consensus record and are not required
to be byte-identical across validators. Small LLM metadata differences therefore
do not create an unnecessary `MAJORITY_DISAGREE`; the economic and lifecycle
boundary is the reduced final verdict. These metadata fields are exposed for
auditability and policy reduction during verification, but do not later authorize
settlement, alter payout amounts, bypass appeals, or change escrow accounting.

The implementation separates registration and frozen terms, multimodal evidence acquisition, round-based challenge/appeal/recovery transitions, and deterministic escrow settlement with append-only audit records. Publisher collateral and challenger collateral are tracked independently; terminal actions can only return each component to its owner or route the publisher security deposit to the beneficiary after final adverse settlement. Adverse principal uses the configured publisher/beneficiary/challenger basis-point split (exactly 10,000 bps), with deterministic remainder allocation.

Registration stores an explicit 64-hex baseline commitment alongside the immutable
statement/topics and baseline reference. A pre-participation baseline update must
replace the reference and commitment atomically; after the first challenge the
baseline is frozen. Publisher/beneficiary identities must differ, while payout
roles are explicit so address overlap cannot corrupt accounting.

Live-source changes are delayed migrations: the old URL remains the adjudicated
source during the challenge window, every activated version is append-only in
source history, and a pending migration is cancelled when participation begins.
Cancellation is disabled after registration, removing the publisher cancellation
race against prospective challengers. Evidence is always delimited as untrusted
data in the adjudication prompt, including page text, screenshots, and challenge
references.

## Lifecycle

`ACTIVE → PENDING (review round) → ACTIVE (preserved/timeout) → PENDING ... → RESOLVED (adverse appeal window) → CLOSED`.
Uncontested expiry is claimable by the publisher. Preserved reviews do not terminate monitoring. Appeals replace the canonical evidence context and keep adverse settlement locked until the appeal deadline.

Pending review state always takes precedence over historical verdict state: a
previous `PRESERVED` verdict cannot authorize expiry settlement while a later
challenge or appeal is pending. Adverse settlement is permissionless after
finality; the contract, not the caller, determines recipients and amounts.

Payout uses one `_send_gen` helper for checks-effects-interactions. It debits an explicit source bucket, records each partial transfer in the audit log, and closes only when all outstanding escrow reaches zero. No transfer mode is assumed beyond the current GenLayer payable-message API.

### Review finality

Each covenant exposes an explicit review type: `ROUND_NONE` (no active
review), `ROUND_CHALLENGE` (ordinary challenge), or `ROUND_APPEAL` (bounded
appeal). Completed verification always returns to `ROUND_NONE`. A preserved
ordinary review refunds challenger collateral and resumes `ACTIVE`; an adverse
review becomes `RESOLVED`, keeps an appeal grace period, and can settle only
after that period. An ordinary challenge timeout resolves only that review and
returns monitoring to `ACTIVE` while the publisher principal remains locked.
If the covenant later expires cleanly, uncontested expiry remains executable
even after earlier timed-out rounds.

Appeal verification can overturn an adverse result, retain an adverse result,
or restore the prior adverse result when appeal evidence is unverifiable. Once
`MAX_APPEALS` is reached no unusable extra appeal window is created. An appeal
timeout restores the saved pre-appeal adverse verdict and leaves settlement
available after finality.

`UNVERIFIABLE` is a completed ordinary review result only when the validators
cannot support a safe category. It enters `RESOLVED + ROUND_NONE` with a
recovery deadline; recovery is blocked before that deadline and returns both
escrow components afterward. Registered covenants snapshot the challenge and
recovery windows, so owner changes affect future covenants only. The bounded
audit store stops recording at its cap without reverting economic exit paths.

The appeal limit is covenant-lifetime scoped: `appeal_count` is monotonic and
does not reset when monitoring resumes after a successful appeal. Live-source
refreshes are delayed migrations: the prior URL remains active during the
challenge window, activated versions are append-only in source history, and a
pending migration is cancelled when participation begins. The baseline and
frozen covenant semantics remain governed separately.

## Layout

- `contracts/meaning_lock.py` is the only deployable source.
- `tests/direct/` and `tests/integration/` are outside `contracts/` so lint/schema extraction cannot mistake them for contracts.
- `scripts/release_check.ps1` verifies source isolation and the single transfer-emission helper invariant.

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

The Studio deployment history and canonical deployment evidence are in
`evidence/DEPLOYMENT.md`. Historical addresses are explicitly marked
`SUPERSEDED`; use only the address in its `CURRENT CANONICAL DEPLOYMENT`
section after checking Explorer source parity.
