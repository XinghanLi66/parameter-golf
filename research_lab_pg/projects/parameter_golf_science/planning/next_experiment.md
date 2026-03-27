# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session promoted-line `TTT_EPOCHS=4 -> 3` evaluation retry, but the round again stopped before launch because the required clean-idle gate on pinned GPUs `0..7` never passed.

- Executed the reviewed brief through the required file re-read, exact promoted-command recovery, helper/checkpoint/artifact identity verification, and bounded clean-idle gate watch.
- No code edits were made in this round.
- No runner-managed control launched.
- No `TTT_EPOCHS=3` candidate launched.
- The round therefore remains a controlled blocker report rather than an epoch-count result.

## Experiment ID
`eval_044_eval038_ttt_epochs_pair_clean_idle_retry`

## Category
- evaluation

Operational subtype: `same-session promoted-line epoch-pair clean-idle retry`

## Baseline / Comparison
Intended primary comparison:
- fresh same-session control on the exact promoted line with `TTT_EPOCHS=4`
- immediate same-session candidate on the exact promoted line with only `TTT_EPOCHS=3`

Interpretation anchors:
- promoted `eval_038=0.19974237`, script `588813ms`, runner `634685ms`, external `634926ms`
- current-regime clean-idle control `eval_042=0.19974395`, script `1507653ms`, runner `1555810ms`, external `1556076ms`
- older same-family result `eval_034`: `TTT_EPOCHS=3` was `+0.00004098` BPB worse and about `70s` faster on the older `EVAL_LOGIT_TEMP=0.95` line

Actual comparison obtained this round:
- required clean-idle gate versus observed pinned-GPU occupancy during the bounded prelaunch watch

## Hypothesis
On the exact promoted `EVAL_LOGIT_TEMP=1.0`, `NGRAM_EVAL_BUCKETS=2097152` legality line, reducing only `TTT_EPOCHS` from `4` to `3` would preserve `val_bpb` within `+0.00005` of the same-session control while saving meaningful wallclock under the current runtime regime.

Operational blocker falsifier for this round:
- if a clean-idle gate on pinned GPUs `0..7` cannot be obtained, the pair cannot be launched interpretabily and the round must stop as `no-launch / clean-idle-gate-fail`

## Why It Might Work
- The live `#1` snapshot line uses legal score-first TTT with `3` epochs, so this remains the cleanest matched evaluation-side SOTA motif left on the locked local stack.
- `eval_034` already showed `TTT_EPOCHS=3` is a real runtime lever on the older same-family line.
- `eval_042` re-established that the promoted stack is semantically stable and that current slowdown interpretation should be anchored to the current regime rather than to historical promoted runtime.
- This remains the smallest refinement-phase intervention: no architecture, optimization, export, or code-path changes.

## Minimal Intervention
No helper, checkpoint, artifact, runner, eval-hyperparameter, or export changes were made.

Intended semantic change:
- candidate `TTT_EPOCHS: 4 -> 3`

Actual executed changes:
- fresh operational identifiers for the intended control and candidate
- bounded clean-idle verification on pinned GPUs `0..7`
- on-disk recording of intended commands and gate evidence after the launch was blocked

## Variables To Change
Intended semantic change:
- candidate `TTT_EPOCHS: 4 -> 3`

Operational-only:
- fresh `RUN_ID`
- fresh runner `--log-dir`
- fresh runner `--run-name`
- synchronized telemetry capture if launch became admissible

Actual executed this round:
- clean-idle gate watch only

## Variables To Hold Fixed
- helper path `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`
- helper bytes/hash `125663 / 2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
- checkpoint path `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.pt`
- checkpoint bytes/hash `106178569 / b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- artifact path `runs/arch_010_record02_leakyrelu2_keep_cudnn_recipe/full_8gpu/final_model.int6.ptz`
- artifact bytes/hash `15555121 / eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- `EVAL_ONLY=1`
- `TTT_ENABLED=1`
- `EVAL_STRIDE=64`
- `EVAL_LOGIT_TEMP=1.0`
- `TTT_LR=0.0025`
- `TTT_CHUNK_TOKENS=32768`
- `TTT_FREEZE_BLOCKS=0`
- `TTT_MOMENTUM=0.9`
- `TTT_BATCH_SEQS=32`
- `TTT_GRAD_CLIP=1.0`
- `NGRAM_EVAL_ENABLED=1`
- `NGRAM_EVAL_BUCKETS=2097152`
- `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1`
- `NGRAM_EVAL_BATCH_TORCH_STATS=1`
- `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`
- tokenizer, dataset, cwd, `physicslm`
- pinned GPU set `0,1,2,3,4,5,6,7`
- launcher `tools/gpu_experiment_runner.py`

## Identity Checks
- Helper:
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
- helper unchanged before vs after the round
- checkpoint unchanged before vs after the round
- artifact unchanged before vs after the round

## Commands Actually Run
No runner-managed eval command was launched because the required clean-idle gate never passed.

The round executed a bounded prelaunch clean-idle watch on pinned GPUs `0..7`, recorded in:
- `runs/eval_044_eval038_ttt_epochs_pair_clean_idle_retry/clean_idle_gate.log`

The exact intended control and candidate commands were recorded, but not executed, in:
- `runs/eval_044_eval038_ttt_epochs_pair_clean_idle_retry/command.txt`

## Clean-Idle Gate Result
- gate status: `fail`
- bounded watch interval: `2026-03-27T12:43:36Z` through `2026-03-27T12:46:41Z`
- the pinned set was already dirty at the first sample and then ramped into a heavy 8-GPU workload during the watch
- first sample at `2026-03-27T12:43:36Z`:
  - GPU `0`: `78114 MiB` free, `2893 MiB` used, `100%` utilization
  - GPUs `1..7`: about `79492 MiB` free, `1515 MiB` used, `0%` utilization
  - compute-app snapshot already showed persistent foreign PIDs `3796173..3796180` across all 8 GPUs, each with process name `[Not Found]`
- by `2026-03-27T12:44:22Z`, the same PIDs had expanded to about `27766..37388 MiB` used across GPUs `0..7`
- final sample at `2026-03-27T12:46:25Z`:
  - GPU free memory ranged from `41902 MiB` to `42404 MiB`
  - GPU used memory ranged from `38596 MiB` to `39096 MiB`
  - GPU utilization ranged from `86%` to `100%`
  - the same PIDs `3796173..3796180` remained present on all 8 GPUs
- because the gate never passed:
  - synchronized telemetry was not started
  - no fresh `TTT_EPOCHS=4` control launched
  - no immediate `TTT_EPOCHS=3` candidate launched

## Success Metric
Primary success required:
- fresh same-session `TTT_EPOCHS=4` control launches on a valid clean-idle gate
- immediate `TTT_EPOCHS=3` candidate launches in the same session
- candidate finishes within `+0.00005 BPB` of the fresh control

Secondary success required:
- candidate saves at least `50s` external wallclock versus the fresh control

Actual status:
- clean-idle gate: `fail`
- fresh control launch: `not attempted`
- candidate launch: `not attempted`
- decision on `hold 4` vs `runtime-only 3` vs `promote 3`: `unanswered`

## Expected Effect
If the gate had passed, the exact same-session pair would have cleanly answered whether reducing only `TTT_EPOCHS` from `4` to `3` is a promotable runtime-quality trade on the current runtime regime.

## Actual Result
- The exact promoted-line epoch pair did not launch.
- The round stopped before telemetry start or runner launch because the pinned `0..7` clean-idle requirement stayed unsatisfied throughout the bounded watch.
- No new `val_loss`, `val_bpb`, script wallclock, runner wallclock, external wallclock, any-match, avg alpha, matched-order histogram, or `ngram_postlookup_vectorized_elapsed_ms` fields were produced.

## Interpretation
- Decision label: `no-launch / clean-idle-gate-fail`
- This round does not supersede `eval_042` and does not answer the promoted-line `TTT_EPOCHS=4 -> 3` question.
- Unlike `eval_043`, which was blocked by a single foreign `GPU 0` workload, this retry was blocked by a persistent 8-GPU foreign workload that expanded during the bounded watch.
- Under the reviewed refinement brief, forcing a dirty launch would have produced a non-interpretable pair, so the correct action was to stop.

## Next Step
Retry the exact same promoted-line same-session `TTT_EPOCHS=4 -> 3` pair when pinned GPUs `0..7` can be confirmed clean-idle. Keep the helper/checkpoint/artifact and all non-epoch variables fixed, and keep the decision baseline anchored to the fresh same-session `TTT_EPOCHS=4` control rather than to the historical `eval_038` runtime band.
