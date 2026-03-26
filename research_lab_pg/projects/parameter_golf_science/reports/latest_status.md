# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The real local `eval_007_arch010_legal_ttt_epochs4_seed2024_confirm` comparison is now measured on one controlled refinement-phase evaluation-only run on top of the locked `arch_010` seed-`2024` export lineage: keep the saved seed-`2024` artifact, the copied legal score-first TTT helper, and the `eval_006` winning TTT setting (`TTT_LR=0.0025`, `TTT_EPOCHS=4`) fixed, and change only the evaluated artifact lineage relative to `eval_006`.
- The guardrail passed before launch, so this remained a clean single-variable confirmation rather than a drifted rerun: the copied helper stayed byte-identical to the `eval_006` helper lineage at `84059` bytes and SHA-256 `d93fc02cd20958d56d49af2df6b886527cef71d98ac46aa6304c4db048211bf8`, while the saved seed-`2024` `final_model.pt` and `final_model.int6.ptz` stayed unchanged at `106178569` bytes / `302fe0ad...` and `15761090` bytes / `479e5ccc...`.
- Because helper and artifact identity stayed locked, the brief did not require rerunning same-script no-TTT parity. The valid comparison baselines therefore remain the locked seed-`2024` legal-TTT baseline `1.12027199`, the inherited same-script no-TTT parity result `1.12225535`, the contextual seed-`1337` `eval_006` result `1.11935008`, the locked legal-TTT 3-seed mean `1.12010450`, and live SOTA `1.1194`.
- The single managed 8-GPU eval-only run in `physicslm` on `8x NVIDIA L20Z` completed cleanly with exit code `0` and produced `legal_ttt_exact val_loss=1.89097347`, `legal_ttt_exact val_bpb=1.11994397`, script TTT eval wallclock `465406ms`, and managed wallclock `506s`.
- Versus the primary seed-`2024` legal-TTT baseline `1.12027199`, the candidate improved by `-0.00032802`; versus the inherited same-script no-TTT parity baseline `1.12225535`, by `-0.00231138`; versus the seed-`1337` `eval_006` breakthrough `1.11935008`, it regressed by `+0.00059389`; versus the locked legal-TTT 3-seed mean `1.12010450`, it improved by `-0.00016053`; and versus live SOTA `1.1194`, it remained `+0.00054397` above.
- Eval-time cost rose materially versus the seed-`2024` locked `TTT_EPOCHS=3` run but stayed below the real limit: script wallclock rose `+65058ms` (`400348 -> 465406`) and managed wallclock rose `+65s` (`441 -> 506`), leaving about `94s` of managed headroom under the practical `10 min` cap.
- The strongest local single-seed post-export result still remains `eval_006` at `1.11935008`, but `eval_007` is a clean positive confirmation on the more discriminating seed and lands in the brief’s “especially strong” band `<= 1.12010` at unchanged total bytes `15845149`, under the cap by `154851`.
- Interpretation against the reviewed thresholds is positive: the run beats the primary decision baseline and stays budget-safe. The remaining caution is that `TTT_EPOCHS=4` is still not fully promoted across the line because the final locked seed-`42` confirmation has not yet been run.

## Most Important Open Question
Does the same locked-helper, locked-artifact `TTT_LR=0.0025`, `TTT_EPOCHS=4` legal-TTT setting also beat the seed-`42` baseline strongly enough, and with acceptable eval cost, to justify promoting `TTT_EPOCHS=4` across the locked `arch_010` legal-TTT line?

## Active Experiment ID
`eval_007_arch010_legal_ttt_epochs4_seed2024_confirm`

## Latest Result Summary
- Completed `eval_007_arch010_legal_ttt_epochs4_seed2024_confirm` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_007_arch010_legal_ttt_epochs4_seed2024_confirm/summary.md).
- Controlled intervention actually executed:
  - copied the exact `eval_006` helper into a fresh `eval_007` run directory
  - reused the exact saved seed-`2024` `arch_010` checkpoint/export lineage unchanged
  - kept `TTT_LR=0.0025`, `TTT_EPOCHS=4` fixed
  - changed only the evaluated artifact lineage from seed `1337 -> 2024`
- Locked identity checks:
  - helper bytes/hash: `84059`, `d93fc02cd20958d56d49af2df6b886527cef71d98ac46aa6304c4db048211bf8`
  - saved seed-`2024` `final_model.pt`: `106178569` bytes, `302fe0ad739f19e51e35ecd6f55e5568009a31a2ead991fd3ebfbcf5be150987`
  - saved seed-`2024` `final_model.int6.ptz`: `15761090` bytes, `479e5ccc5cb21d67fa937abb884fb63f1f812d99402b77b25fe32c2b9d838af3`
- Managed 8-GPU eval-only run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`
  - result: `legal_ttt_exact val_bpb=1.11994397`, `val_loss=1.89097347`
  - bytes: artifact `15761090`, code `84059`, total `15845149`
  - byte status: under cap by `154851`
  - legality: `score_first=True`, `last_chunk_untrained=True`, `1893` chunks of `32768` tokens
  - load/decompress/dequantize status: pass
- Deltas:
  - vs primary seed-`2024` legal-TTT baseline `1.12027199`: `-0.00032802`
  - vs same-script no-TTT parity baseline `1.12225535`: `-0.00231138`
  - vs contextual `eval_006` seed-`1337` result `1.11935008`: `+0.00059389`
  - vs locked legal-TTT 3-seed mean `1.12010450`: `-0.00016053`
  - vs live SOTA `1.1194`: `+0.00054397`
  - vs seed-`2024` locked `TTT_EPOCHS=3` script eval wallclock `400348ms`: `+65058ms`
  - vs seed-`2024` locked `TTT_EPOCHS=3` managed wallclock `441s`: `+65s`
- Decision:
  - hypothesis confirmed on the discriminating seed
  - the locked legal-TTT regime still appears to have real but not uniform extra adaptation-budget headroom
  - the setting is now strong enough to justify the final exact seed-`42` confirmation before promotion

## Recommended Next Step
Run the exact locked-helper, locked-artifact `TTT_LR=0.0025`, `TTT_EPOCHS=4` eval-only test on seed `42`. If that final confirmation stays positive and remains comfortably under the real eval budget, promote `TTT_EPOCHS=4` across the locked `arch_010` legal-TTT line; if not, stop nearby TTT-budget tuning and move to a different single-variable refinement.
