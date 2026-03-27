# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase fresh same-session patched-helper bucket confirmation pair on GPUs `1..7`.

- Executed the reviewed brief as written:
  - re-read the required SOTA, urgent n-gram, planning, reporting, and lineage files before changing anything
  - re-verified helper, checkpoint, and artifact bytes/SHA against the validated patched lineage
  - copied the exact patched helper bytes into a fresh `eval_051` run directory with no helper edits
  - recorded a clean initial gate on GPUs `1..7`
  - launched the fresh `2097152` control through `tools/gpu_experiment_runner.py`
  - checked the control against `eval_049` and `eval_048` before touching the candidate arm
  - recorded an immediate clean handoff sample and then launched the `1048576` candidate
  - captured separate external telemetry for both arms
- The round did not yield a promotability decision because the candidate arm became contaminated after a clean handoff:
  - the control completed admissibly
  - the candidate launched cleanly but a foreign workload appeared on GPUs `1..7` during the candidate arm
  - I stopped the candidate rather than force a dirty comparison
- Final round label: `invalid pair`

## Experiment ID
`eval_051_eval050_buckets_pair_confirm_patched_7gpu`

## Category
- evaluation

Subtype: `fresh same-session bucket confirmation pair`

## Baseline / Comparison
Primary decision baseline for this round:
- fresh same-session patched-helper control at `NGRAM_EVAL_BUCKETS=2097152` on GPUs `1..7`

Immediate candidate:
- same patched-helper path with only `NGRAM_EVAL_BUCKETS=1048576`

Context anchors:
- `eval_049` patched-helper admissible control at `0.19974316`
- `eval_050` candidate-only operational rerun at `0.14602989`

## Hypothesis
If `NGRAM_EVAL_BUCKETS=1048576` is a real improvement on the validated patched `1..7` surrogate path, then a fresh same-session pair should show:
- an admissible fresh `2097152` control
- a clean `1048576` candidate completion
- a candidate post-export `val_bpb` improvement over the fresh control by at least `0.00010`

If the dramatic `eval_050` metric was not comparison-clean evidence, then the candidate should either fail again, get invalidated operationally, or fail to clear the decision floor.

## Why It Might Work
- `eval_049` already validated the patched `2097152` control path.
- `eval_050` already showed that `1048576` can finish on the same patched lineage.
- The missing evidence was the exact same-session control/candidate comparison with only bucket count changed.

## Minimal Intervention
No model-code or evaluation-logic edits were made.

Only these changes were introduced:
- fresh run directory and fresh operational identifiers
- copied patched helper bytes unchanged from `eval_049`
- control arm `NGRAM_EVAL_BUCKETS=2097152`
- candidate arm `NGRAM_EVAL_BUCKETS=1048576`
- fresh gate evidence, handoff evidence, and external telemetry capture

## Variables To Change
- `RUN_ID`
- runner log dirs
- run names
- gate and telemetry logs
- scientific variable: `NGRAM_EVAL_BUCKETS 2097152 -> 1048576`

## Variables To Hold Fixed
- exact patched helper bytes/hash from `eval_049` and `eval_050`
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
- vectorized chunk-based n-gram path: batched lookup, batched torch stats, vectorized postlookup
- GPUs `1,2,3,4,5,6,7`

## Identity Checks
- Patched helper copy:
  - path: `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/train_gpt.py`
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
- copied helper matches `eval_049` and `eval_050` exactly
- checkpoint unchanged before launch
- artifact unchanged before launch

## Commands Actually Run
Exact control and candidate commands were recorded in:
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/command.txt`

Gate evidence was recorded in:
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/clean_idle_gate.log`
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/gate_watch.log`
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/candidate_handoff_gate.log`

External telemetry was recorded in:
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/external_gpu_telemetry_control.log`
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/external_gpu_telemetry_candidate.log`

Runner outputs were recorded in:
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/runner_control_7gpu/20260327T164002Z_eval_051_runner_control_7gpu_t1p00_e4_b2097152_lr0025/`
- `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/runner_candidate_7gpu/20260327T165221Z_eval_051_runner_candidate_7gpu_t1p00_e4_b1048576_lr0025/`

## Clean-Idle Gate Result
- initial fresh sample status: `pass`
- gate sample time: `2026-03-27T16:39:09Z`
- GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
- no compute-app processes were present on the selected subset

## Control Launch Result
- control launch status: `completed cleanly`
- run directory timestamp: `2026-03-27T16:40:02Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- final metrics:
  - `legal_ttt_exact val_loss=0.33725841`
  - `legal_ttt_exact val_bpb=0.19974343`
  - script wallclock `617197ms`
  - runner-managed wallclock `665584ms`
  - external wallclock `665.848s`
  - `runner_start_to_child_spawn_ms=649`
  - `child_runtime_ms=664935`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461559`
  - matched-order histogram:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
  - `ngram_batch_lookup_elapsed_ms=17414`
  - `ngram_torch_stats_elapsed_ms=4366`
  - `ngram_postlookup_vectorized_elapsed_ms=1109722`
  - `ngram_update_batch_timing elapsed_ms=30758`
- runner metadata:
  - exit code `0`
  - timeout `false`
  - `metadata.json` written successfully
- external telemetry showed a normal active tail at `2026-03-27T16:51:01Z` with about `5367..5627 MiB` used and `69..84%` utilization on GPUs `1..7`, followed by clean release at `16:51:07Z`

## Control Admissibility
The fresh control passed the reviewed admissibility requirement.

Versus `eval_049` patched-helper control:
- `+0.00000027` BPB
- `+0.00000045` val_loss
- `+1140ms` script wallclock
- `+3937ms` runner-managed wallclock
- `+3.919s` external wallclock
- `+259ms` `runner_start_to_child_spawn_ms`
- `+3679ms` `child_runtime_ms`
- `+0.00000000` any-match
- `-0.00000168` avg alpha
- identical matched-order histogram
- `-738ms` n-gram batch lookup elapsed
- `+32ms` torch-stats elapsed
- `-2602ms` postlookup elapsed
- `+269ms` update-batch elapsed

Versus `eval_048` patched-helper control:
- `+0.00000005` BPB
- `+0.00000009` val_loss
- `-6605ms` script wallclock
- `-4325ms` runner-managed wallclock
- `-4.293s` external wallclock
- `+238ms` `runner_start_to_child_spawn_ms`
- `-4563ms` `child_runtime_ms`
- `+0.00000000` any-match
- `+0.00000025` avg alpha
- identical matched-order histogram
- `+228ms` n-gram batch lookup elapsed
- `-25ms` torch-stats elapsed
- `+4309ms` postlookup elapsed
- `-91ms` update-batch elapsed

## Candidate Handoff Gate Result
- immediate handoff sample time: `2026-03-27T16:51:56Z`
- GPUs `1..7` each still showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
- no compute-app processes were present at the handoff sample
- handoff status: `pass`

## Candidate Contamination Result
- candidate launch started cleanly under run directory timestamp `2026-03-27T16:52:21Z`
- the candidate was not allowed to produce a decision metric because the pair became dirty after launch:
  - first contamination evidence arrived at `2026-03-27T16:53:37Z`
  - foreign PIDs `1873822..1873828` appeared on GPUs `1..7` while candidate PIDs `1869880..1869886` were already active
  - initial foreign memory footprint was already nonzero on every reviewed GPU, about `714..756 MiB`
  - contamination then escalated through later samples; by `2026-03-27T16:58:43Z` and `16:58:48Z`, GPUs `1..7` were at `100%` utilization with about `36.5..38.9 GiB` foreign memory plus about `5.3..5.6 GiB` candidate memory per GPU
- because the same-session comparison was no longer clean, I interrupted the candidate instead of forcing a dirty final metric
- candidate partial progress before interruption:
  - latest captured stdout reached chunk `221/1893`
  - running `bpb=0.509815`
  - any-match `0.860559`
  - avg alpha `0.629725`
  - helper chunk-time `321.8s`
- candidate runner directory did not write `metadata.json`
- no final post-export `val_loss`
- no final post-export `val_bpb`

## Success Metric
Required outcomes:
- fresh control completes and is admissible
- only then immediate candidate launches
- candidate must remain comparison-clean and finish with final post-export metrics

Actual status:
- control admissibility: `pass`
- handoff cleanliness: `pass`
- candidate comparison cleanliness: `fail`
- candidate completion with final metrics: `not valid`
- final decision basis: `the candidate arm became contaminated after a clean handoff, so the same-session pair is invalid`

## Expected Effect
If `1048576` were a real clean same-session improvement, the candidate should have remained isolated and produced a final post-export metric that beat the fresh control by at least `0.00010 BPB`.

## Actual Result
- The exact patched helper, checkpoint, and artifact identities stayed fixed and correct.
- The fresh `2097152` control completed cleanly and remained admissible versus both `eval_049` and `eval_048`.
- The immediate handoff sample was clean, so launching the candidate was justified.
- The candidate then lost interpretability because a foreign workload appeared on GPUs `1..7` after launch and persisted, materially occupying the same reviewed subset.
- I stopped the candidate once the contamination was clearly persistent rather than let a dirty run finish and masquerade as bucket evidence.

## Interpretation
- Decision label: `invalid pair`
- The control result is valid and confirms the patched `2097152` path remains admissible.
- The round does **not** answer the `2097152 -> 1048576` promotability question because the candidate arm was contaminated after a clean handoff.
- The partial candidate stdout and dirty telemetry are operational evidence only; they are not promotability evidence and should not be compared against the fresh control as if this were a clean pair.

## Next Step
If the bucket question still matters, rerun the same reviewed patched-helper `2097152 -> 1048576` pair only when GPUs `1..7` can remain isolated through both arms, with the same helper/checkpoint/artifact lineage and no semantic changes.

Do not treat this round as evidence to `promote 1048576`, `hold 2097152`, or classify `1048576 unstable`; the correct label for `eval_051` is `invalid pair`.
