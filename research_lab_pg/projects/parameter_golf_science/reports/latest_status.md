# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line remains `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest runtime-only round is now `eval_030_eval027_direct_launcher_ablation`.
- The `eval_030` helper/artifact guardrail stayed clean. The exact `eval_027` helper remained `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`; the saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged before and after the control run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The exact experiment scope stayed within the reviewed evaluation-only launcher-path lane:
  - no repo code edits
  - exact locked child command recovered from prior fresh-control metadata
  - one fresh shared `RUN_ID` used so the child command and helper log destination stayed aligned
  - one fresh official control run through `tools/gpu_experiment_runner.py`
  - external top-level wallclock recorded on the launcher itself
  - direct-launch candidate intentionally not run after the control gate failed
- The fresh control rerun on the unchanged `eval_027` helper scored `legal_ttt_exact val_loss=0.49164458`, `legal_ttt_exact val_bpb=0.29117961`, with script eval wallclock `583199ms`, runner managed wallclock `626554ms`, and external top-level wallclock `626721ms`.
- Gate summary versus historical `eval_027`:
  - `val_bpb`: `0.29117839 -> 0.29117961` (`+0.00000122`) -> `pass`
  - managed wallclock: `615000ms -> 626554ms` (`+11554ms`) -> `fail`
  - reviewed allowance was only `+10000ms`, so the fresh control missed the gate by `1554ms`
- Interpretation: this is a drift-stopped round, not direct-launch evidence. The launcher-path hypothesis remains unanswered because the candidate could not be run under an admissible fresh control. `eval_027` remains the active legality baseline.

## Most Important Open Question
If managed legality is still worth pursuing on the already script-legal `eval_027` line, can a fresh in-gate control still be recovered for the direct-launcher ablation, or has platform variance now become large enough that further launcher-path comparisons are no longer informative?

## Active Experiment ID
`eval_030_eval027_direct_launcher_ablation`

## Latest Result Summary
- Completed `eval_030_eval027_direct_launcher_ablation` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_030_eval027_direct_launcher_ablation/summary.md).
- Controlled intervention actually executed:
  - changed no repo files
  - recovered the exact locked `eval_027` child command from prior metadata
  - ran one fresh official control on the exact unchanged `eval_027` helper/artifact line
  - checked the reviewed control gate before any candidate launch
  - stopped before the direct-launch candidate because the control missed the managed-wallclock gate
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - fresh control: `legal_ttt_exact val_bpb=0.29117961`, `val_loss=0.49164458`
  - candidate: not run
  - bytes stayed unchanged at artifact `15555121`, code `125178`, total `15680299`
  - byte status: under cap by `319701`
- Timing:
  - fresh control script eval wallclock: `583199ms`
  - fresh control managed wallclock: `626554ms`
  - fresh control external top-level wallclock: `626721ms`
- Decision:
  - the fresh control passed the BPB gate but failed the managed-wallclock gate by `1554ms`
  - the direct-launch candidate was not run, per protocol
  - `eval_027` remains the active legality baseline
  - the launcher-path question remains unanswered rather than disproved

## Recommended Next Step
Keep `eval_027` fixed as the active legality baseline. Only revisit the direct-launcher ablation if a fresh in-gate control can be recovered first; otherwise deprioritize further runtime-legality work instead of treating this drift-stopped round as evidence against direct launch.
