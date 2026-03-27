# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase global scoring temperature calibration ablation on top of the locked `eval_027` PR809-style vectorized n-gram plus legal TTT line.

- Executed the reviewed brief materially as written:
  - read the reviewed brief, the required planning/report files, `context/reference_materials/latest_sota_snapshot.md`, `context/reference_materials/user_proposed_ideas_eval_mixing.md`, and the locked `eval_027` helper before editing
  - verified the exact locked helper, checkpoint, and artifact identities before any change
  - copied the exact `eval_027` helper into a fresh `eval_031` run directory and edited only that copied helper
  - added one default-off env knob `EVAL_LOGIT_TEMP`, applied only to neural scoring logits immediately before probability computation and before neural-to-n-gram mixing
  - reused one fixed non-official calibration slice from the frozen `eval_009` held-out train shard and recorded its exact source/offset/token-count identity
  - ran the required calibration grid `T in {0.95, 0.975, 1.00, 1.025, 1.05}` through `tools/gpu_experiment_runner.py` in `physicslm` on the pinned `8x NVIDIA L20Z` set
  - confirmed `T=1.0` parity on the calibration slice
  - launched exactly one full official candidate only after the best non-`1.0` temperature beat `T=1.0` on the slice by more than the reviewed `0.0002` gate
  - measured runner-managed and external wallclock on the official run

## Experiment ID
`eval_031_eval027_global_temperature_calibration`

## Category
- evaluation

Operational subtype: `scoring-only neural-logit temperature calibration on locked eval_027 legality line`

## Baseline / Comparison
Primary locked official baseline:
- `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`
  - `val_bpb=0.29117839`
  - script eval wallclock `574202ms`
  - managed wallclock `615s`

Fresh stability anchor on the same locked line:
- `eval_030` fresh control
  - `val_bpb=0.29117961`
  - script eval wallclock `583199ms`
  - managed wallclock `626554ms`

Calibration-slice parity anchor:
- locked same-helper held-out control from `eval_027`
  - `val_bpb=1.20586072`

## Hypothesis
The locked `eval_027` stack may still be slightly miscalibrated on the neural side after legal TTT and PR809-style n-gram backoff, so applying one global temperature only to neural scoring logits will improve post-export `val_bpb` without changing training, export bytes, or n-gram cache behavior.

## Why It Might Work
- This is a minimal evaluation-side test on top of a line that already contains the current top local legality mechanism stack.
- The user-priority temperature idea was already negative on the plain legal-TTT `arch_010` line (`eval_009`), but that does not make this redundant because `eval_027` adds the PR809 neural-plus-n-gram mixing path, which can change calibration.

## Minimal Intervention
Edit only the copied `eval_031` helper:

- add default-off `EVAL_LOGIT_TEMP`
- apply it only in the PR809 scorer where neural probabilities are formed
- leave TTT adaptation loss, cache updates, n-gram alpha logic, export, training, checkpoint, and artifact untouched

## Variables To Change
- `EVAL_LOGIT_TEMP` only
- fixed calibration sweep: `0.95, 0.975, 1.00, 1.025, 1.05`

## Variables To Hold Fixed
- exact locked `eval_027` helper lineage except for the new default-off temperature knob
- exact saved checkpoint and artifact used by `eval_027`
- exact PR809-style vectorized chunked n-gram settings
- exact legal TTT settings
- tokenizer, dataset, stride `64`
- `physicslm` environment
- GPU count and pinned device set
- no retraining
- no export rewrite
- no n-gram alpha/backoff changes
- no runner-path changes

## Identity Checks
- Helper:
  - source path: `runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337/train_gpt.py`
  - source bytes: `125178`
  - source SHA-256: `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`
  - copied edited path: `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`
  - copied edited bytes: `125663`
  - copied edited SHA-256: `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
- Saved checkpoint:
  - `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
  - bytes: `106178569`
  - SHA-256: `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- Saved artifact:
  - `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
  - bytes: `15555121`
  - SHA-256: `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

## Calibration Slice
This round reused the exact frozen non-official held-out train slice first created in `eval_009`:

- source shard: `/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024/fineweb_train_000000.bin`
- source shard header: magic `20240520`, version `1`
- source start token offset: `8388608`
- copied token count: `2097153`
- scored token count after load: `2097152`
- source end token offset, exclusive: `10485761`
- chunk coverage at `TTT_CHUNK_TOKENS=32768`: exactly `64` chunks
- created shard path reused here: `runs/eval_009_arch010_legal_ttt_temperature_seed1337/heldout_data/fineweb_val_000000.bin`
- created shard bytes: `4195330`
- created shard SHA-256: `8b5e92cca71fcfb03dff3a5b2cbf37b25e15a476e8218d253006f1bbcb4db556`

## Exact Child Command Shape

```bash
env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
  RUN_ID=... \
  EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
  EVAL_LOGIT_TEMP=... \
  TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
  TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
  NGRAM_EVAL_ENABLED=1 \
  NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1 \
  NGRAM_EVAL_BATCH_TORCH_STATS=1 \
  NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1 \
  EVAL_ONLY_FINAL_MODEL_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt \
  EVAL_ONLY_ARTIFACT_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz \
  DATA_PATH=... \
  TOKENIZER_PATH=/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
  torchrun --standalone --nproc_per_node=8 \
  /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/train_gpt.py
```

## Exact Top-Level Commands Actually Run
Calibration sweep command shape:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/calibration_t<TAG>_8gpu \
  --run-name eval_031_calibration_t<TAG> \
  --timeout-seconds 7200 -- \
  env ... EVAL_LOGIT_TEMP=<T> ... \
    DATA_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_009_arch010_legal_ttt_temperature_seed1337/heldout_data \
    ... \
    /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/train_gpt.py
```

Official selected-temperature command:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/official_t0p95_8gpu \
  --run-name eval_031_official_t0p95 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_031_eval027_global_temperature_calibration_official_t0p95 \
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

## Calibration Results
- GPUs for every calibration run: `0,1,2,3,4,5,6,7`
- Held-out results:
  - `T=0.95`: `val_loss=2.02724473`, `val_bpb=1.20029274`, managed wallclock `67580ms`
  - `T=0.975`: `val_loss=2.03140228`, `val_bpb=1.20275434`, managed wallclock `66905ms`
  - `T=1.00`: `val_loss=2.03667307`, `val_bpb=1.20587508`, managed wallclock `66375ms`
  - `T=1.025`: `val_loss=2.04287257`, `val_bpb=1.20954568`, managed wallclock `66422ms`
  - `T=1.05`: `val_loss=2.05002117`, `val_bpb=1.21377823`, managed wallclock `66620ms`

## Calibration Gate Check
- `T=1.0` parity vs locked same-helper held-out control `1.20586072`:
  - this round `T=1.0`: `1.20587508`
  - delta: `+0.00001436`
  - parity decision: `pass`
- Best non-`1.0` temperature:
  - selected `T=0.95`
  - held-out gain vs `T=1.0`: `-0.00558234`
  - reviewed minimum gain: `-0.0002`
  - gate decision: `pass`

## Official Candidate Result
- GPU indices: `0,1,2,3,4,5,6,7`
- Exact result:
  - `val_loss=0.49102869`
  - `val_bpb=0.29081485`
- Script eval wallclock: `584865ms`
- Managed wallclock from runner: `628844ms`
- External top-level wallclock: `629.130s`
- Historical `eval_027` comparison:
  - `val_bpb`: `0.29117839 -> 0.29081485` (`-0.00036354`)
  - script eval wallclock: `574202ms -> 584865ms` (`+10663ms`)
  - managed wallclock: `615000ms -> 628844ms` (`+13844ms`)
- Fresh `eval_030` control comparison:
  - `val_bpb`: `0.29117961 -> 0.29081485` (`-0.00036476`)
  - script eval wallclock: `583199ms -> 584865ms` (`+1666ms`)
  - managed wallclock: `626554ms -> 628844ms` (`+2290ms`)
  - external wallclock: `626721ms -> 629130ms` (`+2409ms`)

## Success Metric
Primary success criterion:
- full official post-export `val_bpb < 0.29117839`

Target improvement:
- `>= 0.0005` BPB better than the locked baseline

Guardrails:
- best non-`1.0` temperature must beat `T=1.0` on the calibration slice by at least `0.0002`
- script eval should stay in the same band as `eval_027`
- script eval should not exceed `600000ms`

Outcome:
- calibration gate passed strongly
- primary success criterion passed
- target improvement missed
- script eval guardrail passed

## Expected Effect
- Slight full-val BPB improvement if the PR809 legality line remained globally miscalibrated on the neural side after neural-plus-n-gram mixing.

## Actual Result
- The copied helper edit stayed clean and default-off.
- Artifact bytes and hashes stayed unchanged before and after all runs.
- The fixed calibration slice selected `T=0.95`, not `T=1.0`.
- The selected `T=0.95` transferred to a real full official improvement at `0.29081485`.
- Runtime remained script-legal but managed-illegal:
  - script headroom vs `600000ms`: `15135ms`
  - managed overrun vs `600000ms`: `28844ms`

## Interpretation
This is a controlled positive calibration result on the locked PR809 legality line.

- It is not a parity failure: `T=1.0` held-out parity stayed within noise.
- It is not selector overfit: the selected `T=0.95` improved the full official run versus both `eval_027` and fresh `eval_030`.
- It is not large enough to satisfy the more ambitious `>=0.0005` improvement target.

Decision:
- `EVAL_LOGIT_TEMP=0.95` is conditionally promotable on the locked `eval_027` line.
- Global temperature scaling on the PR809 legality line should not be retired.
- Nearby scalar sweeps should stop until this selected point is either confirmed or rejected by a fresh full official rerun.

## Next Step
If more confidence is needed before promotion, run one fresh full official confirmation of `T=0.95` against `T=1.0` on the exact locked artifact and pinned GPUs. If that repeats, promote `eval_031` as the new active legality baseline and stop nearby scalar-temperature sweeps.
