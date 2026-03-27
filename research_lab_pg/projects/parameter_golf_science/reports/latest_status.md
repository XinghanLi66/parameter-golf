# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted legality line is now the refreshed promoted-helper transfer `eval_035_eval031_bucket_geometry_pair` at `0.20079980`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest scored refinement round is `eval_035_eval031_bucket_geometry_pair`.
- The helper/artifact guardrail stayed clean before and after the run:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only bucket-geometry lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only `NGRAM_EVAL_BUCKETS` from `4194304` to `2097152`
- Fresh admissible control on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.49102809`
  - `val_bpb=0.29081449`
  - script `591126ms`
  - runner `634475ms`
  - external `634633ms`
- Fresh `NGRAM_EVAL_BUCKETS=2097152` candidate on GPUs `0,1,2,3,4,5,6,7`:
  - `val_loss=0.33904205`
  - `val_bpb=0.20079980`
  - script `582272ms`
  - runner `625013ms`
  - external `625177ms`
- Decision comparisons:
  - fresh control vs `eval_033`: `+0.00000069 BPB`, `+5674ms` script, `+6507ms` runner, `+6494ms` external
  - candidate vs fresh control: `-0.09001469 BPB`, `-8854ms` script, `-9462ms` runner, `-9456ms` external
  - candidate vs promoted `eval_032`: `-0.09001291 BPB`, `-2604ms` script, `-2169ms` runner, `-2244ms` external
  - candidate vs historical `eval_015`: `+0.00105778 BPB`, `-81685ms` script
- Interpretation:
  - control admissibility passed cleanly, so the candidate result is scientifically interpretable
  - primary quality success passed by a very large margin
  - secondary runtime success also passed because the candidate is slightly faster than the fresh control
  - conclusion label is `promote`
  - `NGRAM_EVAL_BUCKETS=2097152` should replace `4194304` as the promoted quality default on the locked `eval_031` PR809 legality line

## Most Important Open Question
What is the next genuinely different single-variable refinement question on top of the promoted `eval_031` `T=0.95`, legal TTT, PR809 vectorized n-gram line with `NGRAM_EVAL_BUCKETS=2097152`, now that scalar temperature, launcher bypass, TTT epoch count, and the first refreshed bucket-geometry test are all answered on this lineage?

## Active Experiment ID
`eval_035_eval031_bucket_geometry_pair`

## Latest Result Summary
- Completed the reviewed single-variable `NGRAM_EVAL_BUCKETS` ablation on the locked promoted `eval_031` helper lineage with no code edits.
- Controlled intervention actually executed:
  - fresh runner-managed control at `NGRAM_EVAL_BUCKETS=4194304`
  - fresh runner-managed candidate at `NGRAM_EVAL_BUCKETS=2097152`
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings in both arms
  - only intended semantic difference between the two fresh arms was `NGRAM_EVAL_BUCKETS=4194304 -> 2097152`
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - control result: `legal_ttt_exact val_bpb=0.29081449`, `val_loss=0.49102809`
  - candidate result: `legal_ttt_exact val_bpb=0.20079980`, `val_loss=0.33904205`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - fresh control: `591126ms` script, `634475ms` runner, `634633ms` external
  - fresh candidate: `582272ms` script, `625013ms` runner, `625177ms` external
- Decision:
  - fresh control passed the reviewed admissibility gate versus `eval_033`
  - promoted default on this helper lineage should now be `NGRAM_EVAL_BUCKETS=2097152`
  - label: `promote`

## Recommended Next Step
Keep the locked PR809 legality stack fixed with promoted `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, and now `NGRAM_EVAL_BUCKETS=2097152`. Move the next refinement round to a genuinely different single-variable question on top of this stronger baseline rather than revisiting bucket geometry immediately.
