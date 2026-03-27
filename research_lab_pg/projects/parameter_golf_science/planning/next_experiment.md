# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase runner-path ablation on top of the locked `eval_027` PR `#809` legality line.

- Executed the reviewed brief materially as written:
  - edited only `tools/gpu_experiment_runner.py`
  - added a default-off runner switch `--minimal-runner`
  - added coarse runner timing logs in both arms
  - kept the exact `eval_027` helper bytes, saved checkpoint bytes, and saved artifact bytes unchanged
  - ran one fresh official control through the default runner path
  - verified the control stayed within the reviewed `val_bpb` and managed-wallclock gate
  - ran one corrected official candidate with the exact same child command and log destination, changing only the outer runner switch
  - recorded a controlled negative result

## Experiment ID
`eval_029_eval027_runner_minpath_seed1337`

## Category
- evaluation

Operational subtype: `runtime-only runner-path ablation on locked eval_027 legality line`

## Baseline / Comparison
Fresh control baseline:
- `eval_029` control on the unchanged `eval_027` helper/artifact line
  - `val_bpb=0.29117992`
  - script eval wallclock `582051ms`
  - managed wallclock `624825ms`

Historical anchors:
- `eval_027`: `val_bpb=0.29117839`, script eval wallclock `574202ms`, managed wallclock `615s`
- `eval_028`: `val_bpb=0.29118133`, helper `process_total_ms=594842`, inferred runner-managed outside-helper overhead `21158ms`, managed wallclock `616s`

## Hypothesis
If the remaining managed overrun is mainly runner-side setup, teardown, and wrapper bookkeeping outside the helper, then a minimal runner mode that preserves identical child execution should reduce managed wallclock enough to reach `<=600s` while preserving `val_bpb` within `±0.0001` of fresh control and historical `eval_027`.

## Why It Might Work
- `eval_027` already proved the exact script path is legal.
- `eval_028` showed helper-local total process time can already fit under budget.
- The untested repo-controlled variable was still the runner path outside the helper.

## Minimal Intervention
Change only `tools/gpu_experiment_runner.py`:

- add one default-off runner switch `--minimal-runner`
- keep the child command, env, cwd, stdout/stderr file capture, exit propagation, and artifact paths unchanged
- add the same timing instrumentation to both arms
- allow minimal mode to skip only nonessential runner-side console mirroring and extra pre-query bookkeeping

## Variables To Change
- new runner switch: `--minimal-runner`
- runner-side console mirroring outside the child path
- runner-side extra pre-query work
- new runner timing fields:
  - `runner_start_to_child_spawn_ms`
  - `child_runtime_ms`
  - `child_exit_to_runner_exit_ms`
  - `runner_total_ms`

## Variables To Hold Fixed
- exact `eval_027` helper bytes and SHA-256
- exact saved seed-`1337` checkpoint/export bytes and SHA-256
- exact official `legal_ttt_exact` eval child command
- tokenizer, dataset, stride `64`
- exact n-gram and TTT settings from `eval_027`
- exact `physicslm` environment and `8x NVIDIA L20Z` launch shape
- no retraining
- no export rewrite
- no scorer-side code changes
- no helper `main()` orchestration edits

## Identity Checks
- Helper:
  - `runs/eval_027.../train_gpt.py`: `125178` bytes
  - SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`
- Saved checkpoint:
  - `final_model.pt`: `106178569` bytes
  - SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
- Saved artifact:
  - `final_model.int6.ptz`: `15555121` bytes
  - SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

## Control Acceptance Gate
- Fresh control `val_bpb=0.29117992`, historical drift `+0.00000153`
- Fresh control managed wallclock `624825ms`, historical drift `+9825ms`
- Gate decision: `pass`

## Final Comparison
- Exact child command identity between final control and final candidate: `pass`
- Control:
  - `val_loss=0.49164510`
  - `val_bpb=0.29117992`
  - script eval wallclock `582051ms`
  - managed wallclock `624825ms`
  - runner split `427 / 624397 / 0 / 624825ms`
- Candidate (`--minimal-runner`):
  - `val_loss=0.49164536`
  - `val_bpb=0.29118007`
  - script eval wallclock `583407ms`
  - managed wallclock `625998ms`
  - runner split `180 / 625818 / 0 / 625998ms`
- Deltas:
  - `val_bpb`: `+0.00000015`
  - script eval wallclock: `+1356ms`
  - managed wallclock: `+1173ms`
  - `runner_start_to_child_spawn_ms`: `-247ms`
  - `child_runtime_ms`: `+1421ms`
  - `child_exit_to_runner_exit_ms`: unchanged at `0ms`

## Notes
- One initial minimal-mode launch used a different `RUN_ID`; it was discarded from comparison because the child command and helper log destination were not strictly identical. The final reported candidate reran with the exact same child command as control.
- The exact `eval_027` helper does not emit `process_total_ms`, so fresh-arm `runner_total_ms - helper_process_total_ms` is unavailable. The closest helper-timed historical anchor remains `eval_028`, which measured outside-helper residual `21158ms`.

## Success Metric
Primary success criterion:
- candidate managed wallclock `<=600s`

Quality guardrail:
- candidate `val_bpb` within `±0.0001` of fresh control and historical `eval_027`

Outcome:
- quality guardrail passed
- managed wallclock target failed by `25998ms`
- minimal runner did not materially reduce managed wallclock
- the only measurable runner-side improvement was a small `247ms` reduction before child spawn
- overall result was slightly worse end-to-end

## Interpretation
This is a controlled negative answer to the runner-path hypothesis inside the repo-controlled launcher. The minimal runner preserved quality and the exact child command but did not buy legality; `eval_027` remains the active legality baseline.

## Next Step
If another runtime round is still warranted, treat the remaining miss as likely dominated by platform or job-wrapper overhead outside this repo’s minimal runner adjustments. Do not spend the next immediate round on another nearby runner micro-trim unless a genuinely different launcher path is available.

## Expected Effect
- Keep BPB locked while reducing managed wallclock below `600s`.

## Actual Result
- BPB stayed effectively locked.
- The helper-local fast path reduced helper pre/post work to about `15.5s` total and kept helper total process time under `600s`.
- Managed wallclock still finished at `616s`, so the round did not achieve full managed legality.

## Interpretation
This is a controlled negative refinement result. `eval_028` should not replace `eval_027` as the active legality baseline.

The new phase split is still useful: the remaining `36.644s` managed minus script gap now decomposes into about `15.487s` of helper-local pre/post work and about `21.158s` outside the helper in the managed runner path.

## Next Step
If another runtime round is warranted, target runner-managed overhead outside the helper rather than another scorer-side or helper-orchestration trim on the locked `eval_027` line.
