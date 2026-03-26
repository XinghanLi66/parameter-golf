# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Experiment ID
`pending_eval_002_arch010_legal_ttt_seed42_confirm`

## Category
- evaluation

Operational subtype: `same-script second-seed TTT confirmation`

## Baseline / Comparison
New strongest local evaluation result from this round:
- `eval_002_arch010_legal_ttt_seed1337_export_eval`
- same-script no-TTT recovery on saved seed-`1337` export lineage: `1.12211550`
- same-script `Legal Score-First TTT` on the same saved seed-`1337` export lineage: `1.11971476`
- TTT gain: `-0.00240074`
- artifact bytes: `15555121`
- code bytes: `84059`
- total bytes: `15639180`

Exact non-TTT locked references:
- `arch_010_record02_leakyrelu2_keep_cudnn_recipe` seed `1337`: `1.12211549`
- `repro_006_record02_leakyrelu2_seed42_confirm` seed `42`: `1.12281449`
- `repro_007_record02_leakyrelu2_seed2024_confirm` seed `2024`: `1.12225480`
- locked exact 3-seed mean: `1.12239493`

Relevant frontier references:
- live `#1`: `1.1194`
- documented record-`#2` seed `1337`: `1.12278022`

## Hypothesis
If the strong seed-`1337` evaluation-only TTT gain is a real transfer on the locked `arch_010` export lineage rather than a favorable one-seed landing, then applying the exact same same-script parity-plus-TTT protocol to the saved seed-`42` export lineage should again beat the recovered same-script no-TTT baseline by at least `-0.0008`.

## Why It Might Work
The seed-`1337` TTT result was not a marginal win; it was a clean parity-qualified gain of `-0.00240074`, which is close to the record-`#1` note’s reported `-0.0025`. That is large enough that the next most useful question is robustness of the evaluation-side transfer, not another new motif.

## Minimal Intervention
Keep the exact `eval_002` run-local script and the fixed TTT recipe unchanged. Change only the saved artifact lineage under evaluation from seed `1337` to seed `42`, and again run no-TTT parity before the TTT candidate.

## Variables To Change
- saved export lineage under evaluation only: seed `1337 -> 42`

## Variables To Hold Fixed
- exact `runs/eval_002_arch010_legal_ttt_seed1337_export_eval/train_gpt.py`
- `TTT_ENABLED=0` parity pass before `TTT_ENABLED=1`
- `TTT_LR=0.002`
- `TTT_EPOCHS=3`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- score-first legality rules and last-chunk-no-train rule
- `LeakyReLU(0.5)^2`
- cuDNN-backed SDPA fallback stack
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
- GPTQ-lite int6 export lineage
- tokenizer/data paths
- shim-free `physicslm`
- managed 8-GPU launch
- evaluation protocol `sliding_window stride=64`
- no retraining
- no new export
- no artifact rewrite

## Success Metric
Primary validity gate:
- same-script recovered no-TTT eval on the saved seed-`42` artifact must match archived `1.12281449` within about `±0.0002`

Primary scientific readout:
- same-script TTT-enabled eval must beat the recovered same-script no-TTT baseline on the seed-`42` artifact

Interpretation thresholds:
- strong positive: gain `<= -0.0015`
- useful but modest positive: `-0.0015 < gain <= -0.0008`
- weak / likely non-actionable: `-0.0008 < gain < 0`
- negative or null: `>= 0`

## Failure Interpretation
If same-script no-TTT parity fails on seed `42`, treat the round as an implementation failure rather than evidence about TTT transfer. If parity passes but TTT gain collapses below about `-0.0008`, then the strong seed-`1337` landing should not yet be promoted to the new default evaluation regime without further explanation.

## Redundancy Check
- Do not change the TTT recipe while asking the second-seed robustness question.
- Do not bundle another architecture, optimization, export, or runtime-path edit into the confirmation.
- Do not retrain or rewrite artifacts.

## Execution Plan
1. Reuse the exact `eval_002` run-local script unchanged.
2. Run one managed 8-GPU eval-only no-TTT parity recovery on the saved seed-`42` export lineage.
3. Only if parity passes, run one managed 8-GPU eval-only TTT-enabled eval on that exact same saved seed-`42` artifact source.
4. Compare the seed-`42` gain against the seed-`1337` gain `-0.00240074`, the locked non-TTT references, and live SOTA.

## Expected Effect
If the transfer is robust, the next round should confirm that evaluation-side `Legal Score-First TTT` is the main remaining gap-closing lever on `arch_010`, not just a strong seed-`1337` landing.
