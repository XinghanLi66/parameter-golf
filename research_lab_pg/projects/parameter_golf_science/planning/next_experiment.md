# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase eval-only launch-path compatibility and surrogate-validity check on the promoted legal-TTT line.

- Executed the reviewed brief through the required file re-read, locked command recovery, copied-helper patch, helper/checkpoint/artifact identity verification, 7-GPU clean-idle acquisition on `1..7`, and one fresh patched-helper `TTT_EPOCHS=4` control launch.
- The intervention was narrowed exactly as reviewed:
  - copied the locked helper into a fresh run directory
  - patched only the eval-only non-divisor `WORLD_SIZE` startup invariant
  - did not change training behavior
  - did not change non-eval launch behavior
  - did not change scorer math, TTT math, cache logic, export logic, checkpoint bytes, or artifact bytes
- The fresh patched 7-GPU control launched, finished, and produced a full telemetry set.
- The immediate `TTT_EPOCHS=3` candidate was intentionally not run in this round, per the reviewed brief.
- The round is a controlled `surrogate admissible` result on the patched `1..7` path.

## Experiment ID
`eval_047_eval045_patched_helper_7gpu_control`

## Category
- evaluation

Operational subtype: `eval-only launch-path compatibility and surrogate-validity check`

## Baseline / Comparison
Primary baseline:
- fresh admissible 8-GPU promoted-line control `eval_045=0.19974186`

Secondary anchor:
- promoted line `eval_038=0.19974237`

Prior blocker evidence:
- `eval_046` no-code-change launch failure on `WORLD_SIZE=7`

Actual comparison obtained this round:
- fresh patched-helper 7-GPU control on GPUs `1..7` with `TTT_EPOCHS=4`
- compared directly against `eval_045` and `eval_038` on:
  - `val_bpb`
  - `val_loss`
  - script wallclock
  - runner wallclock
  - external wallclock
  - any-match fraction
  - avg alpha
  - matched-order histogram
  - `ngram_postlookup_vectorized_elapsed_ms`

## Hypothesis
If the only blocker exposed by `eval_046` was the helper’s startup invariant rather than a real change in evaluation semantics, then a minimal eval-only patch permitting `WORLD_SIZE=7` would produce a fresh promoted-line 7-GPU control that stays in-family with `eval_045`.

Operational falsifier:
- patched launch still fails, or
- patched launch finishes but drifts materially from `eval_045`

## Why It Might Work
- `eval_046` already localized the failure to helper startup rather than GPU cleanliness on the `1..7` subset.
- The eval-only path does not use the training loop or gradient accumulation schedule as a scientific variable.
- A guarded eval-only non-divisor fallback is therefore the smallest operational repair that can answer surrogate validity without mixing scorer, TTT, export, dataset, or checkpoint changes.

## Minimal Intervention
One copied-helper startup patch only:
- introduce `eval_only_nondivisor_world_size = args.eval_only and (8 % world_size != 0)`
- preserve the original `WORLD_SIZE` divisor invariant everywhere else
- set `grad_accum_steps = 1` only on that eval-only non-divisor path
- log when that compatibility path is taken

No other code or artifact changes:
- original locked helper left untouched
- checkpoint unchanged
- artifact unchanged
- runner unchanged
- no candidate arm launched

## Variables To Change
Helper startup logic only:
- copied helper path
- eval-only non-divisor `WORLD_SIZE` compatibility path

Operational-only:
- launch subset `CUDA_VISIBLE_DEVICES=1,2,3,4,5,6,7`
- runner request count `7`
- `torchrun --nproc_per_node=7`
- fresh `RUN_ID`
- fresh runner `--log-dir`
- fresh runner `--run-name`

## Variables To Hold Fixed
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `TTT_EPOCHS=4`
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
- same checkpoint bytes/hash
- same artifact bytes/hash
- same tokenizer, validation data, environment, and runner path

## Identity Checks
- Patched helper:
  - path: `runs/eval_047_eval045_patched_helper_7gpu_control/train_gpt.py`
  - bytes: `126026`
  - SHA-256: `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
- Locked source helper:
  - path: `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`
  - bytes: `125663`
  - SHA-256: `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
- Saved checkpoint:
  - path: `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
  - bytes: `106178569`
  - SHA-256: `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- Saved artifact:
  - path: `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
  - bytes: `15555121`
  - SHA-256: `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

Identity status:
- patched helper differs only by the reviewed eval-only startup patch
- checkpoint unchanged before launch
- artifact unchanged before launch

## Commands Actually Run
Exact patched control command was recorded in:
- `runs/eval_047_eval045_patched_helper_7gpu_control/command.txt`

The 7-GPU clean-idle gate evidence was recorded in:
- `runs/eval_047_eval045_patched_helper_7gpu_control/clean_idle_gate.log`

The fresh patched 7-GPU control was launched via:
- `tools/gpu_experiment_runner.py` in `physicslm`
- pinned subset `1,2,3,4,5,6,7`
- runner log dir `runs/eval_047_eval045_patched_helper_7gpu_control/runner_control_7gpu/`

No candidate command was run in this round.

## Clean-Idle Gate Result
- gate status: `pass`
- gate sample time: `2026-03-27T14:12:53Z`
- GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
- GPU `0` remained occupied by a foreign process at about `74486 MiB`, but that was outside the reviewed `1..7` gate set
- because the gate passed:
  - the fresh patched 7-GPU control launch was attempted immediately

## Helper Diff Summary
- The copied helper now defines `eval_only_nondivisor_world_size = args.eval_only and (8 % world_size != 0)`.
- The original divisor error is still raised for:
  - all training launches
  - all non-eval launches
  - any other non-divisor path outside `EVAL_ONLY=1`
- `grad_accum_steps` now falls back to `1` only on that eval-only non-divisor path; otherwise it remains `8 // world_size` exactly as before.
- A single log line records when the compatibility path is used:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`

## Control Launch Result
- control launch status: `completed`
- exact runner launch start: `2026-03-27T14:13:16Z`
- exact runner end: `2026-03-27T14:24:19Z`
- runner selected GPUs `1,2,3,4,5,6,7` successfully
- compatibility log emitted:
  - `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- final metrics:
  - `legal_ttt_exact val_loss=0.33725596`
  - `legal_ttt_exact val_bpb=0.19974198`
  - script wallclock `616325ms`
  - runner-managed wallclock `662808ms`
  - external wallclock `663.092s`
  - `runner_start_to_child_spawn_ms=428`
  - `child_runtime_ms=662380`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461744`
  - matched-order histogram unchanged:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
  - `ngram_postlookup_vectorized_elapsed_ms=1110166`
- runner metadata:
  - exit code `0`
  - timeout `false`

## Candidate Launch Result
- candidate launch status: `not attempted`
- reason:
  - the reviewed brief explicitly prohibited running `TTT_EPOCHS=3` in this round
  - this round’s purpose was to answer surrogate admissibility first

## Success Metric
Primary operational success required:
- patched 7-GPU control launches and finishes

Primary admissibility success required:
- `val_bpb` within `±0.00002` of `eval_045`

Secondary admissibility checks:
- any-match fraction unchanged or negligible noise
- avg alpha in-family
- matched-order histogram unchanged or numerically negligible drift
- key timing telemetry emitted normally

Actual status:
- launch: `pass`
- finish: `pass`
- `val_bpb` delta vs `eval_045`: `+0.00000012`
- any-match delta vs `eval_045`: `+0.00000000`
- avg alpha delta vs `eval_045`: `+0.00001589`
- histogram delta vs `eval_045`: `exactly unchanged`
- telemetry emission: `pass`
- surrogate-regime decision: `admissible`

## Expected Effect
If the startup invariant were the only blocker, the patched-helper 7-GPU control should launch and finish while remaining semantically in-family with the fresh 8-GPU control.

## Actual Result
- The patched helper launched and completed the full promoted-line 7-GPU control on GPUs `1..7`.
- The control stayed extremely close to the fresh 8-GPU baseline:
  - vs `eval_045`, `val_bpb` was only `+0.00000012`
  - any-match fraction was identical
  - matched-order histogram was identical
  - avg alpha remained in-family
- The control also stayed in-family versus promoted `eval_038`:
  - `val_bpb` delta `-0.00000039`
  - any-match identical
  - matched-order histogram identical
- Timing moved favorably versus the fresh 8-GPU control:
  - script `-689683ms`
  - runner `-687719ms`
  - external `-687713ms`
  - `ngram_postlookup_vectorized_elapsed_ms -373926`

## Interpretation
- Decision label: `7-GPU surrogate admissible`
- The reviewed hypothesis is supported.
- `eval_046` was blocked by a helper startup invariant, not by a necessary change in evaluation semantics on the `1..7` subset.
- The patched 7-GPU control is admissible as a surrogate regime for the promoted 8-GPU control under the reviewed threshold.
- This round does not answer anything about `TTT_EPOCHS=3`; it only reopens that question on a now-validated path.

## Next Step
Run the exact same-session promoted-line `TTT_EPOCHS=4 -> 3` pair on the patched `1..7` path:
- keep the patched eval-only helper fixed
- keep checkpoint, artifact, scorer path, and all non-epoch variables fixed
- run a fresh patched 7-GPU control with `TTT_EPOCHS=4`
- then immediately run the patched 7-GPU candidate with only `TTT_EPOCHS=3`
- compare against the validated surrogate-control regime established here rather than against the blocked no-code-change path
