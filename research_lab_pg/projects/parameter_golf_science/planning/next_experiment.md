# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase single-variable eval-temperature check on the promoted `eval_035` legality line, but stopped cleanly at the fresh-control admissibility gate.

- Executed the reviewed brief materially as written through the required gate:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `context/reference_materials/URGENT_ngram_backoff_breakthrough.md`, `context/reference_materials/user_proposed_ideas_eval_mixing.md`, the required planning/report files, and the active helper before launch
  - confirmed `EVAL_LOGIT_TEMP` was already env-configurable on the active helper, so no code edits were needed
  - re-verified helper, checkpoint, and artifact identities before launch and again after the control run
  - reused the promoted `eval_035` settings with `NGRAM_EVAL_BUCKETS=2097152`
  - ran one fresh runner-managed admissibility control at `EVAL_LOGIT_TEMP=0.95`
  - checked the reviewed admissibility gates versus promoted `eval_035=0.20079980`
  - stopped without launching the `EVAL_LOGIT_TEMP=1.0` candidate because the fresh control failed the external-wallclock gate
  - kept the same `physicslm` environment, cwd, runner path, pinned GPUs, helper, checkpoint, artifact, tokenizer, dataset, stride, `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and PR809-style vectorized n-gram settings

## Experiment ID
`eval_037_eval035_temperature_pair`

## Category
- evaluation

Operational subtype: `single-variable scorer calibration refinement`

## Baseline / Comparison
Primary baseline:
- promoted `eval_035=0.20079980` on the locked promoted legality line with `EVAL_LOGIT_TEMP=0.95`

Planned primary comparison:
- one fresh admissible runner-managed control on the exact same line at `EVAL_LOGIT_TEMP=0.95`
- then one fresh runner-managed candidate on the exact same line with only `EVAL_LOGIT_TEMP=1.0`

Historical anchors:
- fresh admissible `eval_036` control `=0.20079853`
- best same-family quality anchor `eval_015=0.19974202`

## Hypothesis
After promotion to `NGRAM_EVAL_BUCKETS=2097152`, the eval-time neural/ngram mixer may now be slightly over-sharpened at `EVAL_LOGIT_TEMP=0.95`. If that is true, restoring `EVAL_LOGIT_TEMP=1.0` should improve post-export `val_bpb` on the promoted line.

## Why It Might Work
- `EVAL_LOGIT_TEMP=0.95` was validated before the bucket-geometry promotion
- the promoted `2097152`-bucket line shifted mixer behavior materially toward stronger matched-signal trust, so scorer temperature is a clean unresolved variable on the new operating point
- this stays strictly inside evaluation calibration and does not mix in architecture, optimization, export, or cache-mechanism changes

## Minimal Intervention
No code edits in this round.

Planned semantic change:
- `EVAL_LOGIT_TEMP: 0.95 -> 1.0`

Operational identifiers changed only to keep runs separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

Actual scope executed:
- only the fresh admissibility control at `EVAL_LOGIT_TEMP=0.95`
- candidate not launched because the reviewed fresh-control external-wallclock gate failed

## Variables To Change
- planned tested variable: `EVAL_LOGIT_TEMP: 0.95 -> 1.0`

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from `eval_031`
- exact checkpoint path, bytes, and SHA-256
- exact artifact path, bytes, and SHA-256
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `EVAL_STRIDE=64`
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
- existing promoted PR809-style n-gram min/max order, min-count, chunking, and alpha settings
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
- helper unchanged before vs after the control run
- checkpoint unchanged before vs after the control run
- artifact unchanged before vs after the control run

## Exact Top-Level Command Actually Run

Fresh control:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_037_eval035_temperature_pair/runner_control_8gpu \
  --run-name eval_037_runner_control_t0p95_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_037_eval035_temperature_pair_runner_control \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=0.95 \
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

## Fresh Official Result
- Fresh runner-managed control:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.33904036`
  - `val_bpb=0.20079880`
  - script eval wallclock: `603417ms`
  - runner-managed wallclock: `648159ms`
  - runner start-to-spawn: `361ms`
  - child runtime: `647798ms`
  - external top-level wallclock: `648378ms`
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.63990743`
  - matched-order histogram:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`

## Required Comparisons
- Fresh control vs promoted `eval_035` admissibility anchor:
  - `val_loss`: `0.33904205 -> 0.33904036` (`-0.00000169`)
  - `val_bpb`: `0.20079980 -> 0.20079880` (`-0.00000100`)
  - script eval wallclock: `582272ms -> 603417ms` (`+21145ms`)
  - runner-managed wallclock: `625013ms -> 648159ms` (`+23146ms`)
  - external top-level wallclock: `625177ms -> 648378ms` (`+23201ms`)
- Fresh control vs `eval_036` control:
  - `val_loss`: `0.33903990 -> 0.33904036` (`+0.00000046`)
  - `val_bpb`: `0.20079853 -> 0.20079880` (`+0.00000027`)
  - script eval wallclock: `582012ms -> 603417ms` (`+21405ms`)
  - runner-managed wallclock: `626047ms -> 648159ms` (`+22112ms`)
  - external top-level wallclock: `626047ms -> 648378ms` (`+22331ms`)
- Historical same-family quality anchor:
  - `eval_015` vs fresh control `val_bpb`: `0.19974202 -> 0.20079880` (`+0.00105678`)

## Command / Environment Parity Check
- same helper path: `pass`
- same checkpoint path: `pass`
- same artifact path: `pass`
- same cwd: `pass`
- same `physicslm` environment: `pass`
- same runner path: `pass`
- same pinned GPUs via `0,1,2,3,4,5,6,7`: `pass`
- same wrapped child command family as promoted `eval_035`: `pass`
- only wrapped-command differences vs promoted `eval_035` candidate:
  - allowed `RUN_ID`
  - allowed runner log dir
  - allowed runner run name

## Success Metric
Primary planned quality success criterion:
- candidate `val_bpb` improves on a fresh admissible control by at least `0.0001`

Fresh-control admissibility gates:
- BPB gate: `pass`
- external-wallclock gate: `fail`

Reason:
- reviewed external tolerance was `+15000ms`
- actual external drift was `+23201ms`
- overage beyond the gate: `8201ms`

## Expected Effect
If the promoted `2097152`-bucket line was over-sharpened at `EVAL_LOGIT_TEMP=0.95`, then changing only `EVAL_LOGIT_TEMP` to `1.0` should improve post-export `val_bpb` while staying in the same runtime band.

## Actual Result
- The fresh control reproduced promoted-line quality almost exactly, but it did not reproduce promoted-line runtime.
- Quality admissibility passed:
  - fresh control BPB drift was only `-0.00000100` versus promoted `eval_035`
- Runtime admissibility failed:
  - fresh control external wallclock drift was `+23201ms` versus promoted `eval_035`
  - this exceeded the reviewed `+15000ms` gate by `8201ms`
- Because the reviewed brief explicitly required stopping on fresh-control admissibility failure, the `EVAL_LOGIT_TEMP=1.0` candidate was not launched.

## Interpretation
- Classification: `drift-stop`
- The temperature question on the promoted `2097152`-bucket legality line remains unanswered in this round because the fresh control was not externally admissible.
- The control’s BPB and telemetry show that semantics remain in-family, but the runtime drift is too large to support a scientifically clean fresh control/candidate comparison under the reviewed rules.

## Next Step
Re-establish a fresh in-gate control on the exact promoted `eval_035` line first, then rerun the same temperature-only `0.95 -> 1.0` pair. Do not interpret this round as evidence for or against `EVAL_LOGIT_TEMP=1.0`; it is only evidence of runtime drift on the fresh-control rerun.
