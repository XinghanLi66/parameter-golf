# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_044_eval038_ttt_epochs_pair_clean_idle_retry`, which stopped before launch because the clean-idle gate on pinned GPUs `0..7` never passed.
- The newest completed exact promoted-line control remains `eval_042_eval038_clean_idle_telemetry_control`, which established that the promoted helper/checkpoint/artifact stack is semantically stable on the current runtime regime.
- The helper/artifact guardrail stayed clean before and after the blocked round:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only epoch-pair lane up to the stop:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - intended to hold promoted `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152` fixed while changing only candidate `TTT_EPOCHS=4 -> 3`
  - actually changed only fresh operational identifiers plus the bounded clean-idle watch
- Clean-idle gate result on GPUs `0,1,2,3,4,5,6,7`:
  - bounded watch interval `2026-03-27T12:43:36Z` through `2026-03-27T12:46:41Z`
  - all eight GPUs already carried foreign compute-app PIDs `3796173..3796180` at the first sample
  - the watch began with a light all-GPU footprint: GPU `0` at `2893 MiB` used and GPUs `1..7` at `1515 MiB` used
  - the same PIDs expanded during the watch into a heavy 8-GPU workload, ending around `38596..39096 MiB` used per GPU with `86..100%` utilization
  - compute-app snapshots stayed `[Not Found]` for all eight PIDs throughout
- Interpretation:
  - this round is `no-launch / clean-idle-gate-fail`
  - no fresh `TTT_EPOCHS=4` control launched
  - no `TTT_EPOCHS=3` candidate launched
  - no new BPB or wallclock fields were produced
  - the promoted-line epoch-count decision remains pending, but only because of pinned-GPU occupancy rather than a semantic blocker

## Most Important Open Question
When pinned GPUs `0..7` are genuinely clean-idle again, does reducing only `TTT_EPOCHS` from `4` to `3` on the exact promoted `EVAL_LOGIT_TEMP=1.0`, `NGRAM_EVAL_BUCKETS=2097152` line preserve BPB within `+0.00005` of a fresh same-session control while saving at least `50s` external wallclock on the current runtime regime?

## Active Experiment ID
`eval_044_eval038_ttt_epochs_pair_clean_idle_retry`

## Latest Result Summary
- Completed the reviewed exact promoted-line same-session epoch-pair retry as a controlled blocker report.
- Controlled intervention actually executed:
  - required file re-read
  - helper/checkpoint/artifact byte and SHA-256 verification
  - promoted command-family reconstruction from `eval_042`
  - bounded clean-idle gate watch on pinned GPUs `0..7`
  - on-disk recording of intended control/candidate commands and gate evidence in `runs/eval_044_eval038_ttt_epochs_pair_clean_idle_retry/`
- No managed eval run launched:
  - environment would have been `physicslm`
  - GPU allocation requirement remained `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - no fresh `legal_ttt_exact val_loss`
  - no fresh `legal_ttt_exact val_bpb`
  - no script eval wallclock
  - no runner-managed wallclock
  - no external wallclock
  - no `runner_start_to_child_spawn_ms`
  - no `child_runtime_ms`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes stayed `125663`
  - total bytes on the locked evaluation-helper line remain `15680784`
  - byte status remains under cap by `319216`
- Decision:
  - this round is `no-launch / clean-idle-gate-fail`
  - it does not answer `hold 4` vs `runtime-only 3` vs `promote 3`
  - it leaves `eval_042` as the newest completed promoted-line control evidence

## Recommended Next Step
Retry the exact promoted-line `TTT_EPOCHS=4 -> 3` pair unchanged when pinned GPUs `0..7` can be confirmed clean-idle. Keep helper/checkpoint/artifact and all non-epoch variables fixed, and do not force a dirty launch.
