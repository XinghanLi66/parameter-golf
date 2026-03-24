# Latest Status

Update this after each substantive round.

## Current Best Evidence
- External SOTA review indicates the main repo baseline is behind on evaluation and export protocol, not just on architecture.
- The root `train_gpt.py` now supports explicit `non_overlapping` and `sliding_window` evaluation modes, plus `both` for direct comparison, with stride and wall-clock time logged for both pre-export and post-export evaluation.
- The real local `eval_001` comparison is now measured on one fresh baseline checkpoint plus its matching `int8+zlib` artifact, and the result is decision-quality: `sliding_window stride=64` improved the same pair by about `-0.0316` pre-export and `-0.0318` post-export.
- The real local `export_001` comparison is now measured on that same checkpoint with a fixed `int8` payload, and the result is also decision-quality: `zstd-22` reduced artifact bytes by `37362` (`-0.2367%`) versus `zlib-9` with exact roundtrip tensor equality and identical post-export `val_bpb`.
- The real local `export_002` comparison is now measured on that same locked checkpoint with fixed `zstd-22`, and it rules out broad lower-bit export on this checkpoint: `uniform int6` cut artifact bytes by `3365248` (`-21.3692%`) versus regenerated `uniform int8`, but post-export `val_bpb` worsened by `+0.07313349`, far beyond the allowed `+0.003`.
- The real local `export_003` comparison is now measured on that same locked checkpoint with fixed `zstd-22`, and it shows that selective export remains viable: `mlp_int6_else_int8` cut artifact bytes by `1801491` (`-11.4392%`) versus regenerated `uniform int8`, while post-export `val_bpb` worsened by only `+0.00263128`.
- The real local `export_004` comparison is now measured on that same locked checkpoint with fixed `zstd-22`, and it suggests the selective export frontier is near saturation: adding `blocks.*.attn.proj.weight -> int6` on top of `MLP-only int6` cut artifact bytes by `2270838` (`-14.4195%`) versus regenerated `uniform int8`, but post-export `val_bpb` worsened by `+0.00300190`, just beyond the explicit guardrail.
- The real local `opt_001` comparison is now measured on one retrain that changed only `WARMDOWN_ITERS` from `1200` to `3000`, and it modestly improves export robustness under the locked readout: fixed `mlp_int6_else_int8 + zstd-22` improved from `1.22768330` to `1.22696259` and its quantization gap fell from `+0.00762931` to `+0.00682063`, although checkpoint `val_bpb` was essentially flat at `1.22014196` versus `1.22005399`.
- The real local `export_005` retest is now measured on the warmdown-3000 checkpoint with all three regenerated readouts in one run, and it closes the open export question cleanly: `mlp_int6_plus_attn_proj_int6_else_int8` improved to `1.22740875` from the historical `1.22805392`, but it still regressed by `+0.00313158` versus regenerated `uniform int8`, so the guardrail still fails.
- The real local `opt_002` comparison is now measured on one retrain that changed only `MUON_MOMENTUM_WARMUP_STEPS` from `500` to `1500` on top of `WARMDOWN_ITERS=3000`, and it gives another modest export-robustness gain under the locked readout: regenerated `mlp_int6_else_int8 + zstd-22` improved from `1.22696259` to `1.22676204` and its quantization gap fell from `+0.00682063` to `+0.00614561`, while checkpoint `val_bpb` worsened from `1.22014196` to `1.22061644` and regenerated `uniform int8 + zstd-22` stayed essentially flat at `1.22429451` versus `1.22427718`.
- The real local `arch_001` comparison is now measured on one retrain that changed only `MLP_MULT` from `2` to `3` on top of the locked `opt_002` recipe, and it gives a large quality gain on checkpoint and both exported readouts: checkpoint `val_bpb` improved from `1.22061644` to `1.20227788`, regenerated `uniform int8 + zstd-22` improved from `1.22429451` to `1.20534335`, and regenerated `mlp_int6_else_int8 + zstd-22` improved from `1.22676204` to `1.20764933`; however, both exported artifacts exceeded the 16 MB cap at totals `19989838` and `17326746`, so this exact configuration is negative for the submission objective.

## Most Important Open Question
After `MLP3x` proved quality-positive but byte-negative, which single architecture lever can recover some of that gain while staying inside the 16 MB cap under the locked export protocol?

## Active Experiment ID
`arch_001_mlp_3x_capacity_under_locked_export_protocol`

## Latest Result Summary
- Ran one controlled architecture-only retrain in `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_001_mlp_3x_capacity_under_locked_export_protocol` using:
  - baseline checkpoint lineage `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/opt_002_longer_muon_momentum_warmup_for_selective_export_robustness`
  - real tokenizer `/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model`
  - real validation shard `/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024/fineweb_val_000000.bin`
  - fixed comparison standard `EVAL_MODE=sliding_window EVAL_STRIDE=64`
  - distributed launch on 8 local L20Z GPUs via `tools/gpu_experiment_runner.py`
  - fixed training recipe `WARMDOWN_ITERS=3000`, `MUON_MOMENTUM_WARMUP_STEPS=1500`
  - changed only one architecture variable: `MLP_MULT=2 -> 3`
- The retrain preserved the same wallclock-limited launch shape and stopped at step `5600`; final checkpoint metrics were:
  - `non_overlapping`: `val_bpb=1.2336`, `eval_time=4239ms`
  - `sliding_window stride=64`: `val_bpb=1.20227788`, `eval_time=71964ms`
- The fixed export comparison runner then regenerated exactly two readouts on that checkpoint and checked exact roundtrip equality for each serialized payload. Because the comparison tool defaults to `MLP_MULT=2`, the successful scored run explicitly set `MLP_MULT=3` during export loading so the model shape matched the checkpoint:
  - `roundtrip_raw_bytes_equal=True`
  - `roundtrip_quantized_tensor_equal=True`
  - `roundtrip_exact=True`
  - `uniform int8+zstd-22`: `19928545` bytes, total `19989838`, post-export `val_bpb=1.20534335`, quantization gap `+0.00306546`, export `2633.16ms`, load `149.29ms`
  - `mlp_int6_else_int8+zstd-22`: `17265453` bytes, total `17326746`, post-export `val_bpb=1.20764933`, quantization gap `+0.00537144`, export `2100.34ms`, load `1225.48ms`
  - delta `mlp_int6_else_int8 - regenerated uniform int8`: `-2663092` artifact bytes (`-13.3632%`), `+0.00230598 val_bpb`, and `+0.00230598` quantization gap
  - delta versus `opt_002` for regenerated `mlp_int6_else_int8`: `+3326199` artifact bytes, `-0.01911272 val_bpb`, and `-0.00077417` quantization gap
  - delta versus `opt_002` for regenerated `uniform int8`: `+4187828` artifact bytes, `-0.01895116 val_bpb`, and `-0.00061261` quantization gap
- Decision:
  - `MLP3x` is a much stronger quality lever than the recent schedule micro-tuning rounds in this recipe family, but it is not admissible under the current locked export protocol because both fixed exported artifacts miss the byte cap by a wide margin

## Recommended Next Step
Keep `WARMDOWN_ITERS=3000`, `MUON_MOMENTUM_WARMUP_STEPS=1500`, `sliding_window stride=64`, `zstd-22`, and the fixed export readouts, then run one single-variable architecture experiment such as `NUM_LAYERS=10` with `MLP_MULT=2` to test whether depth buys a better quality-per-byte trade than `MLP3x`.
