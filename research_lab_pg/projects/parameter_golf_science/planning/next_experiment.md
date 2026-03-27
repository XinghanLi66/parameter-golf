# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase candidate-only operational diagnosis of the patched-helper `NGRAM_EVAL_BUCKETS=1048576` path on GPUs `1..7`.

- Executed the reviewed brief in the narrowed operational lane:
  - re-read the required SOTA, urgent n-gram, planning, reporting, and `eval_049` lineage files before changing anything
  - re-verified helper, checkpoint, and artifact bytes/SHA against the validated `eval_049` lineage
  - reused the exact patched helper unchanged in a fresh `eval_050` run directory
  - recorded a fresh gate sample, then a bounded launch-ready clean-idle watch on GPUs `1..7`
  - captured full external GPU telemetry during the rerun
  - launched exactly one candidate-only `NGRAM_EVAL_BUCKETS=1048576` rerun through `tools/gpu_experiment_runner.py`
- The operational question is now answered:
  - the prior late `1048576` failure from `eval_049` did **not** reproduce
  - the rerun passed the old failure locus at chunk `1521/1893`
  - it finished cleanly, wrote `metadata.json`, and emitted final post-export metrics
- Because this round intentionally omitted a fresh same-session control arm, the result is `operationally viable`, **not** `promote`.

## Experiment ID
`eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu`

## Category
- evaluation

Operational subtype: `evaluation-path operational diagnosis`

## Baseline / Comparison
Primary comparison for this round:
- prior failed `eval_049` candidate at `NGRAM_EVAL_BUCKETS=1048576`
- one exact rerun on the same patched-helper / checkpoint / artifact / GPU-subset path with only fresh operational identifiers

Context anchors retained but not rerun this round:
- `eval_049` patched-helper admissible control at `NGRAM_EVAL_BUCKETS=2097152`
- `eval_048` patched-helper admissible control at `NGRAM_EVAL_BUCKETS=2097152`
- `eval_047` patched-helper admissible control at `NGRAM_EVAL_BUCKETS=2097152`

## Hypothesis
On the validated patched `1..7` surrogate regime, the `NGRAM_EVAL_BUCKETS=1048576` path is either:
- operationally unstable in a reproducible way, in which case one exact rerun should fail again with comparable late-path evidence, or
- operationally viable, in which case one exact rerun should finish cleanly and produce a final post-export metric.

This round tests stability only, not promotability.

## Why It Might Work
- `eval_049` already provided the fresh admissible patched-helper control, so repeating another control would not answer a new question.
- The only unresolved variable was whether the `1048576` candidate itself is reproducibly broken on this patched `1..7` path.
- Even a negative result would have been scientifically useful because it would have closed `1048576` as operationally unstable on this path.

## Minimal Intervention
No helper-code change beyond copying the already-validated patched helper into a fresh run directory:
- copied `runs/eval_049_eval048_buckets_pair_patched_7gpu/train_gpt.py`
- kept helper bytes/hash identical to `eval_049`, `eval_048`, and `eval_047`
- launched only the candidate-only `NGRAM_EVAL_BUCKETS=1048576` path

No changes to:
- model weights
- checkpoint bytes
- artifact bytes
- scorer math
- cache/update logic
- export logic
- tokenizer
- validation data
- runner path
- TTT settings
- GPU subset `1..7`

## Variables To Change
Operational-only changes:
- fresh `RUN_ID`
- fresh runner log directory
- fresh run name
- fresh gate logs
- fresh external telemetry log

Scientific variable under test:
- `NGRAM_EVAL_BUCKETS=1048576` candidate rerun on the patched helper path

## Variables To Hold Fixed
- exact patched eval-only helper logic from `eval_049`
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
  - path: `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/train_gpt.py`
  - bytes: `126026`
  - SHA-256: `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
- Reference helper from `eval_049` and `eval_047`:
  - path: `runs/eval_049_eval048_buckets_pair_patched_7gpu/train_gpt.py`
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
- copied helper matches `eval_049` and `eval_047` exactly
- checkpoint unchanged before launch
- artifact unchanged before launch

## Commands Actually Run
Exact candidate rerun command was recorded in:
- `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/command.txt`

Gate evidence was recorded in:
- `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/clean_idle_gate.log`
- `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/gate_watch.log`

External telemetry was recorded in:
- `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/external_gpu_telemetry.log`

Candidate runner directory:
- `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/runner_candidate_7gpu/20260327T161117Z_eval_050_runner_candidate_7gpu_t1p00_e4_b1048576_lr0025/`

## Clean-Idle Gate Result
- initial fresh sample status: `fail`
- initial sample time: `2026-03-27T16:10:03Z`
- first sample showed GPUs `1..7` occupied by a foreign 8-GPU workload:
  - about `37543..39141 MiB` used on the selected subset
  - about `41866..43464 MiB` free
  - `100%` utilization on each selected GPU
- bounded watch then recovered a clean launch window:
  - launch-ready pass sample time: `2026-03-27T16:10:35Z`
  - GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - no compute-app processes were present on the selected subset at the pass sample

## Candidate Launch Result
- candidate launch status: `completed cleanly`
- run directory timestamp: `2026-03-27T16:11:17Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- exact failure locus from `eval_049` was crossed cleanly:
  - old failed locus: chunk `1521/1893` at running `bpb=0.161550`, any-match `0.979712`, avg alpha `0.659670`, helper chunk-time `637.6s`
  - rerun at the same locus: chunk `1521/1893` at running `bpb=0.161550`, any-match `0.979712`, avg alpha `0.659664`, helper chunk-time `487.0s`
  - rerun then continued through the remaining `372` chunks and finished
- final metrics:
  - `legal_ttt_exact val_loss=0.24656535`
  - `legal_ttt_exact val_bpb=0.14602989`
  - script wallclock `618438ms`
  - runner-managed wallclock `666370ms`
  - external wallclock `666.594s`
  - `runner_start_to_child_spawn_ms=395`
  - `child_runtime_ms=665975`
  - any-match fraction `0.98387635`
  - avg alpha `0.66088724`
  - matched-order histogram:
    - `order_2=17786`
    - `order_3=95312`
    - `order_4=113192`
    - `order_5=124743`
    - `order_6=175760`
    - `order_7=309994`
    - `order_8=810348`
    - `order_9=59374482`
  - `ngram_batch_lookup_elapsed_ms=14132`
  - `ngram_torch_stats_elapsed_ms=4303`
  - `ngram_postlookup_vectorized_elapsed_ms=1108473`
  - `ngram_update_batch_timing elapsed_ms=29799`
- runner metadata:
  - exit code `0`
  - timeout `false`
  - `metadata.json` written successfully
- external GPU telemetry near the finish showed a normal active tail rather than a crash pattern:
  - at `2026-03-27T16:22:19Z`, GPUs `1..7` were using about `5367..5627 MiB` with `68..82%` utilization
  - at `2026-03-27T16:22:24Z` and `2026-03-27T16:22:30Z`, GPUs `1..7` had returned to `0 MiB` used, about `81007 MiB` free, and `0%` utilization with `subset_apps=none`

## Success Metric
Required outcomes:
- if the path were unstable, the rerun should fail again with comparable late-path evidence
- if the path were viable, the rerun should finish cleanly and emit final post-export metrics

Actual status:
- repeated late failure: `not reproduced`
- clean completion: `pass`
- final post-export metric emitted: `pass`
- metadata written: `pass`
- decision basis: `the exact rerun completed cleanly on the same patched-helper lineage, so the prior late failure is not reproducible enough to close the setting as operationally unstable`

## Expected Effect
If the prior `eval_049` failure was path-level instability, the rerun should fail again near the same late chunk. If it was transient, the rerun should finish and reopen the bucket question for a later fresh same-session comparison.

## Actual Result
- The first fresh gate sample was dirty, but the selected `1..7` subset became clean under a bounded watch and the candidate launched on the exact reviewed path.
- The rerun matched the prior failed candidate’s live trajectory through the old failure zone, then cleanly exceeded it:
  - same chunk `1521/1893`
  - same running `bpb=0.161550`
  - same any-match `0.979712`
  - effectively identical avg alpha
  - but about `150.6s` faster at that locus, with no crash
- The candidate then finished, wrote `metadata.json`, and produced final post-export metrics.
- Relative to the last completed patched-helper `2097152` control from `eval_049`, the completed `1048576` rerun was contextually:
  - `-0.09069261` lower on `val_loss`
  - `-0.05371327` lower on `val_bpb`
  - `+2381ms` slower on script wallclock
  - `+4723ms` slower on runner-managed wallclock
  - `+4.665s` slower on external wallclock
- Those control deltas are informative context only; they are **not** promotability evidence for this round because no fresh same-session control arm was rerun here.

## Interpretation
- Decision label: `1048576 operationally viable but needs fresh same-session comparison`
- The exact `eval_049` late crash is not reproducible enough to close `1048576` as operationally unstable on the patched `1..7` path.
- The candidate-only operational diagnosis therefore succeeds: this setting can finish on the validated patched-helper path.
- Promotability is still unanswered because this round intentionally omitted a fresh same-session `2097152` control.
- The unexpectedly large completed BPB shift relative to the last completed `2097152` control makes a later reviewed same-session control/candidate pair more useful, not less, because the operational blocker is now removed but the scientific bucket conclusion still needs a comparison-clean rerun.

## Next Step
If the bucket question still matters, schedule a later reviewed same-session patched-helper `2097152 -> 1048576` control/candidate comparison on the validated `1..7` surrogate path, keeping helper/checkpoint/artifact lineage and all non-bucket settings fixed.

If that question is no longer the highest-priority refinement target, move the next reviewed round to a different single-variable evaluation question; do not treat `eval_050` alone as a promotion.
