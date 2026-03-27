# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch`, which passed the required continuous clean-idle gate, completed an admissible fresh control, and then lost the candidate handoff to post-gate GPU `0` contamination.
- The newest completed exact promoted-line control is now the fresh control inside `eval_045`, which established that the promoted helper/checkpoint/artifact stack remains semantically stable and is materially faster than `eval_042` under the current regime.
- The helper/artifact guardrail stayed clean before and after the round:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only epoch-pair lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - held promoted `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152` fixed
  - changed only fresh operational identifiers, one continuous clean-idle watch, synchronized telemetry, and the intended candidate `TTT_EPOCHS=4 -> 3`
- Clean-idle and handoff result on GPUs `0,1,2,3,4,5,6,7`:
  - continuous watch interval `2026-03-27T12:58:42Z` through gate pass at `2026-03-27T13:05:27Z`
  - samples `0..25` showed only GPU `0` dirty with foreign `PID 3922791` using `74486 MiB`; GPUs `1..7` stayed idle
  - sample `26` passed with all eight GPUs at about `81007 MiB` free and no compute-app entries
  - during the late control phase, a new foreign `PID 4112518` appeared on GPU `0`
  - by the candidate launch attempt at `2026-03-27T13:29:49Z`, GPU `0` had only `6512 MiB` free and the runner saw only 7 eligible GPUs
- Fresh control result:
  - `legal_ttt_exact val_loss=0.33725577`
  - `legal_ttt_exact val_bpb=0.19974186`
  - script eval wallclock `1306008ms`
  - runner-managed wallclock `1350527ms`
  - external wallclock `1350805ms`
  - `runner_start_to_child_spawn_ms=372`
  - `child_runtime_ms=1350155`
  - any-match `0.98387585`
  - avg alpha `0.65460155`
  - matched-order histogram exactly in-family
  - `ngram_postlookup_vectorized_elapsed_ms=1484092`
- Interpretation:
  - this round is `post-gate contamination / invalid same-session pair`
  - the fresh `TTT_EPOCHS=4` control was valid and admissible
  - the `TTT_EPOCHS=3` candidate never launched because the pinned set was no longer clean
  - the promoted-line epoch-count decision remains pending, but the blocker is now specifically the immediate post-control handoff rather than the prelaunch gate itself

## Most Important Open Question
When pinned GPUs `0..7` can stay clean through both the continuous prelaunch gate and the immediate post-control handoff, does reducing only `TTT_EPOCHS` from `4` to `3` on the exact promoted `EVAL_LOGIT_TEMP=1.0`, `NGRAM_EVAL_BUCKETS=2097152` line preserve BPB within `+0.00005` of a fresh same-session control while saving at least `50s` external wallclock on the current runtime regime?

## Active Experiment ID
`eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch`

## Latest Result Summary
- Completed the reviewed exact promoted-line same-session epoch-pair retry as a controlled post-gate invalid-comparison report.
- Controlled intervention actually executed:
  - required file re-read
  - helper/checkpoint/artifact byte and SHA-256 verification
  - promoted command-family reconstruction from `eval_042` / `eval_044`
  - one continuous clean-idle gate watch on pinned GPUs `0..7`
  - synchronized runtime telemetry
  - fresh same-session control launch
  - immediate candidate launch attempt
  - on-disk recording of commands, gate evidence, telemetry, control logs, and candidate failure metadata in `runs/eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch/`
- Managed eval result:
  - environment `physicslm`
  - GPU allocation at control launch: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - fresh `legal_ttt_exact val_loss=0.33725577`
  - fresh `legal_ttt_exact val_bpb=0.19974186`
  - script eval wallclock `1306008ms`
  - runner-managed wallclock `1350527ms`
  - external wallclock `1350805ms`
  - `runner_start_to_child_spawn_ms=372`
  - `child_runtime_ms=1350155`
  - candidate launch failure before child spawn due only 7 eligible GPUs
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes stayed `125663`
  - total bytes on the locked evaluation-helper line remain `15680784`
  - byte status remains under cap by `319216`
- Decision:
  - this round is `post-gate contamination / invalid same-session pair`
  - it does not answer `hold 4` vs `runtime-only 3` vs `promote 3`
  - it updates the newest completed promoted-line control evidence to the admissible `eval_045` control

## Recommended Next Step
Retry the exact promoted-line `TTT_EPOCHS=4 -> 3` pair unchanged when pinned GPUs `0..7` can plausibly remain clean through both the continuous prelaunch gate and the immediate candidate handoff after control completion. Keep helper/checkpoint/artifact and all non-epoch variables fixed, and do not force a dirty or delayed candidate launch.
