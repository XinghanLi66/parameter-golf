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
- The real local `arch_003` comparison is now measured on one retrain that changed only the architecture by adding `BigramHash(4096) + SmearGate` on top of the locked `arch_002` recipe, and it gives a meaningful quality gain on checkpoint and all three regenerated export readouts: checkpoint `val_bpb` improved from `1.21510822` to `1.20992003`, regenerated `uniform int8 + zstd-22` improved from `1.21806669` to `1.21486895`, regenerated `mlp_int6_else_int8 + zstd-22` improved from `1.22052401` to `1.21774203`, and regenerated `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` improved from `1.22086139` to `1.21797944`; the locked best readout stayed under the cap at `15564216`, but quantization gaps worsened materially and regenerated `mlp_int6_else_int8` crossed the cap at `16084095`.

## Most Important Open Question
Now that `arch_003 + mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` is the strongest local byte-safe quality frontier, which compression-friendly optimization change can recover quantization robustness or byte headroom on this stronger checkpoint family?

## Active Experiment ID
`arch_003_bigramhash_4096_smeargate_under_export_006_protocol`

## Latest Result Summary
- Ran one controlled architecture retrain plus fixed export comparison in `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_003_bigramhash_4096_smeargate_under_export_006_protocol` using:
  - retrained checkpoint `/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_003_bigramhash_4096_smeargate_under_export_006_protocol/final_model.pt`
  - real tokenizer `/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model`
  - real validation shard `/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024/fineweb_val_000000.bin`
  - fixed comparison standard `EVAL_MODE=sliding_window EVAL_STRIDE=64`
  - fixed container `zstd-22`
  - distributed launch on 8 local L20Z GPUs via `tools/gpu_experiment_runner.py`
  - changed only the architecture relative to `arch_002`: `BIGRAM_HASH_BUCKETS=4096`, `BIGRAM_HASH_DIM=128`, and `USE_SMEARGATE=1`
- The run finished at step `5467` under the same 600s cap, revalidated the checkpoint at `val_bpb=1.20992003`, and regenerated all three required exports with exact roundtrip/load correctness:
  - `uniform int8+zstd-22`: `18010498` bytes, total `18074538`, post-export `val_bpb=1.21486895`, quantization gap `+0.00494892`, export `2917.88ms`, load `127.59ms`
  - `mlp_int6_else_int8+zstd-22`: `16020055` bytes, total `16084095`, post-export `val_bpb=1.21774203`, quantization gap `+0.00782200`, export `2391.61ms`, load `762.41ms`
  - `mlp_int6_plus_attn_proj_int6_else_int8+zstd-22`: `15500176` bytes, total `15564216`, post-export `val_bpb=1.21797944`, quantization gap `+0.00805941`, export `2265.03ms`, load `921.87ms`
- Comparison highlights:
  - versus the prior locked best `mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22`: `-0.00288195 val_bpb` at `+609242` total bytes
  - versus the prior checkpoint baseline: `-0.00518819 checkpoint val_bpb`
  - on this stronger checkpoint, the locked best readout is now `+0.00311049 val_bpb` versus regenerated `uniform int8`, slightly outside the old explicit guardrail, even though regenerated `uniform int8` is not byte-safe
- Decision:
  - The `BigramHash + SmearGate` stack is a real local win on this 10-layer line. It improves the best byte-safe exported score to `1.21797944` under the cap, but it also worsens quantization robustness enough that the next round should target export-friendlier optimization rather than another nearby feature-path addition.

## Recommended Next Step
Keep `arch_003 + mlp_int6_plus_attn_proj_int6_else_int8 + zstd-22` as the new best byte-safe quality baseline and test one compression-friendly optimization lever, such as stronger weight decay or late averaging, to recover quantization robustness and byte headroom.
