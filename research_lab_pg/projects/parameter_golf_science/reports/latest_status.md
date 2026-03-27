# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line remains `eval_035_eval031_bucket_geometry_pair` at `0.20079980`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest scored refinement round is `eval_036_eval035_ttt_lr_pair`.
- The helper/artifact guardrail stayed clean before and after both runs:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only TTT-scalar lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - kept `NGRAM_EVAL_BUCKETS=2097152` fixed
  - changed only `TTT_LR` from `0.0025` to `0.0020`
- Fresh admissible control on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.33903990`
  - `val_bpb=0.20079853`
  - script `582012ms`
  - runner `626047ms`
  - external `626047ms` via runner-total proxy; metadata UTC timestamps independently imply about `626000ms`
- Fresh `TTT_LR=0.0020` candidate on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.33907413`
  - `val_bpb=0.20081880`
  - script `591247ms`
  - runner `633936ms`
  - external `634143ms`
- Decision comparisons:
  - fresh control vs promoted `eval_035`: `-0.00000127 BPB`, `-260ms` script, `+1034ms` runner, `+870ms` external
  - candidate vs fresh control: `+0.00002027 BPB`, `+9235ms` script, `+7889ms` runner, `+8096ms` external
  - candidate vs historical `eval_015`: `+0.00107678 BPB`
- Interpretation:
  - control admissibility passed cleanly, so the candidate result is scientifically interpretable
  - primary quality success failed
  - secondary runtime tolerance passed, but only because the candidate remained within the reviewed `+20s` band while still being slower
  - conclusion label is `hold`
  - `TTT_LR=0.0025` should remain the promoted quality default on the locked `eval_035` PR809 legality line

## Most Important Open Question
What is the next genuinely different single-variable refinement question on top of the promoted `eval_035` legality line with `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152`, now that scalar temperature, launcher bypass, TTT epoch count, bucket geometry, and downward TTT-LR retuning are all answered on this lineage?

## Active Experiment ID
`eval_036_eval035_ttt_lr_pair`

## Latest Result Summary
- Completed the reviewed single-variable `TTT_LR` ablation on the promoted `eval_035` legality line with no code edits.
- Controlled intervention actually executed:
  - fresh runner-managed control at `TTT_LR=0.0025`
  - fresh runner-managed candidate at `TTT_LR=0.0020`
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings in both arms
  - only intended semantic difference between the two fresh arms was `TTT_LR=0.0025 -> 0.0020`
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - control result: `legal_ttt_exact val_bpb=0.20079853`, `val_loss=0.33903990`
  - candidate result: `legal_ttt_exact val_bpb=0.20081880`, `val_loss=0.33907413`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh control: `582012ms` script, `626047ms` runner, `626047ms` external via runner-total proxy
  - fresh candidate: `591247ms` script, `633936ms` runner, `634143ms` external
- Decision:
  - fresh control passed the reviewed admissibility gate versus promoted `eval_035`
  - the lower-`TTT_LR` candidate should not replace the promoted default
  - label: `hold`

## Recommended Next Step
Keep the locked PR809 legality stack fixed with promoted `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152`. Move the next refinement round to a different single-variable question rather than spending another immediate round on lower-`TTT_LR` retuning on this helper lineage.
