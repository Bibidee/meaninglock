# MeaningLock deployment evidence

## CURRENT CANONICAL DEPLOYMENT

- Network: GenLayer Studio Network
- Address: `0xEED34BF9054C82622FB6BA62A10546D291F15c8B`
- Deployment transaction: `0xdf42855f6ea768e04266eae2490fc5cb810f99e1176feee00abcaf21311b4da6`
- Source commit: `6307be8edd6cae56344a12b83f46369d172da36b`
- Contract SHA-256: `5A741D898C404F01CB78CAEE9826E2FB332DA0464440D4263424C96FBDF7180B`
- Constructor: minimum bond `1000000000000000000`, challenge window `86400`, recovery window `86400`
- Constructor consensus: `MAJORITY_AGREE`; transaction status `ACCEPTED`
- Schema: 44 methods (24 view, 20 write)
- Protocol read: `[false, "1000000000000000000", 86400, 86400]`
- Explorer source parity: confirmed byte-equivalent after line-ending normalization.

## FINAL CANONICAL PAYABLE LIFECYCLE PROOF

All transactions below are on the canonical address above.

- Covenant ID: `2` (fresh active covenant; ID 1 was used by an earlier retry and is historical test state)
- Publisher: `0x79b3Ecbe6a65beE93b2Fcda78e6909892671507F`
- Challenger: `0xae82effe54dccfd170d9a08eee128339a70347f7`
- Registration transaction: `0xf7d257400e045b503312ae58ab3e277cd1e4868e3a14a003efa258cbc643a667`
- Registration read: `ACTIVE`, verdict `NONE`, review type `ROUND_NONE`, escrow `1000000000000000000`
- Challenge transaction: `0x0fb374f1ce0650c90411a6eee854f9dc96e822d8746e42bae10d258d18b757b0`
- Challenge read: `PENDING`, review type `ROUND_CHALLENGE`, escrow `2000000000000000000`
- Verification transaction: `0xc7f73d1b5da75c133433eb3965656a547395e7402184aa0f5e3eda495d9c8907`
- Verification consensus: `MAJORITY_AGREE`
- Final verdict: `PRESERVED`
- Final read: `ACTIVE`, verdict `PRESERVED`, review type `ROUND_NONE`, escrow `1000000000000000000`
- Challenger bond was resolved and publisher principal remained locked.

## VALIDATION AND TEST EVIDENCE

- `genvm-lint check`: passed (3 checks)
- `genvm-lint validate`: passed; 44 methods
- `genvm-lint schema`: written successfully
- `genvm-lint typecheck`: no type errors
- Direct Mode: 20 passed, 2 skipped
- Full release script: structural checks passed

## EXPLORER ERROR REVIEW

The first payable-proof retry on this deployment used covenant `1` and ended
with transaction `0x9dc40e4c69d9575d9ecc36e9d85109e51fe1eae84bf6926c5da229a5ece34ff7`.
The resulting read was `RESOLVED + UNVERIFIABLE + ROUND_NONE` with escrow still
`2 GEN`; no payout occurred. The available receipt does not conclusively prove
whether this was validator disagreement or unavailable evidence, so it is not
labelled intentional. It is historical test state and is excluded from the
canonical payable proof, which uses covenant `2`.

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
