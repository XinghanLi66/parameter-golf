# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-26` as a controlled positive refinement and discriminating seed-`2024` confirmation.

- Executed exactly as the reviewed brief requested:
  - created `runs/eval_007_arch010_legal_ttt_epochs4_seed2024_confirm`
  - copied the exact `eval_006` helper with no edits
  - reused the exact saved seed-`2024` `arch_010` checkpoint/export lineage unchanged
  - kept the winning TTT setting fixed at `TTT_LR=0.0025`, `TTT_EPOCHS=4`
  - changed only the evaluated artifact lineage from seed `1337 -> 2024`
- Identity guardrail passed before launch:
  - helper bytes: `84059`
  - helper `sha256`: `d93fc02cd20958d56d49af2df6b886527cef71d98ac46aa6304c4db048211bf8`
  - saved seed-`2024` `final_model.pt` bytes/hash: `106178569` / `302fe0ad739f19e51e35ecd6f55e5568009a31a2ead991fd3ebfbcf5be150987`
  - saved seed-`2024` `final_model.int6.ptz` bytes/hash: `15761090` / `479e5ccc5cb21d67fa937abb884fb63f1f812d99402b77b25fe32c2b9d838af3`
- Actual result:
  - post-export legal-TTT `sliding_window stride=64 val_bpb=1.11994397`
  - delta vs seed-`2024` legal-TTT baseline `1.12027199`: `-0.00032802`
  - delta vs same-script no-TTT parity baseline `1.12225535`: `-0.00231138`
  - delta vs `eval_006` seed-`1337` result `1.11935008`: `+0.00059389`
  - delta vs locked legal-TTT 3-seed mean `1.12010450`: `-0.00016053`
  - delta vs live SOTA `1.1194`: `+0.00054397`
  - script eval wallclock: `465406 ms`
  - managed wallclock: `506 s`
  - time deltas vs seed-`2024` locked `TTT_EPOCHS=3` run: `+65058 ms` script, `+65 s` managed
- Decision:
  - hypothesis confirmed on the discriminating seed
  - the run beats the primary decision baseline cleanly and lands in the brief’s “especially strong” band `<= 1.12010`
  - the run remains under the eval-time budget
  - this is strong enough to justify the final seed-`42` confirmation, but not yet enough to promote `TTT_EPOCHS=4` across the full line

## Recommended Follow-Up
Run the exact same locked-helper, locked-artifact `TTT_LR=0.0025`, `TTT_EPOCHS=4` eval-only confirmation on seed `42`. If that final seed stays positive and remains comfortably under the real eval budget, promote `TTT_EPOCHS=4` across the locked `arch_010` legal-TTT line; if not, stop nearby TTT-budget tuning.

## Experiment ID
`eval_007_arch010_legal_ttt_epochs4_seed2024_confirm`

## Category
- evaluation

Operational subtype: `locked legal-TTT cross-seed confirmation`

## Baseline / Comparison
Primary decision baseline:
- `eval_004_arch010_legal_ttt_seed2024_confirm`: `1.12027199`

Context baselines:
- same-script no-TTT parity on the same saved seed-`2024` artifact: `1.12225535`
- `eval_006_arch010_legal_ttt_epochs4_seed1337`: `1.11935008`
- locked legal-TTT 3-seed mean: `1.12010450`
- live SOTA: `1.1194`

## Hypothesis
If the `eval_006` gain reflects real remaining eval-time adaptation headroom rather than a seed-`1337` one-off, then applying the exact same locked `TTT_LR=0.0025`, `TTT_EPOCHS=4` setting to the saved seed-`2024` artifact should improve over the seed-`2024` legal-TTT baseline `1.12027199` while remaining under the practical eval-time budget.

## Why It Might Work
This is the narrowest remaining test of the current top-motif component that is still locally open: legal score-first TTT already transferred positively on all three locked seeds at `TTT_LR=0.002`, `TTT_EPOCHS=3`, and seed `1337` improved again when moved to `TTT_LR=0.0025`, `TTT_EPOCHS=4`. Seed `2024` is the strongest discriminating confirmation because it previously had the weakest absolute TTT landing of the three locked seeds.

## Minimal Intervention
Reuse the exact copied `eval_006` helper with no code edits and the exact saved seed-`2024` `arch_010` checkpoint/export lineage with no rewrite. Change only the evaluated artifact lineage relative to `eval_006`.

## Variables To Change
- saved export lineage under evaluation: `seed 1337 -> seed 2024`

## Variables To Hold Fixed
- exact copied legal-TTT helper code (`84059` bytes)
- exact saved seed-`2024` `arch_010` checkpoint/export lineage
- legal score-first scheduling
- `TTT_LR=0.0025`
- `TTT_EPOCHS=4`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `score_first=True`
- `last_chunk_untrained=True`
- `sliding_window stride=64`
- no training changes
- no export changes
- no artifact rewrite
- shim-free `physicslm`

## Success Metric
Primary readout:
- post-export legal-TTT `sliding_window stride=64 val_bpb` on the saved seed-`2024` artifact

Interpretation thresholds:
- positive confirmation: `< 1.12027199`
- especially strong: `<= 1.12010`
- exceptional: `< 1.1194`
- practical failure: eval materially approaches or exceeds the `10 min` limit without a compensating BPB gain

## Failure Interpretation
If seed `2024` is flat or worse than `1.12027199`, do not promote `TTT_EPOCHS=4` across the line. Interpret `eval_006` as a strong single-seed landing, not yet a robust recipe upgrade. If seed `2024` improves only trivially while eval cost rises materially again, treat the remaining headroom as too weak to justify broader promotion.

## Redundancy Check
- no retraining
- no export rewrite
- no helper code edit
- no same-script no-TTT parity rerun, because helper/artifact identity already proved the comparison was still valid
- no artifact rewrite
- no mixing with any training-side motif

## Execution Plan
1. Copy the exact `eval_006` helper into a fresh `eval_007` run directory.
2. Verify helper bytes/hash and saved seed-`2024` artifact bytes/hash match the locked lineage.
3. Run one managed 8-GPU eval-only job with `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and all other TTT settings fixed.
4. Compare primarily against `1.12027199`, then contextually against `1.12225535`, `1.11935008`, `1.12010450`, and `1.1194`.

## Expected Effect
If the `eval_006` gain reflects real remaining eval-time adaptation headroom rather than a seed-`1337` one-off, this round should produce a small but measurable improvement on the saved seed-`2024` artifact while staying comfortably under the practical eval cap.
