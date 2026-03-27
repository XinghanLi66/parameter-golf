# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase fresh official confirmation pair on the locked `eval_031` PR809 legality lineage.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, the required planning/report files, and the locked `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py` helper before running anything
  - re-verified helper, checkpoint, and artifact identities before launch and again after both runs
  - made no code edits, no export edits, no checkpoint edits, and no runner edits
  - ran exactly one fresh full official control at `EVAL_LOGIT_TEMP=1.0`
  - ran exactly one fresh full official candidate at `EVAL_LOGIT_TEMP=0.95`
  - used `tools/gpu_experiment_runner.py` in `physicslm` on pinned GPUs `0,1,2,3,4,5,6,7`
  - recorded script eval wallclock, runner-managed wallclock, and external top-level wallclock for both runs

## Experiment ID
`eval_032_eval031_temperature_confirmation_pair`

## Category
- evaluation

Operational subtype: `fresh full-official same-helper confirmation pair for global neural-logit temperature`

## Baseline / Comparison
Primary decision pair on the locked `eval_031` lineage:
- fresh official control `EVAL_LOGIT_TEMP=1.0`
- fresh official candidate `EVAL_LOGIT_TEMP=0.95`

Historical anchors reported but not used as the primary promotion decision:
- `eval_027`: `val_bpb=0.29117839`, script eval `574202ms`, managed `615000ms`
- `eval_030` fresh control: `val_bpb=0.29117961`, script eval `583199ms`, managed `626554ms`, external `626721ms`
- prior `eval_031` selected official run at `T=0.95`: `val_bpb=0.29081485`, script eval `584865ms`, managed `628844ms`, external `629130ms`

## Hypothesis
On the locked PR809 legality line, `EVAL_LOGIT_TEMP=0.95` gives a real repeatable full-official BPB improvement over `EVAL_LOGIT_TEMP=1.0` rather than reflecting a one-off selected run.

## Why It Might Work
- `eval_031` already showed aligned selector evidence on the fixed held-out slice plus one official `T=0.95` win.
- This round isolates the only unresolved variable: fresh same-helper repeatability on a back-to-back official control/candidate pair.

## Minimal Intervention
No helper or runner edits in this round.

Only varied:
- `EVAL_LOGIT_TEMP=1.0` for the fresh control
- `EVAL_LOGIT_TEMP=0.95` for the fresh candidate

Also changed only the operational identifiers required to keep the runs separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Change
- `EVAL_LOGIT_TEMP`
  - control `1.0`
  - candidate `0.95`

## Variables To Hold Fixed
- exact `eval_031` helper path, bytes, and SHA-256
- exact saved checkpoint path, bytes, and SHA-256
- exact saved artifact path, bytes, and SHA-256
- exact PR809-style vectorized chunked n-gram settings
- exact legal TTT settings
- tokenizer and dataset
- evaluation stride `64`
- runner path
- `physicslm` environment
- pinned GPU set `0,1,2,3,4,5,6,7`
- no retraining
- no export rewrite
- no other eval-side calibration change
- no additional temperature values

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
- helper unchanged before vs after both fresh runs
- checkpoint unchanged before vs after both fresh runs
- artifact unchanged before vs after both fresh runs

## Exact Top-Level Commands Actually Run
Fresh control:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_032_eval031_temp_confirmation_pair/official_t1p0_8gpu \
  --run-name eval_032_official_t1p0 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_032_eval031_temp_confirmation_pair_official_t1p0 \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=1.0 \
    TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
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

Fresh candidate:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_032_eval031_temp_confirmation_pair/official_t0p95_8gpu \
  --run-name eval_032_official_t0p95 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_032_eval031_temp_confirmation_pair_official_t0p95 \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=0.95 \
    TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
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
- Fresh control `T=1.0`
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.49164677`
  - `val_bpb=0.29118091`
  - script eval wallclock: `591399ms`
  - runner-managed wallclock: `633253ms`
  - external top-level wallclock: `633409ms`
- Fresh candidate `T=0.95`
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.49102508`
  - `val_bpb=0.29081271`
  - script eval wallclock: `584876ms`
  - runner-managed wallclock: `627182ms`
  - external top-level wallclock: `627421ms`

## Required Comparisons
- Fresh candidate vs fresh control:
  - `val_loss`: `0.49164677 -> 0.49102508` (`-0.00062169`)
  - `val_bpb`: `0.29118091 -> 0.29081271` (`-0.00036820`)
  - script eval wallclock: `591399ms -> 584876ms` (`-6523ms`)
  - runner-managed wallclock: `633253ms -> 627182ms` (`-6071ms`)
  - external top-level wallclock: `633409ms -> 627421ms` (`-5988ms`)
- Fresh candidate vs prior `eval_031` selected official run:
  - `val_bpb`: `0.29081485 -> 0.29081271` (`-0.00000214`)
- Fresh control vs `eval_027`:
  - `val_bpb`: `0.29117839 -> 0.29118091` (`+0.00000252`)
  - script eval wallclock: `574202ms -> 591399ms` (`+17197ms`)
  - runner-managed wallclock: `615000ms -> 633253ms` (`+18253ms`)
- Fresh control vs `eval_030`:
  - `val_bpb`: `0.29117961 -> 0.29118091` (`+0.00000130`)
  - script eval wallclock: `583199ms -> 591399ms` (`+8200ms`)
  - runner-managed wallclock: `626554ms -> 633253ms` (`+6699ms`)
  - external top-level wallclock: `626721ms -> 633409ms` (`+6688ms`)
- Fresh candidate vs `eval_027`:
  - `val_bpb`: `0.29117839 -> 0.29081271` (`-0.00036568`)
  - script eval wallclock: `574202ms -> 584876ms` (`+10674ms`)
  - runner-managed wallclock: `615000ms -> 627182ms` (`+12182ms`)

## Fresh-Control Admissibility Check
- control drift vs `eval_027`: `+0.00000252`
- control drift vs `eval_030`: `+0.00000130`
- reviewed drift threshold: `0.0002`
- admissibility decision: `pass`

## Success Metric
Primary success criterion:
- fresh official `T=0.95` beats fresh official `T=1.0` on post-export `val_bpb`

Promotion threshold:
- improvement of at least `0.0002` BPB vs the fresh `T=1.0` control

Guardrails:
- helper bytes/hash unchanged
- checkpoint bytes/hash unchanged
- artifact bytes/hash unchanged
- script eval remains below `600000ms`

Outcome:
- primary success criterion: `pass`
- promotion threshold: `pass` with `-0.00036820`
- fresh-control admissibility: `pass`
- script eval guardrail: `pass` for both runs

## Expected Effect
If the prior `eval_031` win was real, then the fresh full official `T=0.95` run should again beat the fresh full official `T=1.0` run by a meaningful margin without any identity drift.

## Actual Result
- The pair stayed controlled and identity-clean.
- The fresh `T=1.0` control remained fully in-family with both `eval_027` and `eval_030`.
- The fresh `T=0.95` candidate beat the fresh `T=1.0` control by `0.00036820 BPB`, comfortably above the reviewed `0.0002` promotion threshold.
- The fresh `T=0.95` candidate also slightly beat the prior `eval_031` selected official run by `0.00000214 BPB`, so the earlier result was not a one-off spike.

## Interpretation
This is a cleanly confirmatory refinement result.

- Conclusion label: `promote`
- `EVAL_LOGIT_TEMP=0.95` is now confirmed as the default evaluation setting on the locked `eval_031` PR809 legality line.
- Nearby scalar-temperature tuning on this line should now be treated as closed unless a materially different calibration mechanism is proposed.

## Next Step
Hold the promoted `EVAL_LOGIT_TEMP=0.95` setting fixed and move the next refinement round to a genuinely different single-variable question. If managed-runtime work is revisited, do not use this temperature round for launcher conclusions; re-open that path only behind a fresh admissible control.
