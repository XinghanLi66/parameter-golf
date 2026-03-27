# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase clean-idle runtime-diagnosis control on the exact promoted `eval_038` legality line.

- Executed the reviewed brief through the required file re-read, identity verification, promoted-command recovery, full clean-idle gating, synchronized telemetry capture, exact promoted-line launch, and post-run comparison.
- No code edits were made in this round.
- One valid clean-idle control was launched and finished on pinned GPUs `0..7`.
- This round did not test a new leaderboard motif; it remained a refinement-phase operational control needed to make later `TTT_EPOCHS=4 -> 3` comparisons interpretable again.

## Experiment ID
`eval_042_eval038_clean_idle_telemetry_control`

## Category
- evaluation

Operational subtype: `exact promoted-line clean-idle telemetry control`

## Baseline / Comparison
Primary runtime-restoration target:
- promoted `eval_038=0.19974237`
- promoted script eval wallclock `588813ms`
- promoted runner-managed wallclock `634685ms`
- promoted external wallclock `634926ms`

Recent slowdown anchors:
- `eval_039=0.19974161` at `1237494ms` external
- `eval_040 control A=0.19974193` at `1365195ms` external
- `eval_040 control B=0.19974367` at `1298755ms` external

## Hypothesis
The promoted helper/checkpoint/artifact stack is still semantically stable, and the current slowdown is operational rather than semantic.

Falsifiable version:
- if one exact clean-idle rerun launched after a genuinely clean-idle gate returns near the `eval_038` runtime band, the slowdown was transient or externally induced
- if one exact clean-idle rerun launched after a genuinely clean-idle gate remains in the `eval_039` / `eval_040` runtime regime, the slowdown is intrinsic to the current environment or process regime
- if BPB no longer matches the promoted line, semantic drift has appeared

## Why It Might Work
- `eval_039` and `eval_040` already showed that BPB and n-gram telemetry stayed in-family
- the unresolved variable is localization, not semantics
- one exact rerun with enforced clean-idle launch is the smallest refinement-phase experiment that can distinguish external contention from host-side launch overhead and from true in-process runtime drift

## Minimal Intervention
No helper, checkpoint, artifact, runner, eval-hyperparameter, or export changes were made.

Operational-only changes:
- prelaunch clean-idle verification on GPUs `0..7`
- synchronized runtime telemetry capture
- fresh `RUN_ID`
- fresh runner `--log-dir`
- fresh runner `--run-name`

## Variables To Change
Semantic variables:
- none

Operational-only variables:
- clean-idle gate enforcement on GPUs `0..7`
- telemetry capture
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from promoted `eval_038`
- exact checkpoint path, bytes, and SHA-256
- exact artifact path, bytes, and SHA-256
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `EVAL_STRIDE=64`
- `EVAL_LOGIT_TEMP=1.0`
- `TTT_LR=0.0025`
- `TTT_EPOCHS=4`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `NGRAM_EVAL_ENABLED=1`
- `NGRAM_EVAL_BUCKETS=2097152`
- `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1`
- `NGRAM_EVAL_BATCH_TORCH_STATS=1`
- `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`
- tokenizer, dataset, and stride `64`
- `physicslm` environment
- working directory
- pinned GPU set `0,1,2,3,4,5,6,7`
- launcher path `tools/gpu_experiment_runner.py`

## Identity Checks
- Helper:
  - path: `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`
  - bytes: `125663`
  - SHA-256: `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
- Saved checkpoint:
  - path: `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
  - bytes: `106178569`
  - SHA-256: `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- Saved artifact:
  - path: `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
  - bytes: `15555121`
  - SHA-256: `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

Identity status:
- helper unchanged before vs after the round
- checkpoint unchanged before vs after the round
- artifact unchanged before vs after the round

## Commands Actually Run
Clean-idle acquisition and synchronized telemetry were executed from a single top-level control script, then the exact promoted-line eval launched through the runner:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --min-free-memory-gb 10.0 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_042_eval038_clean_idle_telemetry_control/runner_control_8gpu \
  --run-name eval_042_runner_control_t1p00_e4_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_042_eval038_clean_idle_telemetry_control_runner_control \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=1.0 \
    TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
    TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
    NGRAM_EVAL_ENABLED=1 NGRAM_EVAL_BUCKETS=2097152 \
    NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1 \
    NGRAM_EVAL_BATCH_TORCH_STATS=1 NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1 \
    EVAL_ONLY_FINAL_MODEL_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt \
    EVAL_ONLY_ARTIFACT_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz \
    DATA_PATH=/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024 \
    TOKENIZER_PATH=/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
    torchrun --standalone --nproc_per_node=8 \
    /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/train_gpt.py
```

## Clean-Idle Gate Result
- gate status: `pass`
- the declared clean-idle acquisition protocol was honored and passed on the first required sample at `2026-03-27T11:40:19Z`
- pinned GPUs `0..7` were all clean-idle at gate pass:
  - each GPU showed about `81007 MiB` free and `0 MiB` used
  - each GPU showed `0%` utilization
  - `nvidia-smi --query-compute-apps` returned no foreign compute processes
- synchronized telemetry began immediately after the gate pass and continued through the run
- telemetry artifacts:
  - gate log: `runs/eval_042_eval038_clean_idle_telemetry_control/clean_idle_gate.log`
  - runtime telemetry: `runs/eval_042_eval038_clean_idle_telemetry_control/runtime_telemetry.log`
  - top-level command log: `runs/eval_042_eval038_clean_idle_telemetry_control/top_level.log`

## Success Metric
Primary diagnostic success required:
- clean-idle gate passes on GPUs `0..7`
- one exact promoted-line run finishes
- BPB stays within `±0.00005` of promoted `eval_038`
- telemetry is sufficient to classify the slowdown locus

Secondary success required:
- runtime returns to within `+15s` of promoted `eval_038`

Actual status:
- clean-idle gate pass: `pass`
- exact promoted-line run: `completed`
- diagnostic localization from aligned launch telemetry: `obtained`

## Expected Effect
If the slowdown was operational rather than semantic, one exact clean-idle rerun with aligned telemetry should localize whether the drift sits in external contention, launch-side overhead, or the child runtime itself.

## Actual Result
- the exact promoted-line control launched cleanly and finished
- final scored metrics:
  - `legal_ttt_exact val_loss=0.33725929`
  - `legal_ttt_exact val_bpb=0.19974395`
  - script eval wallclock `1507653ms`
  - runner-managed wallclock `1555810ms`
  - external wallclock `1556076ms`
  - `runner_start_to_child_spawn_ms=479`
  - `child_runtime_ms=1555330`
- versus promoted `eval_038`, deltas were:
  - `+0.00000266 val_loss`
  - `+0.00000158 BPB`
  - `+918840ms` script
  - `+921125ms` runner
  - `+921150ms` external
- versus `eval_039`, external wallclock was `+318582ms`
- versus `eval_040 control B`, external wallclock was `+257321ms`
- n-gram telemetry stayed in-family:
  - any-match `0.98387585`
  - avg alpha `0.65459237`
  - matched-order histogram identical to promoted `eval_038`
- runtime telemetry showed:
  - no meaningful launch-side stall
  - child execution began on a clean-idle machine
  - late in the run, GPU `0` picked up an extra non-run PID `3384110` using about `74486 MiB`, but the run was already far behind promoted pace before this appeared
  - `ngram_postlookup_vectorized_elapsed_ms=1540712`, up `+378529ms` vs promoted `eval_038`

## Interpretation
- Decision label: `clean-launch persistent-runtime-shift / child-runtime-inflation`
- The promoted helper/checkpoint/artifact stack remains semantically stable: BPB, any-match, avg alpha, and matched-order histogram all stayed in-family.
- The slowdown is not primarily explained by clean-idle failure or launch overhead, because the gate passed cleanly and `runner_start_to_child_spawn_ms` was only `479ms`.
- The dominant slowdown locus is inside child execution under the current environment/process regime, with especially large inflation in vectorized postlookup time.
- The late extra PID on GPU `0` is real telemetry contamination, but it appeared after the run had already fallen far behind the promoted band, so it does not explain the main classification.
- This round closes the unresolved protocol gap left by `eval_041`.
- The dedicated `TTT_EPOCHS=4 -> 3` refinement pair is now admissible again, but it should be interpreted against the current runtime regime rather than as a restoration test against the old `eval_038` wallclock band.

## Next Step
Reopen the exact same promoted-line `TTT_EPOCHS=4 -> 3` pair as a controlled same-session refinement comparison on the now-diagnosed current runtime regime, while keeping helper/checkpoint/artifact and all non-epoch variables fixed. If runtime-localization work continues, keep synchronized GPU-process telemetry because late foreign occupancy on GPU `0` can still contaminate long runs.
