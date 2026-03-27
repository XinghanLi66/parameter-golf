# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality-recovery baseline on the locked PR `#809` line is now `eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-26 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest controlled runtime-only result is now `eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`.
- The helper/artifact guardrail for `eval_026` passed cleanly. The copied source helper from `eval_025` was `116390` bytes with SHA-256 `2d32bdbf1d28834b12ec82da04860b4faccc019f599373ee4393b703b1be2cd2`; the edited `eval_026` helper stayed fixed before and after launch at `119346` bytes with SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`; the saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` stayed unchanged before and after the run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The exact implementation diff versus `eval_025` stayed within the reviewed single-variable scope:
  - added one env var `NGRAM_EVAL_BATCH_TORCH_STATS`
  - preserved exact `eval_025` behavior when the switch is `0`
  - changed only `score_segments()` so the switch `1` path computes exact `log_probs`, gathered `target_logp`, and entropy once per scorer batch in torch and then reuses those tensors in the existing row loop
  - left `NgramEvalCache`, scorer-batch lookup batching, score-first scheduling, TTT, and accounting logic unchanged
  - added only the requested torch-stats telemetry
- The required disabled parity gate passed at `1.11934940`, only `+0.00000147` versus the locked `eval_025` disabled-parity-equivalent baseline `1.11934793`.
- The required enabled same-helper held-out control also passed:
  - exact `val_bpb=1.20585418`
  - delta vs locked `eval_025` held-out batching-on baseline `1.20584885`: `+0.00000533`
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=2019`
  - `ngram_batch_lookup_positions_total=2097152`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=0`
  - `ngram_torch_stats_elapsed_ms=0`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1172`
- The enabled torch-stats-on held-out screen also stayed controlled:
  - exact `val_bpb=1.20584731`
  - delta vs same-helper held-out control: `-0.00000687`
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=2226`
  - `ngram_batch_lookup_positions_total=2097152`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=1040`
  - `ngram_torch_stats_elapsed_ms=489`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1286`
- The full official `eval_026` run scored `legal_ttt_exact val_loss=0.49164521`, `legal_ttt_exact val_bpb=0.29117999`.
- Delta summary for `eval_026`:
  - vs `eval_025=0.29117983`: `+0.00000016`
  - vs `eval_018=0.29117845`: `+0.00000154`
  - vs official snapshot target `0.4416`: `-0.15042001`
- Final `eval_026` lookup, scorer-stats, and match statistics:
  - `ngram_batch_lookup_call_count=30770`
  - `ngram_batch_lookup_elapsed_ms=19874`
  - `ngram_batch_lookup_positions_total=62021632`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=30770`
  - `ngram_torch_stats_elapsed_ms=3257`
  - `ngram_torch_stats_scored_positions_total=62021632`
  - `ngram_update_batch_timing calls=63 elapsed_ms=32367`
  - context-key precompute `resident_bytes=1984692256 elapsed_ms=21311`
  - any-match fraction `0.98387524`
  - average applied alpha on matched positions `0.64246912`
  - matched-order histogram `{"order_2":120864,"order_3":808024,"order_4":915947,"order_5":767349,"order_6":844813,"order_7":1317753,"order_8":3289964,"order_9":52956834}`
- Runtime improved materially but did not recover legality. The enabled `eval_026` full-val run took `606325ms` script eval wallclock and `647s` managed wallclock, which is `-7903ms` and `-10s` versus `eval_025`, and `-24176ms` and `-24s` versus `eval_018`.
- Lookup and update timings stayed roughly locked relative to `eval_025`, while the new scorer-side telemetry showed `ngram_torch_stats_elapsed_ms=3257`, so the result is a real runtime improvement from scorer-side tensorization rather than a semantic drift artifact.

## Most Important Open Question
What non-overlapping runtime lever, stacked on top of `eval_026`, can close the remaining `6325ms` script overrun on the locked `eval_018` PR `#809` evaluator without breaking the now-validated batched-scorer plus batched-torch-stats semantics?

## Active Experiment ID
`eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`

## Latest Result Summary
- Completed `eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337/summary.md).
- Controlled intervention actually executed:
  - copied the exact `eval_025` helper into a fresh `eval_026` run directory
  - reused the exact saved seed-`1337` `arch_010` checkpoint/export lineage unchanged
  - changed only scorer-side neural-stat extraction through a default-off `NGRAM_EVAL_BATCH_TORCH_STATS` switch layered on top of the locked scorer-batch lookup path
  - kept `NgramEvalCache`, sparse touched-bin updates, scorer-batch lookup batching, score-first scheduling, TTT, alpha math, chunking, tokenizer, dataset, and artifact bytes fixed
  - added only minimal torch-stats telemetry
  - ran one disabled parity eval, one enabled same-helper torch-stats-off held-out control, one enabled held-out torch-stats-on screen, and one enabled managed full-val torch-stats-on eval-only comparison on `8x NVIDIA L20Z` in `physicslm`
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`
  - disabled parity result: `legal_ttt_exact val_bpb=1.11934940`, `val_loss=1.88996957`
  - torch-stats-off control result: `legal_ttt_exact val_bpb=1.20585418`, `val_loss=2.03663777`
  - torch-stats-on held-out screen: `legal_ttt_exact val_bpb=1.20584731`, `val_loss=2.03662617`
  - final enabled result: `legal_ttt_exact val_bpb=0.29117999`, `val_loss=0.49164521`
  - bytes: artifact `15555121`, code `119346`, total `15674467`
  - byte status: under cap by `325533`
- Timing:
  - final script eval wallclock: `606325ms`
  - final managed wallclock: `647s`
  - vs `eval_025` script eval wallclock `614228ms`: `-7903ms`
  - practical budget status: final result exceeded budget by `6325ms` script time and `47s` managed wallclock
- Decision:
  - helper/artifact identity stayed locked and both controls passed, so the result is directly comparable to `eval_025`
  - batched exact torch-side scorer stats preserved BPB almost exactly while improving end-to-end runtime further on the same helper line
  - the end-to-end runtime win is real but still insufficient for legality
  - the correct interpretation is `runtime-improved-but-still-illegal`, and this line should replace `eval_025` as the active legality baseline

## Recommended Next Step
Keep `eval_026` fixed as the best legality-recovery baseline, and run the next controlled runtime-only follow-up on the same saved artifact line against a different end-to-end lever rather than abandoning scorer-batch lookup batching plus batched torch-side stats.
