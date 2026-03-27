# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted 8-GPU anchor remains `eval_038_eval035_temperature_pair` at `0.19974237`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_048_eval047_ttt_epochs_pair_patched_7gpu`, which ran the reviewed same-session patched-helper `TTT_EPOCHS=4 -> 3` pair on GPUs `1..7`.
- The helper/checkpoint/artifact guardrail stayed exact for both arms:
  - patched helper `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/train_gpt.py`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - source helper from `eval_047`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- Fresh gate and launch result:
  - gate sample time `2026-03-27T14:36:53Z`
  - GPUs `1..7` all showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - GPU `0` stayed occupied by a foreign process at about `74486 MiB`, but it was outside the reviewed gate set
  - the fresh control then launched at `2026-03-27T14:37:26Z`, finished at `2026-03-27T14:48:36Z`, and passed admissibility versus `eval_047`
  - the immediate candidate launched at `2026-03-27T14:49:01Z` and finished at `2026-03-27T15:06:22Z`
- Fresh control metrics:
  - `legal_ttt_exact val_loss=0.33725832`
  - `legal_ttt_exact val_bpb=0.19974338`
  - script wallclock `623802ms`
  - runner-managed wallclock `669909ms`
  - external wallclock `670.141s`
  - `runner_start_to_child_spawn_ms=411`
  - `child_runtime_ms=669498`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461534`
  - matched-order histogram identical to `eval_047`, `eval_045`, and `eval_038`
  - `ngram_postlookup_vectorized_elapsed_ms=1105413`
- Control admissibility versus `eval_047=0.19974198`:
  - `val_bpb` delta `+0.00000140`
  - `val_loss` delta `+0.00000236`
  - script delta `+7477ms`
  - runner delta `+7101ms`
  - external delta `+7.049s`
  - avg alpha delta `-0.00000210`
  - histogram `unchanged`
  - postlookup delta `-4753ms`
  - decision `admissible`
- Immediate candidate metrics:
  - `legal_ttt_exact val_loss=0.33730055`
  - `legal_ttt_exact val_bpb=0.19976839`
  - script wallclock `998177ms`
  - runner-managed wallclock `1041138ms`
  - external wallclock `1041.407s`
  - `runner_start_to_child_spawn_ms=306`
  - `child_runtime_ms=1040831`
  - any-match fraction `0.98387585`
  - avg alpha `0.65467460`
  - matched-order histogram unchanged
  - `ngram_postlookup_vectorized_elapsed_ms=1353120`
- Candidate minus fresh control:
  - `val_bpb` `+0.00002501`
  - `val_loss` `+0.00004223`
  - script wallclock `+374375ms`
  - runner-managed wallclock `+371229ms`
  - external wallclock `+371.266s`
  - any-match `+0.00000000`
  - avg alpha `+0.00005926`
  - matched-order histogram `unchanged`
  - `ngram_postlookup_vectorized_elapsed_ms` `+247707ms`
- Interpretation:
  - this round is `hold TTT_EPOCHS=4`
  - the candidate stayed inside the reviewed BPB tolerance band, so quality did not collapse
  - but the candidate was dramatically slower than the fresh control, so the runtime-optimization hypothesis failed cleanly
  - because both arms completed and only `TTT_EPOCHS` changed, this is a valid negative answer rather than a blocked round

## Most Important Open Question
Which different single-variable refinement question should replace epoch count on the patched promoted-line surrogate path, now that `TTT_EPOCHS=3` has been answered negatively and `TTT_EPOCHS=4` remains the default?

## Active Experiment ID
`eval_048_eval047_ttt_epochs_pair_patched_7gpu`

## Latest Result Summary
- Completed the reviewed same-session patched-helper epoch-count pair on the validated `1..7` surrogate path.
- Controlled intervention actually executed:
  - required file re-read
  - exact patched-helper reuse from `eval_047`
  - helper/checkpoint/artifact byte and SHA-256 verification
  - one fresh clean-idle gate sample on GPUs `1..7`
  - one fresh patched `TTT_EPOCHS=4` control launch through `tools/gpu_experiment_runner.py`
  - one admissibility check against `eval_047`
  - one immediate patched `TTT_EPOCHS=3` candidate launch through `tools/gpu_experiment_runner.py`
  - on-disk recording of command, gate evidence, and runner logs in `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/`
- Managed launch results:
  - environment `physicslm`
  - GPU allocation at launch: `7x NVIDIA L20Z`, specifically `1,2,3,4,5,6,7`
  - control `legal_ttt_exact val_bpb=0.19974338`
  - candidate `legal_ttt_exact val_bpb=0.19976839`
  - both artifacts stayed unchanged at `15555121` bytes
  - patched helper code bytes stayed `126026`
  - total bytes on this evaluation-helper line stayed `15681147`
  - byte status remains under cap by `318853`
- Decision:
  - `hold TTT_EPOCHS=4`
  - the fresh control was admissible
  - the immediate `TTT_EPOCHS=3` candidate was slightly worse on BPB and much slower on all wallclocks
  - `TTT_EPOCHS=3` should not be promoted as a runtime-optimized setting on this patched path

## Recommended Next Step
Keep `TTT_EPOCHS=4` fixed on the patched promoted-line surrogate path and move the next reviewed refinement round to a different single-variable evaluation question; only reopen `TTT_EPOCHS=3` if a separate operational-diagnosis brief is explicitly desired.
