# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session patched-helper `TTT_EPOCHS=4 -> 3` pair on the validated `1..7` surrogate path.

- Executed the reviewed brief through the required file re-read, exact `eval_047` helper/command recovery, copied-helper reuse, helper/checkpoint/artifact identity verification, fresh clean-idle gating on GPUs `1..7`, one fresh patched-helper `TTT_EPOCHS=4` control, an admissibility check against `eval_047`, and one immediate patched-helper `TTT_EPOCHS=3` candidate.
- The intervention stayed controlled exactly as reviewed:
  - reused the validated patched eval-only helper from `eval_047` unchanged
  - kept checkpoint, artifact, scorer path, tokenizer, data, runner path, and all non-epoch eval settings fixed
  - changed only the candidate arm’s `TTT_EPOCHS: 4 -> 3`
- Both arms launched and finished cleanly.
- The fresh control was admissible versus `eval_047`.
- The candidate stayed within the reviewed BPB tolerance but was substantially slower, so the round closes as `hold TTT_EPOCHS=4`.

## Experiment ID
`eval_048_eval047_ttt_epochs_pair_patched_7gpu`

## Category
- evaluation

Operational subtype: `same-session patched-helper epoch-count comparison`

## Baseline / Comparison
Primary baseline:
- fresh same-session patched-helper 7-GPU control on GPUs `1..7` with `TTT_EPOCHS=4`

Admissibility anchors:
- `eval_047=0.19974198` patched-helper 7-GPU admissible control
- `eval_045=0.19974186` fresh admissible promoted-line 8-GPU control
- `eval_038=0.19974237` promoted 8-GPU anchor

Primary comparison obtained this round:
- immediate patched-helper 7-GPU candidate with only `TTT_EPOCHS: 4 -> 3`
- compared first and only for decision against the fresh same-session control

## Hypothesis
On the validated patched `1..7` surrogate regime, reducing only `TTT_EPOCHS` from `4` to `3` will keep post-export `val_bpb` within `+0.00005` of the fresh same-session control while saving meaningful eval wallclock.

Operational falsifier:
- fresh control is not admissible versus `eval_047`, or
- candidate loses by more than `+0.00005 BPB`, or
- candidate does not deliver a meaningful runtime saving

## Why It Might Work
- The current leaderboard #1 uses legal score-first TTT with `3` epochs, so this remained the cleanest unresolved evaluation-side mismatch to test on the promoted local line.
- `eval_034` on the older `T=0.95` line had already shown that `3` epochs can buy real runtime while keeping the quality loss small enough to stay interesting.
- `eval_047` had already restored interpretability by proving the patched `1..7` helper path is an admissible surrogate regime.

## Minimal Intervention
No code change beyond copying the already-validated patched helper into a fresh run directory:
- copied `runs/eval_047_eval045_patched_helper_7gpu_control/train_gpt.py`
- kept helper bytes/hash identical to `eval_047`
- kept control arm at `TTT_EPOCHS=4`
- changed only the candidate arm’s `TTT_EPOCHS` from `4` to `3`

No changes to:
- model weights
- checkpoint/artifact bytes
- scorer math
- n-gram cache/update logic
- export logic
- tokenizer
- validation data
- runner path
- GPU subset

## Variables To Change
Control arm operational-only changes:
- fresh `RUN_ID`
- fresh runner log dir
- fresh runner run name

Candidate arm scientific change:
- `TTT_EPOCHS: 4 -> 3`

## Variables To Hold Fixed
- exact patched eval-only helper logic from `eval_047`
- helper bytes/hash
- checkpoint bytes/hash
- artifact bytes/hash
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `TTT_LR=0.0025`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `EVAL_STRIDE=64`
- `EVAL_LOGIT_TEMP=1.0`
- `NGRAM_EVAL_ENABLED=1`
- `NGRAM_EVAL_BUCKETS=2097152`
- `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1`
- `NGRAM_EVAL_BATCH_TORCH_STATS=1`
- `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`
- tokenizer, validation data, environment, runner path, and GPU subset `1..7`

## Identity Checks
- Patched helper:
  - path: `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/train_gpt.py`
  - bytes: `126026`
  - SHA-256: `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
- Reference helper from `eval_047`:
  - path: `runs/eval_047_eval045_patched_helper_7gpu_control/train_gpt.py`
  - bytes: `126026`
  - SHA-256: `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
- Saved checkpoint:
  - path: `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
  - bytes: `106178569`
  - SHA-256: `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- Saved artifact:
  - path: `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
  - bytes: `15555121`
  - SHA-256: `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

Identity status:
- copied helper matches `eval_047` exactly
- checkpoint unchanged before both arms
- artifact unchanged before both arms

## Commands Actually Run
Exact paired commands were recorded in:
- `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/command.txt`

Fresh gate evidence was recorded in:
- `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/clean_idle_gate.log`

Control runner directory:
- `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/runner_control_7gpu/20260327T143726Z_eval_048_runner_control_7gpu_t1p00_e4_b2097152_lr0025/`

Candidate runner directory:
- `runs/eval_048_eval047_ttt_epochs_pair_patched_7gpu/runner_candidate_7gpu/20260327T144901Z_eval_048_runner_candidate_7gpu_t1p00_e3_b2097152_lr0025/`

## Clean-Idle Gate Result
- gate status: `pass`
- gate sample time: `2026-03-27T14:36:53Z`
- GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
- GPU `0` remained occupied by a foreign process at about `74486 MiB`, but that was outside the reviewed `1..7` gate set
- because the gate passed:
  - the fresh control launched immediately
  - the candidate was launched immediately after the control passed admissibility

## Control Launch Result
- control launch status: `completed`
- exact runner launch start: `2026-03-27T14:37:26Z`
- exact runner end: `2026-03-27T14:48:36Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- final metrics:
  - `legal_ttt_exact val_loss=0.33725832`
  - `legal_ttt_exact val_bpb=0.19974338`
  - script wallclock `623802ms`
  - runner-managed wallclock `669909ms`
  - external wallclock `670.141s`
  - `runner_start_to_child_spawn_ms=411`
  - `child_runtime_ms=669498`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461534`
  - matched-order histogram unchanged:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
  - `ngram_postlookup_vectorized_elapsed_ms=1105413`
- runner metadata:
  - exit code `0`
  - timeout `false`

Control admissibility vs `eval_047`:
- `val_bpb` delta `+0.00000140`
- `val_loss` delta `+0.00000236`
- script delta `+7477ms`
- runner delta `+7101ms`
- external delta `+7.049s`
- avg alpha delta `-0.00000210`
- matched-order histogram `unchanged`
- `ngram_postlookup_vectorized_elapsed_ms` delta `-4753ms`
- admissibility decision: `pass`

## Candidate Launch Result
- candidate launch status: `completed`
- exact runner launch start: `2026-03-27T14:49:01Z`
- exact runner end: `2026-03-27T15:06:22Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- final metrics:
  - `legal_ttt_exact val_loss=0.33730055`
  - `legal_ttt_exact val_bpb=0.19976839`
  - script wallclock `998177ms`
  - runner-managed wallclock `1041138ms`
  - external wallclock `1041.407s`
  - `runner_start_to_child_spawn_ms=306`
  - `child_runtime_ms=1040831`
  - any-match fraction `0.98387585`
  - avg alpha `0.65467460`
  - matched-order histogram unchanged:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
  - `ngram_postlookup_vectorized_elapsed_ms=1353120`
- runner metadata:
  - exit code `0`
  - timeout `false`

Primary comparison, candidate minus fresh control:
- `val_loss` `+0.00004223`
- `val_bpb` `+0.00002501`
- script wallclock `+374375ms`
- runner-managed wallclock `+371229ms`
- external wallclock `+371.266s`
- any-match fraction `+0.00000000`
- avg alpha `+0.00005926`
- matched-order histogram `unchanged`
- `ngram_postlookup_vectorized_elapsed_ms` `+247707ms`

## Success Metric
Required outcomes:
- fresh control admissible versus `eval_047`
- candidate no worse than `+0.00005 BPB` versus fresh control
- candidate saves at least `50s` wallclock

Actual status:
- fresh control admissibility: `pass`
- candidate BPB tolerance: `pass`
- candidate runtime saving: `fail`
- candidate telemetry family check: `pass for any-match and histogram; slightly higher avg alpha but still in-family`

## Expected Effect
If the promoted-line epoch mismatch to leaderboard `#1` were still a valid runtime lever on the patched `1..7` path, then `TTT_EPOCHS=3` would preserve post-export BPB while finishing materially faster than the fresh same-session `TTT_EPOCHS=4` control.

## Actual Result
- The fresh control reproduced the patched surrogate regime and passed admissibility versus `eval_047`.
- The immediate `TTT_EPOCHS=3` candidate finished cleanly and stayed within the reviewed `+0.00005 BPB` tolerance band.
- But the candidate was much slower rather than faster:
  - `+374375ms` script wallclock
  - `+371229ms` runner wallclock
  - `+371.266s` external wallclock
  - `+247707ms` on `ngram_postlookup_vectorized_elapsed_ms`
- Quality also moved in the wrong direction:
  - `+0.00002501 BPB`
  - `+0.00004223 val_loss`

## Interpretation
- Decision label: `hold TTT_EPOCHS=4`
- The reviewed promotion hypothesis is falsified on runtime and not rescued by quality.
- This is not a blocked result:
  - both arms launched and completed
  - the control was admissible
  - the candidate changed only the reviewed epoch count
  - the comparison therefore answers the intended question directly
- On the validated patched `1..7` surrogate path, `TTT_EPOCHS=3` is neither a runtime optimization nor a quality improvement.

## Next Step
Close nearby epoch-count work on this patched surrogate line:
- keep `TTT_EPOCHS=4` as the quality default
- do not promote `TTT_EPOCHS=3` as a runtime-optimized setting
- if runtime work remains important, require a new reviewed brief for a dedicated operational diagnosis of why the `3`-epoch path inflated wallclock despite fewer TTT epochs
- otherwise move the next refinement round to a different single-variable evaluation question
