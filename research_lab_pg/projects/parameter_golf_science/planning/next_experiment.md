# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase direct-launcher ablation attempt on top of the locked `eval_027` PR `#809` legality line, but the round stopped after the required fresh control missed the acceptance gate.

- Executed the reviewed brief materially as written:
  - read the reviewed brief, the required planning/report files, `context/reference_materials/latest_sota_snapshot.md`, and the prior `eval_027` / `eval_028` / `eval_029` metadata needed to recover the exact child command and lineage
  - changed no repo code and edited no helper, scorer, export, or runner files
  - verified the exact `eval_027` helper bytes plus the saved checkpoint and artifact bytes and SHA-256 values before launch
  - recovered the exact locked child command from the prior fresh-control metadata and reused it with a fresh shared `RUN_ID`
  - ran one fresh official control through the default `tools/gpu_experiment_runner.py` path in `physicslm`
  - measured outer wallclock externally on the top-level launcher
  - checked the reviewed control gate immediately after the run
  - stopped before the direct-launch candidate because the control missed the managed-wallclock gate by `1554ms`

## Experiment ID
`eval_030_eval027_direct_launcher_ablation`

## Category
- evaluation

Operational subtype: `runtime-only direct-launcher ablation on locked eval_027 legality line`

## Baseline / Comparison
Primary historical anchor:
- `eval_027`: `val_bpb=0.29117839`, script eval wallclock `574202ms`, managed wallclock `615s`

Nearest fresh-control context:
- `eval_029` fresh control: `val_bpb=0.29117992`, script eval wallclock `582051ms`, managed wallclock `624825ms`

Reviewed acceptance gate before any candidate launch:
- `val_bpb` within `±0.0001` of historical `eval_027`
- managed wallclock no worse than `+10s` versus historical `eval_027`

## Hypothesis
If a material share of the remaining managed overrun comes from the outer launcher path rather than the child eval itself, then bypassing `tools/gpu_experiment_runner.py` with a direct shell launch of the exact locked child command should reduce end-to-end wallclock by at least `10s` while preserving `val_bpb` within noise.

## Why It Might Work
- `eval_027` already made the script path legal.
- `eval_028` showed helper-local total process time can fit under `600s`.
- `eval_029` showed nearby repo-runner trimming did not solve the miss.
- Research memory still left a genuinely different direct-launcher path as the last unresolved repo-adjacent runtime lever.

## Minimal Intervention
Change only the outer launcher path:

- control via `tools/gpu_experiment_runner.py`
- candidate planned as a direct `physicslm` launch with `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`

No repo files were edited for this round.

## Variables To Change
- outer launcher path only

## Variables To Hold Fixed
- exact `eval_027` helper bytes and SHA-256
- exact saved `final_model.pt` bytes and SHA-256
- exact saved `final_model.int6.ptz` bytes and SHA-256
- exact official `legal_ttt_exact` child command semantics
- exact PR809-style vectorized chunked n-gram settings
- exact TTT settings
- tokenizer, dataset, stride `64`
- `physicslm` environment
- exact pinned GPU indices
- no retraining
- no export rewrite
- no scorer-side edits
- no helper-side edits
- same outer wallclock measurement method for both arms
- same outer stdout/stderr capture policy for both arms

## Identity Checks
- Helper:
  - `runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337/train_gpt.py`
  - bytes: `125178`
  - SHA-256: `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`
- Saved checkpoint:
  - `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
  - bytes: `106178569`
  - SHA-256: `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- Saved artifact:
  - `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
  - bytes: `15555121`
  - SHA-256: `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

## Exact Child Command Recovered

```bash
env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
  RUN_ID=eval_030_eval027_direct_launcher_ablation_shared \
  EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
  TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
  TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
  NGRAM_EVAL_ENABLED=1 \
  NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1 \
  NGRAM_EVAL_BATCH_TORCH_STATS=1 \
  NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1 \
  EVAL_ONLY_FINAL_MODEL_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt \
  EVAL_ONLY_ARTIFACT_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz \
  DATA_PATH=/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024 \
  TOKENIZER_PATH=/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
  torchrun --standalone --nproc_per_node=8 \
  /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337/train_gpt.py
```

## Exact Top-Level Commands

Control command actually run:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_030_eval027_direct_launcher_ablation/control_via_runner_8gpu \
  --run-name eval_030_control_via_runner \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_030_eval027_direct_launcher_ablation_shared \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
    TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
    NGRAM_EVAL_ENABLED=1 NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1 \
    NGRAM_EVAL_BATCH_TORCH_STATS=1 NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1 \
    EVAL_ONLY_FINAL_MODEL_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt \
    EVAL_ONLY_ARTIFACT_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz \
    DATA_PATH=/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024 \
    TOKENIZER_PATH=/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
    torchrun --standalone --nproc_per_node=8 \
    /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337/train_gpt.py
```

Candidate command planned but not run after the gate failure:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
PROPOSAL_LAB_SELECTED_GPUS=0,1,2,3,4,5,6,7 \
PROPOSAL_LAB_DEVICE=gpu \
conda run --no-capture-output -n physicslm \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_030_eval027_direct_launcher_ablation_shared \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
    TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
    NGRAM_EVAL_ENABLED=1 NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1 \
    NGRAM_EVAL_BATCH_TORCH_STATS=1 NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1 \
    EVAL_ONLY_FINAL_MODEL_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt \
    EVAL_ONLY_ARTIFACT_PATH=/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz \
    DATA_PATH=/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024 \
    TOKENIZER_PATH=/newcpfs/lxh/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
    torchrun --standalone --nproc_per_node=8 \
    /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337/train_gpt.py
```

## Fresh Control Result
- GPU indices: `0,1,2,3,4,5,6,7`
- Exact result:
  - `val_loss=0.49164458`
  - `val_bpb=0.29117961`
- Script eval wallclock: `583199ms`
- Managed wallclock from runner: `626554ms`
- External top-level wallclock: `626721ms`
- Historical `eval_027` comparison:
  - `val_bpb`: `0.29117839 -> 0.29117961` (`+0.00000122`)
  - managed wallclock: `615000ms -> 626554ms` (`+11554ms`)
- Fresh `eval_029` control comparison:
  - `val_bpb`: `0.29117992 -> 0.29117961` (`-0.00000031`)
  - script eval wallclock: `582051ms -> 583199ms` (`+1148ms`)
  - managed wallclock: `624825ms -> 626554ms` (`+1729ms`)

## Control Acceptance Gate
- BPB gate: `pass`
- Managed-wallclock gate: `fail`
- Gate decision: `stop`

Reason:
- the reviewed gate allowed at most `625000ms`
- the fresh control landed at `626554ms`
- overrun vs gate: `+1554ms`

## Candidate
- Not run.
- Per the reviewed brief, the direct-launch candidate had to be skipped because the fresh control missed the acceptance gate, so this round must be recorded as environment drift rather than launcher evidence.

## Success Metric
Primary success criterion:
- candidate outer wallclock `<=600s`

Secondary:
- at least `10s` reduction versus fresh control if full legality is not reached

Outcome:
- fresh control quality stayed inside the reviewed BPB tolerance
- fresh control managed wallclock failed the reviewed admission gate
- direct-launch candidate was not executed

## Expected Effect
- Keep BPB locked while reducing end-to-end wallclock enough to test whether bypassing the repo runner closes the remaining managed-legality gap.

## Actual Result
- The exact helper and artifact lineage stayed unchanged before and after the control run.
- The fresh control remained quality-stable at `legal_ttt_exact val_bpb=0.29117961`.
- The fresh control missed the reviewed managed-wallclock gate at `626554ms`, which is `+11554ms` versus historical `eval_027` and `+1554ms` beyond the allowed `+10s` drift.
- The direct-launch candidate was therefore not run.

## Interpretation
This round is a controlled drift stop, not a direct-launch positive or negative result.

- The last unresolved direct-launcher hypothesis remains unanswered.
- The evidence from this round is only that the environment was slightly slower than the admissible band for a fair comparison.
- `eval_027` remains the active legality baseline.

## Next Step
If runtime-legality work is still worth pursuing, first obtain a fresh in-gate control on the locked `eval_027` line, then rerun the direct-launch candidate on the same pinned GPUs and shared child command. If that cannot be achieved reliably, deprioritize further launcher-path work rather than treating this drift-stopped round as evidence against direct launch.
