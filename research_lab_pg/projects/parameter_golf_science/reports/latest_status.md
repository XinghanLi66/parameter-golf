# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active promoted legality line remains the `eval_031` lineage confirmed by `eval_032_eval031_temperature_confirmation_pair`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest scored refinement round is `eval_034_eval031_ttt_epochs3_candidate`.
- The helper/artifact guardrail stayed clean before and after the run:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only epoch-count lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only `TTT_EPOCHS` from `4` to `3`
- Fresh `TTT_EPOCHS=3` candidate on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.49109611`
  - `val_bpb=0.29085478`
  - script `514515ms`
  - runner `558261ms`
  - external `558444ms`
- Decision comparisons:
  - candidate vs fresh `eval_033` control: `+0.00004098 BPB`, `-70937ms` script, `-69707ms` runner, `-69695ms` external
  - candidate vs promoted `eval_032`: `+0.00004207 BPB`, `-70361ms` script, `-68921ms` runner, `-68977ms` external
- Interpretation:
  - primary quality success failed because BPB got worse
  - secondary operational success passed because the regression stayed within `±0.0001` while runtime improved by about `70s`
  - conclusion label is `runtime-only operational win`
  - `TTT_EPOCHS=4` remains the promoted quality default on the locked `eval_031` PR809 legality line
  - `TTT_EPOCHS=3` is now the runtime-optimized operational variant for the same line

## Most Important Open Question
What is the next genuinely different single-variable refinement question on top of the promoted `eval_031` `T=0.95`, legal TTT, PR809 vectorized n-gram line, now that scalar temperature, launcher bypass, and TTT epoch count are all effectively closed on this lineage?

## Active Experiment ID
`eval_034_eval031_ttt_epochs3_candidate`

## Latest Result Summary
- Completed the reviewed single-variable `TTT_EPOCHS` ablation on the locked promoted `eval_031` helper lineage with no code edits.
- Controlled intervention actually executed:
  - fresh runner-managed candidate at `TTT_EPOCHS=3`
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings as fresh `eval_033`
  - only intended semantic difference versus fresh `eval_033` was `TTT_EPOCHS=4 -> 3`
- Managed run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - result: `legal_ttt_exact val_bpb=0.29085478`, `val_loss=0.49109611`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh candidate: `514515ms` script, `558261ms` runner, `558444ms` external
  - fresh `eval_033` control reference: `585452ms` script, `627968ms` runner, `628139ms` external
- Decision:
  - quality default remains `TTT_EPOCHS=4`
  - runtime-only operational variant is now `TTT_EPOCHS=3`
  - label: `runtime-only operational win`

## Recommended Next Step
Keep the locked PR809 legality stack fixed with promoted `EVAL_LOGIT_TEMP=0.95` and quality-default `TTT_EPOCHS=4`. If runtime matters more than the last `~4.1e-5` BPB on this line, use `TTT_EPOCHS=3`; otherwise move the next refinement round to a genuinely different single-variable question.
