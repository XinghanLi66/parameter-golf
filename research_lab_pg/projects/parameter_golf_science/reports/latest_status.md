# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active promoted legality line is now `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_038_eval035_temperature_pair`, and it cleanly answered the promoted-line scorer-temperature question with a same-session control/candidate pair.
- The helper/artifact guardrail stayed clean before and after both runs:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only temperature lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - reused promoted `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and `NGRAM_EVAL_BUCKETS=2097152`
  - changed only `EVAL_LOGIT_TEMP` between fresh control `0.95` and immediate candidate `1.0`
- Fresh control on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.33904065`
  - `val_bpb=0.20079897`
  - script `585778ms`
  - runner `631265ms`
  - external `631449ms`
  - any-match `0.98387585`
  - avg alpha on matched `0.63990741`
- Fresh candidate on the same GPUs:
  - `val_loss=0.33725663`
  - `val_bpb=0.19974237`
  - script `588813ms`
  - runner `634685ms`
  - external `634926ms`
  - any-match `0.98387585`
  - avg alpha on matched `0.65459911`
- Decision comparisons:
  - fresh control vs promoted `eval_035`: `-0.00000083 BPB`, `+3506ms` script, `+6252ms` runner, `+6272ms` external
  - fresh control vs fresh `eval_036` control: `+0.00000044 BPB`, `+3766ms` script, `+5218ms` runner, `+5402ms` external
  - fresh candidate vs fresh control: `-0.00105660 BPB`, `+3035ms` script, `+3420ms` runner, `+3477ms` external
  - fresh candidate vs historical `eval_015`: `+0.00000035 BPB`
- Interpretation:
  - fresh control admissibility passed cleanly on BPB, telemetry, and runtime context
  - the `EVAL_LOGIT_TEMP=1.0` candidate produced a large same-session quality win while staying comfortably within the reviewed runtime band
  - conclusion label is `promote`
  - `EVAL_LOGIT_TEMP=1.0` should replace `0.95` on the promoted `2097152`-bucket legality line

## Most Important Open Question
On top of the newly promoted `EVAL_LOGIT_TEMP=1.0` legality line, which single-variable runtime/quality tradeoff is now most valuable to test next without reopening closed calibration work? The cleanest reopened question is whether `TTT_EPOCHS=3` now offers a better runtime-quality point on the stronger calibrated baseline.

## Active Experiment ID
`eval_038_eval035_temperature_pair`

## Latest Result Summary
- Completed the reviewed single-variable eval-temperature check on the promoted `eval_035` legality line with no code edits and with the full same-session pair.
- Controlled intervention actually executed:
  - one fresh runner-managed control at `EVAL_LOGIT_TEMP=0.95`
  - one immediate fresh runner-managed candidate at `EVAL_LOGIT_TEMP=1.0`
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings as the promoted line
- Managed run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - control result: `legal_ttt_exact val_bpb=0.20079897`, `val_loss=0.33904065`
  - candidate result: `legal_ttt_exact val_bpb=0.19974237`, `val_loss=0.33725663`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh control: `585778ms` script, `631265ms` runner, `631449ms` external
  - fresh candidate: `588813ms` script, `634685ms` runner, `634926ms` external
- Decision:
  - fresh control remained in-family and comparison-clean
  - the `EVAL_LOGIT_TEMP=1.0` candidate beat the fresh control by `0.00105660 BPB`
  - candidate runtime stayed only `+3477ms` external versus the fresh control
  - label: `promote`

## Recommended Next Step
Keep `EVAL_LOGIT_TEMP=1.0` fixed as the promoted default on this helper lineage and move to a different single-variable refinement round on top of the stronger calibrated baseline. The highest-signal next step is to test `TTT_EPOCHS=3` against the newly promoted `TTT_EPOCHS=4` / `EVAL_LOGIT_TEMP=1.0` line, because that runtime-saving question may have changed on the new operating point.
