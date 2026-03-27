# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase single-variable TTT learning-rate refinement on the promoted `eval_035` legality line.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `context/reference_materials/URGENT_ngram_backoff_breakthrough.md`, `context/reference_materials/user_proposed_ideas_eval_mixing.md`, the required planning/report files, and the active helper before launch
  - confirmed `TTT_LR` was already env-configurable on the active helper, so no code edits were needed
  - re-verified helper, checkpoint, and artifact identities before launch and again after both arms
  - reused the promoted `eval_035` settings with `NGRAM_EVAL_BUCKETS=2097152`
  - ran one fresh runner-managed admissibility control at `TTT_LR=0.0025`
  - checked the reviewed admissibility gates versus promoted `eval_035=0.20079980`
  - ran one fresh runner-managed candidate with only `TTT_LR=0.0020`
  - kept the same `physicslm` environment, cwd, runner path, pinned GPUs, helper, checkpoint, artifact, tokenizer, dataset, stride, `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, and PR809-style vectorized n-gram settings

## Experiment ID
`eval_036_eval035_ttt_lr_pair`

## Category
- evaluation

Operational subtype: `single-variable TTT scalar refinement`

## Baseline / Comparison
Primary baseline:
- fresh admissible runner-managed control on the promoted `eval_035` settings with `TTT_LR=0.0025`

Primary comparison:
- fresh runner-managed candidate on the exact same settings with only `TTT_LR=0.0020`

Historical anchors:
- promoted line `eval_035=0.20079980`, script `582272ms`, runner `625013ms`, external `625177ms`
- best same-family quality anchor `eval_015=0.19974202`
- prior epoch-count answer `eval_034`, which kept `TTT_EPOCHS=4` as the quality default

## Hypothesis
After promotion to `NGRAM_EVAL_BUCKETS=2097152`, the eval-time mixer may now be over-adapting slightly at `TTT_LR=0.0025`. Lowering only `TTT_LR` to `0.0020` will reduce over-adaptation and improve post-export `val_bpb` on the promoted line.

## Why It Might Work
- the live SOTA motif still uses legal score-first TTT at a lower LR than the promoted local line
- `eval_035` increased matched-signal trust on the promoted helper, so a slightly smaller TTT step size could preserve that gain while avoiding overshooting during chunk adaptation
- this directly tests the remaining clean eval mismatch without mixing architecture, optimization, export, or cache-geometry changes

## Minimal Intervention
No code edits in this round.

Only varied:
- `TTT_LR: 0.0025 -> 0.0020`

Also changed only the operational identifiers required to keep the runs separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Change
- `TTT_LR: 0.0025 -> 0.0020`

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from `eval_031`
- exact checkpoint path, bytes, and SHA-256
- exact artifact path, bytes, and SHA-256
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `EVAL_STRIDE=64`
- `EVAL_LOGIT_TEMP=0.95`
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
- helper unchanged before vs after both runs
- checkpoint unchanged before vs after both runs
- artifact unchanged before vs after both runs

## Exact Top-Level Commands Actually Run

Control:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_036_eval035_ttt_lr_pair/runner_control_8gpu \
  --run-name eval_036_runner_control_t0p95_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_036_eval035_ttt_lr_pair_runner_control \
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

Candidate:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_036_eval035_ttt_lr_pair/runner_candidate_8gpu \
  --run-name eval_036_runner_candidate_t0p95_b2097152_lr0020 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_036_eval035_ttt_lr_pair_runner_candidate \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=0.95 \
    TTT_LR=0.0020 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
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

## Measurement Note
- The candidate outer wallclock was captured directly by bash `time`: `external_real_seconds=634.143`.
- The control was not wrapped with a separate outer timer on the first launch, so its recorded external top-level wallclock is `626047ms` from `runner_total_ms`; the metadata UTC timestamps (`07:54:21Z -> 08:04:47Z`) independently agree at about `626000ms`.
- This does not affect the reviewed admissibility or pairwise decision because the runtime gates are much looser than the sub-second measurement uncertainty on the control external field.

## Fresh Official Results
- Fresh runner-managed control:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.33903990`
  - `val_bpb=0.20079853`
  - script eval wallclock: `582012ms`
  - runner-managed wallclock: `626047ms`
  - runner start-to-spawn: `391ms`
  - child runtime: `625655ms`
  - external top-level wallclock: `626047ms` via runner-total proxy
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.63990797`
- Fresh runner-managed candidate:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.33907413`
  - `val_bpb=0.20081880`
  - script eval wallclock: `591247ms`
  - runner-managed wallclock: `633936ms`
  - runner start-to-spawn: `536ms`
  - child runtime: `633400ms`
  - external top-level wallclock: `634143ms`
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.63995303`

## Required Comparisons
- Fresh control vs promoted `eval_035` admissibility anchor:
  - `val_loss`: `0.33904205 -> 0.33903990` (`-0.00000215`)
  - `val_bpb`: `0.20079980 -> 0.20079853` (`-0.00000127`)
  - script eval wallclock: `582272ms -> 582012ms` (`-260ms`)
  - runner-managed wallclock: `625013ms -> 626047ms` (`+1034ms`)
  - external top-level wallclock: `625177ms -> 626047ms` (`+870ms`)
- Fresh candidate vs fresh control:
  - `val_loss`: `0.33903990 -> 0.33907413` (`+0.00003423`)
  - `val_bpb`: `0.20079853 -> 0.20081880` (`+0.00002027`)
  - script eval wallclock: `582012ms -> 591247ms` (`+9235ms`)
  - runner-managed wallclock: `626047ms -> 633936ms` (`+7889ms`)
  - external top-level wallclock: `626047ms -> 634143ms` (`+8096ms`)
- Fresh candidate vs historical `eval_015` anchor:
  - `val_bpb`: `0.19974202 -> 0.20081880` (`+0.00107678`)

## Command / Environment Parity Check
- same helper path: `pass`
- same checkpoint path: `pass`
- same artifact path: `pass`
- same cwd: `pass`
- same `physicslm` environment: `pass`
- same runner path: `pass`
- same pinned GPUs via `0,1,2,3,4,5,6,7`: `pass`
- same wrapped child command family between fresh control and candidate: `pass`
- only wrapped-command differences between fresh control and candidate:
  - allowed `RUN_ID`
  - tested variable `TTT_LR=0.0025 -> 0.0020`

## Success Metric
Primary success criterion:
- candidate `val_bpb` improves on fresh control by at least `0.0001`

Secondary operational success criterion:
- candidate stays within `+20s` external wallclock of fresh control

Stretch success criterion:
- candidate beats `eval_015=0.19974202`

Outcome:
- primary quality success: `fail`
- secondary operational success: `pass`
- stretch success: `fail`

## Expected Effect
If the promoted `2097152`-bucket line was over-adapting at `TTT_LR=0.0025`, then lowering only `TTT_LR` to `0.0020` should improve post-export `val_bpb` while staying in roughly the same runtime band.

## Actual Result
- The fresh control passed the reviewed admissibility gate cleanly before the candidate was launched.
- The candidate preserved full command and identity parity with the fresh control except for the intended `TTT_LR` change, the allowed operational identifiers, and the candidate-side outer timing wrapper.
- Lowering `TTT_LR` to `0.0020` slightly regressed quality and slowed runtime:
  - `+0.00002027 BPB` vs the fresh control
  - `+9235ms` script
  - `+7889ms` runner-managed
  - `+8096ms` external
- The emitted n-gram telemetry stayed almost unchanged:
  - any-match fraction `0.98387585 -> 0.98387585`
  - avg alpha on matched `0.63990797 -> 0.63995303`

## Interpretation
- Classification: `hold`
- The promoted `2097152`-bucket legality line still prefers the more aggressive `TTT_LR=0.0025`.
- This is a clean negative answer for downward `TTT_LR` retuning on this helper lineage: the lower step size did not improve post-export `val_bpb` and also cost about `8s` of end-to-end runtime.
- `eval_015` remains the best same-family quality anchor by `0.00107678 BPB`, and the fresh control effectively reproduces the promoted `eval_035` result.

## Next Step
Hold `TTT_LR=0.0025` fixed as the quality default on the promoted `eval_035` legality line and move the next refinement round to a different single-variable question. Do not spend another immediate round on lower-`TTT_LR` retuning on this helper lineage unless a materially different operating point is introduced first.
