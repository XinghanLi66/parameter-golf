# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Experiment ID
`pending_opt_009_arch010_parallel_muon_seed1337_nottt`

## Category
- optimization

Operational subtype: `training-side current-#1 motif isolation`

## Baseline / Comparison
Locked non-TTT `arch_010` references:
- `arch_010_record02_leakyrelu2_keep_cudnn_recipe` seed `1337`: `1.12211549`
- `repro_006_record02_leakyrelu2_seed42_confirm` seed `42`: `1.12281449`
- `repro_007_record02_leakyrelu2_seed2024_confirm` seed `2024`: `1.12225480`
- locked exact 3-seed mean: `1.12239493`

Locked evaluation-side TTT references on the same export lineage:
- `eval_002_arch010_legal_ttt_seed1337_export_eval`: `1.11971476`
- `eval_003_arch010_legal_ttt_seed42_confirm`: `1.12032675`
- `eval_004_arch010_legal_ttt_seed2024_confirm`: `1.12027199`
- exact TTT 3-seed mean: `1.12010450`

Relevant frontier references:
- live `#1`: `1.1194` with `LeakyReLU² + Legal Score-First TTT + Parallel Muon`
- strongest local unmatched live-`#1` motif: `Parallel Muon`

## Hypothesis
If the remaining miss to live SOTA on the locked `arch_010` line is now mainly the missing training-side optimizer/runtime motif from the current `#1` stack, then adding only `Parallel Muon` to the locked seed-`1337` `arch_010` recipe should improve the standard no-TTT post-export `sliding_window stride=64 val_bpb` by at least `-0.0005`.

## Why It Might Work
The reviewed TTT question is now answered across all three locked saved export seeds, so the next unresolved current-`#1` motif is `Parallel Muon`. The live record note describes it as part of the winning training-side stack, and it is the clearest remaining single variable that can be tested without changing architecture, export schema, or evaluation legality again.

## Minimal Intervention
Fork the exact locked `arch_010` training script and change only the optimizer/runtime path needed to reproduce `Parallel Muon`. Keep architecture, activation, export, tokenizer/data, and standard no-TTT exported evaluation fixed.

## Variables To Change
- optimizer/runtime implementation only:
  - current local cuDNN-backed `arch_010` optimizer path
  - `->` `Parallel Muon` transfer

## Variables To Hold Fixed
- locked `arch_010` architecture and export stack
- `SEED=1337` for the first controlled transfer
- `LeakyReLU(0.5)^2`
- `11L / 512 / 8 heads / 4 KV heads / MLP3x`
- `XSA_LAST_N=4`
- `ROPE_DIMS=16`
- `LN_SCALE=1`
- `VE128`
- `BigramHash(2048,128)` and `SmearGate`
- `EMA decay=0.997`
- `SWA_EVERY=50`
- `WARMDOWN_ITERS=3500`
- late QAT threshold `0.15`
- GPTQ-lite int6 export lineage and container path
- tokenizer/data paths
- shim-free `physicslm`
- managed 8-GPU launch
- evaluation protocol `sliding_window stride=64`
- no legal-TTT in the primary readout
- no architecture edits
- no export-schema edits

## Success Metric
Primary readout:
- post-export no-TTT `sliding_window stride=64 val_bpb` on seed `1337`

Primary comparison:
- beat locked seed-`1337` non-TTT baseline `1.12211549`

Interpretation thresholds:
- strong positive: gain `<= -0.0010`
- useful positive: `-0.0010 < gain <= -0.0005`
- weak / likely non-actionable: `-0.0005 < gain < 0`
- null or negative: `>= 0`

## Failure Interpretation
If the `Parallel Muon` transfer does not beat the locked no-TTT baseline, then the remaining local gap is unlikely to be solved by porting that optimizer path alone, and the next refinement should shift to a different single motif rather than bundling more training/runtime changes into `arch_010`.

## Redundancy Check
- Do not spend another round on more seed-only legal-TTT confirmation; that question is now answered across all three locked saved export seeds.
- Do not bundle `Parallel Muon` with `Parameter Banking`, different `BigramHash`, or a new evaluation path in the same first transfer.
- Do not make legal-TTT the primary readout for the first `Parallel Muon` test; keep the training-side effect interpretable first.

## Execution Plan
1. Fork the locked `arch_010` script into a new run directory.
2. Implement only the `Parallel Muon` transfer needed for a controlled training-side comparison.
3. Run one managed 8-GPU smoke if required by the implementation change.
4. Run one managed 8-GPU full seed-`1337` training/export evaluation under the standard no-TTT exported readout.
5. Compare the result directly against the locked seed-`1337` non-TTT baseline and against live SOTA context.

## Expected Effect
If `Parallel Muon` is the remaining missing training-side piece of the current `#1` stack, this round should produce a measurable no-TTT gain on the locked `arch_010` line and justify a later follow-up that evaluates the improved artifact under the already-locked legal-TTT regime.
