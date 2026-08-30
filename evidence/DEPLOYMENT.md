# MeaningLock deployment evidence

## CURRENT CANONICAL DEPLOYMENT (CORRECTED SOURCE)

The newest frozen-source deployment is the sole canonical submission address.
Its complete payable lifecycle proof is finalized and source-matched.

- Address: `0x74FB9B259a3BC0d8852de0c2597952360903294e`
- Deployment transaction: `0xa5dad7eca10b63dd76630ead7a465d4d5fc84df01e576c0b748f960fc42b8e12`
- Source commit: `b8ec382da301ad2358a674e517da45bd3331d326`
- Contract SHA-256: `8E71D9660853E3D0364B994B3F0849EDBF0F93A04F37B81B60F2F0CC35B6F022`
- Constructor: `1000000000000000000`, `86400`, `86400`; deployment `FINALIZED`, consensus `ACCEPTED`
- Schema: 50 methods (28 view, 22 write)
- Covenant 1 registration: `0x27a0dfef5c693cbb649f53252aad8134a1b0c30c8252c92a09daa782aafa742f` — `FINALIZED`
- Covenant 1 activation: `0x0a84acc919434648a7873563d3bfa76e02ea09ed2aec2bac52b74ff4fa5b1034` — `FINALIZED`
- Covenant 1 challenge: `0xb40543d6fa8ad9f04bed516ede3c5fe475e65677d9837771ddd33723203ce256` — `FINALIZED`, `SUCCESS`
- Covenant 1 verification: `0x6b43b5f75b62aff44e402f508a3c949109a1413a23a708c2c1c560a45eea5fa2` — `ACCEPTED`, `SUCCESS`, consensus `Accepted`
- Final read: `ACTIVE`, verdict `PRESERVED`, review type `ROUND_NONE`, escrow `1000000000000000000`
- Payout totals: total `1000000000000000000`; publisher `0`; beneficiary `0`; challenger `1000000000000000000`
- Challenger bond: returned/resolved (`0` remaining); publisher bond: locked (`1000000000000000000` remaining)
- Protocol read: `[false, "1000000000000000000", 86400, 86400]`
- Explorer source parity: confirmed against the frozen source commit and SHA-256 above.
- CI: successful workflow run `33335268486` on final HEAD; Direct Mode `35 passed, 2 skipped`.


- Network: GenLayer Studio Network
- Address: `0x40336e78de0ecc6d92c6d863a02d9f5775ce4c1c`
- Deployment transaction: `0x40336e78de0ecc6d92c6d863a02d9f5775ce4c1cf71ad135d937b900430e8d61`
- Source commit: `010c2ffb60c574ad3baddd6a80649132ce6846d1`
- Contract SHA-256: `65C376CD63FDBB9C46151B22D6103CAD4A0E106862526B27DF275D2269DCC9F3`
- Constructor: `1000000000000000000`, `86400`, `86400`; deployment `FINALIZED`, consensus `ACCEPTED`
- Schema: 50 methods (28 view, 22 write), including `get_challenge_source_version` and `get_round_evidence_reference`
- Live covenant ID: `1`
- Registration: `0x548152cb42dc272fc74c20961deedb6f890440decad3dd06f8973adb85d8df9a` — `FINALIZED`
- Activation: `0x6bf5894a2b7b853fe2c1866ccf65d4984543b08d1139840b7740c39141a14d07` — `FINALIZED`
- Challenge: `0xd09bbdf4ae60dc42c0cd8d1e0d2aaf4eb88416372c249f85009d4514225c1e44` — `FINALIZED`
- Verification: `0xa742f13823afe3e5ac0beb16d6569d084a98f6c2833960891203b7c64411b1d4` — `FINALIZED`, `ACCEPTED`
- Final read: `ACTIVE`, verdict `PRESERVED`, review type `ROUND_NONE`, escrow `1000000000000000000`
- Challenger bond was resolved; publisher principal remains locked.

## HISTORICAL DEPLOYMENT (SOURCE-PREVIOUS)

> **Superseded historical deployment.** The corrected source has since been
> validated and freshly deployed at the canonical address above. Do not use
> this address for submission.

The deployment below is superseded historical evidence for the final hardening
source. It is not the canonical submission address.

- Network: GenLayer Studio Network
- Address: `0x7ef7f667ceC8DB0d68b6E0c11263c97Af0238109`
- Deployment transaction: `0xb2640d352c5a0369007e1e0fb26923236959a87fc418095dfb042cfc2a673bfb`
- Updated source commit: `abcac704ce995a890461da548a8f8464bd58c3c7`
- Updated contract SHA-256: `DA1C66BC66A3D3C2E57248B9B2502E2F29928EA4E2AF2F1A7EAC6CA68BBA1B36`
- Constructor: minimum bond `1000000000000000000`, challenge window `86400`, recovery window `86400`
- Constructor consensus: `MAJORITY_AGREE`; transaction status `ACCEPTED`
- Historical schema: 48 methods (26 view, 22 write)
- Protocol read: `[false, "1000000000000000000", 86400, 86400]`
- Explorer source parity: confirmed; Explorer exposes the final source and 48-method ABI.

## FINAL PAYABLE LIFECYCLE PROOF

- Covenant ID: `1`
- Publisher: `0x3506660bF99b7517e941ae6CAEF16DCa2428d691`
- Challenger: `0x607AD92a6B771745E6046bC0A5F4329e3a521309`
- Registration transaction: `0xb6ce2a77cd97b86e63074c6e377dcea17afb9194b751c57cd90e9140e5e89e05` — `FINALIZED`, `SUCCESS`
- Activation transaction: `0x595159ebdfc66376750839f2a64e920c82affd774ad10643715c748e5745a307` — `FINALIZED`, `SUCCESS`
- Challenge transaction: `0xcab24631568136b10b7b1b7fd07bcd88429ec359828ad3b3fc8407bcd777537c` — `FINALIZED`, `SUCCESS`
- Verification transaction: `0x19be2a691d10d7f2758c78e9505f7b584a540b4eece5a7dedcce3e198e282896` — `FINALIZED`, `SUCCESS`
- Verification consensus: `Accepted`; deterministic result `UNVERIFIABLE` (baseline commitment mismatch safely prevented a trusted verdict)
- Final read: `RESOLVED`, verdict `UNVERIFIABLE`, review type `ROUND_NONE`, escrow `2000000000000000000`
- No failed user-initiated writes exist on this canonical address.

## FAILED REPLACEMENT ATTEMPTS (NOT CANONICAL)

- `0x6c127b25a340Bce9b57d342993cA59CCf5280849` — deployment
  `0xd3f95fc6399f0be3a9eda96cd78614b3dd63e38579611137550de2ed55fc4b97`;
  registration `0x294d13883d163c00c9051515136e5fa6acfa1d11fbf138f6d3eb254903432ae3`
  finalized with a GenVM `Address(int)` conversion error.
- `0xdEd8c00B613af1f5C0Ae461c32ABd2E117298669` — deployment
  `0x742ca2f7a21cd30d30017cdfca60e42afde9ba0788b399966ad6dcbcb78c15f3` finalized,
  but Studio emitted schema-generation indentation diagnostics; no writes were attempted.

## HISTORICAL PAYABLE LIFECYCLE PROOF (SUPERSEDED ADDRESS)

These transactions belong to the superseded pre-hardening deployment
`0x689Af928b6E030a5b0881f0B141f74ADcA7f7497`.

- Covenant ID: `1`
- Publisher: `0x79b3Ecbe6a65beE93b2Fcda78e6909892671507F`
- Challenger: `0xae82effe54dccfd170d9a08eee128339a70347f7`
- Registration transaction: `0xf25a454c57511b787ac7b4bbe3c8a82a0a67a54c2b8b75e62505a3bcb35b638e`
- Registration read: `ACTIVE`, verdict `NONE`, review type `ROUND_NONE`, escrow `1000000000000000000`
- Challenge transaction: `0x01f47341c2df44e04304742aa152c61074e528855cc331844036abafa07dbb37`
- Challenge read: `PENDING`, review type `ROUND_CHALLENGE`, escrow `2000000000000000000`
- Verification transaction: `0x79cca66941809c450efdbd8f6914997ba9bc02d7cb912aaea42ae8d3af45f6a4`
- Verification consensus: `MAJORITY_AGREE`
- Final verdict: `PRESERVED`
- Final read: `ACTIVE`, verdict `PRESERVED`, review type `ROUND_NONE`, escrow `1000000000000000000`
- Challenger bond was resolved and publisher principal remained locked.
- Evidence source: immutable raw GitHub file pinned to commit `5226426d2627f4f3c54bcdaf7e024961df31c284`.

## VALIDATION AND TEST EVIDENCE

- `genvm-lint check`: passed (3 checks)
- `genvm-lint validate`: passed for the historical source; 48 methods (26 view, 22 write)
- `genvm-lint schema`: written successfully
- `genvm-lint typecheck`: no type errors
- Direct Mode: 35 passed, 2 skipped (including targeted semantic-verdict equivalence, baseline mismatch, and DRAFT lifecycle coverage)
- Plain integration pytest: 1 skipped when no live `MEANINGLOCK_ADDRESS`/RPC environment is configured; canonical payable lifecycle evidence is recorded above.
- Full release script: structural checks passed

## EXPLORER ERROR REVIEW

The canonical address has only successful user-initiated deployment,
registration, challenge, and verification transactions. Internal validator
`ERROR`/`idle` diagnostics were present in the consensus receipt but did not
prevent final `MAJORITY_AGREE` or mutate the transaction outcome.

## LIVE-EVIDENCE LIMITATIONS (CURRENT PASS)

The canonical deployment has a successful semantic verification, but that
verification safely resolved `UNVERIFIABLE` because the supplied baseline
commitment did not match the rendered remote document. A follow-up attempt to
register a second covenant was rejected by Studio before contract execution:
its schema runner loaded an unrelated stale `ClaimVerifier` artifact. No
transaction hash was created by that attempt, and no retry was issued.

The repository's Direct Mode suite remains the authoritative executable proof
for adverse settlement, appeal finality, timeout recovery, repeated preserved
rounds, audit-cap liveness, and multimodal mocks. A fresh live `PRESERVED`
receipt and live adverse/appeal/recovery writes still require a healthy Studio
schema/runtime session and funded wallets; they are not claimed here.

## SUPERSEDED DEPLOYMENTS

The following addresses are historical and must not be used as the submission address:

- `0x0894953D7d3abf45Eb28713a0d03eb587ae20aDA` — superseded by the timeout-to-expiry correction.
- `0x4ff0a1C8c240E8685cDe19491BA2F04B21a21C48` — superseded prior canonical deployment.
- `0x45CA69FdF8C98839398Af62c0Fb2B690A4b9da81` — initial historical deployment.
- `0x05d6b9821473C103A183652F46fA34EdD69999dD` — superseded closure deployment.
- `0x0eF33abd47Acf477Ec45fD317A8091516CF4CA54` — superseded settlement deployment.
- `0x1a8161F5f593b73536cbef75a3569ff71a2D7406` — superseded; challenge receipt rolled back as `inactive or expired`.
- `0x120Cf583bC1f563Af0686B3aDbF8f90b85fd64A0` — superseded; verification finalized `MAJORITY_DISAGREE` / `UNVERIFIABLE`.
- `0xc7754290690596D4e0Ba8b6E453A2cDc718fcfB2` — superseded; verification finalized `MAJORITY_DISAGREE` and remained pending.
- `0x7b18134d65d2E271BDEBCD5A2A42B2df587CfF32` — superseded; static-content verification finalized `MAJORITY_DISAGREE` / `UNVERIFIABLE`.
- `0xEED34BF9054C82622FB6BA62A10546D291F15c8B` — superseded by semantic-verdict equivalence correction.
- `0xf10696275B6847fA328E24e8A82ddBb2337Cf525` — superseded; verification reached `MAJORITY_AGREE` but classified the README evidence as `UNVERIFIABLE`.
