# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line is now `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest controlled runtime-only result is now `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`.
- The helper/artifact guardrail for `eval_027` passed cleanly. The copied source helper from `eval_026` was `119346` bytes with SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`; the edited `eval_027` helper stayed fixed before and after launch at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`; the saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` stayed unchanged before and after the run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The exact implementation diff versus `eval_026` stayed within the reviewed single-variable scope:
  - added one env var `NGRAM_EVAL_VECTORIZE_POSTLOOKUP`
  - preserved exact `eval_026` behavior when the switch is `0`
  - changed only `score_segments()` so the switch `1` path vectorizes the remaining post-lookup matched-order, alpha, probability-mixing, byte-accounting, and histogram work across the scorer batch
  - left `NgramEvalCache`, scorer-batch lookup batching, batch torch-stats extraction, score-first scheduling, TTT, and accounting semantics unchanged
  - added only the requested vectorized-postlookup telemetry
- The required disabled parity gate passed at `1.11934901`, only `-0.00000039` versus the locked `eval_026` disabled-parity reference `1.11934940`.
- The required enabled same-helper held-out control also passed:
  - exact `val_bpb=1.20586072`
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=1769`
  - `ngram_torch_stats_batches=1040`
  - `ngram_torch_stats_elapsed_ms=469`
  - `ngram_postlookup_vectorized_batches=0`
  - `ngram_postlookup_vectorized_elapsed_ms=0`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1139`
- The enabled vectorized held-out screen also stayed controlled:
  - exact `val_bpb=1.20586294`
  - delta vs same-helper control: `+0.00000222`
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=1866`
  - `ngram_torch_stats_batches=1040`
  - `ngram_torch_stats_elapsed_ms=480`
  - `ngram_postlookup_vectorized_batches=1040`
  - `ngram_postlookup_vectorized_positions_total=2097152`
  - `ngram_postlookup_vectorized_elapsed_ms=40753`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1157`
- The full official `eval_027` run scored `legal_ttt_exact val_loss=0.49164251`, `legal_ttt_exact val_bpb=0.29117839`.
- Delta summary for `eval_027`:
  - vs `eval_026=0.29117999`: `-0.00000160`
  - vs official snapshot target `0.4416`: `-0.15042161`
- Final `eval_027` lookup, scorer-stats, vectorized-postlookup, and match statistics:
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
  - any-match fraction `0.98387524`
  - average applied alpha on matched positions `0.64247077`
  - matched-order histogram `{"order_2":120864,"order_3":808024,"order_4":915947,"order_5":767349,"order_6":844813,"order_7":1317753,"order_8":3289964,"order_9":52956834}`
- Runtime improved materially and now recovers script legality. The enabled `eval_027` full-val run took `574202ms` script eval wallclock and `615s` managed wallclock, which is `-32123ms` and `-32s` versus `eval_026`. The script path is now legal by `25798ms`, while managed wallclock remains `15s` above `600s`.

## Most Important Open Question
Now that the locked PR `#809` evaluator is script-legal, is any further runtime work even necessary, and if so, should it target `update_batch()` / managed-path overhead rather than scorer-side post-lookup bookkeeping?

## Active Experiment ID
`eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`

## Latest Result Summary
- Completed `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337/summary.md).
- Controlled intervention actually executed:
  - copied the exact `eval_026` helper into a fresh `eval_027` run directory
  - reused the exact saved seed-`1337` `arch_010` checkpoint/export lineage unchanged
  - changed only scorer-side post-lookup bookkeeping through a default-off `NGRAM_EVAL_VECTORIZE_POSTLOOKUP` switch layered on top of the locked scorer-batch lookup and batched torch-stats paths
  - kept `NgramEvalCache`, score-first scheduling, TTT, alpha math, chunking, tokenizer, dataset, and artifact bytes fixed
  - added only minimal vectorized-postlookup telemetry
  - ran one disabled parity eval, one enabled same-helper held-out control, one enabled held-out screen, and one enabled managed full-val candidate on `8x NVIDIA L20Z` in `physicslm`
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`
  - disabled parity result: `legal_ttt_exact val_bpb=1.11934901`, `val_loss=1.88996891`
  - held-out control result: `legal_ttt_exact val_bpb=1.20586072`, `val_loss=2.03664882`
  - held-out candidate result: `legal_ttt_exact val_bpb=1.20586294`, `val_loss=2.03665257`
  - final enabled result: `legal_ttt_exact val_bpb=0.29117839`, `val_loss=0.49164251`
  - bytes: artifact `15555121`, code `125178`, total `15680299`
  - byte status: under cap by `319701`
- Timing:
  - final script eval wallclock: `574202ms`
  - final managed wallclock: `615s`
  - vs `eval_026` script eval wallclock `606325ms`: `-32123ms`
  - practical budget status: final result is script-legal by `25798ms`; managed wallclock remains `15s` over `600s`
- Decision:
  - helper/artifact identity stayed locked and all controls passed, so the result is directly comparable to `eval_026`
  - scorer-side vectorized post-lookup accounting preserved BPB while recovering the remaining script-time miss
  - `eval_027` should replace `eval_026` as the active legality baseline on the locked PR `#809` line

## Recommended Next Step
Keep `eval_027` fixed as the active legality baseline. If more runtime margin is still useful, target a different non-overlapping cost center such as `update_batch()` or managed-path overhead rather than scorer-side post-lookup work again.
