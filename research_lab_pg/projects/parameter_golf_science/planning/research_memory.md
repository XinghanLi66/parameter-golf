# Research Memory

This file is the compact scientific memory for the project. Keep it updated so the planner can avoid redundant work.

## Working SOTA Anchor - 2026-03-26

**TARGET SOTA: PR #803 at `0.4416 BPB`** - Complementary Training + Backoff N-gram + TTT.  
PR `#809` at `0.2952` remains legality-pending and is not the official target.

This line is in **REFINEMENT phase**:
- strongest measured local run: `eval_015=0.19974202`
- strongest runtime-improved legality baseline: `eval_026=0.29117999`
- previous legality baseline: `eval_025=0.29117983`
- newest controlled runtime-only result: `eval_026=0.29117999`
- official-anchor gap on the active legality line: `0.29117999 - 0.4416 = -0.15042001`
- open problem: close the remaining `6325ms` script overrun on the locked PR `#809` evaluator without changing validated semantics

`context/reference_materials/URGENT_ngram_backoff_breakthrough.md` remains authoritative for the n-gram mechanism family.  
`context/reference_materials/latest_sota_snapshot.md` remains authoritative for the official comparison target.

## Newest Critical Result - `eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`

- The reviewed refinement-phase scorer-side tensorization follow-up is now answered directly on the exact `eval_025` helper/artifact lineage. The copied source helper from `eval_025` was `116390` bytes with SHA-256 `2d32bdbf1d28834b12ec82da04860b4faccc019f599373ee4393b703b1be2cd2`. The new `eval_026` helper stayed fixed before and after launch at `119346` bytes with SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged before and after all runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff versus `eval_025` stayed inside the reviewed single-variable scope:
  - added one env var: `NGRAM_EVAL_BATCH_TORCH_STATS`
  - preserved exact `eval_025` behavior when the switch is `0`
  - changed only `score_segments()` so the switch `1` path computes exact `log_probs`, gathered `target_logp`, and entropy once per scorer batch in torch and reuses those slices in the existing row loop
  - left `NgramEvalCache`, scorer-batch lookup batching, and all accounting logic untouched
  - added only the requested torch-stats telemetry
- The required disabled parity gate passed cleanly. With `NGRAM_EVAL_ENABLED=0`, the copied helper scored `legal_ttt_exact val_bpb=1.11934940`, only `+0.00000147` versus the locked `eval_025` disabled-parity-equivalent baseline `1.11934793`, at `469094ms` script wallclock and `511s` managed.
- The required enabled same-helper held-out control also passed cleanly on the frozen `eval_009` held-out slice. With `NGRAM_EVAL_BATCH_TORCH_STATS=0`, the helper scored `legal_ttt_exact val_bpb=1.20585418`, only `+0.00000533` versus the locked `eval_025` held-out batching-on baseline `1.20584885`, with `ngram_batch_lookup_call_count=1040`, `ngram_batch_lookup_elapsed_ms=2019`, `ngram_torch_stats_elapsed_ms=0`, and `ngram_update_batch_timing calls=3 elapsed_ms=1172`.
- The enabled torch-stats-on held-out screen also stayed fully controlled on the frozen slice. It scored `legal_ttt_exact val_bpb=1.20584731`, only `-0.00000687` versus the same-helper control, with `ngram_batch_lookup_call_count=1040`, `ngram_batch_lookup_elapsed_ms=2226`, `ngram_torch_stats_batches=1040`, `ngram_torch_stats_elapsed_ms=489`, and `ngram_update_batch_timing calls=3 elapsed_ms=1286`, so the reviewed stop gate did not trigger.
- The enabled full-val run scored `legal_ttt_exact val_loss=0.49164521`, `legal_ttt_exact val_bpb=0.29117999`, with script eval wallclock `606325ms` and managed wallclock `647s`. That keeps BPB effectively identical to `eval_025` (`+0.00000016 val_bpb`) while improving runtime materially (`-7903ms` script, `-10s` managed).
- Final enabled full-val telemetry stayed almost locked outside the new scorer-stats path:
  - `ngram_ctx_key_precompute resident_bytes=1984692256 elapsed_ms=21311`
  - `ngram_batch_lookup_call_count=30770`
  - `ngram_batch_lookup_elapsed_ms=19874`
  - `ngram_batch_lookup_positions_total=62021632`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=30770`
  - `ngram_torch_stats_elapsed_ms=3257`
  - `ngram_torch_stats_scored_positions_total=62021632`
  - `ngram_update_batch_timing calls=63 elapsed_ms=32367`
- Final matched-order behavior stayed on the validated `eval_025` line: any-match fraction `0.98387524`, average alpha `0.64246912`, and histogram `order_2=120864`, `order_3=808024`, `order_4=915947`, `order_5=767349`, `order_6=844813`, `order_7=1317753`, `order_8=3289964`, `order_9=52956834`.
- The run remained under the byte cap at `15555121` artifact bytes, `119346` code bytes, `15674467` total, leaving `325533` bytes of headroom.
- Decision: treat `eval_026` as a positive runtime probe that becomes the new legality-recovery baseline. The controls passed and BPB stayed locked, and scorer-side exact torch stats were a real remaining lever, but the full run still missed legality by `6325ms` script and `47s` managed.

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
- `eval_026`: scorer-side batched exact torch stats preserved the held-out controls and full-val BPB, recovered another `7903ms` script time on top of `eval_025`, and measured `ngram_torch_stats_elapsed_ms=3257`, but still missed the script budget by `6325ms`; this line should now replace `eval_025` as the active legality baseline.

## Best Next Step

Keep `eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337` as the active legality-recovery baseline.  
Do not revert to pre-batched scorer lookup or to per-row neural-stat extraction, and do not spend another immediate round on already-answered global entropy gating or table-width sweeps. The next controlled experiment should target a different non-overlapping end-to-end runtime lever on top of the now-batched scorer plus batched torch-stats path.
