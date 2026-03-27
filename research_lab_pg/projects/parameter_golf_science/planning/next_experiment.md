# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase single-variable same-session eval-temperature pair on the promoted `eval_035` legality line.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `context/reference_materials/URGENT_ngram_backoff_breakthrough.md`, `context/reference_materials/user_proposed_ideas_eval_mixing.md`, the required planning/report files, and the active helper before launch
  - confirmed `EVAL_LOGIT_TEMP` was already env-configurable on the active helper, so no code edits were needed
  - re-verified helper, checkpoint, and artifact identities before launch and again after both runs
  - reused the promoted `eval_035` settings with `NGRAM_EVAL_BUCKETS=2097152`
  - ran one fresh runner-managed same-session control at `EVAL_LOGIT_TEMP=0.95`
  - judged admissibility from BPB and telemetry, not from historical external wallclock drift alone
  - immediately ran one fresh runner-managed same-session candidate with only `EVAL_LOGIT_TEMP=1.0`
  - kept the same `physicslm` environment, cwd, runner path, pinned GPUs, helper, checkpoint, artifact, tokenizer, dataset, stride, `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and PR809-style vectorized n-gram settings

## Experiment ID
`eval_038_eval035_temperature_pair`

## Category
- evaluation

Operational subtype: `single-variable scorer calibration refinement`

## Baseline / Comparison
Primary baseline:
- fresh admissible runner-managed control on the promoted `eval_035` legality line at `EVAL_LOGIT_TEMP=0.95`

Primary comparison:
- one fresh runner-managed candidate on the exact same line with only `EVAL_LOGIT_TEMP=1.0`

Historical anchors:
- promoted `eval_035=0.20079980`
- freshest admissible prior control `eval_036 control=0.20079853`
- strongest same-family quality anchor `eval_015=0.19974202`
- stale drift-only context `eval_037 control=0.20079880`

## Hypothesis
After promotion to `NGRAM_EVAL_BUCKETS=2097152`, the eval-time neural/ngram mixer may now be slightly over-sharpened at `EVAL_LOGIT_TEMP=0.95`. If that is true, restoring `EVAL_LOGIT_TEMP=1.0` should improve post-export `val_bpb` on the promoted line.

## Why It Might Work
- `EVAL_LOGIT_TEMP=0.95` was validated before the bucket-geometry promotion
- the promoted `2097152`-bucket line shifted mixer behavior materially toward stronger matched-signal trust, so scorer temperature remained the clean unresolved variable on the new operating point
- this stayed strictly inside evaluation calibration and did not mix in architecture, optimization, export, or cache-mechanism changes

## Minimal Intervention
No code edits in this round.

Changed variable:
- `EVAL_LOGIT_TEMP: 0.95 -> 1.0`

Operational identifiers changed only to keep runs separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Change
- tested variable: `EVAL_LOGIT_TEMP: 0.95 -> 1.0`

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
- helper unchanged before vs after the pair
- checkpoint unchanged before vs after the pair
- artifact unchanged before vs after the pair

## Exact Top-Level Commands Actually Run

Fresh control:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_038_eval035_temperature_pair/runner_control_8gpu \
  --run-name eval_038_runner_control_t0p95_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_038_eval035_temperature_pair_runner_control \
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

Fresh candidate:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_038_eval035_temperature_pair/runner_candidate_8gpu \
  --run-name eval_038_runner_candidate_t1p00_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_038_eval035_temperature_pair_runner_candidate \
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

## Fresh Official Results
- Fresh runner-managed control:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.33904065`
  - `val_bpb=0.20079897`
  - script eval wallclock: `585778ms`
  - runner-managed wallclock: `631265ms`
  - runner start-to-spawn: `357ms`
  - child runtime: `630908ms`
  - external top-level wallclock: `631449ms`
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.63990741`
  - matched-order histogram:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
- Fresh runner-managed candidate:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.33725663`
  - `val_bpb=0.19974237`
  - script eval wallclock: `588813ms`
  - runner-managed wallclock: `634685ms`
  - runner start-to-spawn: `366ms`
  - child runtime: `634319ms`
  - external top-level wallclock: `634926ms`
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.65459911`
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
  - `val_loss`: `0.33904205 -> 0.33904065` (`-0.00000140`)
  - `val_bpb`: `0.20079980 -> 0.20079897` (`-0.00000083`)
  - script eval wallclock: `582272ms -> 585778ms` (`+3506ms`)
  - runner-managed wallclock: `625013ms -> 631265ms` (`+6252ms`)
  - external top-level wallclock: `625177ms -> 631449ms` (`+6272ms`)
- Fresh control vs `eval_036` control:
  - `val_loss`: `0.33903990 -> 0.33904065` (`+0.00000075`)
  - `val_bpb`: `0.20079853 -> 0.20079897` (`+0.00000044`)
  - script eval wallclock: `582012ms -> 585778ms` (`+3766ms`)
  - runner-managed wallclock: `626047ms -> 631265ms` (`+5218ms`)
  - external top-level wallclock: `626047ms -> 631449ms` (`+5402ms`)
- Fresh candidate vs fresh admissible control:
  - `val_loss`: `0.33904065 -> 0.33725663` (`-0.00178402`)
  - `val_bpb`: `0.20079897 -> 0.19974237` (`-0.00105660`)
  - script eval wallclock: `585778ms -> 588813ms` (`+3035ms`)
  - runner-managed wallclock: `631265ms -> 634685ms` (`+3420ms`)
  - external top-level wallclock: `631449ms -> 634926ms` (`+3477ms`)
- Historical same-family quality anchor:
  - `eval_015` vs fresh candidate `val_bpb`: `0.19974202 -> 0.19974237` (`+0.00000035`)

## Command / Environment Parity Check
- same helper path: `pass`
- same checkpoint path: `pass`
- same artifact path: `pass`
- same cwd: `pass`
- same `physicslm` environment: `pass`
- same runner path: `pass`
- same pinned GPUs via `0,1,2,3,4,5,6,7`: `pass`
- same wrapped child command family between fresh control and candidate: `pass`
- only wrapped-command differences:
  - allowed `EVAL_LOGIT_TEMP`
  - allowed `RUN_ID`
  - allowed runner log dir
  - allowed runner run name

## Success Metric
Primary planned quality success criterion:
- candidate `val_bpb` improves on the fresh admissible control by at least `0.0001`

Fresh-control admissibility gates:
- BPB gate: `pass`
- telemetry consistency gate: `pass`
- runtime context vs promoted `eval_035`: `pass`

Candidate success gates:
- quality gate: `pass`
- runtime gate: `pass`
- stretch target `<= 0.2003`: `pass`

## Expected Effect
If the promoted `2097152`-bucket line was over-sharpened at `EVAL_LOGIT_TEMP=0.95`, then changing only `EVAL_LOGIT_TEMP` to `1.0` should improve post-export `val_bpb` while staying in the same runtime band.

## Actual Result
- The fresh `0.95` control stayed semantically in-family and also stayed comfortably inside the historical runtime band, so the candidate launch was admissible.
- The fresh `1.0` candidate then improved post-export quality very strongly:
  - `0.20079897 -> 0.19974237` (`-0.00105660`) vs the fresh control
  - `0.20079980 -> 0.19974237` (`-0.00105743`) vs promoted `eval_035`
  - `0.20079853 -> 0.19974237` (`-0.00105616`) vs fresh `eval_036` control
- Runtime stayed comparison-clean:
  - candidate external wallclock was only `+3477ms` versus the fresh control
- Telemetry stayed stable except for the intended calibration shift:
  - identical any-match fraction
  - identical matched-order histogram
  - higher avg alpha on matched `0.63990741 -> 0.65459911`

## Interpretation
- Classification: `promote`
- The promoted `2097152`-bucket legality line was indeed over-sharpened at `EVAL_LOGIT_TEMP=0.95`.
- `EVAL_LOGIT_TEMP=1.0` should replace `0.95` as the promoted default on this exact helper/checkpoint/artifact lineage.
- Historical external drift versus `eval_035` did not recur materially in the fresh control rerun, so the earlier `eval_037` stop should be treated as stale context rather than the final answer to this temperature question.
- The new candidate essentially matches the strongest same-family quality anchor `eval_015`, trailing by only `0.00000035 BPB`.

## Next Step
Hold `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and `NGRAM_EVAL_BUCKETS=2097152` as the new promoted legality baseline, then test one fresh single-variable runtime/quality tradeoff on top of this stronger calibrated line rather than revisiting scalar temperature again. The cleanest next question is whether `TTT_EPOCHS=3` reopens as a better runtime-quality point now that the promoted line uses the newly validated `EVAL_LOGIT_TEMP=1.0`.
