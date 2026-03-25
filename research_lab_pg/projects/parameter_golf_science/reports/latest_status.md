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
- The real local `arch_002` comparison is now measured on one retrain that changed only `NUM_LAYERS` from `9` to `10` on top of the locked `opt_002` recipe, and it gives a medium-sized quality gain with materially smaller byte growth than `MLP3x`: checkpoint `val_bpb` improved from `1.22061644` to `1.21510822`, regenerated `uniform int8 + zstd-22` improved from `1.22429451` to `1.21806669`, and regenerated `mlp_int6_else_int8 + zstd-22` improved from `1.22676204` to `1.22052401`; the regenerated `mlp_int6_else_int8` artifact stayed under the cap at `15482717` total bytes, while regenerated `uniform int8` remained over the cap at `17480480`.
- The real local `export_006` retest is now measured on the locked `arch_002` 10-layer checkpoint with all three regenerated readouts in one run, and it reopens the prior `attn.proj` frontier cleanly: `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` scored `1.22086139` at `14954974` total bytes, saving `527743` artifact bytes versus regenerated `mlp_int6_else_int8` while regressing only `+0.00033737`, and staying within the explicit `+0.003` guardrail at `+0.00279470` versus regenerated `uniform int8`.

## Most Important Open Question
Now that `arch_002 + mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` is the strongest local byte-safe export frontier, which single-variable architecture or optimization change can improve exported quality from this stronger baseline without giving back its byte advantage?

## Active Experiment ID
`export_006_retest_attn_proj_subset_on_arch_002_checkpoint`

## Latest Result Summary
- Ran one controlled export-only retest in `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/export_006_retest_attn_proj_subset_on_arch_002_checkpoint` using:
  - locked checkpoint `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_002_depth_10l_under_locked_export_protocol/final_model.pt`
  - real tokenizer `/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model`
  - real validation shard `/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024/fineweb_val_000000.bin`
  - fixed comparison standard `EVAL_MODE=sliding_window EVAL_STRIDE=64`
  - fixed container `zstd-22`
  - distributed launch on 8 local L20Z GPUs via `tools/gpu_experiment_runner.py`
  - changed only one export variable relative to the prior safe policy: added `blocks.*.attn.proj.weight -> int6` on top of `mlp_int6_else_int8`
- The run revalidated the checkpoint at `val_bpb=1.21510822` and regenerated all three required exports with exact roundtrip/load correctness:
  - `uniform int8+zstd-22`: `17419187` bytes, total `17480480`, post-export `val_bpb=1.21806669`, quantization gap `+0.00295847`, export `2167.93ms`, load `113.24ms`
  - `mlp_int6_else_int8+zstd-22`: `15421424` bytes, total `15482717`, post-export `val_bpb=1.22052401`, quantization gap `+0.00541579`, export `1790.26ms`, load `851.58ms`
  - `mlp_int6_plus_attn_proj_int6_else_int8+zstd-22`: `14893681` bytes, total `14954974`, post-export `val_bpb=1.22086139`, quantization gap `+0.00575317`, export `1681.34ms`, load `1021.57ms`
- Comparison highlights:
  - versus regenerated `uniform int8`: `-2525506` artifact bytes and `+0.00279470 val_bpb`
  - versus regenerated `mlp_int6_else_int8`: `-527743` artifact bytes and `+0.00033737 val_bpb`
  - versus historical `export_005` candidate on the weaker checkpoint: `-0.00654737 val_bpb` at `+1419928` artifact bytes, reflecting the stronger 10-layer checkpoint family
- Decision:
  - The stronger `arch_002` checkpoint reopened the `attn.proj` selective-export frontier. This candidate is now the best local byte-safe export readout on this lineage because it stays under the cap and inside the explicit `+0.003` guardrail versus regenerated `uniform int8`.

## Recommended Next Step
Lock `arch_002 + mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` as the new baseline and test one single-variable architecture motif with current leaderboard support, such as a small `BigramHash`, rather than spending the next round on another nearby export-subset retest.
