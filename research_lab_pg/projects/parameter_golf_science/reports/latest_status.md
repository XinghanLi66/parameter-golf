# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_035_eval031_bucket_geometry_pair` at `0.20079980`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_037_eval035_temperature_pair`, and it stopped cleanly as drift before the candidate arm.
- The helper/artifact guardrail stayed clean before and after the fresh control run:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only temperature lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - reused promoted `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and `NGRAM_EVAL_BUCKETS=2097152`
  - ran only the required fresh admissibility control at `EVAL_LOGIT_TEMP=0.95`
  - did not launch the `EVAL_LOGIT_TEMP=1.0` candidate after the control failed the reviewed external-wallclock gate
- Fresh control on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.33904036`
  - `val_bpb=0.20079880`
  - script `603417ms`
  - runner `648159ms`
  - external `648378ms`
  - any-match `0.98387585`
  - avg alpha on matched `0.63990743`
- Decision comparisons:
  - fresh control vs promoted `eval_035`: `-0.00000100 BPB`, `+21145ms` script, `+23146ms` runner, `+23201ms` external
  - fresh control vs fresh `eval_036` control: `+0.00000027 BPB`, `+21405ms` script, `+22112ms` runner, `+22331ms` external
  - fresh control vs historical `eval_015`: `+0.00105678 BPB`
- Interpretation:
  - quality admissibility passed cleanly
  - external runtime admissibility failed by `8201ms` beyond the reviewed `+15000ms` tolerance
  - conclusion label is `drift-stop`
  - the promoted-line `EVAL_LOGIT_TEMP=0.95 -> 1.0` question remains unanswered because the candidate was not launched

## Most Important Open Question
Can the promoted `eval_035` legality line be rerun with a fresh control that stays within the reviewed external admissibility gate, so the still-open single-variable scorer-temperature test `EVAL_LOGIT_TEMP=0.95 -> 1.0` can be answered cleanly on the promoted `NGRAM_EVAL_BUCKETS=2097152` operating point?

## Active Experiment ID
`eval_037_eval035_temperature_pair`

## Latest Result Summary
- Completed the reviewed single-variable eval-temperature check on the promoted `eval_035` legality line with no code edits, but only through the fresh-control gate.
- Controlled intervention actually executed:
  - one fresh runner-managed control at `EVAL_LOGIT_TEMP=0.95`
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings as the promoted line
  - no candidate arm, because the control failed the reviewed external runtime gate
- Managed run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - control result: `legal_ttt_exact val_bpb=0.20079880`, `val_loss=0.33904036`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh control: `603417ms` script, `648159ms` runner, `648378ms` external
- Decision:
  - control quality drift versus promoted `eval_035` was trivially acceptable
  - control external runtime drift versus promoted `eval_035` was not acceptable under the reviewed gate
  - the `EVAL_LOGIT_TEMP=1.0` candidate was not launched
  - label: `drift-stop`

## Recommended Next Step
Re-establish a fresh in-gate control on the exact promoted `eval_035` line, then rerun the same temperature-only pair. Keep the promoted legality stack fixed otherwise, and do not treat this round as evidence for or against replacing `EVAL_LOGIT_TEMP=0.95`.
