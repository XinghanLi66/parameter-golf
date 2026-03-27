# Research Memory

This file is the compact scientific memory for the project. Keep it updated so the planner can avoid redundant work.

## Working SOTA Anchor - 2026-03-27

**TARGET SOTA: PR #803 at `0.4416 BPB`** - Complementary Training + Backoff N-gram + TTT.  
PR `#809` at `0.2952` remains legality-pending and is not the official target.

This line is in **REFINEMENT phase**:
- strongest measured local run: `eval_015=0.19974202`
- promoted quality baseline on the locked legality line is now `eval_038 candidate=0.19974237` with `EVAL_LOGIT_TEMP=1.0`
- freshest admissible same-session control on the promoted line: `eval_045 control=0.19974186`
- newest refinement round: `eval_047 patched-helper 7-GPU control -> surrogate admissible`
- previous promoted line before the temperature fix: `eval_035=0.20079980`
- previous fresh admissible prior control on the old promoted line: `eval_036 control=0.20079853`
- previous legality baseline: `eval_027=0.29117839`
- newest completed exact promoted-line control on the validated surrogate path: `eval_047=0.19974198` with script `616325ms`, runner `662808ms`, external `663.092s`
- official-anchor gap on the active legality line: `0.19974237 - 0.4416 = -0.24185763`
- open problem: promoted-line scorer temperature is closed positively on this helper lineage, and the only unanswered nearby refinement question is now again the exact promoted-line `TTT_EPOCHS=4 -> 3` pair. `eval_047` shows that the patched `1..7` eval-only path is a valid surrogate regime, so the next round should keep `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152` fixed and run the same-session `4 -> 3` pair on that patched helper path.

`context/reference_materials/URGENT_ngram_backoff_breakthrough.md` remains authoritative for the n-gram mechanism family.  
`context/reference_materials/latest_sota_snapshot.md` remains authoritative for the official comparison target.

## Newest Critical Result - `eval_047_eval045_patched_helper_7gpu_control`

- The reviewed refinement-phase eval-only launch-path compatibility and surrogate-validity check completed successfully: the copied helper was patched only on the eval-only non-divisor startup path, the fresh 7-GPU control on GPUs `1..7` launched and finished, and the result stayed semantically in-family with the fresh 8-GPU control `eval_045`.
- The code change was structurally minimal and stayed inside the reviewed lane:
  - copied `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py` into `runs/eval_047_eval045_patched_helper_7gpu_control/train_gpt.py`
  - preserved the original `WORLD_SIZE` divisor invariant for all training and non-eval launches
  - allowed only `EVAL_ONLY=1` plus non-divisor `WORLD_SIZE` to fall back to `grad_accum_steps=1`
  - added one explicit compatibility log line
  - left scorer math, TTT logic, cache logic, export logic, checkpoint bytes, artifact bytes, and runner code unchanged
- Identity state before launch:
  - patched helper `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - locked source helper `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint unchanged at `106178569` bytes / `b8291ad1...`
  - artifact unchanged at `15555121` bytes / `eb062c96...`
- 7-GPU clean-idle gate evidence:
  - gate sample at `2026-03-27T14:12:53Z`
  - GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - GPU `0` remained occupied by a foreign process at about `74486 MiB`, but it was outside the reviewed gate set
- Fresh patched-helper control result:
  - runner launch start `2026-03-27T14:13:16Z`
  - runner end `2026-03-27T14:24:19Z`
  - compatibility log emitted: `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
  - `legal_ttt_exact val_loss=0.33725596`
  - `legal_ttt_exact val_bpb=0.19974198`
  - script eval wallclock `616325ms`
  - runner-managed wallclock `662808ms`
  - external wallclock `663.092s`
  - `runner_start_to_child_spawn_ms=428`
  - `child_runtime_ms=662380`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461744`
  - matched-order histogram identical to `eval_045` and `eval_038`
  - `ngram_postlookup_vectorized_elapsed_ms=1110166`
- Required admissibility comparisons:
  - versus `eval_045`, BPB was `+0.00000012`, any-match was identical, histogram was identical, avg alpha was `+0.00001589`, script was `-689683ms`, runner was `-687719ms`, external was `-687713ms`, and postlookup was `-373926ms`
  - versus promoted `eval_038`, BPB was `-0.00000039`, any-match was identical, histogram was identical, avg alpha was `+0.00001833`, script was `+27512ms`, runner was `+28123ms`, external was `+28166ms`, and postlookup was `-52017ms`
- Decision label: `7-GPU surrogate admissible`.
- Interpretation: `eval_046` was blocked by a helper startup invariant, not by a semantic mismatch on the `1..7` subset. The patched eval-only 7-GPU path is now validated as an admissible surrogate regime for the promoted 8-GPU control, so the exact `TTT_EPOCHS=4 -> 3` comparison is scientifically reopened on that path.

## Previous Critical Result - `eval_046_eval045_ttt_epochs_pair_7gpu_subset`

- The reviewed refinement-phase exact promoted-line same-session `TTT_EPOCHS=4 -> 3` retry on the fixed `1..7` subset did not reach a surrogate-regime control because the locked helper rejects `WORLD_SIZE=7` before any evaluation work begins.
- No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The round stayed exactly inside the reviewed single-variable lane up to the operational stop:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, and the required `eval_045` command/gate artifacts before any action
  - re-verified helper, checkpoint, and artifact identities
  - recovered the exact intended same-session command family from `eval_045`
  - changed no helper code, no checkpoint, no artifact, no runner code, no export path, and no evaluation hyperparameters
  - changed only the reviewed operational launch subset to `1,2,3,4,5,6,7`, the runner request count to `7`, and the intended candidate-only semantic change `TTT_EPOCHS=4 -> 3`
- 7-GPU clean-idle gate evidence:
  - gate sample at `2026-03-27T13:56:56Z`
  - GPUs `1..7` each showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - GPU `0` remained occupied by a foreign process at about `74486 MiB`, which was acceptable because the reviewed gate set was only `1..7`
- Fresh 7-GPU control launch result:
  - runner launch start `2026-03-27T13:57:15Z`
  - runner selected GPUs `1,2,3,4,5,6,7` successfully
  - `torchrun --standalone --nproc_per_node=7` then failed before evaluation with `ValueError: WORLD_SIZE=7 must divide 8 so grad_accum_steps stays integral`
  - runner metadata recorded external wallclock `34.181s`, runner total `33914ms`, `runner_start_to_child_spawn_ms=424`, `child_runtime_ms=33489`, and exit code `1`
  - torchrun surfaced `ChildFailedError`, with the first observed root-cause failure at rank `5`
- Because the control never reached an admissible surrogate-regime result:
  - no control `val_loss`
  - no control `val_bpb`
  - no control scorer telemetry
  - no candidate launch
- Commands, gate evidence, and runner logs were recorded in `runs/eval_046_eval045_ttt_epochs_pair_7gpu_subset/`.
- Decision label: `operationally blocked`.
- Interpretation: this round narrows the blocker beyond GPU cleanliness. The `1..7` subset itself is usable, but the locked helper cannot execute a true 7-process launch under the reviewed no-code-change rules, so the 7-GPU surrogate regime is not currently a valid path to answering the epoch-count question.

## Previous Critical Result - `eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch`

- The reviewed refinement-phase exact promoted-line same-session `TTT_EPOCHS=4 -> 3` retry advanced farther than `eval_043` / `eval_044`: the required continuous clean-idle gate passed, the fresh exact control completed admissibly, but the immediate `TTT_EPOCHS=3` candidate was invalidated by post-gate contamination on pinned GPU `0` before child spawn.
- No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The round stayed exactly inside the reviewed single-variable lane:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, the active helper, and the required `eval_042` / `eval_044` logs before any action
  - re-verified helper, checkpoint, and artifact identities
  - recovered the exact intended same-session control and candidate command family from `eval_042` and `eval_044`
  - changed no helper code, no checkpoint, no artifact, no runner code, no export path, and no evaluation hyperparameters
  - changed only fresh operational identifiers, one uninterrupted continuous clean-idle watch, synchronized telemetry, and the intended candidate-only semantic change `TTT_EPOCHS=4 -> 3`
- Continuous clean-idle gate evidence:
  - uninterrupted watch from `2026-03-27T12:58:42Z` through gate pass at `2026-03-27T13:05:27Z`
  - samples `0..25` showed GPU `0` occupied by foreign PID `3922791` at about `74486 MiB` while GPUs `1..7` were idle
  - sample `26` at `2026-03-27T13:05:27Z` showed all eight pinned GPUs clean with about `81007 MiB` free, `0 MiB` used, `0%` utilization, and no compute-app processes
- Fresh exact control result:
  - `legal_ttt_exact val_loss=0.33725577`
  - `legal_ttt_exact val_bpb=0.19974186`
  - script eval wallclock `1306008ms`
  - runner-managed wallclock `1350527ms`
  - external wallclock `1350805ms`
  - `runner_start_to_child_spawn_ms=372`
  - `child_runtime_ms=1350155`
  - any-match fraction `0.98387585`
  - avg alpha `0.65460155`
  - matched-order histogram identical to promoted `eval_038` and fresh `eval_042`
  - `ngram_postlookup_vectorized_elapsed_ms=1484092`
- Control admissibility result:
  - versus `eval_042`, BPB was `-0.00000209` with the same any-match fraction and the exact same matched-order histogram
  - versus promoted `eval_038`, BPB was `-0.00000051`, any-match was identical, histogram was identical, and avg alpha stayed in-family
  - therefore the fresh control passed the reviewed semantic admissibility gate
- Immediate candidate failure mode:
  - the immediate `TTT_EPOCHS=3` runner launch was attempted at `2026-03-27T13:29:49Z`, but the runner found only `7` GPUs meeting the `>=10 GiB free` requirement
  - GPU `0` had only `6512 MiB` free, `74495 MiB` used, and `100%` utilization
  - synchronized telemetry showed foreign PID `4112518` appear on GPU `0` during the late control tail, coexist briefly with the expected control PID, and then remain alone on GPU `0` through the candidate attempt while GPUs `1..7` stayed idle
  - because the candidate never reached child spawn, no candidate `val_loss`, `val_bpb`, wallclock, any-match, avg alpha, histogram, or postlookup timing fields exist for this round
- Commands, gate evidence, telemetry, and runner logs were recorded in `runs/eval_045_eval038_ttt_epochs_pair_clean_idle_continuous_watch/`.
- Decision label: `post-gate contamination / invalid same-session pair`.
- Interpretation: the new evidence is valuable even though the scientific pair is still unanswered. The longer continuous watch removed the previous prelaunch admissibility blocker and yielded a fresh admissible promoted-line control, so the remaining blocker has narrowed to keeping pinned GPUs clean through the immediate candidate handoff rather than merely obtaining one clean launch.

## Previous Critical Result - `eval_044_eval038_ttt_epochs_pair_clean_idle_retry`

- The reviewed refinement-phase exact promoted-line same-session `TTT_EPOCHS=4 -> 3` retry did not launch because the required clean-idle gate on pinned GPUs `0..7` never passed.
- No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The round stayed exactly inside the reviewed single-variable lane up to the stop:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, the active helper, and the required `eval_042` logs before any action
  - re-verified helper, checkpoint, and artifact identities
  - recovered the exact intended same-session control and candidate command family from `eval_042` and `eval_043`
  - changed no helper code, no checkpoint, no artifact, no runner code, no export path, and no evaluation hyperparameters
  - prepared only fresh operational identifiers plus the intended candidate-only semantic change `TTT_EPOCHS=4 -> 3`, but intentionally did not launch after the gate failed
- Clean-idle gate evidence:
  - repeated UTC samples from `2026-03-27T12:43:36Z` through `2026-03-27T12:46:41Z`
  - the watch started with persistent foreign compute-app PIDs `3796173..3796180` already present across all eight pinned GPUs, initially using `2884 MiB` on GPU `0` and `1506 MiB` on GPUs `1..7`
  - by `2026-03-27T12:44:22Z`, the same PIDs had expanded to about `27766..37388 MiB` used across GPUs `0..7`
  - by the final sample at `2026-03-27T12:46:25Z`, all eight GPUs were still occupied with about `38596..39096 MiB` used, `41902..42404 MiB` free, and `86..100%` utilization
  - compute-app snapshots stayed `[Not Found]` for all eight PIDs throughout the watch
- Because the gate never passed:
  - no synchronized telemetry loop was started
  - no runner-managed fresh `TTT_EPOCHS=4` control was started
  - no immediate `TTT_EPOCHS=3` candidate was started
  - no new `val_loss`, `val_bpb`, script wallclock, runner wallclock, external wallclock, `runner_start_to_child_spawn_ms`, `child_runtime_ms`, any-match, avg alpha, matched-order histogram, or postlookup timing fields exist for this round
- Intended commands and blocker evidence were recorded in `runs/eval_044_eval038_ttt_epochs_pair_clean_idle_retry/`.
- Decision label: `no-launch / clean-idle-gate-fail`.
- Interpretation: this round does not answer the promoted-line epoch-count question and does not supersede `eval_042`. The new evidence is that the blocker can appear as a persistent foreign 8-GPU workload rather than only the single-GPU occupancy seen in `eval_043`, so the correct next action remains a clean-idle retry rather than a dirty launch.

## Previous Critical Result - `eval_043_eval038_ttt_epochs_pair_clean_idle_blocked`

- The reviewed refinement-phase exact promoted-line same-session `TTT_EPOCHS=4 -> 3` pair did not launch because the required clean-idle gate on pinned GPUs `0..7` never passed.
- No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The round stayed exactly inside the reviewed single-variable lane up to the stop:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, the active helper, and the required `eval_042` logs before any action
  - re-verified helper, checkpoint, and artifact identities
  - recovered the exact intended same-session control and candidate command family from `eval_042`
  - changed no helper code, no checkpoint, no artifact, no runner code, no export path, and no evaluation hyperparameters
  - prepared only fresh operational identifiers plus the intended candidate-only semantic change `TTT_EPOCHS=4 -> 3`, but intentionally did not launch after the gate failed
- Clean-idle gate evidence:
  - repeated UTC samples from `2026-03-27T12:27:56Z` through `2026-03-27T12:30:45Z`
  - GPU `0` remained occupied throughout with `6512 MiB` free, `74495 MiB` used, and `100%` utilization
  - compute-app snapshots showed `GPU-d45bfedb-df91-05be-293c-7375698e87dd, PID 3676150, process_name=[Not Found], used_memory=74486 MiB`
  - GPUs `1..7` stayed idle with about `81007 MiB` free and `0%` utilization
- Because the gate never passed:
  - no synchronized telemetry loop was started
  - no runner-managed fresh `TTT_EPOCHS=4` control was started
  - no immediate `TTT_EPOCHS=3` candidate was started
  - no new `val_loss`, `val_bpb`, script wallclock, runner wallclock, external wallclock, `runner_start_to_child_spawn_ms`, `child_runtime_ms`, any-match, avg alpha, matched-order histogram, or postlookup timing fields exist for this round
- Intended commands and blocker evidence were recorded in `runs/eval_043_eval038_ttt_epochs_pair_clean_idle_blocked/`.
- Decision label: `no-launch / clean-idle-gate-fail`.
- Interpretation: this round does not answer the promoted-line epoch-count question and does not supersede `eval_042`. The only new evidence is that external occupancy on pinned GPU `0` again prevented an interpretable same-session pair, so the correct next action is a clean-idle retry rather than a dirty launch.

## Previous Critical Result - `eval_042_eval038_clean_idle_telemetry_control`

- The reviewed refinement-phase clean-idle runtime-diagnosis control on the promoted `eval_038` legality line completed with a valid clean-idle launch and full telemetry.
- No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The round stayed exactly inside the reviewed control-only lane:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, and the active helper before any action
  - re-verified helper, checkpoint, and artifact identities
  - recovered the exact promoted `eval_038` runner command family from on-disk metadata
  - changed no helper code, no checkpoint, no artifact, no runner code, no export path, and no evaluation hyperparameters
  - changed only clean-idle acquisition, synchronized telemetry capture, and fresh operational identifiers
- Clean-idle gate evidence:
  - the declared clean-idle acquisition protocol was honored and passed on the first required sample at `2026-03-27T11:40:19Z`
  - GPUs `0..7` all showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - `nvidia-smi --query-compute-apps` returned no foreign compute processes at gate pass
- The exact promoted-line runner command then launched and finished:
  - `legal_ttt_exact val_loss=0.33725929`
  - `legal_ttt_exact val_bpb=0.19974395`
  - script eval wallclock `1507653ms`
  - runner-managed wallclock `1555810ms`
  - external wallclock `1556076ms`
  - `runner_start_to_child_spawn_ms=479`
  - `child_runtime_ms=1555330`
- Required comparisons versus promoted `eval_038`:
  - `+0.00000266 val_loss`
  - `+0.00000158 BPB`
  - `+918840ms` script
  - `+921125ms` runner
  - `+921150ms` external
- Emitted telemetry stayed semantically identical to the promoted line:
  - any-match fraction `0.98387585`
  - avg alpha `0.65459237`
  - matched-order histogram identical to promoted `eval_038`
- Runtime-localization telemetry:
  - no meaningful launch-side stall; clean-launch `runner_start_to_child_spawn_ms` was only `479ms`
  - the child runtime itself remained catastrophically slow
  - `ngram_postlookup_vectorized_elapsed_ms=1540712`, which is `+378529ms` vs promoted `eval_038`
  - a late extra foreign PID `3384110` appeared on GPU `0`, but only after the run had already fallen far behind promoted pace
- Decision label: `clean-launch persistent-runtime-shift / child-runtime-inflation`.
- Interpretation: the clean-idle protocol gap from `eval_041` is now closed. The promoted helper/checkpoint/artifact stack remains semantically stable, the slowdown is not primarily launch-side, and the dominant current-environment shift sits inside child execution. The dedicated `TTT_EPOCHS=4 -> 3` pair is now admissible again as a same-session current-regime comparison.

## Previous Critical Result - `eval_041_eval038_clean_idle_telemetry_control`

- The reviewed refinement-phase clean-idle runtime-diagnosis attempt on the promoted `eval_038` legality line did not launch because the required prelaunch gate on pinned GPUs `0,1,2,3,4,5,6,7` never passed.
- No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The round stayed exactly inside the reviewed control-only lane up to the stop:
  - re-read `context/reference_materials/latest_sota_snapshot.md`, `planning/next_experiment.md`, `planning/research_memory.md`, `planning/experiment_ledger.md`, `reports/latest_status.md`, `reports/comparison_summary.md`, and the active helper before any action
  - re-verified helper, checkpoint, and artifact identities
  - recovered the exact promoted `eval_038` runner command family from on-disk metadata
  - changed no helper code, no checkpoint, no artifact, no runner code, no export path, and no evaluation hyperparameters
  - prepared the exact promoted-line control command with only allowed operational identifier changes, but intentionally did not launch it after the gate failed
- Clean-idle gate evidence:
  - repeated UTC samples from `2026-03-27T11:23:11Z` through `2026-03-27T11:25:26Z`
  - GPU `0` remained occupied throughout with `6512 MiB` free, `74495 MiB` used, and `100%` utilization
  - compute-app snapshots showed `GPU-d45bfedb-df91-05be-293c-7375698e87dd, PID 3106138, process_name=[Not Found], used_memory=74486 MiB`
  - GPUs `1..7` stayed idle with about `81007 MiB` free and `0%` utilization
- Because the gate never passed:
  - no synchronized launch/execution/teardown telemetry loop was started
  - no runner-managed eval process was started
  - no new `val_loss`, `val_bpb`, script wallclock, runner wallclock, external wallclock, `runner_start_to_child_spawn_ms`, or `child_runtime_ms` fields exist for this round
- Decision label: `no-launch / clean-idle-gate-fail`.
- Interpretation: this round did not supersede the existing `persistent-runtime-shift` evidence from `eval_040`; it only recorded that the exact clean-idle diagnostic control was still pending because the required pinned GPU set was externally occupied.

## Previous Critical Result - `eval_040_eval038_duplicate_control`
- The reviewed refinement-phase duplicate-control reproducibility check completed as written with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed control-only lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=1.0` fixed
  - kept `TTT_LR=0.0025` fixed
  - kept `TTT_EPOCHS=4` fixed
  - launched `control A` and `control B` with only allowed operational identifier changes
- Successful same-session controls on the pinned `0,1,2,3,4,5,6,7` GPU set scored:
  - control A: `legal_ttt_exact val_loss=0.33725588`, `val_bpb=0.19974193`, script `1316129ms`, runner `1364893ms`, external `1365195ms`, any-match `0.98387585`, avg alpha `0.65459876`
  - control B: `legal_ttt_exact val_loss=0.33725882`, `val_bpb=0.19974367`, script `1249634ms`, runner `1298509ms`, external `1298755ms`, any-match `0.98387585`, avg alpha `0.65459430`
- Required comparisons versus promoted `eval_038`:
  - control A: `-0.00000075 val_loss`, `-0.00000044 BPB`, `+727316ms` script, `+730208ms` runner, `+730269ms` external, `-0.00000035` avg alpha
  - control B: `+0.00000219 val_loss`, `+0.00000130 BPB`, `+660821ms` script, `+663824ms` runner, `+663829ms` external, `-0.00000481` avg alpha
- Required comparisons versus drifted `eval_039`:
  - control A: `+0.00000053 val_loss`, `+0.00000032 BPB`, `+125652ms` script, `+127623ms` runner, `+127701ms` external
  - control B: `+0.00000347 val_loss`, `+0.00000206 BPB`, `+59157ms` script, `+61239ms` runner, `+61261ms` external
- Control B vs Control A:
  - `+0.00000294 val_loss`
  - `+0.00000174 BPB`
  - `-66495ms` script
  - `-66384ms` runner
  - `-66440ms` external
- Emitted telemetry stayed semantically identical to promoted `eval_038`:
  - identical any-match fraction
  - identical matched-order histogram
  - avg alpha stayed within a few parts per million
- Operational note:
  - a root-owned external `run_humaneval.py` / `VLLM::EngineCore` workload overlapped GPU `0` during `control A`
  - `control B` was launched only after that workload cleared and still remained deep in the slowdown regime
- Decision label: `persistent-runtime-shift`.
- Interpretation: this is no longer just a one-control drift stop. The exact promoted helper/checkpoint/artifact stack still reproduces semantics, but two same-session exact controls do not return to the promoted runtime band. There is within-shift jitter, but the round-level answer is that the promoted runtime regime is not presently reproducible, so `TTT_EPOCHS=4 -> 3` remains inadmissible.

## Previous Critical Result - `eval_039_eval038_ttt_epochs_pair`

- The reviewed refinement-phase epoch-count check on the promoted `eval_038` legality line stopped after the fresh control because the admissibility gate failed on runtime. No code edits were made. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the round at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane up to the stop:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=1.0` fixed
  - kept `TTT_LR=0.0025` fixed
  - kept `TTT_EPOCHS=4` fixed in the actual executed control
  - planned but did not launch the immediate `TTT_EPOCHS=3` candidate after the fresh-control gate failed
- The fresh runner-managed control in `physicslm` on the pinned `0,1,2,3,4,5,6,7` GPU set scored:
  - `legal_ttt_exact val_loss=0.33725535`
  - `legal_ttt_exact val_bpb=0.19974161`
  - script eval wallclock `1190477ms`
  - runner-managed wallclock `1237270ms`
  - external top-level wallclock `1237494ms`
  - any-match fraction `0.98387585`
  - avg alpha on matched `0.65459666`
- Required admissibility comparison versus promoted `eval_038`:
  - `val_loss`: `0.33725663 -> 0.33725535` (`-0.00000128`)
  - `val_bpb`: `0.19974237 -> 0.19974161` (`-0.00000076`)
  - script eval wallclock: `588813ms -> 1190477ms` (`+601664ms`)
  - runner-managed wallclock: `634685ms -> 1237270ms` (`+602585ms`)
  - external top-level wallclock: `634926ms -> 1237494ms` (`+602568ms`)
  - avg alpha on matched: `0.65459911 -> 0.65459666` (`-0.00000245`)
- Emitted telemetry stayed semantically identical to the promoted line:
  - identical any-match fraction
  - identical matched-order histogram
  - essentially identical avg alpha
- Decision label: `drift-stop`.
- Interpretation: this is not evidence for or against `TTT_EPOCHS=3` on the promoted `EVAL_LOGIT_TEMP=1.0` line. The control reproduced the same quality regime but not the same runtime regime, so the reviewed same-session comparison became inadmissible before the candidate could be launched.

## Previous Critical Result - `eval_038_eval035_temperature_pair`

- The reviewed refinement-phase promoted-line temperature pair executed cleanly as a same-session two-arm comparison with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `TTT_LR=0.0025` fixed
  - kept `TTT_EPOCHS=4` fixed
  - kept `NGRAM_EVAL_BUCKETS=2097152` fixed
  - changed only `EVAL_LOGIT_TEMP` between fresh control `0.95` and immediate candidate `1.0`
- The fresh runner-managed control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.33904065`
  - `legal_ttt_exact val_bpb=0.20079897`
  - script eval wallclock `585778ms`
  - runner-managed wallclock `631265ms`
  - external top-level wallclock `631449ms`
- The fresh runner-managed candidate with only `EVAL_LOGIT_TEMP=1.0` scored:
  - `legal_ttt_exact val_loss=0.33725663`
  - `legal_ttt_exact val_bpb=0.19974237`
  - script eval wallclock `588813ms`
  - runner-managed wallclock `634685ms`
  - external top-level wallclock `634926ms`
- Required comparisons:
  - control vs promoted `eval_035`: `-0.00000083 BPB`, `+3506ms` script, `+6252ms` runner-managed, `+6272ms` external
  - control vs fresh `eval_036` control: `+0.00000044 BPB`, `+3766ms` script, `+5218ms` runner-managed, `+5402ms` external
  - candidate vs fresh control: `-0.00105660 BPB`, `+3035ms` script, `+3420ms` runner-managed, `+3477ms` external
  - candidate vs historical `eval_015`: `+0.00000035 BPB`
- Emitted telemetry stayed in-family with the promoted line:
  - any-match fraction `0.98387585 -> 0.98387585`
  - avg alpha on matched `0.63990741 -> 0.65459911`
  - order histogram identical to the promoted `2097152`-bucket pattern
- Decision label: `promote`.
- Interpretation: the promoted `2097152`-bucket legality line was indeed over-sharpened at `EVAL_LOGIT_TEMP=0.95`, and restoring `EVAL_LOGIT_TEMP=1.0` produces a large same-session gain while keeping runtime well inside the reviewed `+15s` band. Historical external drift versus `eval_035` did not recur materially in the fresh control rerun, so the earlier `eval_037` stop should be treated as stale context rather than the final answer to this temperature question.

## Previous Critical Result - `eval_036_eval035_ttt_lr_pair`

- The reviewed refinement-phase TTT-learning-rate pair executed cleanly on the promoted `eval_035` legality lineage with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - kept `NGRAM_EVAL_BUCKETS=2097152` fixed
  - changed only `TTT_LR` between `0.0025` and `0.0020`
  - changed only operational identifiers such as `RUN_ID`, runner log dir, and runner run name
- The fresh runner-managed control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.33903990`
  - `legal_ttt_exact val_bpb=0.20079853`
  - script eval wallclock `582012ms`
  - runner-managed wallclock `626047ms`
  - external top-level wallclock `626047ms` via runner-total proxy, with metadata UTC timestamps independently implying about `626000ms`
- The fresh control passed the reviewed admissibility gate versus promoted `eval_035`:
  - `val_bpb` drift `-0.00000127`
  - external wallclock drift `+870ms`
- The fresh runner-managed candidate with `TTT_LR=0.0020` scored:
  - `legal_ttt_exact val_loss=0.33907413`
  - `legal_ttt_exact val_bpb=0.20081880`
  - script eval wallclock `591247ms`
  - runner-managed wallclock `633936ms`
  - external top-level wallclock `634143ms`
- Required comparisons:
  - candidate vs fresh control: `+0.00002027 BPB`, `+9235ms` script, `+7889ms` runner-managed, `+8096ms` external
  - control vs promoted `eval_035`: `-0.00000127 BPB`, `-260ms` script, `+1034ms` runner-managed, `+870ms` external
  - candidate vs historical `eval_015`: `+0.00107678 BPB`
- Emitted telemetry stayed essentially flat across the pair:
  - any-match fraction `0.98387585 -> 0.98387585`
  - avg alpha on matched `0.63990797 -> 0.63995303`
- Decision label: `hold`.
- Interpretation: the promoted `2097152`-bucket legality line still prefers `TTT_LR=0.0025`. Downward TTT-LR retuning is now closed negatively on this helper lineage unless a future round changes the operating point materially.

## Previous Critical Result - `eval_035_eval031_bucket_geometry_pair`

- The reviewed refinement-phase bucket-geometry pair executed cleanly on the locked promoted `eval_031` legality lineage at `EVAL_LOGIT_TEMP=0.95` with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only `NGRAM_EVAL_BUCKETS` between `4194304` and `2097152`
  - changed only operational identifiers such as `RUN_ID`, runner log dir, and runner run name
- The fresh runner-managed control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49102809`
  - `legal_ttt_exact val_bpb=0.29081449`
  - script eval wallclock `591126ms`
  - runner-managed wallclock `634475ms`
  - external top-level wallclock `634633ms`
- The fresh control passed the reviewed admissibility gate versus `eval_033`:
  - `val_bpb` drift `+0.00000069`
  - external wallclock drift `+6494ms`
- The fresh runner-managed candidate with `NGRAM_EVAL_BUCKETS=2097152` scored:
  - `legal_ttt_exact val_loss=0.33904205`
  - `legal_ttt_exact val_bpb=0.20079980`
  - script eval wallclock `582272ms`
  - runner-managed wallclock `625013ms`
  - external top-level wallclock `625177ms`
- Required comparisons:
  - candidate vs fresh control: `-0.09001469 BPB`, `-8854ms` script, `-9462ms` runner-managed, `-9456ms` external
  - candidate vs promoted `eval_032`: `-0.09001291 BPB`, `-2604ms` script, `-2169ms` runner-managed, `-2244ms` external
  - candidate vs historical `eval_015`: `+0.00105778 BPB`, `-81685ms` script, roughly `-80s` runner-managed
- Emitted telemetry also shifted materially on the stronger line:
  - any-match fraction `0.98387524 -> 0.98387585`
  - avg alpha on matched `0.62766972 -> 0.63990334`
  - order histogram concentrated even more mass in `order_9`
- Decision label: `promote`.
- Interpretation: smaller bucket geometry transfers extremely strongly to the promoted `T=0.95` legality line and should now be the default on this helper lineage. `eval_015` still remains the absolute best same-family bucket result, but the promoted helper has now nearly matched it while preserving the newer scorer-path stack.

## Previous Critical Result - `eval_034_eval031_ttt_epochs3_candidate`

- The reviewed refinement-phase epoch-count ablation executed cleanly on the locked promoted `eval_031` legality lineage at `EVAL_LOGIT_TEMP=0.95` with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only `TTT_EPOCHS` from `4` to `3`
  - changed only operational identifiers such as `RUN_ID`, runner log dir, and runner run name
- The fresh runner-managed candidate in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49109611`
  - `legal_ttt_exact val_bpb=0.29085478`
  - script eval wallclock `514515ms`
  - runner-managed wallclock `558261ms`
  - external top-level wallclock `558444ms`
- Required comparisons:
  - candidate vs fresh `eval_033` runner control: `+0.00004098 BPB`, `-70937ms` script, `-69707ms` runner-managed, `-69695ms` external
  - candidate vs promoted `eval_032`: `+0.00004207 BPB`, `-70361ms` script, `-68921ms` runner-managed, `-68977ms` external
- Decision label: `runtime-only operational win`.
- Interpretation: reducing to `TTT_EPOCHS=3` buys a very large runtime gain of about `70s`, but the fourth epoch still buys a small quality gain on the promoted line. Keep `TTT_EPOCHS=4` as the quality default, remember `TTT_EPOCHS=3` as the runtime-optimized variant, and move the next refinement round to a different single-variable question.

## Previous Critical Result - `eval_033_eval031_direct_launch_pair`

- The reviewed refinement-phase launcher-path control pair executed cleanly on the locked promoted `eval_031` legality lineage at `EVAL_LOGIT_TEMP=0.95` with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed in both arms
  - changed only the outer launcher path between fresh control `runner` and fresh candidate `direct launch`
  - changed only operational identifiers such as `RUN_ID` and capture directories
- The fresh runner control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49102692`
  - `legal_ttt_exact val_bpb=0.29081380`
  - script eval wallclock `585452ms`
  - runner-managed wallclock `627968ms`
  - external top-level wallclock `628139ms`
- The fresh control passed the reviewed admissibility gate against `eval_032`:
  - `val_bpb` drift `+0.00000109` vs `0.29081271`
  - external wallclock drift `+718ms` vs `627421ms`
- The direct-launch candidate recovered the exact wrapped child command from the fresh control metadata and reused the same cwd, same `physicslm`, and same pinned GPUs via `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`. The only wrapped-command token difference was the allowed `RUN_ID`.
- The fresh direct-launch candidate scored:
  - `legal_ttt_exact val_loss=0.49102993`
  - `legal_ttt_exact val_bpb=0.29081558`
  - script eval wallclock `583370ms`
  - external top-level wallclock `625537ms`
- Required comparisons:
  - candidate vs fresh control: `+0.00000178 BPB`, `-2082ms` script, `-2602ms` external
  - fresh control vs `eval_032`: `+0.00000109 BPB`, `+718ms` external
  - candidate vs `eval_032`: `+0.00000287 BPB`, `-1884ms` external
- Decision label: `negative`.
- Interpretation: launcher bypass on the promoted `eval_031` `T=0.95` line preserves BPB but only saves `2.602s` externally, below the reviewed `<3s -> negative` threshold. Direct launch should therefore not become the new legality/runtime baseline on this line.

## Previous Critical Result - `eval_032_eval031_temperature_confirmation_pair`

- The reviewed refinement-phase fresh official confirmation pair executed cleanly on the locked `eval_031` legality lineage with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - changed only `EVAL_LOGIT_TEMP` between fresh official control `1.0` and fresh official candidate `0.95`
  - changed only `RUN_ID`, log dir, and run name as operational bookkeeping
- Fresh same-helper full official control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49164677`
  - `legal_ttt_exact val_bpb=0.29118091`
  - script eval wallclock `591399ms`
  - runner-managed wallclock `633253ms`
  - external top-level wallclock `633409ms`
- Fresh same-helper full official candidate at `EVAL_LOGIT_TEMP=0.95` on the same GPUs scored:
  - `legal_ttt_exact val_loss=0.49102508`
  - `legal_ttt_exact val_bpb=0.29081271`
  - script eval wallclock `584876ms`
  - runner-managed wallclock `627182ms`
  - external top-level wallclock `627421ms`
- Required comparisons:
  - fresh `T=0.95` vs fresh `T=1.0`: `0.29118091 -> 0.29081271` (`-0.00036820`)
  - fresh `T=0.95` vs prior `eval_031`: `0.29081485 -> 0.29081271` (`-0.00000214`)
  - fresh `T=1.0` vs `eval_027`: `0.29117839 -> 0.29118091` (`+0.00000252`)
  - fresh `T=1.0` vs `eval_030`: `0.29117961 -> 0.29118091` (`+0.00000130`)
  - runtime vs `eval_027`:
    - fresh `T=1.0`: `+17197ms` script, `+18253ms` runner-managed
    - fresh `T=0.95`: `+10674ms` script, `+12182ms` runner-managed
- Fresh-control admissibility passed cleanly because the fresh `T=1.0` control stayed far within the reviewed `0.0002` drift band against both `eval_027` and `eval_030`.
- Decision label: `promote`.
- Interpretation: this is a clean confirmatory result, not drift-limited and not another one-off selected run. `EVAL_LOGIT_TEMP=0.95` is now the promoted default on the locked `eval_031` PR809 legality line, and nearby scalar-temperature tuning should be considered closed on this line.

## Previous Critical Result - `eval_031_eval027_global_temperature_calibration`

- The reviewed refinement-phase temperature calibration ablation executed cleanly on the locked `eval_027` PR809 legality line. The exact source helper was verified first at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The copied edited `eval_031` helper changed only to `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` stayed unchanged before and after all runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff stayed inside the reviewed single-variable evaluation lane:
  - copied `eval_027` into fresh `eval_031`
  - added one default-off env var `EVAL_LOGIT_TEMP`
  - applied it only to neural scoring logits immediately before `log_softmax` / `softmax` inside the PR809 scorer
  - left TTT adaptation loss, cache updates, n-gram alpha logic, training, export, checkpoint, and artifact untouched
- This round reused the exact frozen non-official held-out slice from `eval_009`:
  - source shard `/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024/fineweb_train_000000.bin`
  - source start token offset `8388608`
  - copied token count `2097153`
  - scored token count `2097152`
  - shard SHA-256 `8b5e92cca71fcfb03dff3a5b2cbf37b25e15a476e8218d253006f1bbcb4db556`
- Calibration sweep on that fixed slice in `physicslm` on GPUs `0,1,2,3,4,5,6,7` produced:
  - `T=0.95 -> 1.20029274`
  - `T=0.975 -> 1.20275434`
  - `T=1.00 -> 1.20587508`
  - `T=1.025 -> 1.20954568`
  - `T=1.05 -> 1.21377823`
- `T=1.0` parity stayed clean: the locked same-helper held-out control from `eval_027` was `1.20586072`, so the new `T=1.0` result drifted by only `+0.00001436`. The best non-`1.0` temperature was `T=0.95`, beating `T=1.0` on the fixed slice by `0.00558234`, which passed the reviewed `0.0002` gate by a wide margin.
- Exactly one full official candidate was then run at `T=0.95`. It scored:
  - `legal_ttt_exact val_loss=0.49102869`
  - `legal_ttt_exact val_bpb=0.29081485`
  - script eval wallclock `584865ms`
  - runner managed wallclock `628844ms`
  - external wallclock `629.130s`
- Official comparisons:
  - vs locked `eval_027`: `0.29117839 -> 0.29081485` (`-0.00036354`)
  - vs fresh `eval_030` control: `0.29117961 -> 0.29081485` (`-0.00036476`)
  - script runtime vs `eval_027`: `+10663ms`
  - managed runtime vs `eval_027`: `+13844ms`
- Decision: this is a controlled positive calibration result, not selector overfit. The selected `T=0.95` transferred from the fixed non-official slice to a real full official BPB improvement. The primary success criterion passed, but the more ambitious `>=0.0005` improvement target was not met. Treat `eval_031` as the new active single-seed legality baseline and do not retire the temperature motif on the PR809 line.

## Previous Controlled Negative Result - `eval_030_eval027_direct_launcher_ablation`

- The reviewed refinement-phase direct-launcher ablation was executable as written, but it stopped at the required fresh-control gate rather than reaching the candidate. The helper stayed unchanged at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged before and after the control run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed evaluation-only lane:
  - no repo code edits
  - no helper edits
  - no scorer edits
  - no export edits
  - recovered the exact locked child command from prior `eval_029` metadata
  - reused one fresh shared `RUN_ID` and the exact `eval_027` helper path
  - measured top-level wallclock externally while also preserving runner metadata
- The fresh official control rerun in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49164458`
  - `legal_ttt_exact val_bpb=0.29117961`
  - script eval wallclock `583199ms`
  - runner managed wallclock `626554ms`
  - external top-level wallclock `626721ms`
- Gate check vs historical `eval_027`:
  - `val_bpb` drift `+0.00000122` -> pass
  - managed wallclock drift `+11554ms` -> fail
  - reviewed allowance was only `+10000ms`, so the control missed the gate by `1554ms`
- Per the reviewed brief, the direct-launch candidate was not run after that gate failure. This round must therefore be interpreted as environment drift rather than launcher evidence.
- Decision: keep `eval_027` as the active legality baseline, and do not treat `eval_030` as either a positive or a negative direct-launch result. The direct-launcher hypothesis remains unanswered.

## Previous Controlled Negative Result - `eval_029_eval027_runner_minpath_seed1337`

- The reviewed refinement-phase runner-path ablation is still answered directly on the exact `eval_027` helper/artifact lineage. The helper stayed unchanged at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff stayed inside the reviewed runner-only scope:
  - edited only `tools/gpu_experiment_runner.py`
  - added one default-off switch `--minimal-runner`
  - added the same runner timing fields in both arms:
    - `runner_start_to_child_spawn_ms`
    - `child_runtime_ms`
    - `child_exit_to_runner_exit_ms`
    - `runner_total_ms`
  - kept child command, env, cwd, stdout/stderr file capture, exit propagation, and artifact paths unchanged
  - allowed minimal mode to skip only console mirroring and the extra pre-query bookkeeping
- The fresh official control rerun answered the stability gate cleanly enough to compare:
  - `legal_ttt_exact val_loss=0.49164510`
  - `legal_ttt_exact val_bpb=0.29117992`
  - script eval wallclock `582051ms`
  - managed wallclock `624825ms`
  - drift vs historical `eval_027`: `+0.00000153 val_bpb`, `+9825ms` managed
- A first minimal-mode attempt with a different `RUN_ID` was discarded because the child command and helper log destination were not strictly identical. The final candidate reran with the exact same child command as control and changed only the outer runner switch.
- The corrected final candidate scored:
  - `legal_ttt_exact val_loss=0.49164536`
  - `legal_ttt_exact val_bpb=0.29118007`
  - script eval wallclock `583407ms`
  - managed wallclock `625998ms`
- Final control-vs-candidate deltas were:
  - `val_bpb`: `+0.00000015`
  - script eval wallclock: `+1356ms`
  - managed wallclock: `+1173ms`
  - `runner_start_to_child_spawn_ms`: `427 -> 180` (`-247ms`)
  - `child_runtime_ms`: `624397 -> 625818` (`+1421ms`)
  - `child_exit_to_runner_exit_ms`: `0 -> 0`
- The exact `eval_027` helper intentionally remained untouched, so the fresh arms do not emit helper-local `process_total_ms`. The closest helper-timed historical anchor remains `eval_028`, which measured `process_total_ms=594842` and inferred outside-helper residual `21158ms`.
- Decision: do not promote the new minimal runner mode. This is a controlled negative result for the repo-controlled runner-path hypothesis inside the runner itself.

## Previous Positive Baseline Result - `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`

- The reviewed refinement-phase scorer-side post-lookup vectorization follow-up is now answered directly on the exact `eval_026` helper/artifact lineage. The copied source helper from `eval_026` was `119346` bytes with SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`. The new `eval_027` helper stayed fixed before and after launch at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged before and after all runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff versus `eval_026` stayed inside the reviewed single-variable scope:
  - added one env var: `NGRAM_EVAL_VECTORIZE_POSTLOOKUP`
  - preserved exact `eval_026` behavior when the switch is `0`
  - changed only `score_segments()` so the switch `1` path vectorizes the remaining matched-order, alpha, probability-mixing, byte-accounting, and histogram work across the scorer batch after the already-validated batch-lookup and batch-torch-stats paths
  - left `NgramEvalCache`, scorer-batch lookup batching, TTT, and all other accounting semantics untouched
  - added only the requested vectorized-postlookup telemetry
- The required disabled parity gate passed cleanly. With `NGRAM_EVAL_ENABLED=0`, the copied helper scored `legal_ttt_exact val_bpb=1.11934901`, only `-0.00000039` versus the locked `eval_026` disabled-parity reference `1.11934940`, at `468349ms` script wallclock and `511s` managed.
- The required same-helper held-out control passed cleanly on the frozen `eval_009` slice. With `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=0`, the helper scored `legal_ttt_exact val_bpb=1.20586072`, with `ngram_batch_lookup_call_count=1040`, `ngram_batch_lookup_elapsed_ms=1769`, `ngram_torch_stats_elapsed_ms=469`, `ngram_postlookup_vectorized_elapsed_ms=0`, and `ngram_update_batch_timing calls=3 elapsed_ms=1139`.
- The enabled held-out candidate also stayed fully controlled. With `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`, it scored `legal_ttt_exact val_bpb=1.20586294`, only `+0.00000222` versus the same-helper control, with `ngram_postlookup_vectorized_batches=1040`, `ngram_postlookup_vectorized_positions_total=2097152`, and `ngram_postlookup_vectorized_elapsed_ms=40753`, so the reviewed stop gate did not trigger.
- The enabled full official run scored `legal_ttt_exact val_loss=0.49164251`, `legal_ttt_exact val_bpb=0.29117839`, with script eval wallclock `574202ms` and managed wallclock `615s`. That keeps BPB effectively locked to `eval_026` (`-0.00000160 val_bpb`) while improving runtime materially (`-32123ms` script, `-32s` managed) and, critically, making the script path legal.
- Final enabled full-val telemetry stayed nearly locked in the pre-existing measured blocks:
  - `ngram_ctx_key_precompute resident_bytes=1984692256 elapsed_ms=20904`
  - `ngram_batch_lookup_call_count=30770`
  - `ngram_batch_lookup_elapsed_ms=20336`
  - `ngram_batch_lookup_positions_total=62021632`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=30770`
  - `ngram_torch_stats_elapsed_ms=3223`
  - `ngram_torch_stats_scored_positions_total=62021632`
  - `ngram_postlookup_vectorized_batches=30770`
  - `ngram_postlookup_vectorized_positions_total=62021632`
  - `ngram_postlookup_vectorized_elapsed_ms=1177650`
  - `ngram_update_batch_timing calls=63 elapsed_ms=32130`
- Final matched-order behavior stayed on the validated `eval_026` line: any-match fraction `0.98387524`, average alpha `0.64247077`, and histogram `order_2=120864`, `order_3=808024`, `order_4=915947`, `order_5=767349`, `order_6=844813`, `order_7=1317753`, `order_8=3289964`, `order_9=52956834`.
- The run remained under the byte cap at `15555121` artifact bytes, `125178` code bytes, `15680299` total, leaving `319701` bytes of headroom.
- Decision: promote `eval_027` as the new active legality baseline. The controls passed, BPB stayed locked, and the official script wallclock is now legal by `25798ms`. Managed wallclock still sits `15s` above `600s`, so any next runtime round should target extra headroom or managed-path overhead rather than scorer-side post-lookup bookkeeping again.

## What Is Already Answered On The Locked PR `#809` Legality Line

- `eval_014`: lowering max order helped runtime only modestly and cost too much BPB.
- `eval_015`: halving buckets changed semantics strongly and stayed runtime-illegal.
- `eval_016`: coarser chunk updates barely helped runtime and regressed BPB.
- `eval_017`: cached context-key reuse was a real runtime win and preserved BPB.
- `eval_018`: sparse touched-bin `update_batch()` preserved BPB and recovered another `15494ms` script time.
- `eval_019`: exact deduplicated lookup gathers preserved BPB but made runtime worse than `eval_018`.
- `eval_020`: exact cached full-key reuse preserved BPB and sped up the hot path, but the added `1.98 GB` tables plus precompute cost erased the gain and left the full run slightly slower than `eval_018`.
- `eval_021`: exact fused scratch-backed `batch_lookup()` preserved BPB and passed both gates, but the full run still regressed versus `eval_018`.
- `eval_022`: exact CUDA-resident tables plus exact CUDA lookup/update execution preserved BPB and passed both gates, but the full run regressed sharply versus `eval_018`, so backend locality was answered negatively.
- `eval_023`: same-helper gate-off control passed, but a global `seg_entropy >= 3.0` pre-lookup gate collapsed full-val BPB to `0.59711635` while still missing runtime legality, so simple global lookup eligibility should be considered answered negatively.
- `eval_024`: saturating `uint16` tables preserved the held-out controls and full-val BPB, but full runtime worsened slightly and full-val saturation telemetry was nontrivial, so count-table precision should be considered answered negatively as a legality lever.
- `eval_025`: scorer-side lookup batching preserved the held-out controls and full-val BPB, slashed lookup call count and lookup elapsed time, and improved end-to-end runtime materially, but still missed the script budget by `14228ms`; this line should be kept as the new active runtime baseline rather than closed as a negative.
- `eval_026`: scorer-side batched exact torch stats preserved the held-out controls and full-val BPB, recovered another `7903ms` script time on top of `eval_025`, and measured `ngram_torch_stats_elapsed_ms=3257`, but still missed the script budget by `6325ms`; it is now superseded by `eval_027`.
- `eval_027`: scorer-side post-lookup vectorization preserved the held-out controls and full-val BPB, recovered `32123ms` script time on top of `eval_026`, and brought the official script eval to `574202ms`; this was the prior active legality baseline before `eval_031`.
- `eval_028`: helper-only official-eval orchestration trimming preserved full-val BPB and reduced helper-local pre/post overhead to about `15.5s`, but managed wallclock stayed `616s` because about `21.2s` now localizes outside the helper in the managed runner path; do not promote it over `eval_027`.
- `eval_029`: a default-off minimal runner mode preserved the exact child command and full official BPB but reduced pre-spawn time by only `247ms` and still worsened managed wallclock by `1173ms`; do not spend another immediate round on nearby repo-controlled runner micro-trims.
- `eval_030`: the direct-launcher ablation did not reach its candidate because the fresh control missed the reviewed managed-wallclock gate by `1554ms`; treat this as drift, not as evidence for or against direct launch.
- `eval_031`: scoring-only neural-logit temperature scaling on the locked PR809 legality line was locally positive and selected `T=0.95`; it is now superseded by `eval_032`, which cleanly confirmed the same setting on a fresh full official control/candidate pair.
- `eval_032`: fresh same-helper full official control/candidate confirmation on the locked `eval_031` line promoted `EVAL_LOGIT_TEMP=0.95` as the default. The fresh control stayed admissible, the fresh candidate won by `0.00036820 BPB`, and nearby scalar-temperature tuning on this line should now be treated as closed.
- `eval_033`: fresh admissible runner control plus direct-launch candidate on the promoted `eval_031` `T=0.95` line preserved BPB but saved only `2602ms` externally, which is below the reviewed `3s` floor; launcher bypass should now be treated as answered negatively on this line.
- `eval_034`: fresh runner-managed `TTT_EPOCHS=3` on the promoted `eval_031` `T=0.95` line worsened BPB by `+0.00004098` versus fresh `eval_033` but saved about `70s` end-to-end, so epoch count is now closed as quality-default `4` versus runtime-optimized `3`.

## Best Next Step

Keep the promoted `eval_035` legality line as the active baseline with `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152`.  
Remember `TTT_EPOCHS=3` only as a runtime-optimized operational variant, and remember that downward `TTT_LR` retuning and launcher-path reruns are already answered on this lineage. The one still-open nearby question is the promoted-line temperature check `0.95 -> 1.0`, but it must be retried only after obtaining a fresh in-gate control.
