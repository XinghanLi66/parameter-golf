# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session `TTT_EPOCHS` check on the promoted `eval_038` legality line, but stopped after the fresh control because admissibility failed on runtime.

- Executed the reviewed brief materially as written up to the control gate:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, `context/reference_materials/user_proposed_ideas_eval_mixing.md`, and the active helper before launch
  - re-verified helper, checkpoint, and artifact identities before launch and again after the control run
  - recovered the exact promoted `eval_038` runner command family from on-disk metadata
  - launched one fresh runner-managed control on the exact promoted `eval_038` stack with `TTT_EPOCHS=4`
  - stopped before launching the `TTT_EPOCHS=3` candidate because the fresh control drifted massively in runtime versus the promoted `eval_038` line
- No code edits were made in this round.

## Experiment ID
`eval_039_eval038_ttt_epochs_pair`

## Category
- evaluation

Operational subtype: `single-variable TTT epoch-count refinement`

## Baseline / Comparison
Planned primary baseline:
- one fresh admissible runner-managed control on the promoted `eval_038=0.19974237` legality line with `TTT_EPOCHS=4`

Planned primary comparison:
- one immediate fresh runner-managed candidate on the exact same line with only `TTT_EPOCHS=3`

Historical anchors:
- promoted `eval_038=0.19974237`
- strongest historical same-family run `eval_015=0.19974202`
- prior epoch-count result `eval_034`, where `TTT_EPOCHS=3` was much faster but slightly worse on the older `EVAL_LOGIT_TEMP=0.95` line

## Hypothesis
On the stronger calibrated `EVAL_LOGIT_TEMP=1.0` line, the fourth TTT epoch may no longer buy enough quality to justify its runtime. If so, reducing only `TTT_EPOCHS` from `4` to `3` should keep post-export `val_bpb` essentially unchanged while recovering substantial wallclock.

## Why It Might Work
- leaderboard `#1` in `latest_sota_snapshot.md` uses legal score-first TTT with `3` epochs
- `eval_034` already showed that `TTT_EPOCHS=3` is a strong runtime lever, but that answer was measured on the older `EVAL_LOGIT_TEMP=0.95` operating point
- the promoted line now uses `NGRAM_EVAL_BUCKETS=2097152` and `EVAL_LOGIT_TEMP=1.0`, so epoch count was a legitimately reopened refinement question

## Minimal Intervention
No code edits in this round.

Planned semantic change:
- `TTT_EPOCHS: 4 -> 3`

Actual executed control arm changed only operational identifiers:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

The candidate arm was not launched.

## Variables To Change
Planned tested variable:
- `TTT_EPOCHS: 4 -> 3`

Actual executed semantic variables:
- none; the fresh control reran the promoted `TTT_EPOCHS=4` line exactly

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from `eval_038`
- exact checkpoint path, bytes, and SHA-256
- exact artifact path, bytes, and SHA-256
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `EVAL_STRIDE=64`
- `EVAL_LOGIT_TEMP=1.0`
- `TTT_LR=0.0025`
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

## Exact Top-Level Command Actually Run

Fresh control:

```bash
TIMEFORMAT='external_real_seconds=%3R'; time python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_039_eval038_ttt_epochs_pair/runner_control_8gpu \
  --run-name eval_039_runner_control_t1p00_e4_b2097152_lr0025 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_039_eval038_ttt_epochs_pair_runner_control \
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

Candidate status:
- not launched because the fresh control failed the reviewed admissibility gate on runtime

## Fresh Official Result
- Fresh runner-managed control:
  - GPU path: runner-managed `physicslm` on the pinned 8-GPU set
  - `val_loss=0.33725535`
  - `val_bpb=0.19974161`
  - script eval wallclock: `1190477ms`
  - runner-managed wallclock: `1237270ms`
  - runner start-to-spawn: `474ms`
  - child runtime: `1236796ms`
  - external top-level wallclock: `1237494ms`
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.65459666`
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
- Fresh control vs promoted `eval_038` anchor:
  - `val_loss`: `0.33725663 -> 0.33725535` (`-0.00000128`)
  - `val_bpb`: `0.19974237 -> 0.19974161` (`-0.00000076`)
  - script eval wallclock: `588813ms -> 1190477ms` (`+601664ms`)
  - runner-managed wallclock: `634685ms -> 1237270ms` (`+602585ms`)
  - external top-level wallclock: `634926ms -> 1237494ms` (`+602568ms`)
  - avg alpha on matched: `0.65459911 -> 0.65459666` (`-0.00000245`)
- Fresh control vs historical `eval_034` runtime-only candidate context:
  - external top-level wallclock: `558444ms -> 1237494ms` (`+679050ms`)
  - script eval wallclock: `514515ms -> 1190477ms` (`+675962ms`)
  - runner-managed wallclock: `558261ms -> 1237270ms` (`+679009ms`)

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

## Success Metric
Planned promotion criterion:
- candidate no worse than fresh control by more than `0.00005 BPB`
- and candidate saves at least `50s` external wallclock

Fresh-control admissibility gate:
- BPB gate: `pass`
- telemetry consistency gate: `pass`
- runtime context vs promoted `eval_038`: `fail`

Candidate launch gate:
- `fail`; candidate not launched

## Expected Effect
If the fourth TTT epoch no longer buys enough quality on the promoted `EVAL_LOGIT_TEMP=1.0` line, then reducing only `TTT_EPOCHS` from `4` to `3` should preserve post-export `val_bpb` while recovering substantial runtime.

## Actual Result
- The fresh control stayed semantically in-family with the promoted line:
  - slightly better `val_bpb` by `0.00000076`
  - slightly better `val_loss` by `0.00000128`
  - identical any-match fraction
  - identical matched-order histogram
  - essentially identical avg alpha on matched
- But the fresh control failed the reviewed admissibility gate catastrophically on runtime:
  - script eval wallclock increased by `601664ms`
  - runner-managed wallclock increased by `602585ms`
  - external top-level wallclock increased by `602568ms`
- Because the control was not comparison-clean versus the promoted `eval_038` line, the `TTT_EPOCHS=3` candidate was not launched.

## Interpretation
- Classification: `drift-stop`
- This is not evidence for or against changing `TTT_EPOCHS` on the promoted `EVAL_LOGIT_TEMP=1.0` line.
- The control proves the exact promoted helper/checkpoint/artifact stack can still reproduce the same quality regime, but not the same runtime regime, under the present session conditions.
- The old `eval_034` runtime-only answer on the earlier `EVAL_LOGIT_TEMP=0.95` line therefore does not cleanly transfer to this round, because the new control itself lost the runtime admissibility needed for a same-session epoch-count decision.

## Next Step
Re-establish one fresh in-gate control on the exact promoted `eval_038` line with `TTT_EPOCHS=4`, then rerun the same epoch-count-only pair. Do not treat this drift-stopped round as either a promotion or a rejection of `TTT_EPOCHS=3` on the promoted `EVAL_LOGIT_TEMP=1.0` legality baseline.
