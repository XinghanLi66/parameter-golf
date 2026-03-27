# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase launcher-path control pair on the locked promoted `eval_031` PR809 legality lineage at `EVAL_LOGIT_TEMP=0.95`.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, the required planning/report files, the locked helper, and `tools/gpu_experiment_runner.py` before running anything
  - re-verified helper, checkpoint, and artifact identities before launch and again after both runs
  - made no code edits, no helper edits, no export edits, no checkpoint edits, and no runner edits
  - ran exactly one fresh runner control through `tools/gpu_experiment_runner.py`
  - recovered the exact wrapped child command from the fresh control `metadata.json`
  - ran exactly one direct-launch candidate only after the fresh control passed the reviewed admissibility gate
  - kept the same `physicslm` environment, cwd, GPU pinning, helper, checkpoint, artifact, `EVAL_LOGIT_TEMP=0.95`, legal TTT settings, PR809 vectorized n-gram settings, tokenizer, dataset, and stride
  - recorded script eval wallclock, runner-managed wallclock for the control, and external top-level wallclock for both arms

## Experiment ID
`eval_033_eval031_direct_launch_pair`

## Category
- evaluation

Operational subtype: `fresh promoted-line launcher-path control pair`

## Baseline / Comparison
Primary comparison on the locked promoted `eval_031` lineage:
- fresh runner control at `EVAL_LOGIT_TEMP=0.95`
- fresh direct-launch candidate reusing the exact same wrapped child command and env, bypassing only the outer runner path

Historical admissibility anchors:
- `eval_031` official candidate: `val_bpb=0.29081485`
- `eval_032` fresh confirmation candidate: `val_bpb=0.29081271`, script eval `584876ms`, runner `627182ms`, external `627421ms`

## Hypothesis
On the locked promoted `eval_031` legality line, materially remaining runtime overhead is still in the outer launcher path, so bypassing `tools/gpu_experiment_runner.py` should reduce end-to-end wallclock without changing post-export `val_bpb`.

## Why It Might Work
- `eval_028` showed helper-local total process time could already fit under budget.
- `eval_029` showed runner-internal micro-trims were not enough.
- `eval_030` did not answer the direct-launch question because its fresh control failed the gate before the candidate ran.
- That left direct launcher bypass as the clean remaining launcher-path variable on the current promoted line.

## Minimal Intervention
No helper or runner edits in this round.

Only varied:
- launcher path
  - control: `tools/gpu_experiment_runner.py`
  - candidate: direct launch of the same wrapped child command

Also changed only the operational identifiers required to keep the runs separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`
- direct-launch capture directory

## Variables To Change
- outer launch path
  - `runner`
  - `direct launch`

## Variables To Hold Fixed
- exact `eval_031` helper path, bytes, and SHA-256
- exact saved checkpoint path, bytes, and SHA-256
- exact saved artifact path, bytes, and SHA-256
- `EVAL_LOGIT_TEMP=0.95`
- exact legal TTT settings
- exact PR809-style vectorized chunked n-gram settings
- tokenizer and dataset
- evaluation stride `64`
- `physicslm` environment
- working directory
- pinned GPU set `0,1,2,3,4,5,6,7`
- no retraining
- no export rewrite
- no helper edits

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
Fresh runner control:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_033_eval031_direct_launch_pair/runner_control_8gpu \
  --run-name eval_033_runner_control_t0p95 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_033_eval031_direct_launch_pair_runner_control \
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

Fresh direct-launch candidate:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
conda run --no-capture-output -n physicslm \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_033_eval031_direct_launch_pair_direct_candidate \
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
- Fresh runner control:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.49102692`
  - `val_bpb=0.29081380`
  - script eval wallclock: `585452ms`
  - runner-managed wallclock: `627968ms`
  - runner start-to-spawn: `389ms`
  - child runtime: `627579ms`
  - external top-level wallclock: `628139ms`
- Fresh direct-launch candidate:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.49102993`
  - `val_bpb=0.29081558`
  - script eval wallclock: `583370ms`
  - external top-level wallclock: `625537ms`

## Required Comparisons
- Fresh control vs `eval_032` anchor:
  - `val_bpb`: `0.29081271 -> 0.29081380` (`+0.00000109`)
  - external top-level wallclock: `627421ms -> 628139ms` (`+718ms`)
- Fresh candidate vs fresh control:
  - `val_loss`: `0.49102692 -> 0.49102993` (`+0.00000301`)
  - `val_bpb`: `0.29081380 -> 0.29081558` (`+0.00000178`)
  - script eval wallclock: `585452ms -> 583370ms` (`-2082ms`)
  - external top-level wallclock: `628139ms -> 625537ms` (`-2602ms`)
- Fresh candidate vs `eval_032` anchor:
  - `val_bpb`: `0.29081271 -> 0.29081558` (`+0.00000287`)
  - external top-level wallclock: `627421ms -> 625537ms` (`-1884ms`)

## Fresh-Control Admissibility Check
- control drift vs `eval_032` BPB anchor: `+0.00000109`
- control external wallclock vs `eval_032`: `+718ms`
- reviewed thresholds:
  - BPB within `0.0002`
  - external wallclock no worse than `+15000ms`
- admissibility decision: `pass`

## Command / Environment Parity Check
- same cwd across arms: `pass`
- same `physicslm` environment across arms: `pass`
- same pinned GPUs across arms via `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`: `pass`
- same wrapped child command recovered from fresh control metadata and reused for direct launch: `pass`
- only wrapped-command token difference was the allowed operational identifier:
  - `RUN_ID=eval_033_eval031_direct_launch_pair_runner_control`
  - `RUN_ID=eval_033_eval031_direct_launch_pair_direct_candidate`

## Success Metric
Primary success criterion:
- candidate `val_bpb` within `±0.0001` of fresh control
- candidate external wallclock at least `5s` lower than fresh control

Promotion threshold:
- candidate `val_bpb` within `±0.0001` of fresh control
- candidate external wallclock at least `10s` lower than fresh control

Guardrails:
- helper bytes/hash unchanged
- checkpoint bytes/hash unchanged
- artifact bytes/hash unchanged

Outcome:
- fresh-control admissibility: `pass`
- BPB comparability guardrail: `pass`
- primary runtime success criterion: `fail` with only `-2602ms`
- reviewed classification threshold for `<3s` runtime savings: `negative`
- secondary runtime target vs `eval_032` anchor: `pass` only by `-1884ms`, which is not enough to overturn the round classification

## Expected Effect
If outer launcher overhead was still materially unresolved on the promoted line, the direct-launch candidate should preserve BPB while saving at least `5s` externally and ideally at least `10s`.

## Actual Result
- The fresh control was fully admissible against the `eval_032` anchor.
- The direct-launch candidate preserved BPB cleanly on the promoted line.
- Direct launch was only `2602ms` faster externally than the fresh runner control.
- That runtime delta is below the reviewed `3s` minimum for a meaningful positive signal.

## Interpretation
This is a controlled negative refinement result for launcher bypass on the promoted `eval_031` `T=0.95` line.

- Conclusion label: `negative`
- Direct launch does not save enough top-level wallclock on this line to become the new legality/runtime baseline.
- The launcher-path question is now effectively closed on this promoted line unless a genuinely different platform-side condition appears.

## Next Step
Hold the promoted `EVAL_LOGIT_TEMP=0.95` setting fixed and stop spending immediate rounds on runner-vs-direct-launch path changes for this line. Move the next refinement round to a genuinely different single-variable question rather than another nearby launcher-path rerun.
