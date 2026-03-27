# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase scorer-side post-lookup vectorization follow-up on the locked `eval_026` PR `#809` legality line.

- Executed the reviewed brief materially as written:
  - created `runs/eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`
  - copied the exact `eval_026` helper into the new run directory
  - changed only one scorer-side runtime lever: the remaining post-lookup accounting path in `score_segments()` is now optionally vectorized across the scorer batch after the already-validated batch lookup and batch torch-stats steps
  - kept the saved seed-`1337` checkpoint/export lineage unchanged
  - ran one disabled full-val parity check
  - ran one enabled same-helper held-out control with `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=0`
  - ran one enabled held-out candidate screen with `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`
  - ran one enabled full official eval in `physicslm` on `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`

## Experiment ID
`eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`

## Category
- evaluation

Operational subtype: `runtime-only scorer-side post-lookup accounting vectorization on locked PR #809 legality line`

## Baseline / Comparison
Primary runtime baseline:
- `eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`
  - `val_bpb=0.29117999`
  - script eval wallclock `606325ms`
  - managed wallclock `647s`

Required semantic control anchors:
- disabled parity from `eval_026`: `1.11934940`
- continuity held-out reference from `eval_026`: `1.20584731`
- same-helper held-out control for this round: `1.20586072`

External comparison:
- official snapshot target `PR #803`: `0.4416`

## Hypothesis
If the remaining `6325ms` legality miss after `eval_026` is dominated by Python-side post-lookup scorer bookkeeping, then vectorizing matched-order selection, alpha selection, probability mixing, byte accounting, and histogram updates across the scorer batch will recover the missing script time without materially changing BPB.

## Why It Might Work
- `eval_025` already removed most outer lookup-call overhead.
- `eval_026` already removed repeated per-row exact neural-stat extraction.
- The remaining clean residual cost was the Python row loop after lookup results and exact batch neural stats already existed.

## Minimal Intervention
Copy the exact `eval_026` helper into a fresh run directory, add one default-off env switch, and change only the enabled scorer path in `score_segments()` so the remaining post-lookup accounting is vectorized across the scorer batch. Keep checkpoint/export lineage, lookup behavior, TTT behavior, alpha math, chunking, tokenizer, dataset, and export path fixed.

## Variables To Change
- new env control: `NGRAM_EVAL_VECTORIZE_POSTLOOKUP`
- reviewed candidate setting: `1`
- scorer behavior when enabled:
  - build one scorer-batch score mask
  - flatten scorer positions and targets once
  - keep lookup batched through the existing `cache.batch_lookup()` by-batch path
  - compute matched-order / alpha / probability mixing in vectorized form
  - reduce byte/token counters in batch form
  - update the matched-order histogram from batched counts
- minimal telemetry:
  - `ngram_postlookup_vectorized_batches`
  - `ngram_postlookup_vectorized_positions_total`
  - `ngram_postlookup_vectorized_elapsed_ms`

## Variables To Hold Fixed
- exact saved seed-`1337` `final_model.pt` and `final_model.int6.ptz`
- exact `eval_026` helper outside the new scorer switch
- exact `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1`
- exact `NGRAM_EVAL_BATCH_TORCH_STATS=1`
- exact `NgramEvalCache` lookup/update semantics
- `NGRAM_EVAL_MIN_ORDER=2`
- `NGRAM_EVAL_MAX_ORDER=9`
- `NGRAM_EVAL_BUCKETS=4194304`
- `NGRAM_EVAL_MIN_COUNT=2`
- `NGRAM_EVAL_CHUNK_TOKENS=1000000`
- locked alpha / entropy / order-mult settings
- legal score-first TTT settings
- tokenizer, dataset, eval protocol, export bytes
- no retraining
- no export rewrite
- no order / bucket / chunk / backend / lookup-policy / scorer-batch-size sweep

## Exact Implementation Diff Versus `eval_026`
- added one env var in `Hyperparameters`:
  - `ngram_eval_vectorize_postlookup = bool(int(os.environ.get("NGRAM_EVAL_VECTORIZE_POSTLOOKUP", "0")))`
- changed the legal scorer log line to expose `vectorize_postlookup`
- added scorer-side vectorized-postlookup telemetry accumulators:
  - `postlookup_vectorized_batches`
  - `postlookup_vectorized_positions_total`
  - `postlookup_vectorized_elapsed_ms`
- changed only `score_segments()` to:
  - preserve exact `eval_026` behavior when the switch is `0`
  - when the switch is `1`, and only on top of the already-enabled batch-lookup plus batch-torch-stats path, compute post-lookup accounting on one flattened scorer batch instead of in the per-row Python loop
  - keep `NgramEvalCache`, TTT, lookup policy, and all held-fixed settings unchanged

## Identity Checks
- Source helper from `eval_026` before copy:
  - `train_gpt.py`: `119346` bytes
  - SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`
- New helper before launch and after all runs:
  - `runs/eval_027.../train_gpt.py`: `125178` bytes
  - SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`
- Saved artifact lineage stayed unchanged before and after all runs:
  - `final_model.pt`: `106178569` bytes, `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - `final_model.int6.ptz`: `15555121` bytes, `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

## Disabled Parity
- Full-val exact result:
  - `val_loss=1.88996891`
  - `val_bpb=1.11934901`
- Delta vs `eval_026` disabled parity `1.11934940`: `-0.00000039`
- Script eval wallclock: `468349ms`
- Managed wallclock: `511s`
- Parity decision: `pass`

## Enabled Same-Helper Held-Out Control
- Frozen held-out exact result:
  - `val_loss=2.03664882`
  - `val_bpb=1.20586072`
- Telemetry:
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=1769`
  - `ngram_torch_stats_batches=1040`
  - `ngram_torch_stats_elapsed_ms=469`
  - `ngram_postlookup_vectorized_batches=0`
  - `ngram_postlookup_vectorized_elapsed_ms=0`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1139`
- Script eval wallclock: `24971ms`
- Managed wallclock: `66s`
- Control decision: `pass`

## Enabled Held-Out Screen
- Frozen held-out exact result:
  - `val_loss=2.03665257`
  - `val_bpb=1.20586294`
- Delta vs same-helper control `1.20586072`: `+0.00000222`
- Telemetry:
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=1866`
  - `ngram_torch_stats_batches=1040`
  - `ngram_torch_stats_elapsed_ms=480`
  - `ngram_postlookup_vectorized_batches=1040`
  - `ngram_postlookup_vectorized_positions_total=2097152`
  - `ngram_postlookup_vectorized_elapsed_ms=40753`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1157`
- Script eval wallclock: `24453ms`
- Managed wallclock: `67s`
- Screen decision: `controlled, proceed to full eval`

## Enabled Full Official Eval
- Exact result:
  - `val_loss=0.49164251`
  - `val_bpb=0.29117839`
- Script eval wallclock: `574202ms`
- Managed wallclock: `615s`
- Telemetry:
  - context-key precompute `resident_bytes=1984692256 elapsed_ms=20904`
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
  - average alpha on matched positions `0.64247077`
  - matched-order histogram:
    - `order_2=120864`
    - `order_3=808024`
    - `order_4=915947`
    - `order_5=767349`
    - `order_6=844813`
    - `order_7=1317753`
    - `order_8=3289964`
    - `order_9=52956834`

## Delta Summary
- Vs `eval_026`:
  - `val_bpb`: `-0.00000160`
  - script eval wallclock: `-32123ms`
  - managed wallclock: `-32s`
  - `ngram_ctx_key_precompute elapsed_ms`: `-407ms`
  - `ngram_batch_lookup_elapsed_ms`: `+462ms`
  - `ngram_torch_stats_elapsed_ms`: `-34ms`
  - `ngram_update_batch_timing elapsed_ms`: `-237ms`
  - `ngram_postlookup_vectorized_elapsed_ms`: `0 -> 1177650`
- Vs script budget:
  - `600000ms -> 574202ms` (`-25798ms`, legal)
- Vs official target `0.4416`:
  - `val_bpb`: `-0.15042161`

## Bytes
- Artifact bytes: `15555121`
- Code bytes: `125178`
- Total bytes: `15680299`
- Headroom under `16,000,000`: `319701`

## Success Metric
Primary success criterion:
- script eval wallclock `<= 600000ms`

Secondary success criterion:
- improve by at least `6325ms` vs `eval_026`

Quality guardrails:
- disabled parity within `+-0.0002`
- enabled held-out candidate within `+-0.0001` of same-helper control
- full official `val_bpb` within `+-0.0005` of `eval_026`

Outcome:
- all required controls passed
- full official BPB stayed effectively locked
- script eval improved by `32123ms` and is now legal
- managed wallclock improved by `32s` but remains `15s` above `600s`

## Expected Effect
- Recover the remaining legality gap on the locked `eval_026` line without materially changing BPB.

## Actual Result
- The intervention preserved semantics and improved BPB slightly.
- The official script eval crossed from `606325ms` to `574202ms`, so legality was recovered on the script metric.
- Other measured cost centers stayed near-locked, which supports the reviewed interpretation that the removed row-by-row Python post-lookup path was the residual bottleneck.

## Interpretation
This reviewed refinement-phase runtime-only follow-up succeeded. `eval_027` should replace `eval_026` as the active legality baseline on the locked PR `#809` evaluator line.

The new `ngram_postlookup_vectorized_elapsed_ms` counter is an absolute cumulative timing for the replacement block, not a before/after delta against the old loop. The decisive evidence is the end-to-end wallclock recovery with near-flat lookup / torch-stats / update timings.

## Next Step
Keep `eval_027` fixed as the new active legality baseline. If more runtime headroom is still useful, target a different non-overlapping cost center such as `update_batch()` or the managed-path overhead rather than scorer-side post-lookup accounting again.
