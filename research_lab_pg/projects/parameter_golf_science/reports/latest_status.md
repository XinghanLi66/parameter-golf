# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_046_eval045_ttt_epochs_pair_7gpu_subset`, which passed the reviewed clean-idle gate on GPUs `1..7` and then failed immediately at helper startup because the locked helper rejects `WORLD_SIZE=7`.
- The newest completed exact promoted-line control is still the admissible fresh control inside `eval_045`, which established that the promoted helper/checkpoint/artifact stack remains semantically stable and is materially faster than `eval_042` under the current regime.
- The helper/artifact guardrail stayed clean before the round:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only epoch-pair lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - held promoted `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152` fixed
  - changed only the reviewed operational subset to GPUs `1..7`, the runner request count to `7`, and the intended candidate `TTT_EPOCHS=4 -> 3`
- 7-GPU gate and launch result:
  - gate sample time `2026-03-27T13:56:56Z`
  - GPUs `1..7` all showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - GPU `0` stayed occupied by a foreign process at about `74486 MiB`, but it was outside the reviewed gate set
  - the runner then selected GPUs `1,2,3,4,5,6,7` successfully and launched the fresh control at `2026-03-27T13:57:15Z`
  - the child failed before evaluation with `ValueError: WORLD_SIZE=7 must divide 8 so grad_accum_steps stays integral`
- Control launch timing and outcome:
  - no `legal_ttt_exact val_loss`
  - no `legal_ttt_exact val_bpb`
  - no scorer telemetry
  - external wallclock `34.181s`
  - runner-managed wallclock `33914ms`
  - `runner_start_to_child_spawn_ms=424`
  - `child_runtime_ms=33489`
  - runner metadata exit code `1`
- Interpretation:
  - this round is `operationally blocked`
  - the reviewed 7-GPU surrogate control path is not executable on the locked helper
  - the promoted-line epoch-count decision remains pending
  - the blocker is now broader than GPU `0` contamination alone: a true 7-process launch is incompatible with the helper’s startup invariants

## Most Important Open Question
What newly reviewed helper-compatible operational path should be used to answer the exact promoted-line `TTT_EPOCHS=4 -> 3` question, given that the reviewed 7-GPU surrogate regime on `CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7` is not executable on the locked helper because it rejects `WORLD_SIZE=7`?

## Active Experiment ID
`eval_046_eval045_ttt_epochs_pair_7gpu_subset`

## Latest Result Summary
- Completed the reviewed exact promoted-line same-session 7-GPU surrogate retry as a controlled launch-path block report.
- Controlled intervention actually executed:
  - required file re-read
  - helper/checkpoint/artifact byte and SHA-256 verification
  - promoted command-family reconstruction from `eval_045`
  - one clean-idle gate sample on GPUs `1..7`
  - fresh 7-GPU control launch attempt through `tools/gpu_experiment_runner.py`
  - on-disk recording of commands, gate evidence, and runner logs in `runs/eval_046_eval045_ttt_epochs_pair_7gpu_subset/`
- Managed launch result:
  - environment `physicslm`
  - GPU allocation at launch: `7x NVIDIA L20Z`, specifically `1,2,3,4,5,6,7`
  - no control BPB because the helper failed before evaluation
  - startup failure: `ValueError: WORLD_SIZE=7 must divide 8 so grad_accum_steps stays integral`
  - external wallclock `34.181s`
  - runner-managed wallclock `33914ms`
  - `runner_start_to_child_spawn_ms=424`
  - `child_runtime_ms=33489`
  - candidate not attempted
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes stayed `125663`
  - total bytes on the locked evaluation-helper line remain `15680784`
  - byte status remains under cap by `319216`
- Decision:
  - this round is `operationally blocked`
  - it does not answer `hold 4` vs `runtime-only 3` vs `promote 3`
  - it does prove that the reviewed 7-GPU surrogate path cannot be executed unchanged on the locked helper

## Recommended Next Step
Do not retry the exact reviewed 7-GPU surrogate path unchanged. Require a new reviewed brief that either authorizes a helper patch for non-divisor eval-only world sizes or specifies a different helper-compatible topology before reopening the promoted-line `TTT_EPOCHS=4 -> 3` question.
