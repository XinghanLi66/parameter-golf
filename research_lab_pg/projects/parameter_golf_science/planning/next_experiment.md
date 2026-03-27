# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session patched-helper `NGRAM_EVAL_BUCKETS=2097152 -> 1048576` pair on the validated `1..7` surrogate path.

- Executed the reviewed brief through the required file re-read, exact `eval_047` / `eval_048` helper-command recovery, copied-helper reuse, helper/checkpoint/artifact identity verification, fresh clean-idle gating on GPUs `1..7`, one fresh patched-helper `2097152` control, admissibility checks against `eval_048` and `eval_047`, and one immediate patched-helper `1048576` candidate launch.
- The intervention stayed controlled exactly as reviewed:
  - reused the validated patched eval-only helper from `eval_047` unchanged
  - kept checkpoint, artifact, scorer path, tokenizer, data, runner path, TTT settings, and all non-bucket eval settings fixed
  - changed only the candidate arm’s `NGRAM_EVAL_BUCKETS: 2097152 -> 1048576`
- The fresh control completed and was admissible versus both `eval_048` and `eval_047`.
- The immediate candidate launched, but it did not finish cleanly:
  - it reached chunk `1521/1893`
  - then failed late with `torch.AcceleratorError: CUDA error: unspecified launch failure`
  - torchrun hung in distributed teardown after the child-side failure
  - I interrupted the stuck runner only after the failure had already been recorded so GPUs `1..7` were released cleanly
- Because the candidate never produced a final post-export metric, the round closes as `blocked`, not `promote` or `hold`.

## Experiment ID
`eval_049_eval048_buckets_pair_patched_7gpu`

## Category
- evaluation

Operational subtype: `same-session patched-helper bucket-count comparison`

## Baseline / Comparison
Primary baseline:
- fresh same-session patched-helper 7-GPU control on GPUs `1..7` with `NGRAM_EVAL_BUCKETS=2097152`

Admissibility anchors:
- `eval_048 control=0.19974338` patched-helper 7-GPU admissible control
- `eval_047=0.19974198` patched-helper 7-GPU admissible control
- `eval_045=0.19974186` fresh admissible promoted-line 8-GPU control
- historical bucket-family signal `eval_015=0.19974202`

Primary comparison attempted this round:
- immediate patched-helper 7-GPU candidate with only `NGRAM_EVAL_BUCKETS: 2097152 -> 1048576`
- compared first and only for decision against the fresh same-session control

## Hypothesis
On the validated patched `1..7` surrogate regime, reducing only `NGRAM_EVAL_BUCKETS` from `2097152` to `1048576` will keep post-export `val_bpb` within `+0.00010` of the fresh same-session control while saving at least `30s` external wallclock.

Operational falsifier:
- fresh control is not admissible versus `eval_048` / `eval_047`, or
- candidate loses by more than `+0.00010 BPB`, or
- candidate does not save at least `30s` external wallclock

## Why It Might Work
- This is a refinement-phase runtime/promotability question, not a new architecture change.
- `eval_015` already established that `2097152` beat `4194304` on an older line, but it did not answer whether one more bucket halving is still safe on the stronger patched-helper regime with `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, and `TTT_EPOCHS=4`.
- The active local line already sits far past the accepted leaderboard anchor on BPB, so the unresolved question is whether the same line can be made cheaper to run without damaging decision quality.

## Minimal Intervention
No code change beyond copying the already-validated patched helper into a fresh run directory:
- copied `runs/eval_047_eval045_patched_helper_7gpu_control/train_gpt.py`
- kept helper bytes/hash identical to `eval_047` and `eval_048`
- kept the control arm at `NGRAM_EVAL_BUCKETS=2097152`
- changed only the candidate arm’s `NGRAM_EVAL_BUCKETS` from `2097152` to `1048576`

No changes to:
- model weights
- checkpoint/artifact bytes
- scorer math
- cache/update logic
- export logic
- tokenizer
- validation data
- runner path
- GPU subset
- TTT hyperparameters

## Variables To Change
Control arm operational-only changes:
- fresh `RUN_ID`
- fresh runner log dir
- fresh runner run name

Candidate arm scientific change:
- `NGRAM_EVAL_BUCKETS: 2097152 -> 1048576`

## Variables To Hold Fixed
- exact patched eval-only helper logic from `eval_047`
- helper bytes/hash
- checkpoint bytes/hash
- artifact bytes/hash
- `EVAL_ONLY=1`
- `EVAL_LOGIT_TEMP=1.0`
- `TTT_ENABLED=1`
- `TTT_LR=0.0025`
- `TTT_EPOCHS=4`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `EVAL_STRIDE=64`
- `NGRAM_EVAL_ENABLED=1`
- `NGRAM_EVAL_MIN_ORDER=2`
- `NGRAM_EVAL_MAX_ORDER=9`
- `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1`
- `NGRAM_EVAL_BATCH_TORCH_STATS=1`
- `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`
- tokenizer, validation data, environment, runner path, and GPU subset `1..7`

## Identity Checks
- Patched helper:
  - path: `runs/eval_049_eval048_buckets_pair_patched_7gpu/train_gpt.py`
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
- copied helper matches `eval_047` / `eval_048` exactly
- checkpoint unchanged before both arms
- artifact unchanged before both arms

## Commands Actually Run
Exact paired commands were recorded in:
- `runs/eval_049_eval048_buckets_pair_patched_7gpu/command.txt`

Fresh gate evidence was recorded in:
- `runs/eval_049_eval048_buckets_pair_patched_7gpu/clean_idle_gate.log`

Control runner directory:
- `runs/eval_049_eval048_buckets_pair_patched_7gpu/runner_control_7gpu/20260327T152213Z_eval_049_runner_control_7gpu_t1p00_e4_b2097152_lr0025/`

Candidate runner directory:
- `runs/eval_049_eval048_buckets_pair_patched_7gpu/runner_candidate_7gpu/20260327T153346Z_eval_049_runner_candidate_7gpu_t1p00_e4_b1048576_lr0025/`

## Clean-Idle Gate Result
- gate status: `pass`
- gate sample time: `2026-03-27T15:21:54Z`
- GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
- no compute-app processes were present on the selected `1..7` subset at gate sample time
- because the gate passed:
  - the fresh control launched immediately
  - the candidate was launched immediately after the control passed admissibility

## Control Launch Result
- control launch status: `completed`
- run directory timestamp: `2026-03-27T15:22:13Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- final metrics:
  - `legal_ttt_exact val_loss=0.33725796`
  - `legal_ttt_exact val_bpb=0.19974316`
  - script wallclock `616057ms`
  - runner-managed wallclock `661647ms`
  - external wallclock `661.929s`
  - `runner_start_to_child_spawn_ms=390`
  - `child_runtime_ms=661256`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461727`
  - matched-order histogram unchanged:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
  - `ngram_postlookup_vectorized_elapsed_ms=1112324`
- runner metadata:
  - exit code `0`
  - timeout `false`

Control admissibility vs `eval_048`:
- `val_bpb` delta `-0.00000022`
- `val_loss` delta `-0.00000036`
- script delta `-7745ms`
- runner delta `-8262ms`
- external delta `-8.212s`
- avg alpha delta `+0.00000193`
- matched-order histogram `unchanged`
- `ngram_postlookup_vectorized_elapsed_ms` delta `+6911ms`
- admissibility decision: `pass`

Control admissibility vs `eval_047`:
- `val_bpb` delta `+0.00000118`
- `val_loss` delta `+0.00000200`
- script delta `-268ms`
- runner delta `-1161ms`
- external delta `-1.163s`
- avg alpha delta `-0.00000017`
- matched-order histogram `unchanged`
- `ngram_postlookup_vectorized_elapsed_ms` delta `+2158ms`
- admissibility decision: `pass`

## Candidate Launch Result
- candidate launch status: `failed late / blocked`
- run directory timestamp: `2026-03-27T15:33:46Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- the candidate did not reach a final `legal_ttt_exact` line
- last recorded helper progress before failure:
  - chunk `1521/1893`
  - running `bpb=0.161550`
  - any-match `0.979712`
  - avg alpha `0.659670`
  - helper chunk-time field `637.6s`
- failure evidence:
  - `rank0` raised `torch.AcceleratorError: CUDA error: unspecified launch failure`
  - failure occurred inside `score_segments()` while materializing `local_score_starts_t`
  - `stderr.log` also recorded the NCCL teardown warning that `destroy_process_group()` was not called before process exit
- post-failure runner state:
  - torchrun hung in distributed teardown and did not write `metadata.json`
  - because the child failure had already been captured and GPUs remained occupied, I interrupted the stuck top-level runner at `2026-03-27T15:54:48Z` to release GPUs `1..7`
  - after interruption, GPUs `1..7` returned to `0 MiB` used, about `81007 MiB` free, and `0%` utilization

## Success Metric
Required outcomes:
- fresh control admissible versus `eval_048` / `eval_047`
- candidate no worse than `+0.00010 BPB` versus fresh control
- candidate saves at least `30s` external wallclock

Actual status:
- fresh control admissibility: `pass`
- candidate clean completion: `fail`
- candidate BPB tolerance: `not measurable`
- candidate runtime saving: `not measurable`
- decision basis: `blocked after admissible control because the candidate failed before producing final post-export metrics`

## Expected Effect
If one more bucket halving were still safe on the patched promoted-line surrogate path, then `NGRAM_EVAL_BUCKETS=1048576` would preserve final post-export BPB within the reviewed tolerance while finishing at least `30s` faster than the fresh same-session `2097152` control.

## Actual Result
- The fresh control reproduced the patched surrogate regime and passed admissibility versus both `eval_048` and `eval_047`.
- The immediate `1048576` candidate launched cleanly on the same helper, checkpoint, artifact, and GPU subset, but it never reached a final post-export result.
- Before the crash, the candidate showed a different live trajectory from the control:
  - same general match-coverage growth
  - higher running alpha
  - lower running chunk BPB
  - then a severe late-tail slowdown before the CUDA launch failure
- Because the candidate did not finish and required manual interruption after the failure to release GPUs, there is no valid same-session final BPB or final wallclock comparison for the candidate arm.

## Interpretation
- Decision label: `blocked`
- This is not a `hold NGRAM_EVAL_BUCKETS=2097152` result and not a `promote NGRAM_EVAL_BUCKETS=1048576` result.
- The reviewed bucket-geometry question remains unanswered because the candidate arm failed operationally after an admissible control had already been obtained.
- The fresh control does strengthen confidence that the patched `1..7` surrogate path itself remains valid and repeatable.
- The only safe scientific conclusion from round 24 is narrower:
  - `2097152` remains the last completed validated default on this patched path
  - `1048576` cannot be judged from this round because the candidate never produced the required final metrics

## Next Step
Do not infer a bucket-geometry conclusion from round 24.

If this question remains important, require a new reviewed brief for a dedicated operational diagnosis or controlled retry of the late `1048576` CUDA failure on the patched `1..7` path.

Otherwise, leave `NGRAM_EVAL_BUCKETS=2097152` as the currently validated default by default-of-evidence and move the next refinement round to a different single-variable evaluation question.
