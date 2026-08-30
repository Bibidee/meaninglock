# MeaningLock Studio deployment record

## Historical deployment (superseded by current source changes)

- Network: GenLayer Studio Network
- Deployer account: `faultline-dev`
- Deployer address: `0x79b3Ecbe6a65beE93b2Fcda78e6909892671507F`
- Contract address: `0x45CA69FdF8C98839398Af62c0Fb2B690A4b9da81`
- Transaction hash: `0x01984b7f08aba1cdf1217bb1876bb30017d33f3da560a52aa329ac3c9c5af2f3`
- Consensus result: `MAJORITY_AGREE`
- Transaction status: `ACCEPTED`
- Constructor: minimum bond `1000000000000000000`, challenge window `86400`, recovery window `86400`

The source has since changed to add uncontested-expiry settlement, round-preserving
monitoring, challenge-bond minimums, component-safe payouts, bounded inputs, and
collision-safe evidence keys. Therefore this address is historical evidence only;
a fresh deployment is required before submission.

## Fresh deployment for closure source

- Network: GenLayer Studio Network
- Contract address: `0x05d6b9821473C103A183652F46fA34EdD69999dD`
- Deployment transaction: `0x38a2c151e867d11d85925d2ed90c6bf31710fd6ec20dfcb2911363be57db1d39`
- Source commit: `5e44e028c7228aaff65259f9d11a526a6bf18fdc`
- Local source SHA-256: `428742DD1A3CDA6D61955ADE2E0EB7FEF4E7BDAB672C70B5804B3E418A25FD35`
- Constructor consensus: `MAJORITY_AGREE`, transaction `ACCEPTED`
- Protocol read: `[false, '1000000000000000000', 86400, 86400]`
- Explorer source parity: confirmed equal after transport line-ending normalization; schema retrieved successfully.

## Final warning-free deployment

The settlement split was subsequently corrected so configured basis points are
actually applied to adverse principal with deterministic remainder allocation.
This is the current canonical deployment:

- Contract address: `0x0eF33abd47Acf477Ec45fD317A8091516CF4CA54`
- Deployment transaction: `0x287df0ae6d2855a594610fad6d8f50a34dcde2fa4beb48b2559e81281eaf966e`
- Source commit: `4f88132`
- Source SHA-256: `C73FDF8F220AFD2E0EB4CA2DFC5EB17838BB2DDF1389E38397D09A80CA1303FF`
- Constructor consensus: `MAJORITY_AGREE`, transaction `ACCEPTED`
- Schema extraction and source parity should be checked against this address before submission.

## Live verification

The read-only `get_protocol_config` call returned:

```text
[false, '1000000000000000000', 86400, 86400]
```

The deployed source returned by Studio matches the local source after normalizing
line endings and trailing transport whitespace. The deployed schema exposes the
same 39-method ABI generated locally.

## Live smoke test

- Read `get_protocol_config`: `[false, '1000000000000000000', 86400, 86400]`
- Write `set_paused(false)`: accepted with transaction hash `0xfd30eacdd2963508ea1dbfaf4a690b851b357bf07bbae3c26f99596c7aa8faf8`
- Post-write read: unchanged configuration, confirming the live write path and state persistence.

## Payable-flow smoke test

- Registration transaction: `0x98c1d4a30dc409f84e08a3b6d16f96ddbf9c9d374127d63cbaa07c57f28e1804` (1 GEN)
- Registered state: `[1,0,0,0,"1000000000000000000"]`
- Challenge transaction: `0x09bf934aac63662da0728ddcf275e0c3138f6817d52df4f94b19f0d01c2961b6` (0.001 GEN)
- Challenged state: `[2,0,0,0,"1001000000000000000"]`
- Verification transaction: `0x6a1af2eb7bbb2dbee7992c9a0d45c4a9c0dbcea056daf0e4d94e02d7b01c145d`
- Verification finalized as `MAJORITY_DISAGREE` because the intentionally missing live URL produced `WEBPAGE_LOAD_FAILED`; the covenant remains pending and no payout was emitted.
- Payout is correctly time-gated by the configured 86400-second challenge window, so timeout recovery was not eligible during this run.
- Temporary test keystores were removed after the run.

The payable-flow transactions above were executed against the immediately prior
deployment (`0x83a93a6db193da82AC7f6B2e6B93b24A5BA2A2a4`), whose code is identical
except for the defensive `get_payout` read fix. That prior address is superseded;
the canonical address for new use is the one in the deployment header.

The same payable sequence was then rerun against the canonical deployment:

- Registration: `0x37ecafad7bb3b459dea070284f273dcf3bff4f07a4f8c1c73f4646e532da0c61` — accepted, 1 GEN credited.
- Challenge: `0xa3b3381654954c9855a864c643d2fcc365314d1e0df31ff37b3bdbfbee0a8c63` — accepted, 0.001 GEN credited.
- Verification: `0xf522d19622fc06c1afc90dd60c9b1cf6116e7aec3cdba98c86786e4961969d7a` — finalized `MAJORITY_DISAGREE` on the intentionally unavailable URL; state remains pending and escrow remains `1001000000000000000` wei.
- The corrected `get_payout(1)` path now returns a safe unpaid record instead of raising a storage `KeyError`.

A follow-up valid-URL semantic-change run was also submitted for covenant 2:
registration `0x29dba5034832de07dd4381fb90f0bf6bc336c69a93f1f257300fa7a2f996d0f5`,
challenge `0xb04ee479b37bce9ffd659893f62c14361f6baf87a61dbb9e0cc32d7f814db605`,
and verification `0xfde8535b41d2fc357591a5f0f529d1232968fb348f047f83184ab4d24ad54cd2`.
At the time of this release check, verification remained in Studio processing
status 5; no payout claim was submitted without a finalized adverse verdict.

That verification later finalized `MAJORITY_AGREE` with an adverse verdict:
`get_status(2)` returned `[3,2,2,2,"1001000000000000000"]`. The beneficiary then
claimed the escrow in transaction
`0x522fb484879b23ce48fd648a44d77fbf2e9ecbb75bac05ff2623de9891624cdc`.
The accepted claim returned `get_payout(2)` as
`[true,"0xae82effe54dccfd170d9a08eee128339a70347f7","1001000000000000000","adverse settlement"]`,
confirming the ledger was zeroed and marked paid before the transfer emission.

## Superseded attempts

The first transaction (`0x46ca7de7451de1d4b71395788a05eecf2101ee2d4b97fa57b5ba475cc8a6f3c2`, address `0xD27e2436980E78E21180E82c706e33A075FEe68C`) reached majority agreement but its constructor failed on every execution path because untyped `TreeMap()` values were assigned to typed storage descriptors. It must not be used. The corrected source uses `gl.storage.inmem_allocate(TreeMap[K, V])` for every persisted map and was deployed at the address above.

The intermediate deployments `0x637DFc653a9508984b933ebF9CAeE0Ce51240Be8`, `0x94874646E3fB1F63087222a228e9DbE9D52c7432`, and `0x83a93a6db193da82AC7f6B2e6B93b24A5BA2A2a4` are superseded and must not be used.

## Final closure deployment

### Terminal-state closure deployment (current)

- Contract address: `0x4ff0a1C8c240E8685cDe19491BA2F04B21a21C48`
- Deployment transaction: `0x41bf7108d5d217f6a6102a863f6d86bd9fbfeeecd29899415e95e210ba92eb90`
- Constructor parameters: `1000000000000000000, 86400, 86400`
- Constructor consensus: `MAJORITY_AGREE`, transaction `ACCEPTED`
- Source SHA-256: `668800422EFE8B64D5A0ACCFF07D59B92CCD049EB5117562D5F93E86E8437FFE`
- Schema extraction: successful (44 methods, 24 views, 20 writes)
- Protocol read: `[false, '1000000000000000000', 86400, 86400]`
- Explorer/source parity: confirmed byte-for-byte after transport line-ending normalization.
- Source length: 1,319 physical lines.

### Final canonical payable lifecycle proof

All transactions below use only the canonical address
`0x4ff0a1C8c240E8685cDe19491BA2F04B21a21C48` and the frozen source.

- Registration: `0x697a6bc173a73138ca94cff80f4c993a9e45d55d9045727a30f6fff98246f0a5`
  (publisher `0x79b3Ecbe6a65beE93b2Fcda78e6909892671507F`, 1 GEN, finalized
  `MAJORITY_AGREE`). The returned covenant ID is `1`.
- Registration read: `get_status(1) = [1, 0, 0, 0, "1000000000000000000"]`.
- Challenge: `0xc347e352b2bf111d4e858e977da5a74b0b72a8bf6324bd46ddf3e3c3fca21663`
  (distinct challenger `0xae82EFfe54dCcfd170d9a08EeE128339A70347f7`, 1 GEN,
  finalized). Readback: `get_status(1) = [2, 1, 0, 2, "2000000000000000000"]`,
  `get_review_type(1) = 1` (`ROUND_CHALLENGE`).
- Verification: `0x3ab1a49b7a4db3f41e9ab8a016efcc5612d2ca12613f5ca0d580825bd72575e1`,
  finalized `MAJORITY_AGREE`.
- Final readback: `get_status(1) = [1, 1, 0, 2, "1000000000000000000"]`,
  `get_review_type(1) = 0` (`ROUND_NONE`), and
  `get_deadlines(1) = [1788683598, 0, 0, 0]`.

This proves the final-address payable registration/challenge/verification
path, challenger resolution, preserved verdict, cleared terminal review type,
and publisher principal remaining locked. The executable Direct Mode suite
independently proves adverse settlement, UNVERIFIABLE recovery, appeal
finality/timeout, repeated preserved rounds, multimodal evidence, escrow
conservation, and audit-cap liveness (`15 passed, 3 skipped`).

The environment-configured integration test also passed against this address,
reading `get_protocol_config` and `get_status(1)` over the Studio RPC.

This is the sole canonical submission address. It supersedes
`0xFe25f083c550268bd7e164EECe218F73f66b3E18` because the terminal-state
closure source changed.

The deployment below supersedes every earlier address in this file and is the
only address that matches the final closure source:

- Contract address: `0xFe25f083c550268bd7e164EECe218F73f66b3E18`
- Deployment transaction: `0x3c7c665893c44eeda12f75697571405cd2986ad010bbd78a3020d5dea2ae42c8`
- Source SHA-256: `77337CAE1BE5E4AB39EE77B783F14B57DF1E52D71AB52B4C23CA418A0E94F3AC`
- Constructor consensus: `MAJORITY_AGREE`, transaction `ACCEPTED`
- Protocol read: `[false, '1000000000000000000', 86400, 86400]`
- Schema extraction: successful (44 methods, 24 views, 20 writes)
- Explorer source parity: confirmed byte-for-byte after normalizing transport line endings.
- Source length: 1,298 physical lines; no generated padding.

This final source adds explicit challenge/appeal round typing, per-covenant
window snapshots, caller-independent timeout recovery, bounded appeal finality,
strict unverifiable recovery, source-bucket payout accounting, and audit-cap
liveness safeguards. The older closure deployment immediately below is
superseded because the source changed.

- Contract address: `0xAc49136B2d1243b3a06DF17F061CE11241aAC8eC`
- Deployment transaction: `0x4ce8d3efa46dfe78fdaee694946e45832949c94bdd695c2296201b2628945be9`
- Source SHA-256: `83DD0162674EEB8E7136046C2B5975357B0DD13E8C8D79AACD96399FF0EE2270`
- Constructor consensus: `MAJORITY_AGREE`, transaction `ACCEPTED`
- Protocol read: `[false, '1000000000000000000', 86400, 86400]`
- Schema extraction: successful (40 methods, 21 views, 19 writes)
- Explorer source parity: confirmed after normalizing transport line endings.
