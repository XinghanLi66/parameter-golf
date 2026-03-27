# Research Memory

This file is the compact scientific memory for the project. Keep it updated so the planner can avoid redundant work.

## Working SOTA Anchor - 2026-03-27

**TARGET SOTA: PR #803 at `0.4416 BPB`** - Complementary Training + Backoff N-gram + TTT.  
PR `#809` at `0.2952` remains legality-pending and is not the official target.

This line is in **REFINEMENT phase**:
- strongest measured local run: `eval_015=0.19974202`
- strongest runtime-improved legality baseline: `eval_027=0.29117839`
- previous legality baseline: `eval_026=0.29117999`
- newest controlled runtime-only result: `eval_027=0.29117839`
- official-anchor gap on the active legality line: `0.29117839 - 0.4416 = -0.15042161`
- open problem: the script legality issue is now answered; any next runtime round should target extra headroom or managed-path overhead rather than scorer-side post-lookup bookkeeping again

`context/reference_materials/URGENT_ngram_backoff_breakthrough.md` remains authoritative for the n-gram mechanism family.  
`context/reference_materials/latest_sota_snapshot.md` remains authoritative for the official comparison target.

## Newest Critical Result - `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`

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
- `eval_027`: scorer-side post-lookup vectorization preserved the held-out controls and full-val BPB, recovered `32123ms` script time on top of `eval_026`, and brought the official script eval to `574202ms`; this is now the active legality baseline.

## Best Next Step

Keep `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337` as the active legality baseline.  
Do not revert to pre-batched scorer lookup, per-row neural-stat extraction, or per-row post-lookup bookkeeping, and do not spend another immediate round on already-answered global entropy gating or table-width sweeps. If more runtime headroom is still desired, the next controlled experiment should target a different non-overlapping cost center such as `update_batch()` or managed-path overhead.
