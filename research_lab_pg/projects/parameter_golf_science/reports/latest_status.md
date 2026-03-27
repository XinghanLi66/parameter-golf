# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line remains `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest controlled runtime-only result is now `eval_029_eval027_runner_minpath_seed1337`.
- The `eval_029` helper/artifact guardrail stayed clean. The exact `eval_027` helper remained `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`; the saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The exact implementation diff stayed within the reviewed runner-only scope:
  - edited only `tools/gpu_experiment_runner.py`
  - added one default-off switch `--minimal-runner`
  - added the same runner timing fields in both arms
  - kept child command, env, cwd, stdout/stderr file capture, exit propagation, and artifact paths unchanged
  - allowed minimal mode to skip only console mirroring and the extra pre-query bookkeeping
- The fresh control rerun on the unchanged `eval_027` helper scored `legal_ttt_exact val_loss=0.49164510`, `legal_ttt_exact val_bpb=0.29117992`, with script eval wallclock `582051ms` and managed wallclock `624825ms`. That passed the reviewed control gate versus historical `eval_027` by staying within `+0.00000153 val_bpb` and `+9825ms` managed.
- A first minimal-mode attempt with a different `RUN_ID` was discarded because the child command and helper log destination were not strictly identical. The final candidate reran with the exact same child command as control and changed only the outer runner switch.
- The corrected final candidate scored `legal_ttt_exact val_loss=0.49164536`, `legal_ttt_exact val_bpb=0.29118007`, with script eval wallclock `583407ms` and managed wallclock `625998ms`.
- Delta summary for the final control-vs-candidate comparison:
  - `val_bpb`: `+0.00000015`
  - script eval wallclock: `582051ms -> 583407ms` (`+1356ms`)
  - managed wallclock: `624825ms -> 625998ms` (`+1173ms`)
  - `runner_start_to_child_spawn_ms`: `427 -> 180` (`-247ms`)
  - `child_runtime_ms`: `624397 -> 625818` (`+1421ms`)
  - `child_exit_to_runner_exit_ms`: `0 -> 0`
- Interpretation: the minimal runner preserved quality and the exact child command, but it did not reduce managed wallclock and does not make the line legal. `eval_027` remains the active legality baseline, and the remaining managed miss now looks unlikely to be recoverable through another nearby repo-controlled runner micro-trim.

## Most Important Open Question
If managed legality is still worth pursuing on the already script-legal `eval_027` line, is there any genuinely different launcher or platform-side lever left, or should the remaining managed miss be treated as outside the scope of repo-controlled micro-trims?

## Active Experiment ID
`eval_029_eval027_runner_minpath_seed1337`

## Latest Result Summary
- Completed `eval_029_eval027_runner_minpath_seed1337` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_029_eval027_runner_minpath_seed1337/summary.md).
- Controlled intervention actually executed:
  - edited only `tools/gpu_experiment_runner.py`
  - added one default-off switch `--minimal-runner`
  - added coarse runner timing instrumentation active in both arms
  - ran one fresh official control on the exact unchanged `eval_027` helper/artifact line
  - after one discarded mismatched-`RUN_ID` draft candidate, reran one corrected official candidate with the exact same child command and changed only the runner switch
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`
  - fresh control: `legal_ttt_exact val_bpb=0.29117992`, `val_loss=0.49164510`
  - corrected candidate: `legal_ttt_exact val_bpb=0.29118007`, `val_loss=0.49164536`
  - bytes stayed unchanged at artifact `15555121`, code `125178`, total `15680299`
  - byte status: under cap by `319701`
- Timing:
  - fresh control script eval wallclock: `582051ms`
  - corrected candidate script eval wallclock: `583407ms`
  - fresh control managed wallclock: `624825ms`
  - corrected candidate managed wallclock: `625998ms`
  - runner split delta:
    - `runner_start_to_child_spawn_ms`: `427 -> 180` (`-247ms`)
    - `child_runtime_ms`: `624397 -> 625818` (`+1421ms`)
    - `child_exit_to_runner_exit_ms`: `0 -> 0`
- Decision:
  - the fresh control was stable enough to compare
  - the corrected candidate preserved quality and exact child-command identity
  - minimal runner did not reduce managed wallclock and does not replace the default path
  - `eval_027` remains the active legality baseline

## Recommended Next Step
Keep `eval_027` fixed as the active legality baseline. Do not spend the next immediate round on another nearby repo-controlled runner trim; only revisit managed legality if a genuinely different launcher path or platform-side lever becomes available.
