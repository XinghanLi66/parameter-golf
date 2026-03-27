# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_042_eval038_clean_idle_telemetry_control`, and it completed with a valid clean-idle launch on pinned GPUs `0..7`.
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
  - changed only clean-idle acquisition, synchronized telemetry capture, and fresh operational identifiers
- Clean-idle gate result on GPUs `0,1,2,3,4,5,6,7`:
  - the declared clean-idle acquisition protocol was honored and passed on the first required sample at `2026-03-27T11:40:19Z`
  - all eight GPUs were idle with about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - `nvidia-smi --query-compute-apps` returned no foreign compute processes at launch time
- Interpretation:
  - the exact promoted-line control finished at `legal_ttt_exact val_loss=0.33725929`, `val_bpb=0.19974395`
  - wallclocks were script `1507653ms`, runner `1555810ms`, external `1556076ms`
  - `runner_start_to_child_spawn_ms=479`, so the slowdown is not primarily launch-side
  - the existing `persistent-runtime-shift` classification is now strengthened and localized as `clean-launch persistent-runtime-shift / child-runtime-inflation`
  - n-gram semantics stayed in-family, while vectorized postlookup time inflated sharply to `1540712ms`
  - `TTT_EPOCHS=3` is now admissible again as a same-session current-regime comparison on the promoted `EVAL_LOGIT_TEMP=1.0` line

## Most Important Open Question
Now that the exact promoted `eval_038` control has launched cleanly and localized the slowdown inside child execution, does reducing only `TTT_EPOCHS` from `4` to `3` recover meaningful runtime on the current regime without losing more than the reviewed BPB tolerance?

## Active Experiment ID
`eval_042_eval038_clean_idle_telemetry_control`

## Latest Result Summary
- Completed the reviewed clean-idle runtime-diagnosis control on the promoted `eval_038` legality line with a valid clean-idle launch and full telemetry.
- Controlled intervention actually executed:
  - required file re-read
  - helper/checkpoint/artifact byte and SHA-256 verification
  - promoted command-family reconstruction from on-disk metadata
  - full clean-idle gate on pinned GPUs `0..7`
  - synchronized telemetry during the run
- Managed eval run launched and finished:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - final `legal_ttt_exact val_loss=0.33725929`
  - final `legal_ttt_exact val_bpb=0.19974395`
  - script eval wallclock `1507653ms`
  - runner-managed wallclock `1555810ms`
  - external wallclock `1556076ms`
  - `runner_start_to_child_spawn_ms=479`
  - `child_runtime_ms=1555330`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line remain `15680784`
  - byte status: under cap by `319216`
- Decision:
  - this round is `clean-launch persistent-runtime-shift / child-runtime-inflation`
  - it closes the unresolved protocol gap from `eval_041`
  - it makes the dedicated `TTT_EPOCHS=4 -> 3` pair admissible again on the current runtime regime

## Recommended Next Step
Run the exact promoted-line `TTT_EPOCHS=4 -> 3` pair as a controlled same-session refinement comparison on top of the now-diagnosed current regime, keeping helper/checkpoint/artifact and all non-epoch variables fixed. Keep runtime telemetry enabled if late foreign GPU occupancy remains possible.
