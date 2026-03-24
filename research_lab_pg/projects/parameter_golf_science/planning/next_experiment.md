# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Experiment ID
`arch_002_depth_10l_under_locked_export_protocol`

## Category
- architecture

## Baseline / Comparison
Locked local optimization/export baseline after the completed negative `arch_001_mlp_3x_capacity_under_locked_export_protocol` result:
- byte-safe baseline checkpoint lineage `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/opt_002_longer_muon_momentum_warmup_for_selective_export_robustness`
- fixed local evaluation standard `EVAL_MODE=sliding_window EVAL_STRIDE=64`
- fixed export container `zstd-22`
- fixed export readouts for scoring: regenerated `uniform int8 + zstd-22` and regenerated `mlp_int6_else_int8 + zstd-22`
- most relevant locked numbers from `opt_002`:
  - checkpoint `val_bpb=1.22061644`
  - regenerated `uniform int8 + zstd-22` post-export `val_bpb=1.22429451`
  - regenerated `mlp_int6_else_int8 + zstd-22` post-export `val_bpb=1.22676204`
  - regenerated `uniform int8 + zstd-22` total submission bytes `15802010`
  - regenerated `mlp_int6_else_int8 + zstd-22` total submission bytes `14000547`

Candidate:
- keep the improved optimization/export protocol fixed
- retrain once with only `NUM_LAYERS: 9 -> 10`

## Hypothesis
If the remaining gap is better addressed by a more export-efficient form of capacity than `MLP 3x`, then adding one layer while keeping `MLP_MULT=2` should recover some of the architecture-side quality gain while staying within the fixed byte cap.

## Why It Might Work
`arch_001` showed that extra capacity clearly helps quality on this recipe family, but the `MLP 3x` form overshot the byte cap by a large margin even after fixed selective export. A single extra layer is the next clean architecture-side lever from the current SOTA motif list, and it may spend bytes more efficiently than tripling every block MLP.

## Minimal Intervention
Run one retrain that changes only `NUM_LAYERS`, then score the resulting checkpoint with regenerated `uniform int8 + zstd-22` and regenerated `mlp_int6_else_int8 + zstd-22`. Do not change evaluation protocol, container, export policy, `MLP_MULT`, or the already-tested warmdown and Muon warmup settings in the same round.

## Variables To Change
- `NUM_LAYERS`: `9 -> 10`

## Variables To Hold Fixed
- tokenizer
- dataset and validation shard pattern
- optimizer family and optimizer hyperparameters
- `WARMDOWN_ITERS=3000`
- `MUON_MOMENTUM_WARMUP_STEPS=1500`
- `MLP_MULT=2`
- total wallclock-limited training setup
- distributed launch shape
- evaluation mode: `sliding_window`
- evaluation stride: `64`
- export container: `zstd-22`
- export schema
- export readouts used for scoring: regenerated `uniform int8 + zstd-22` and regenerated `mlp_int6_else_int8 + zstd-22`
- metric definitions and reporting fields

## Success Metric
Primary:
- improve regenerated `mlp_int6_else_int8 + zstd-22` post-export `val_bpb` versus `1.22676204` while keeping total submission bytes within the 16 MB cap
- improve regenerated `uniform int8 + zstd-22` post-export `val_bpb` versus `1.22429451` while keeping total submission bytes within the 16 MB cap

Secondary:
- improve checkpoint `val_bpb` versus `1.22061644`
- avoid materially worsening the `mlp_int6_else_int8` quantization gap versus `+0.00614561`
- preserve exact export roundtrip/load correctness

## Failure Interpretation
If `10L / MLP2x` still misses the byte cap or fails to improve exported readouts, then the remaining architecture-side progress likely requires stronger export machinery rather than another simple capacity reallocation within the current clean recipe.

## Redundancy Check
- This is not redundant with `opt_001`, which changed only `WARMDOWN_ITERS`.
- This is not redundant with `opt_002`, which changed only `MUON_MOMENTUM_WARMUP_STEPS`.
- This is not redundant with `arch_001`, which changed only `MLP_MULT` and improved quality but failed the byte cap.
- This does not reopen closed export-subset search; it keeps the export policy fixed and asks one different architecture-side question.

## Execution Plan
1. Reuse the locked `opt_002` recipe and change only `NUM_LAYERS` from `9` to `10`.
2. Retrain once under the same wallclock-limited distributed setup.
3. Evaluate the resulting checkpoint under `EVAL_MODE=sliding_window EVAL_STRIDE=64`.
4. Regenerate and score `uniform int8 + zstd-22` on that checkpoint.
5. Regenerate and score `mlp_int6_else_int8 + zstd-22` on that checkpoint.
6. Validate roundtrip/load correctness for both exported artifacts.
7. Compare checkpoint `val_bpb`, post-export `val_bpb`, quantization gap, bytes, export time, and load time against `opt_002`.

## Expected Effect
If `MLP 3x` was the right direction but the wrong byte trade, one extra layer should deliver a smaller quality gain than `arch_001` but may do so with materially better byte efficiency and therefore a better chance of being admissible under the fixed export protocol.
