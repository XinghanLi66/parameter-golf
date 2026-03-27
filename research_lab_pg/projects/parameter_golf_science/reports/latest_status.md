# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_041_eval038_clean_idle_telemetry_control`, and it did not launch because the required clean-idle gate on pinned GPUs `0..7` never passed.
- The helper/artifact guardrail stayed clean before and after the round:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only runtime-diagnosis lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - held promoted `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and `NGRAM_EVAL_BUCKETS=2097152` fixed
  - actual executed commands were limited to prelaunch `nvidia-smi` / process-state probes because the clean-idle gate failed
- Clean-idle gate result on GPUs `0,1,2,3,4,5,6,7`:
  - repeated UTC samples from `2026-03-27T11:23:11Z` through `2026-03-27T11:25:26Z`
  - GPU `0` stayed occupied at about `6512 MiB` free, `74495 MiB` used, and `100%` utilization
  - compute-app snapshots showed `GPU-d45bfedb-df91-05be-293c-7375698e87dd`, `PID 3106138`, `process_name=[Not Found]`, `used_memory=74486 MiB`
  - GPUs `1..7` stayed idle with about `81007 MiB` free and `0%` utilization
- Interpretation:
  - no valid diagnostic control was launched
  - no new `val_loss`, `val_bpb`, script wallclock, runner wallclock, external wallclock, `runner_start_to_child_spawn_ms`, or `child_runtime_ms` fields were produced
  - the existing `persistent-runtime-shift` classification from `eval_040` remains the last completed runtime-diagnosis evidence, but this round did not localize the slowdown further
  - `TTT_EPOCHS=3` remains unanswered on the promoted `EVAL_LOGIT_TEMP=1.0` line because the required clean-idle exact control is still missing

## Most Important Open Question
When can the exact promoted `eval_038` control be launched on a genuinely clean-idle pinned `0..7` set, and once that happens does aligned telemetry localize the existing slowdown to external contention, launch-side overhead, or true in-process runtime drift?

## Active Experiment ID
`eval_041_eval038_clean_idle_telemetry_control`

## Latest Result Summary
- Completed the reviewed clean-idle runtime-diagnosis attempt on the promoted `eval_038` legality line, but the attempt stopped before launch because the gate failed.
- Controlled intervention actually executed:
  - required file re-read
  - helper/checkpoint/artifact byte and SHA-256 verification
  - promoted command-family reconstruction from on-disk metadata
  - repeated GPU/process gate probes on pinned GPUs `0..7`
- No managed eval run was launched:
  - environment intended: `physicslm`
  - GPU allocation intended: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - actual gate blocker: foreign compute occupancy on GPU `0`
  - new quality/runtime fields: none
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line remain `15680784`
  - byte status: under cap by `319216`
- Decision:
  - this round is `no-launch / clean-idle-gate-fail`
  - it does not supersede `eval_040` as the main runtime classification evidence
  - the exact clean-idle control remains pending

## Recommended Next Step
Retry the exact same `eval_041` clean-idle telemetry control once exclusive access to GPUs `0,1,2,3,4,5,6,7` can be guaranteed. Do not return to the `TTT_EPOCHS=4 -> 3` pair until that diagnostic control succeeds.
