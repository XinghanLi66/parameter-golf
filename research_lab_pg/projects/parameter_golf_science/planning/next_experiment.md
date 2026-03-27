# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session promoted-line `TTT_EPOCHS=4 -> 3` retry on the fixed `7-GPU` subset `1..7`, but the round terminated before any admissible control metric because the locked helper rejects `WORLD_SIZE=7`.

- Executed the reviewed brief through the required file re-read, promoted-command recovery, helper/checkpoint/artifact identity verification, 7-GPU clean-idle acquisition on `1..7`, and the fresh 7-GPU control launch attempt.
- No code edits were made in this round.
- The clean-idle gate on GPUs `1..7` passed immediately.
- The fresh control did not reach evaluation because `torchrun --nproc_per_node=7` failed at helper startup with `ValueError: WORLD_SIZE=7 must divide 8 so grad_accum_steps stays integral`.
- The immediate `TTT_EPOCHS=3` candidate was therefore not attempted.
- The round is a controlled `operationally blocked` result on the reviewed 7-GPU launch path, not an epoch-count comparison.

## Experiment ID
`eval_046_eval045_ttt_epochs_pair_7gpu_subset`

## Category
- evaluation

Operational subtype: `same-session promoted-line epoch-pair 7-GPU launch-path check`

## Baseline / Comparison
Intended primary comparison:
- fresh same-session 7-GPU surrogate control on the exact promoted line with `TTT_EPOCHS=4`
- immediate same-session 7-GPU surrogate candidate on the same subset with only `TTT_EPOCHS=3`

Interpretation anchors:
- promoted 8-GPU line `eval_038=0.19974237`
- fresh admissible 8-GPU control `eval_045 control=0.19974186`

Actual comparison obtained this round:
- clean-idle admissibility of the fixed `1..7` subset
- reviewed 7-GPU control launch request versus the locked helper’s startup invariants

## Hypothesis
If the repeated blocker was specifically GPU `0` contamination rather than the epoch-count hypothesis itself, then moving the same-session pair to the persistently cleaner subset `1..7` would produce a valid surrogate control, after which a fresh same-session `TTT_EPOCHS=3` candidate could answer the epoch-count question.

Operational falsifier for this round:
- if the fixed-helper launch path itself cannot execute at `WORLD_SIZE=7`, the 7-GPU surrogate regime cannot be used to answer the epoch-count question without an explicitly reviewed helper or topology change

## Why It Might Work
- GPUs `1..7` had repeatedly appeared clean while GPU `0` was the recurring blocker.
- The reviewed brief kept every semantic evaluation variable fixed except the intended candidate epoch count.
- This remained the narrowest operationally motivated retry of the strongest current leaderboard-aligned evaluation motif.

## Minimal Intervention
No helper, checkpoint, artifact, runner, eval-hyperparameter, or export changes were made.

Intended semantic change:
- candidate `TTT_EPOCHS: 4 -> 3`

Actual executed changes:
- fresh operational identifiers for a new run namespace
- launch subset changed from pinned `0..7` to pinned `1..7`
- runner request count changed from `8` to `7`
- attempted control launch used `torchrun --nproc_per_node=7`

## Variables To Change
Intended semantic change:
- candidate `TTT_EPOCHS: 4 -> 3`

Operational-only:
- fresh `RUN_ID`
- fresh runner `--log-dir`
- fresh runner `--run-name`
- launch subset `CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7`
- runner request count `7`
- `torchrun --nproc_per_node=7`

Actual executed this round:
- 7-GPU clean-idle gate on `1..7`
- fresh 7-GPU control launch attempt with `TTT_EPOCHS=4`

## Variables To Hold Fixed
- helper path `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`
- helper bytes/hash `125663 / 2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
- checkpoint path `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
- checkpoint bytes/hash `106178569 / b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- artifact path `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
- artifact bytes/hash `15555121 / eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
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
- tokenizer, dataset, cwd, `physicslm`
- launcher `tools/gpu_experiment_runner.py`

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
- helper unchanged before launch
- checkpoint unchanged before launch
- artifact unchanged before launch

## Commands Actually Run
The exact intended 7-GPU control and candidate commands were recorded in:
- `runs/eval_046_eval045_ttt_epochs_pair_7gpu_subset/command.txt`

The 7-GPU clean-idle gate evidence was recorded in:
- `runs/eval_046_eval045_ttt_epochs_pair_7gpu_subset/clean_idle_gate.log`

The fresh 7-GPU control command was actually launched via:
- `tools/gpu_experiment_runner.py` in `physicslm`
- pinned subset `1,2,3,4,5,6,7`
- runner log dir `runs/eval_046_eval045_ttt_epochs_pair_7gpu_subset/runner_control_7gpu/`

The immediate candidate command was intentionally not launched after the control failed at startup.

## Clean-Idle Gate Result
- gate status: `pass`
- gate sample time: `2026-03-27T13:56:56Z`
- GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
- GPU `0` remained occupied by a foreign process at about `74486 MiB`, but that was outside the reviewed `1..7` gate set
- because the gate passed:
  - the fresh 7-GPU control launch was attempted immediately

## Control Launch Result
- control launch status: `blocked at helper startup`
- exact runner launch start: `2026-03-27T13:57:15Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- no evaluation metric was produced because the child failed before model evaluation
- root startup failure on every rank:
  - `ValueError: WORLD_SIZE=7 must divide 8 so grad_accum_steps stays integral`
- runner timing:
  - external wallclock `34.181s`
  - runner-managed wallclock `33914ms`
  - `runner_start_to_child_spawn_ms=424`
  - `child_runtime_ms=33489`
- child process status:
  - torchrun exited with `ChildFailedError`
  - first observed root-cause failure was rank `5`
  - runner metadata exit code `1`

## Candidate Launch Result
- candidate launch status: `not attempted`
- reason:
  - the control never reached an admissible surrogate-regime result
  - the reviewed brief explicitly allowed candidate launch only if the control was admissible
- therefore no candidate `val_loss`, `val_bpb`, script wallclock, runner wallclock, or external wallclock exist for this round

## Success Metric
Primary success required:
- 7-GPU control launches and finishes
- 7-GPU control is admissible as a surrogate regime
- immediate 7-GPU `TTT_EPOCHS=3` candidate also launches and finishes

Actual status:
- clean-idle gate on `1..7`: `pass`
- control launch on `1..7`: `failed before evaluation`
- surrogate-regime admissibility: `not measurable`
- candidate launch: `not attempted`
- epoch-count decision: `unanswered`

## Expected Effect
If the 7-GPU subset were both clean and executable on the locked helper, the fresh control would establish whether the `1..7` regime is an acceptable surrogate, after which the immediate `TTT_EPOCHS=3` candidate could answer the epoch-count question without GPU `0`.

## Actual Result
- The fixed `1..7` subset was clean and the runner selected it successfully.
- The control did not reach evaluation because the locked helper enforces `8 % WORLD_SIZE == 0` before any eval-only logic runs.
- A true 7-process launch therefore fails immediately under the reviewed no-code-change constraints.
- Because the control never produced BPB or telemetry, the candidate was not attempted.

## Interpretation
- Decision label: `operationally blocked`
- This round answered the reviewed operational question negatively: excluding GPU `0` is not sufficient on the locked helper because the helper itself is not compatible with `WORLD_SIZE=7`.
- The scientific `TTT_EPOCHS=4 -> 3` question remains unanswered.
- Under the reviewed minimal-intervention rules, silently switching to a different process topology or patching the helper would have mixed in an unreviewed extra change, so the correct action was to stop here.

## Next Step
Do not spend another immediate round on the exact reviewed 7-GPU surrogate path unless a new reviewed brief explicitly authorizes one of these helper-compatible changes:
- patching the locked helper to support non-divisor world sizes in eval-only mode, or
- using a different reviewed operational topology that keeps the epoch-count comparison interpretable.

Until then, treat the promoted-line `TTT_EPOCHS=4 -> 3` question as blocked by launch-shape incompatibility rather than by GPU `0` cleanliness alone.
