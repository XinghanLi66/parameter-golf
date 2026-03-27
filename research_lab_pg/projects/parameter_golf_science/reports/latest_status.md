# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active promoted legality line is now `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_039_eval038_ttt_epochs_pair`, and it stopped after the fresh control because runtime drift made the reviewed same-session epoch-count comparison inadmissible.
- The helper/artifact guardrail stayed clean before and after the round:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only epoch-count lane up to the stop:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - reused promoted `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and `NGRAM_EVAL_BUCKETS=2097152`
  - planned candidate-only change was `TTT_EPOCHS: 4 -> 3`
  - candidate was not launched after the fresh control failed runtime admissibility
- Fresh control on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.33725535`
  - `val_bpb=0.19974161`
  - script `1190477ms`
  - runner `1237270ms`
  - external `1237494ms`
  - any-match `0.98387585`
  - avg alpha on matched `0.65459666`
- Decision comparisons:
  - fresh control vs promoted `eval_038`: `-0.00000076 BPB`, `-0.00000128 val_loss`, `+601664ms` script, `+602585ms` runner, `+602568ms` external
  - fresh control vs old-line `eval_034` runtime-only context: `+679050ms` external
- Interpretation:
  - fresh control stayed semantically in-family with the promoted line on BPB and telemetry
  - runtime drift was catastrophic, so the same-session epoch-count comparison was not admissible
  - conclusion label is `drift-stop`
  - `TTT_EPOCHS=3` remains unanswered on the promoted `EVAL_LOGIT_TEMP=1.0` line

## Most Important Open Question
Can a fresh in-gate control be re-established on the exact promoted `eval_038` legality line so the reopened `TTT_EPOCHS=3` question can be answered cleanly on the stronger calibrated baseline? The scientific next step is still the epoch-count-only `4 -> 3` pair, but only after runtime admissibility is restored.

## Active Experiment ID
`eval_039_eval038_ttt_epochs_pair`

## Latest Result Summary
- Completed the reviewed single-variable epoch-count check only through the fresh control on the promoted `eval_038` legality line; the candidate was not launched because the control failed the runtime admissibility gate.
- Controlled intervention actually executed:
  - one fresh runner-managed control at the exact promoted settings with `TTT_EPOCHS=4`
  - no candidate launch after admissibility failure
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings as the promoted line
- Managed run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - control result: `legal_ttt_exact val_bpb=0.19974161`, `val_loss=0.33725535`
  - candidate result: not run
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh control: `1190477ms` script, `1237270ms` runner, `1237494ms` external
- Decision:
  - fresh control remained in-family on BPB and telemetry but failed runtime admissibility by about `+602.6s` external versus promoted `eval_038`
  - the reviewed same-session `TTT_EPOCHS=3` candidate was therefore not launched
  - label: `drift-stop`

## Recommended Next Step
Keep `EVAL_LOGIT_TEMP=1.0` fixed as the promoted default on this helper lineage and re-establish one fresh admissible control on the exact promoted line before retrying the same `TTT_EPOCHS=4 -> 3` pair. Do not interpret this round as a quality-default hold, a runtime-only win, or a promotion for `TTT_EPOCHS=3`.
