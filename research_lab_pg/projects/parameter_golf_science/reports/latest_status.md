# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line is now the promoted `eval_031` lineage confirmed by `eval_032_eval031_temperature_confirmation_pair`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest scored refinement round is `eval_032_eval031_temperature_confirmation_pair`.
- The helper/artifact guardrail stayed clean across both fresh official runs:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only confirmation lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - changed only `EVAL_LOGIT_TEMP` between fresh official control `1.0` and fresh official candidate `0.95`
- Fresh official pair on GPUs `0,1,2,3,4,5,6,7`:
  - control `T=1.0`: `val_loss=0.49164677`, `val_bpb=0.29118091`, script `591399ms`, runner `633253ms`, external `633409ms`
  - candidate `T=0.95`: `val_loss=0.49102508`, `val_bpb=0.29081271`, script `584876ms`, runner `627182ms`, external `627421ms`
- Decision comparisons:
  - fresh `T=0.95` vs fresh `T=1.0`: `-0.00036820 BPB`
  - fresh `T=0.95` vs prior `eval_031`: `-0.00000214 BPB`
  - fresh `T=1.0` vs `eval_027`: `+0.00000252 BPB`
  - fresh `T=1.0` vs `eval_030`: `+0.00000130 BPB`
- Interpretation:
  - fresh-control admissibility passed cleanly
  - promotion threshold `>=0.0002 BPB` passed comfortably
  - conclusion label is `promote`
  - `EVAL_LOGIT_TEMP=0.95` is now the promoted default on the locked `eval_031` PR809 legality line
  - nearby scalar-temperature tuning on this line is now closed

## Most Important Open Question
What is the next genuinely different single-variable refinement question on top of the now-promoted `eval_031` `T=0.95` legality line, given that nearby scalar-temperature tuning is closed and the separate direct-launch runtime question remains unanswered?

## Active Experiment ID
`eval_032_eval031_temperature_confirmation_pair`

## Latest Result Summary
- Completed the reviewed fresh confirmation pair on the locked `eval_031` helper lineage with no code edits.
- Controlled intervention actually executed:
  - fresh official control at `EVAL_LOGIT_TEMP=1.0`
  - fresh official candidate at `EVAL_LOGIT_TEMP=0.95`
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - fresh control result: `legal_ttt_exact val_bpb=0.29118091`, `val_loss=0.49164677`
  - fresh candidate result: `legal_ttt_exact val_bpb=0.29081271`, `val_loss=0.49102508`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh control: `591399ms` script, `633253ms` runner, `633409ms` external
  - fresh candidate: `584876ms` script, `627182ms` runner, `627421ms` external
- Decision:
  - fresh-control admissibility passed
  - fresh candidate beat fresh control by `0.00036820 BPB`
  - label: `promote`
  - the locked `eval_031` line with `EVAL_LOGIT_TEMP=0.95` is now the active legality baseline
  - nearby scalar-temperature work is closed on this line

## Recommended Next Step
Keep the locked PR809 legality stack fixed with promoted `EVAL_LOGIT_TEMP=0.95` and move the next refinement round to a genuinely different single-variable question rather than another nearby scalar calibration. If managed-runtime work is revisited, require a fresh admissible control first and treat it as a separate question from the now-closed temperature result.
