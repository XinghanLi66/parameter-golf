# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase same-session promoted-line `TTT_EPOCHS=4 -> 3` evaluation retry with the required single continuous clean-idle watch, but the round still stopped short of a valid pair because post-gate GPU contamination blocked the immediate candidate launch after an admissible fresh control.

- Executed the reviewed brief through the required file re-read, exact promoted-command recovery, helper/checkpoint/artifact identity verification, one uninterrupted clean-idle acquisition window, synchronized telemetry capture, and the fresh `TTT_EPOCHS=4` control launch.
- No code edits were made in this round.
- The clean-idle gate passed within the continuous watch.
- The fresh control launched and finished admissibly.
- The immediate `TTT_EPOCHS=3` candidate did not launch because the pinned set was no longer clean at candidate launch time.
- The round therefore remains an invalid same-session pair rather than an epoch-count decision.

## Experiment ID
`eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch`

## Category
- evaluation

Operational subtype: `same-session promoted-line epoch-pair continuous clean-idle watch`

## Baseline / Comparison
Intended primary comparison:
- fresh same-session control on the exact promoted line with `TTT_EPOCHS=4`
- immediate same-session candidate on the exact promoted line with only `TTT_EPOCHS=3`

Interpretation anchors:
- promoted `eval_038=0.19974237`, script `588813ms`, runner `634685ms`, external `634926ms`
- current-regime clean-idle control `eval_042=0.19974395`, script `1507653ms`, runner `1555810ms`, external `1556076ms`
- older same-family result `eval_034`: `TTT_EPOCHS=3` was `+0.00004098` BPB worse and about `70s` faster on the older `EVAL_LOGIT_TEMP=0.95` line

Actual comparison obtained this round:
- required clean-idle gate versus observed pinned-GPU occupancy during the continuous prelaunch watch
- fresh admissible `TTT_EPOCHS=4` control versus the exact promoted-line control family
- immediate candidate launch admissibility versus actual post-control pinned-GPU state

## Hypothesis
On the exact promoted `EVAL_LOGIT_TEMP=1.0`, `NGRAM_EVAL_BUCKETS=2097152` legality line, reducing only `TTT_EPOCHS` from `4` to `3` would preserve `val_bpb` within `+0.00005` of the same-session control while saving meaningful wallclock under the current runtime regime.

Operational blocker falsifier for this round:
- if a clean-idle gate on pinned GPUs `0..7` cannot be obtained, or if post-gate contamination prevents the immediate candidate launch, the pair cannot be launched interpretably and the round must stop as an invalid comparison

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
- fresh operational identifiers for the control and candidate
- one continuous clean-idle verification window on pinned GPUs `0..7`
- synchronized runtime telemetry during the control and candidate handoff
- fresh same-session control launch at `TTT_EPOCHS=4`
- immediate candidate launch attempt at `TTT_EPOCHS=3`, blocked before child spawn

## Variables To Change
Intended semantic change:
- candidate `TTT_EPOCHS: 4 -> 3`

Operational-only:
- fresh `RUN_ID`
- fresh runner `--log-dir`
- fresh runner `--run-name`
- one uninterrupted clean-idle acquisition window
- synchronized telemetry capture across the admissible control and attempted candidate handoff

Actual executed this round:
- continuous clean-idle gate watch
- fresh control with `TTT_EPOCHS=4`
- immediate candidate launch attempt with `TTT_EPOCHS=3`, blocked prelaunch

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
The round executed the required single continuous prelaunch clean-idle watch on pinned GPUs `0..7`, recorded in:
- `runs/eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch/clean_idle_gate.log`

The exact intended control and candidate commands were recorded in:
- `runs/eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch/command.txt`

The fresh control command was actually launched and completed via:
- `tools/gpu_experiment_runner.py` in `physicslm` on pinned GPUs `0,1,2,3,4,5,6,7`
- runner log dir `runs/eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch/runner_control_8gpu/`

The immediate candidate command was attempted via the same runner path and pinned GPU set, but it failed prelaunch GPU selection before child spawn because only 7 GPUs met the free-memory gate.

## Clean-Idle Gate Result
- gate status: `pass`
- continuous watch interval: `2026-03-27T12:58:42Z` through gate pass at `2026-03-27T13:05:27Z`
- the pinned set began dirty only on GPU `0`, with foreign `PID 3922791` using `74486 MiB` and leaving `6512 MiB` free while GPUs `1..7` stayed idle
- samples `0..25` kept that same single-GPU blocker pattern with GPUs `1..7` clean
- sample `26` at `2026-03-27T13:05:27Z` showed all eight GPUs back to about `81007 MiB` free, `0 MiB` used, `0%` utilization, and no compute-app entries
- because the gate passed:
  - synchronized telemetry was started
  - the fresh `TTT_EPOCHS=4` control launched immediately

## Control Result
- control admissibility: `pass`
- exact result:
  - `legal_ttt_exact val_loss=0.33725577`
  - `legal_ttt_exact val_bpb=0.19974186`
  - script eval wallclock `1306008ms`
  - runner-managed wallclock `1350527ms`
  - external wallclock `1350805ms`
  - `runner_start_to_child_spawn_ms=372`
  - `child_runtime_ms=1350155`
- telemetry family check versus `eval_042` / `eval_038`:
  - any-match `0.98387585`, exactly unchanged
  - matched-order histogram exactly unchanged
  - avg alpha `0.65460155`, still in-family
  - `ngram_postlookup_vectorized_elapsed_ms=1484092`
- comparison versus `eval_042` clean-idle control:
  - `val_loss -0.00000352`
  - `val_bpb -0.00000209`
  - script `-201645ms`
  - runner `-205283ms`
  - external `-205271ms`
- comparison versus promoted `eval_038`:
  - `val_loss -0.00000086`
  - `val_bpb -0.00000051`
  - script `+717195ms`
  - runner `+715842ms`
  - external `+715879ms`

## Candidate Launch Result
- candidate launch status: `blocked before child spawn`
- attempted launch time: `2026-03-27T13:29:49Z`
- runner failure:
  - `Requested 8 GPU(s), but only found 7 meeting the requirement of 10.0 GiB free memory.`
- candidate metadata showed:
  - GPU `0`: `6512 MiB` free, `74495 MiB` used, `100%` utilization
  - GPUs `1..7`: about `81007 MiB` free, `0 MiB` used, `0%` utilization
- synchronized telemetry around the handoff showed post-gate contamination on GPU `0`:
  - `2026-03-27T13:28:32Z` and `13:28:52Z`: expected control PID plus foreign `PID 4112518` on GPU `0`
  - `2026-03-27T13:29:13Z` onward: only foreign `PID 4112518` remained on GPU `0` using `74486 MiB`, while GPUs `1..7` were idle
- because the immediate candidate never launched:
  - no candidate `val_loss`
  - no candidate `val_bpb`
  - no candidate script / runner / external wallclock
  - no candidate any-match / avg alpha / matched-order histogram / postlookup timing

## Success Metric
Primary success required:
- fresh same-session `TTT_EPOCHS=4` control launches on a valid clean-idle gate
- immediate `TTT_EPOCHS=3` candidate launches in the same session
- candidate finishes within `+0.00005 BPB` of the fresh control

Secondary success required:
- candidate saves at least `50s` external wallclock versus the fresh control

Actual status:
- clean-idle gate: `pass`
- fresh control launch: `completed and admissible`
- candidate launch: `attempted but blocked before child spawn`
- decision on `hold 4` vs `runtime-only 3` vs `promote 3`: `unanswered`

## Expected Effect
If the gate and immediate handoff had both remained clean, the exact same-session pair would have cleanly answered whether reducing only `TTT_EPOCHS` from `4` to `3` is a promotable runtime-quality trade on the current runtime regime.

## Actual Result
- The continuous clean-idle watch passed and the fresh exact promoted-line control completed successfully.
- The control stayed semantically in-family and was materially faster than `eval_042`, so the control admissibility requirement passed.
- The immediate candidate did not launch because post-gate contamination reoccupied GPU `0` before candidate launch, leaving only 7 eligible GPUs for the runner gate.
- The round therefore produced a valid fresh control but not a valid same-session epoch pair.

## Interpretation
- Decision label: `post-gate contamination / invalid same-session pair`
- This round supersedes the earlier bounded-watch blocker reports by showing that the single continuous watch requirement can pass and that the fresh control remains admissible.
- It still does not answer the promoted-line `TTT_EPOCHS=4 -> 3` question, because the immediate candidate never launched.
- The key new evidence is operational: the pinned set can clear long enough for a valid control, but a foreign `GPU 0` workload can reappear before the candidate handoff, invalidating the pair.
- Under the reviewed refinement brief, retrying the candidate after this failed handoff would have forced an invalid comparison, so the correct action was to stop.

## Next Step
Retry the exact same promoted-line same-session `TTT_EPOCHS=4 -> 3` pair again when pinned GPUs `0..7` can remain clean not only through the continuous prelaunch gate but also through the immediate post-control candidate handoff. Keep the helper/checkpoint/artifact and all non-epoch variables fixed, reuse the fresh-control admissibility criteria established here, and do not infer `hold 4` / `runtime-only 3` / `promote 3` from this invalidated pair.
