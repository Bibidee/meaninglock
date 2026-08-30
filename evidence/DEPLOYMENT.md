# MeaningLock deployment evidence

## CURRENT CANONICAL DEPLOYMENT

**Pending fresh deployment.** The previously deployed address below is retained
as historical evidence only because the contract source changed in the final
security pass. It must not be presented as the canonical deployment until the
new source is deployed and Explorer parity is confirmed.

- Network: GenLayer Studio Network
- Address: `0x689Af928b6E030a5b0881f0B141f74ADcA7f7497` (superseded pending fresh deployment)
- Deployment transaction: `0x2959d6c807c88e166def8bef85b725497a7979acc1cc7810be9c602fdc5b9f44`
- Updated source commit: `96487cb8620c82c3900f0ceb2daf89e5795b1781`
- Updated contract SHA-256: `F64A3F4254AD867338E351E18939CDFCD3785AD481AC32576E473D23C22309A7`
- Constructor: minimum bond `1000000000000000000`, challenge window `86400`, recovery window `86400`
- Constructor consensus: `MAJORITY_AGREE`; transaction status `ACCEPTED`
- Updated schema: 47 methods (26 view, 21 write)
- Protocol read: `[false, "1000000000000000000", 86400, 86400]`
- Explorer source parity: confirmed byte-equivalent after line-ending normalization.

## HISTORICAL PAYABLE LIFECYCLE PROOF (SUPERSEDED ADDRESS)

All transactions below are on the canonical address above.

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
- `genvm-lint validate`: passed; 44 methods
- `genvm-lint schema`: written successfully
- `genvm-lint typecheck`: no type errors
- Direct Mode: 26 passed, 2 skipped (including targeted semantic-verdict equivalence and malformed-record normalization)
- Plain integration pytest: 1 skipped when no live `MEANINGLOCK_ADDRESS`/RPC environment is configured; canonical payable lifecycle evidence is recorded above.
- Full release script: structural checks passed

## EXPLORER ERROR REVIEW

The canonical address has only successful user-initiated deployment,
registration, challenge, and verification transactions. Internal validator
`ERROR`/`idle` diagnostics were present in the consensus receipt but did not
prevent final `MAJORITY_AGREE` or mutate the transaction outcome.

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
