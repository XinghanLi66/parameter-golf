# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session duplicate-control reproducibility check on the promoted `eval_038` legality line.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, and the active helper before launch
  - re-verified helper, checkpoint, and artifact identities before launch and again after the round
  - recovered the exact promoted `eval_038` runner command family from on-disk metadata
  - launched `control A` and `control B` on the exact promoted stack in the same session
  - changed only operational identifiers between the two successful controls
- No code edits were made in this round.

## Experiment ID
`eval_040_eval038_duplicate_control`

## Category
- evaluation

Operational subtype: `same-session duplicate-control runtime reproducibility`

## Baseline / Comparison
Primary baseline:
- promoted `eval_038=0.19974237`

Historical anchors:
- promoted external wallclock `634926ms`
- promoted runner-managed wallclock `634685ms`
- promoted script eval wallclock `588813ms`
- fresh drifted `eval_039=0.19974161`
- fresh drifted external wallclock `1237494ms`

## Hypothesis
The `eval_039` slowdown was a transient session/runtime event rather than a persistent shift in the promoted evaluation regime. If true, two fresh exact controls should reproduce promoted BPB and telemetry and return to the promoted runtime band.

## Why It Might Work
- `eval_039` already showed that the promoted helper/checkpoint/artifact stack still reproduces the same quality regime
- the unresolved variable is runtime reproducibility, not semantics
- a duplicate-control probe is the smallest refinement-phase experiment that can distinguish restored promoted runtime from runtime jitter or a persistent runtime shift

## Minimal Intervention
No code edits in this round.

Actual executed changes were operational only:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Change
Semantic variables:
- none

Operational-only variables:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from `eval_038`
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

## Exact Top-Level Commands Actually Run

Control A:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_040_eval038_duplicate_control/runner_control_a_8gpu \
  --run-name eval_040_runner_controlA_t1p00_e4_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_040_eval038_duplicate_control_runner_control_a \
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

Control B:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_040_eval038_duplicate_control/runner_control_b_8gpu \
  --run-name eval_040_runner_controlB_t1p00_e4_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_040_eval038_duplicate_control_runner_control_b \
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
- one pre-launch `control A` attempt and one immediate post-`control A` `control B` attempt failed before child spawn because only 7 GPUs met the runner free-memory gate
- the two successful completed controls above are the official results for this round

## Fresh Official Results
- Control A:
  - `val_loss=0.33725588`
  - `val_bpb=0.19974193`
  - script eval wallclock `1316129ms`
  - runner-managed wallclock `1364893ms`
  - runner start-to-spawn `382ms`
  - child runtime `1364510ms`
  - external top-level wallclock `1365195ms`
  - any-match fraction `0.98387585`
  - avg alpha on matched `0.65459876`
  - matched-order histogram:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
- Control B:
  - `val_loss=0.33725882`
  - `val_bpb=0.19974367`
  - script eval wallclock `1249634ms`
  - runner-managed wallclock `1298509ms`
  - runner start-to-spawn `479ms`
  - child runtime `1298030ms`
  - external top-level wallclock `1298755ms`
  - any-match fraction `0.98387585`
  - avg alpha on matched `0.65459430`
  - matched-order histogram:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`

## Command / Environment Parity Check
- same helper path: `pass`
- same checkpoint path: `pass`
- same artifact path: `pass`
- same cwd: `pass`
- same `physicslm` environment: `pass`
- same runner path: `pass`
- same pinned GPUs via runner request `0,1,2,3,4,5,6,7`: `pass`
- same wrapped child command family as promoted `eval_038`: `pass`
- only wrapped-command differences:
  - allowed `RUN_ID`
  - allowed runner log dir
  - allowed runner run name

## Required Comparisons
- Control A vs promoted `eval_038`:
  - `val_loss`: `0.33725663 -> 0.33725588` (`-0.00000075`)
  - `val_bpb`: `0.19974237 -> 0.19974193` (`-0.00000044`)
  - script eval wallclock: `588813ms -> 1316129ms` (`+727316ms`)
  - runner-managed wallclock: `634685ms -> 1364893ms` (`+730208ms`)
  - external top-level wallclock: `634926ms -> 1365195ms` (`+730269ms`)
  - runner start-to-spawn: `366ms -> 382ms` (`+16ms`)
  - child runtime: `634319ms -> 1364510ms` (`+730191ms`)
  - avg alpha on matched: `0.65459911 -> 0.65459876` (`-0.00000035`)
- Control B vs promoted `eval_038`:
  - `val_loss`: `0.33725663 -> 0.33725882` (`+0.00000219`)
  - `val_bpb`: `0.19974237 -> 0.19974367` (`+0.00000130`)
  - script eval wallclock: `588813ms -> 1249634ms` (`+660821ms`)
  - runner-managed wallclock: `634685ms -> 1298509ms` (`+663824ms`)
  - external top-level wallclock: `634926ms -> 1298755ms` (`+663829ms`)
  - runner start-to-spawn: `366ms -> 479ms` (`+113ms`)
  - child runtime: `634319ms -> 1298030ms` (`+663711ms`)
  - avg alpha on matched: `0.65459911 -> 0.65459430` (`-0.00000481`)
- Control B vs Control A:
  - `val_loss`: `0.33725588 -> 0.33725882` (`+0.00000294`)
  - `val_bpb`: `0.19974193 -> 0.19974367` (`+0.00000174`)
  - script eval wallclock: `1316129ms -> 1249634ms` (`-66495ms`)
  - runner-managed wallclock: `1364893ms -> 1298509ms` (`-66384ms`)
  - external top-level wallclock: `1365195ms -> 1298755ms` (`-66440ms`)
  - runner start-to-spawn: `382ms -> 479ms` (`+97ms`)
  - child runtime: `1364510ms -> 1298030ms` (`-66480ms`)
  - avg alpha on matched: `0.65459876 -> 0.65459430` (`-0.00000446`)
- Control A vs fresh `eval_039` drifted control:
  - `val_loss`: `0.33725535 -> 0.33725588` (`+0.00000053`)
  - `val_bpb`: `0.19974161 -> 0.19974193` (`+0.00000032`)
  - script eval wallclock: `1190477ms -> 1316129ms` (`+125652ms`)
  - runner-managed wallclock: `1237270ms -> 1364893ms` (`+127623ms`)
  - external top-level wallclock: `1237494ms -> 1365195ms` (`+127701ms`)
  - runner start-to-spawn: `474ms -> 382ms` (`-92ms`)
  - child runtime: `1236796ms -> 1364510ms` (`+127714ms`)
- Control B vs fresh `eval_039` drifted control:
  - `val_loss`: `0.33725535 -> 0.33725882` (`+0.00000347`)
  - `val_bpb`: `0.19974161 -> 0.19974367` (`+0.00000206`)
  - script eval wallclock: `1190477ms -> 1249634ms` (`+59157ms`)
  - runner-managed wallclock: `1237270ms -> 1298509ms` (`+61239ms`)
  - external top-level wallclock: `1237494ms -> 1298755ms` (`+61261ms`)
  - runner start-to-spawn: `474ms -> 479ms` (`+5ms`)
  - child runtime: `1236796ms -> 1298030ms` (`+61234ms`)

## Success Metric
Primary success condition:
- both fresh controls within `±0.00005 BPB` of promoted `eval_038`: `pass`
- both fresh controls within `±15000ms` external wallclock of promoted `634926ms`: `fail`

Secondary stability condition:
- `control A` and `control B` within `±15000ms` external wallclock of each other: `fail`
- script eval wallclock and runner child/runtime fields show no restored promoted-band behavior: `fail`
- telemetry remains in-band: `pass`

## Expected Effect
If the `eval_039` slowdown was transient, both fresh exact controls should return to the promoted runtime band while staying semantically identical to the promoted `eval_038` line.

## Actual Result
- both controls stayed semantically in-family on BPB and telemetry
- neither control returned to the promoted runtime band
- control A ran with observed external overlap from a root-owned Humaneval/VLLM workload on GPU `0`
- control B ran after that overlap cleared and still stayed deep in the slowdown regime

## Interpretation
- Classification: `persistent-runtime-shift`
- This round answered the reviewed duplicate-control question directly:
  - not `runtime-restored`, because neither fresh control returned anywhere near promoted runtime
  - not round-level `runtime-jitter`, because both controls remained much closer to the already-drifted `eval_039` regime than to the promoted `eval_038` runtime regime
- The promoted helper/checkpoint/artifact stack still reproduces semantics, but the promoted runtime regime is not presently reproducible.

## Next Step
Do not return to the dedicated `TTT_EPOCHS=4 -> 3` comparison next round. First diagnose the runtime shift on the exact promoted `eval_038` legality line, because the epoch-count comparison is still inadmissible under the reviewed same-session standard.
