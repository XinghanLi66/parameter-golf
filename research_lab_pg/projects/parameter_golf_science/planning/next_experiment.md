# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Experiment ID
`opt_003_arch_003_muon_wd004_plus_late_swa`

## Category
- optimization

## Baseline / Comparison
Locked local best byte-safe configuration after the successful `arch_003` feature-stack run:
- checkpoint/export lineage:
  - training checkpoint `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_003_bigramhash_4096_smeargate_under_export_006_protocol/final_model.pt`
  - fixed scored export winner `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_003_bigramhash_4096_smeargate_under_export_006_protocol/artifacts/final_model.mlp_int6_plus_attn_proj_int6_else_int8.zstd.ptz`
- fixed evaluation standard `EVAL_MODE=sliding_window EVAL_STRIDE=64`
- fixed export container `zstd-22`
- fixed export policy for scoring: `mlp_int6_plus_attn_proj_int6_else_int8`
- most relevant locked numbers:
  - checkpoint `val_bpb=1.20992003`
  - regenerated `uniform int8 + zstd-22` post-export `val_bpb=1.21486895`, total `18074538`
  - regenerated `mlp_int6_else_int8 + zstd-22` post-export `val_bpb=1.21774203`, total `16084095`
  - regenerated `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` post-export `val_bpb=1.21797944`, total `15564216`

Candidate:
- retrain one `10L / MLP2x + BigramHash(4096) + SmearGate` model with bundled optimization changes `Muon decoupled weight decay = 0.04` plus one fixed late `SWA` window
- score the same locked export readouts after retraining

## Hypothesis
If the new feature-stack checkpoint is quality-strong but not quantization-robust enough, then adding the nearby frontier optimization bundle `Muon WD=0.04 + late SWA` should recover export robustness and byte headroom efficiency, improving the locked exported readout or its quantization gap without giving back too much raw checkpoint quality.

## Why It Might Work
Current leaderboard recipes repeatedly pair cheap feature additions with stronger compression-friendly optimization and late averaging. Local `arch_003` already proved that the feature stack improves raw and exported quality, but its quantization gap worsened materially and the old safe `mlp_int6_else_int8` readout crossed the byte cap. That makes the missing `WD + late averaging` bundle the clearest next lever.

## Minimal Intervention
Retrain once from the current `arch_003` recipe lineage and change only optimization behavior: apply `Muon weight decay = 0.04` in the matrix-parameter path and enable one fixed late `SWA` collection window. Keep architecture, evaluation protocol, and export protocol fixed.

## Variables To Change
- optimization: set Muon decoupled weight decay to `0.04`
- late averaging: enable `SWA`
- SWA window: collect every `50` steps while the learning-rate multiplier is below `0.5`

## Variables To Hold Fixed
- architecture `10L / MLP2x + BigramHash(4096) + SmearGate`
- tokenizer
- dataset and validation shard pattern
- optimizer family
- `WARMDOWN_ITERS=3000`
- `MUON_MOMENTUM_WARMUP_STEPS=1500`
- wallclock-limited launch shape and 8-GPU execution pattern
- evaluation mode `sliding_window`
- evaluation stride `64`
- export container `zstd-22`
- export schema
- scored export policies: regenerate `uniform int8`, `mlp_int6_else_int8`, and `mlp_int6_plus_attn_proj_int6_else_int8`
- metric definitions and reporting format

## Success Metric
Primary:
- improve regenerated `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` beyond `1.21797944`
- reduce its quantization gap below `+0.00805941`
- keep the locked best readout under the 16 MB cap

Secondary:
- make regenerated `mlp_int6_else_int8 + zstd-22` byte-safe again
- preserve the checkpoint-quality gain from `arch_003` as much as practical
- preserve exact export roundtrip/load correctness

## Failure Interpretation
If `WD=0.04 + late SWA` does not improve export robustness on top of the successful feature-stack architecture, then this checkpoint family is likely bottlenecked less by this generic optimization layer and more by a stronger frontier stack such as `EMA`, `GPTQ-lite`, or a structural architecture/capacity change.

## Redundancy Check
- This does not repeat the already-answered `BigramHash + SmearGate` architecture question.
- This directly targets the newly exposed bottleneck from `arch_003`: worse quantization gap and reduced byte headroom on the stronger checkpoint.
- Local work has not yet tested `WD=0.04`, `SWA`, or the exact `arch_003` retrain with this optimization bundle.

## Execution Plan
1. Reuse the `arch_003` recipe and change only the optimization bundle: `Muon weight decay = 0.04` plus one fixed late `SWA` window.
2. Train via `tools/gpu_experiment_runner.py` on the same 8-GPU wallclock-limited setup.
3. Evaluate the resulting checkpoint under `EVAL_MODE=sliding_window EVAL_STRIDE=64`.
4. Regenerate `uniform int8 + zstd-22`, `mlp_int6_else_int8 + zstd-22`, and `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22`.
5. Validate roundtrip/load correctness and compare bytes, totals, post-export `val_bpb`, and quantization gaps against the locked `arch_003` baseline.

## Expected Effect
Best case: the bundled frontier optimization change keeps most of the `arch_003` raw-quality gain while making the exported readouts safer, ideally pulling the locked best readout back inside the old `+0.003` relative band and reopening some byte headroom.
