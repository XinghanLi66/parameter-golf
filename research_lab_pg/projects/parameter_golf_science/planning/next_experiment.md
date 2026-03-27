# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase clean-idle runtime-diagnosis attempt on the exact promoted `eval_038` legality line.

- Executed the reviewed brief through the required file re-read, identity verification, promoted-command recovery, and repeated prelaunch gate sampling.
- No code edits were made in this round.
- No evaluation run was launched because the required clean-idle gate on GPUs `0..7` never passed.
- This round did not test a new leaderboard motif; it remained a refinement-phase operational control needed to make later `TTT_EPOCHS=4 -> 3` comparisons interpretable again.

## Experiment ID
`eval_041_eval038_clean_idle_telemetry_control`

## Category
- evaluation

Operational subtype: `clean-idle gated runtime diagnosis on the exact promoted stack`

## Baseline / Comparison
Primary runtime-restoration target:
- promoted `eval_038=0.19974237`
- promoted script eval wallclock `588813ms`
- promoted runner-managed wallclock `634685ms`
- promoted external wallclock `634926ms`

Recent slowdown anchors:
- `eval_039=0.19974161` at `1237494ms` external
- `eval_040 control B=0.19974367` at `1298755ms` external

## Hypothesis
The promoted helper/checkpoint/artifact stack is still semantically stable, and the current slowdown is operational rather than semantic.

Falsifiable version:
- if one exact clean-idle rerun still shows inflated child runtime with no foreign-process overlap and no large launch-side stall, the slowdown is intrinsic to the current infrastructure/process regime
- if telemetry instead shows overlap, idle gaps, or launch-side stalls, the slowdown is operationally localized and not an in-process semantic shift

## Why It Might Work
- `eval_039` and `eval_040` already showed that BPB and n-gram telemetry stayed in-family
- the unresolved variable is localization, not semantics
- one exact rerun with enforced clean-idle launch is the smallest refinement-phase experiment that can distinguish external contention from host-side launch overhead and from true in-process runtime drift

## Minimal Intervention
No helper, checkpoint, artifact, runner, eval-hyperparameter, or export changes were made.

Intended operational-only changes:
- prelaunch clean-idle verification on GPUs `0..7`
- synchronized runtime telemetry capture
- fresh `RUN_ID`
- fresh runner `--log-dir`
- fresh runner `--run-name`

Actual executed changes:
- only prelaunch clean-idle and process-state measurements

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
Prelaunch gate and process-state probes:

```bash
date -u --iso-8601=seconds
nvidia-smi --query-gpu=index,name,memory.total,memory.free,memory.used,utilization.gpu,utilization.memory --format=csv,noheader,nounits -i 0,1,2,3,4,5,6,7
nvidia-smi --query-compute-apps=gpu_uuid,gpu_name,pid,process_name,used_memory --format=csv,noheader,nounits
nvidia-smi pmon -i 0,1,2,3,4,5,6,7 -c 1
```

Bounded clean-idle watch:

```bash
for i in 1 2 3 4 5 6; do
  date -u --iso-8601=seconds
  nvidia-smi --query-gpu=index,memory.free,memory.used,utilization.gpu --format=csv,noheader,nounits -i 0,1,2,3,4,5,6,7
  nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader,nounits
  echo '---'
  sleep 20
done
```

## Exact Top-Level Eval Command Prepared But Not Launched

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_041_eval038_clean_idle_telemetry_control/runner_control_8gpu \
  --run-name eval_041_runner_control_t1p00_e4_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_041_eval038_clean_idle_telemetry_control_runner_control \
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

Operational note:
- this command was intentionally not launched because the reviewed clean-idle gate never passed

## Clean-Idle Gate Result
- gate status: `fail`
- repeated UTC samples from `2026-03-27T11:23:11Z` through `2026-03-27T11:25:26Z` showed the pinned GPU set was not clean-idle
- GPU `0` remained occupied the entire watch window:
  - free memory `6512 MiB`
  - used memory `74495 MiB`
  - utilization `100%`
  - compute-app snapshot `GPU-d45bfedb-df91-05be-293c-7375698e87dd, PID 3106138, process_name=[Not Found], used_memory=74486 MiB`
- GPUs `1..7` stayed idle with about `81007 MiB` free and `0%` utilization
- because the gate never passed, no synchronized prelaunch/child/teardown telemetry loop and no runner-managed eval launch were started

## Success Metric
Primary diagnostic success required:
- clean-idle gate passes on GPUs `0..7`
- one exact promoted-line run finishes
- BPB stays within `±0.00005` of promoted `eval_038`
- telemetry is sufficient to classify the slowdown locus

Secondary success required:
- runtime returns to within `+15s` of promoted `eval_038`

Actual status:
- clean-idle gate pass: `fail`
- exact promoted-line run: `not launched`
- diagnostic localization from aligned launch telemetry: `not obtained`

## Expected Effect
If the slowdown was operational rather than semantic, one exact clean-idle rerun with aligned telemetry should have localized whether the drift sits in external contention, launch-side overhead, or the child runtime itself.

## Actual Result
- no valid diagnostic control was launched
- no new `val_loss`, `val_bpb`, script wallclock, runner wallclock, external wallclock, `runner_start_to_child_spawn_ms`, or `child_runtime_ms` fields were produced
- the round produced only a clean-idle gate failure record on the pinned `0..7` GPU set

## Interpretation
- Decision label: `no-launch / clean-idle-gate-fail`
- The round does not update the existing `persistent-runtime-shift` classification from `eval_040`; it only shows that the reviewed clean-idle diagnostic control could not be executed because the required pinned GPU set was externally occupied.
- Because the exact clean-idle control did not run, the slowdown locus is still not newly localized in this round.

## Next Step
Retry the exact same clean-idle telemetry control once exclusive access to GPUs `0,1,2,3,4,5,6,7` can be guaranteed. Do not reopen the dedicated `TTT_EPOCHS=4 -> 3` refinement pair until that clean-idle diagnostic control succeeds.
