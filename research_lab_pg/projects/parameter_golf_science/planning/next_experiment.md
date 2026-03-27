# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase single-variable epoch-count ablation on the promoted `eval_031 / eval_032 / eval_033` legality line at `EVAL_LOGIT_TEMP=0.95`.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `context/reference_materials/user_proposed_ideas_eval_mixing.md`, `context/reference_materials/sota_record_01_1.11940_2026-03-23_LeakyReLU_LegalTTT_ParallelMuon.md`, the required planning/report files, the active helper, and `tools/gpu_experiment_runner.py` before launching
  - re-verified helper, checkpoint, and artifact identities before launch and again after the run
  - confirmed `TTT_EPOCHS` was already env-configurable on the active helper, so no code edits were needed
  - ran exactly one fresh runner-managed candidate through `tools/gpu_experiment_runner.py`
  - kept the same `physicslm` environment, cwd, runner path, pinned GPUs, helper, checkpoint, artifact, tokenizer, dataset, stride, `EVAL_LOGIT_TEMP=0.95`, legal TTT settings, and PR809 vectorized n-gram settings
  - changed only `TTT_EPOCHS` from `4` to `3` plus required operational identifiers such as `RUN_ID`, runner log dir, and runner run name

## Experiment ID
`eval_034_eval031_ttt_epochs3_candidate`

## Category
- evaluation

Operational subtype: `single-variable TTT epoch-count refinement`

## Baseline / Comparison
Primary comparison:
- fresh admissible runner-managed control from `eval_033` on the promoted line with `TTT_EPOCHS=4`: `val_bpb=0.29081380`
- fresh runner-managed candidate on the same line with `TTT_EPOCHS=3`

Historical admissibility anchors:
- `eval_032` promoted candidate: `val_bpb=0.29081271`, script `584876ms`, runner `627182ms`, external `627421ms`
- `eval_033` fresh runner control: `val_bpb=0.29081380`, script `585452ms`, runner `627968ms`, external `628139ms`

## Hypothesis
On the promoted `T=0.95` PR809 legality line, the fourth TTT epoch is unnecessary or mildly over-adapts each chunk after n-gram mixing and temperature calibration. Reducing to `TTT_EPOCHS=3` should preserve or improve post-export `val_bpb` while reducing eval runtime.

## Why It Might Work
- the live official #1 record uses legal score-first TTT with `3` epochs
- the promoted local line still used `4` epochs
- temperature calibration and launcher-path variation were already closed, so epoch count was the clean remaining evaluation-side mismatch

## Minimal Intervention
No code edits in this round.

Only varied:
- `TTT_EPOCHS: 4 -> 3`

Also changed only the operational identifiers required to keep the run separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Change
- `TTT_EPOCHS: 4 -> 3`

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from `eval_031`
- exact checkpoint path, bytes, and SHA-256
- exact artifact path, bytes, and SHA-256
- `EVAL_LOGIT_TEMP=0.95`
- `TTT_LR=0.0025`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `NGRAM_EVAL_ENABLED=1`
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
- helper unchanged before vs after the run
- checkpoint unchanged before vs after the run
- artifact unchanged before vs after the run

## Exact Top-Level Command Actually Run

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_034_eval031_ttt_epochs3_candidate/runner_candidate_8gpu \
  --run-name eval_034_ttt_epochs3_t0p95 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_034_eval031_ttt_epochs3_candidate \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=0.95 \
    TTT_LR=0.0025 TTT_EPOCHS=3 TTT_CHUNK_TOKENS=32768 \
    TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
    NGRAM_EVAL_ENABLED=1 NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1 \
    NGRAM_EVAL_BATCH_TORCH_STATS=1 NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1 \
    EVAL_ONLY_FINAL_MODEL_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt \
    EVAL_ONLY_ARTIFACT_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz \
    DATA_PATH=/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024 \
    TOKENIZER_PATH=/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
    torchrun --standalone --nproc_per_node=8 \
    /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/train_gpt.py
```

## Fresh Official Results
- Fresh runner-managed candidate:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.49109611`
  - `val_bpb=0.29085478`
  - script eval wallclock: `514515ms`
  - runner-managed wallclock: `558261ms`
  - runner start-to-spawn: `471ms`
  - child runtime: `557790ms`
  - external top-level wallclock: `558444ms`

## Required Comparisons
- Fresh candidate vs fresh `eval_033` runner control:
  - `val_loss`: `0.49102692 -> 0.49109611` (`+0.00006919`)
  - `val_bpb`: `0.29081380 -> 0.29085478` (`+0.00004098`)
  - script eval wallclock: `585452ms -> 514515ms` (`-70937ms`)
  - runner-managed wallclock: `627968ms -> 558261ms` (`-69707ms`)
  - external top-level wallclock: `628139ms -> 558444ms` (`-69695ms`)
- Fresh candidate vs promoted `eval_032` anchor:
  - `val_bpb`: `0.29081271 -> 0.29085478` (`+0.00004207`)
  - script eval wallclock: `584876ms -> 514515ms` (`-70361ms`)
  - runner-managed wallclock: `627182ms -> 558261ms` (`-68921ms`)
  - external top-level wallclock: `627421ms -> 558444ms` (`-68977ms`)

## Command / Environment Parity Check
- same helper path: `pass`
- same checkpoint path: `pass`
- same artifact path: `pass`
- same cwd: `pass`
- same `physicslm` environment: `pass`
- same runner path: `pass`
- same pinned GPUs via `0,1,2,3,4,5,6,7`: `pass`
- same wrapped child command family as fresh `eval_033` control: `pass`
- only wrapped-command differences vs fresh `eval_033` control:
  - allowed `RUN_ID`
  - tested variable `TTT_EPOCHS=4 -> 3`

## Success Metric
Primary success criterion:
- candidate `val_bpb` improves on fresh `eval_033` control by at least `0.0001`

Secondary operational success criterion:
- candidate stays within `±0.0001 BPB` of fresh `eval_033`
- candidate saves at least `20s` on external or runner-managed wallclock

Outcome:
- primary quality success: `fail`
- secondary operational success: `pass`

## Expected Effect
If the fourth TTT epoch was unnecessary on the promoted `T=0.95` PR809 legality line, then `TTT_EPOCHS=3` should preserve or improve BPB while running faster than the fresh `TTT_EPOCHS=4` control.

## Actual Result
- The candidate preserved full command and identity parity with the fresh `eval_033` runner control except for the intended `TTT_EPOCHS` change and operational `RUN_ID`.
- Reducing `TTT_EPOCHS` to `3` made the run much faster:
  - `-70937ms` script
  - `-69707ms` runner-managed
  - `-69695ms` external
- But quality regressed:
  - `val_bpb` worsened by `+0.00004098` vs fresh `eval_033`
  - `val_bpb` worsened by `+0.00004207` vs promoted `eval_032`

## Interpretation
- Classification: `runtime-only operational win`
- The primary hypothesis is not supported as a quality-side promotion: the fourth TTT epoch still buys a small but real BPB gain on this line.
- The run does satisfy the reviewed secondary operational success criterion, because the BPB regression stayed inside `±0.0001` while wallclock improved by about `70s`.
- `TTT_EPOCHS=4` should remain the promoted quality default on the locked `T=0.95` PR809 legality line.
- `TTT_EPOCHS=3` is worth remembering as a runtime-optimized operational variant when evaluation speed matters more than the last `~4.1e-5` BPB.

## Next Step
Close TTT epoch count on this line as follows:
- quality default: keep `TTT_EPOCHS=4`
- runtime-optimized variant: `TTT_EPOCHS=3`

The next refinement round should move to a genuinely different single-variable question on the promoted `EVAL_LOGIT_TEMP=0.95` legality line rather than revisiting nearby epoch-count reruns.
