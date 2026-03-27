# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line is now the promoted `eval_031` lineage confirmed by `eval_032_eval031_temperature_confirmation_pair`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest scored refinement round is `eval_033_eval031_direct_launch_pair`.
- The helper/artifact guardrail stayed clean across both fresh official runs:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only launcher-path lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only launch path between fresh runner control and fresh direct-launch candidate
- Fresh launcher pair on GPUs `0,1,2,3,4,5,6,7`:
  - runner control: `val_loss=0.49102692`, `val_bpb=0.29081380`, script `585452ms`, runner `627968ms`, external `628139ms`
  - direct-launch candidate: `val_loss=0.49102993`, `val_bpb=0.29081558`, script `583370ms`, external `625537ms`
- Decision comparisons:
  - fresh runner control vs `eval_032`: `+0.00000109 BPB`, `+718ms` external
  - direct-launch candidate vs fresh runner control: `+0.00000178 BPB`, `-2602ms` external
  - direct-launch candidate vs `eval_032`: `+0.00000287 BPB`, `-1884ms` external
- Interpretation:
  - fresh-control admissibility passed cleanly
  - direct-launch BPB comparability passed cleanly
  - external runtime saving was only `2602ms`, below the reviewed `<3s -> negative` threshold
  - conclusion label is `negative`
  - `EVAL_LOGIT_TEMP=0.95` remains the promoted default on the locked `eval_031` PR809 legality line
  - direct launch should not replace the runner path as the new legality/runtime baseline on this line

## Most Important Open Question
What is the next genuinely different single-variable refinement question on top of the promoted `eval_031` `T=0.95` legality line, now that nearby scalar-temperature tuning is closed and direct-launch bypass is also negative on this line?

## Active Experiment ID
`eval_033_eval031_direct_launch_pair`

## Latest Result Summary
- Completed the reviewed launcher-path control pair on the locked promoted `eval_031` helper lineage with no code edits.
- Controlled intervention actually executed:
  - fresh runner control at `EVAL_LOGIT_TEMP=0.95`
  - fresh direct-launch candidate at `EVAL_LOGIT_TEMP=0.95`
  - same helper, checkpoint, artifact, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - direct-launch command recovered from fresh control metadata and reused with the same wrapped child command, same cwd, same `physicslm`, and same pinned GPUs
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - fresh runner control result: `legal_ttt_exact val_bpb=0.29081380`, `val_loss=0.49102692`
  - fresh direct-launch result: `legal_ttt_exact val_bpb=0.29081558`, `val_loss=0.49102993`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh runner control: `585452ms` script, `627968ms` runner, `628139ms` external
  - fresh direct launch: `583370ms` script, `625537ms` external
- Decision:
  - fresh-control admissibility passed
  - direct launch preserved BPB within `±0.0001`
  - direct launch saved only `2602ms` externally
  - label: `negative`
  - the locked `eval_031` line with `EVAL_LOGIT_TEMP=0.95` remains the active legality baseline
  - launcher bypass should be treated as closed negative on this line

## Recommended Next Step
Keep the locked PR809 legality stack fixed with promoted `EVAL_LOGIT_TEMP=0.95` and move the next refinement round to a genuinely different single-variable question rather than another nearby launcher-path or scalar-calibration rerun.
