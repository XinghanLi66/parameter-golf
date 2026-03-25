# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Experiment ID
`arch_003_bigramhash_4096_under_export_006_protocol`

## Category
- architecture

## Baseline / Comparison
Locked local best byte-safe configuration after the successful `export_006` retest:
- checkpoint/export lineage:
  - training checkpoint `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_002_depth_10l_under_locked_export_protocol/final_model.pt`
  - fixed scored export winner `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/export_006_retest_attn_proj_subset_on_arch_002_checkpoint/artifacts/final_model.mlp_int6_plus_attn_proj_int6_else_int8.zstd.ptz`
- fixed evaluation standard `EVAL_MODE=sliding_window EVAL_STRIDE=64`
- fixed export container `zstd-22`
- fixed export policy for scoring: `mlp_int6_plus_attn_proj_int6_else_int8`
- most relevant locked numbers:
  - checkpoint `val_bpb=1.21510822`
  - regenerated `uniform int8 + zstd-22` post-export `val_bpb=1.21806669`, total `17480480`
  - regenerated `mlp_int6_else_int8 + zstd-22` post-export `val_bpb=1.22052401`, total `15482717`
  - regenerated `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` post-export `val_bpb=1.22086139`, total `14954974`

Candidate:
- retrain one `10L / MLP2x` model with a small `BigramHash(4096)` feature path
- keep the newly accepted `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` export readout fixed for scoring

## Hypothesis
If the current `10L / MLP2x` recipe is still underpowered in token-pair context modeling, then adding only a small `BigramHash(4096)` auxiliary path should improve checkpoint and exported `val_bpb` more efficiently than another raw-capacity increase, while the stronger `export_006` readout should still remain under the 16 MB cap.

## Why It Might Work
`BigramHash` appears repeatedly in current leaderboard entries and is one of the lowest-cost recurring architecture motifs in the local SOTA notes. The project now has about `1.045 MB` of submission headroom under the cap with `export_006`, so a modest auxiliary feature is a more disciplined next test than either another nearby export subset tweak or a much larger capacity jump like `MLP3x`.

## Minimal Intervention
Retrain once from the current `arch_002` recipe lineage and change only one architecture variable: enable a small `BigramHash` pathway with `4096` buckets. Score the resulting checkpoint with regenerated `uniform int8 + zstd-22`, regenerated `mlp_int6_else_int8 + zstd-22`, and the fixed local-best `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22`.

## Variables To Change
- architecture feature: add `BigramHash(4096)` only

## Variables To Hold Fixed
- depth `NUM_LAYERS=10`
- width, heads, KV heads, and `MLP_MULT=2`
- tokenizer
- dataset and validation shard pattern
- optimizer family and the locked schedule settings `WARMDOWN_ITERS=3000` and `MUON_MOMENTUM_WARMUP_STEPS=1500`
- wallclock-limited launch shape and 8-GPU execution pattern
- evaluation mode `sliding_window`
- evaluation stride `64`
- export container `zstd-22`
- export schema
- primary export readout for decision-making: `mlp_int6_plus_attn_proj_int6_else_int8`
- metric definitions and reporting format

## Success Metric
Primary:
- improve regenerated `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` post-export `val_bpb` versus the current `1.22086139`
- keep the same readout under the 16 MB cap

Secondary:
- improve checkpoint `val_bpb` versus `1.21510822`
- avoid materially worsening the quantization gap of the locked best export readout
- preserve exact export roundtrip/load correctness

## Failure Interpretation
If a small `BigramHash` does not improve the locked best exported readout or pushes the export over the byte cap, then the next architecture-side move should likely shift to a different motif such as `SmearGate` or an optimization/export machinery change rather than more auxiliary-context variants.

## Redundancy Check
- This is not another nearby export-subset retest; `export_006` already answered the most obvious remaining selective-export question positively.
- This tests one current leaderboard motif with a single architecture change against the strongest local byte-safe export baseline.

## Execution Plan
1. Reuse the `arch_002` recipe and change only the architecture by adding `BigramHash(4096)`.
2. Train via `tools/gpu_experiment_runner.py` on the same 8-GPU wallclock-limited setup.
3. Evaluate the resulting checkpoint under `EVAL_MODE=sliding_window EVAL_STRIDE=64`.
4. Regenerate `uniform int8 + zstd-22`, `mlp_int6_else_int8 + zstd-22`, and `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22`.
5. Validate roundtrip/load correctness and compare bytes, totals, post-export `val_bpb`, and quantization gaps against the locked `export_006` baseline.

## Expected Effect
Best case: `BigramHash(4096)` yields a modest but real quality gain on the locked exported readout while preserving byte safety thanks to the stronger `export_006` baseline. A clean failure would still be informative because it would rule out one of the cheaper leaderboard motifs before attempting more invasive architecture changes.
