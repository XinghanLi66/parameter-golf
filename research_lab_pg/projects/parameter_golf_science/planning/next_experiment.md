# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase single-variable n-gram bucket-geometry refinement on the promoted `eval_031 / eval_032 / eval_033` legality line at `EVAL_LOGIT_TEMP=0.95`.

- Executed the reviewed brief materially as written:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `context/reference_materials/URGENT_ngram_backoff_breakthrough.md`, the required planning/report files, and the active helper before launch
  - re-verified helper, checkpoint, and artifact identities before launch and again after both arms
  - confirmed `NGRAM_EVAL_BUCKETS` was already env-configurable on the active helper, so no code edits were needed
  - ran one fresh runner-managed control with `NGRAM_EVAL_BUCKETS=4194304`
  - checked admissibility versus `eval_033` before launching the candidate
  - ran one fresh runner-managed candidate with only `NGRAM_EVAL_BUCKETS=2097152`
  - kept the same `physicslm` environment, cwd, runner path, pinned GPUs, helper, checkpoint, artifact, tokenizer, dataset, stride, `EVAL_LOGIT_TEMP=0.95`, legal TTT settings, and PR809 vectorized n-gram settings

## Experiment ID
`eval_035_eval031_bucket_geometry_pair`

## Category
- evaluation

Operational subtype: `single-variable n-gram cache geometry refinement`

## Baseline / Comparison
Primary comparison:
- fresh admissible runner-managed control on the promoted line with `NGRAM_EVAL_BUCKETS=4194304`
- fresh runner-managed candidate on the same line with only `NGRAM_EVAL_BUCKETS=2097152`

Historical anchors:
- promoted candidate `eval_032=0.29081271`, script `584876ms`, runner `627182ms`, external `627421ms`
- fresh admissible control `eval_033=0.29081380`, script `585452ms`, runner `627968ms`, external `628139ms`
- older same-family bucket signal `eval_015=0.19974202`, script `663957ms`, managed `705s`

## Hypothesis
On the promoted `T=0.95` legality line, reducing `NGRAM_EVAL_BUCKETS` from `4194304` to `2097152` will improve post-export `val_bpb` by changing collision and regularization behavior in a way that still benefits the PR809-style mixer after the newer scorer-path optimizations.

## Why It Might Work
- `eval_015` was the strongest unresolved quality signal inside this n-gram legality family, and bucket geometry was the distinguishing variable
- that exact question had not yet been re-asked on the promoted helper with `EVAL_LOGIT_TEMP=0.95`, scorer-batch lookup, batched torch stats, and vectorized postlookup all fixed
- the live snapshot still supports eval-side gains, and no newer local result had displaced the PR809 n-gram family on this line

## Minimal Intervention
No code edits in this round.

Only varied:
- `NGRAM_EVAL_BUCKETS: 4194304 -> 2097152`

Also changed only the operational identifiers required to keep the runs separate:
- `RUN_ID`
- runner `--log-dir`
- runner `--run-name`

## Variables To Change
- `NGRAM_EVAL_BUCKETS: 4194304 -> 2097152`

## Variables To Hold Fixed
- exact helper path, bytes, and SHA-256 from `eval_031`
- exact checkpoint path, bytes, and SHA-256
- exact artifact path, bytes, and SHA-256
- `EVAL_LOGIT_TEMP=0.95`
- `TTT_LR=0.0025`
- `TTT_EPOCHS=4`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `NGRAM_EVAL_ENABLED=1`
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
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_035_eval031_bucket_geometry_pair/runner_control_8gpu \
  --run-name eval_035_runner_control_t0p95_b4194304 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_035_eval031_bucket_geometry_pair_runner_control \
    EVAL_ONLY=1 TTT_ENABLED=1 EVAL_STRIDE=64 \
    EVAL_LOGIT_TEMP=0.95 \
    TTT_LR=0.0025 TTT_EPOCHS=4 TTT_CHUNK_TOKENS=32768 \
    TTT_FREEZE_BLOCKS=0 TTT_MOMENTUM=0.9 TTT_BATCH_SEQS=32 TTT_GRAD_CLIP=1.0 \
    NGRAM_EVAL_ENABLED=1 NGRAM_EVAL_BUCKETS=4194304 \
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
python tools/gpu_experiment_runner.py \
  --gpus 8 \
  --gpu-indices 0,1,2,3,4,5,6,7 \
  --conda-env physicslm \
  --cwd /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science \
  --log-dir /newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_035_eval031_bucket_geometry_pair/runner_candidate_8gpu \
  --run-name eval_035_runner_candidate_t0p95_b2097152 \
  --timeout-seconds 7200 -- \
  env OMP_NUM_THREADS=1 PYTHONUNBUFFERED=1 \
    RUN_ID=eval_035_eval031_bucket_geometry_pair_candidate \
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

## Fresh Official Results
- Fresh runner-managed control:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.49102809`
  - `val_bpb=0.29081449`
  - script eval wallclock: `591126ms`
  - runner-managed wallclock: `634475ms`
  - runner start-to-spawn: `377ms`
  - child runtime: `634098ms`
  - external top-level wallclock: `634633ms`
  - any-match fraction: `0.98387524`
  - avg alpha on matched: `0.62766972`
- Fresh runner-managed candidate:
  - GPU indices: `0,1,2,3,4,5,6,7`
  - `val_loss=0.33904205`
  - `val_bpb=0.20079980`
  - script eval wallclock: `582272ms`
  - runner-managed wallclock: `625013ms`
  - runner start-to-spawn: `477ms`
  - child runtime: `624536ms`
  - external top-level wallclock: `625177ms`
  - any-match fraction: `0.98387585`
  - avg alpha on matched: `0.63990334`

## Required Comparisons
- Fresh control vs `eval_033` admissibility anchor:
  - `val_loss`: `0.49102692 -> 0.49102809` (`+0.00000117`)
  - `val_bpb`: `0.29081380 -> 0.29081449` (`+0.00000069`)
  - script eval wallclock: `585452ms -> 591126ms` (`+5674ms`)
  - runner-managed wallclock: `627968ms -> 634475ms` (`+6507ms`)
  - external top-level wallclock: `628139ms -> 634633ms` (`+6494ms`)
- Fresh candidate vs fresh control:
  - `val_loss`: `0.49102809 -> 0.33904205` (`-0.15198604`)
  - `val_bpb`: `0.29081449 -> 0.20079980` (`-0.09001469`)
  - script eval wallclock: `591126ms -> 582272ms` (`-8854ms`)
  - runner-managed wallclock: `634475ms -> 625013ms` (`-9462ms`)
  - external top-level wallclock: `634633ms -> 625177ms` (`-9456ms`)
- Fresh candidate vs promoted `eval_032` anchor:
  - `val_bpb`: `0.29081271 -> 0.20079980` (`-0.09001291`)
  - script eval wallclock: `584876ms -> 582272ms` (`-2604ms`)
  - runner-managed wallclock: `627182ms -> 625013ms` (`-2169ms`)
  - external top-level wallclock: `627421ms -> 625177ms` (`-2244ms`)
- Fresh candidate vs historical `eval_015` anchor:
  - `val_bpb`: `0.19974202 -> 0.20079980` (`+0.00105778`)
  - script eval wallclock: `663957ms -> 582272ms` (`-81685ms`)
  - runner-managed wallclock: `705s -> 625013ms` (`about -80s`)

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
  - tested variable `NGRAM_EVAL_BUCKETS=4194304 -> 2097152`

## Success Metric
Primary success criterion:
- candidate `val_bpb` improves on fresh control by at least `0.0001`

Secondary operational success criterion:
- candidate shows any BPB improvement over fresh control while keeping external wallclock within `+20s`

Outcome:
- primary quality success: `pass`
- secondary operational success: `pass`

## Expected Effect
If the old bucket-geometry win still transfers to the promoted `T=0.95` legality line, then `NGRAM_EVAL_BUCKETS=2097152` should beat the fresh `4194304` control on post-export `val_bpb` with comparable runtime.

## Actual Result
- The fresh control passed the reviewed admissibility gate cleanly before the candidate was launched.
- The candidate preserved full command and identity parity with the fresh control except for the intended `NGRAM_EVAL_BUCKETS` change and operational `RUN_ID`.
- Reducing `NGRAM_EVAL_BUCKETS` to `2097152` improved both quality and runtime:
  - `-0.09001469 BPB` vs the fresh control
  - `-8854ms` script
  - `-9462ms` runner-managed
  - `-9456ms` external
- Relative to the fresh control, the emitted telemetry also shifted to a higher matched alpha regime:
  - any-match fraction `0.98387524 -> 0.98387585`
  - avg alpha on matched `0.62766972 -> 0.63990334`

## Interpretation
- Classification: `promote`
- The old bucket-geometry signal transfers extremely strongly to the promoted `T=0.95` legality line.
- The smaller-bucket candidate is still slightly worse than the old `eval_015` historical anchor by `+0.00105778 BPB`, but it is now close enough that bucket geometry should be considered re-opened and promoted on the current helper lineage rather than treated as an old-helper curiosity.
- Inference from telemetry: the smaller bucket setting increased effective trust in matched n-gram signal on this line, which is consistent with the large BPB gain, but the causal mechanism is still only inferred from the observed alpha and order-histogram shift.

## Next Step
Promote `NGRAM_EVAL_BUCKETS=2097152` as the new default on the promoted `eval_031` legality line at `EVAL_LOGIT_TEMP=0.95`, then move the next refinement round to a different single-variable question on top of this stronger baseline.
