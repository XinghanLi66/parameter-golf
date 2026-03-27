# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-26` as the reviewed refinement-phase scorer-side tensorization follow-up on the locked `eval_025` PR `#809` legality line.

- Executed the reviewed brief materially as written:
  - created `runs/eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`
  - copied the exact `eval_025` helper into the new run directory
  - changed only one scorer-side runtime lever: exact neural `target_logp` and entropy are now optionally computed once per scorer batch in torch instead of being recomputed per row in the Python loop
  - kept the saved seed-`1337` checkpoint/export lineage unchanged
  - ran one disabled full-val parity check
  - ran one enabled same-helper held-out control with `NGRAM_EVAL_BATCH_TORCH_STATS=0` on the frozen `eval_009` slice
  - ran one enabled held-out screen with `NGRAM_EVAL_BATCH_TORCH_STATS=1` on that same slice
  - ran one enabled full official torch-stats-on eval in `physicslm` on `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`

## Experiment ID
`eval_026_arch010_pr809_chunk_ngram_ttt_batch_torch_stats_seed1337`

## Category
- evaluation

Operational subtype: `runtime-only scorer-side tensorization on locked PR #809 legality line`

## Baseline / Comparison
Primary baseline:
- `eval_025_arch010_pr809_chunk_ngram_ttt_batch_lookup_by_batch_seed1337`
  - `val_bpb=0.29117983`
  - script eval wallclock `614228ms`
  - managed wallclock `657s`

Continuity context:
- `eval_018_arch010_pr809_chunk_ngram_ttt_sparse_updates_seed1337`
  - `val_bpb=0.29117845`
  - script eval wallclock `630501ms`
  - managed wallclock `671s`
- `eval_021_arch010_pr809_chunk_ngram_ttt_fused_lookup_scratch_seed1337`
  - `val_bpb=0.29117893`
  - script eval wallclock `641669ms`
  - managed wallclock `682s`

External comparison:
- official snapshot target `PR #803`: `0.4416`

Required semantic control baselines:
- disabled parity equivalent from `eval_025`: `1.11934793`
- locked enabled same-slice baseline from `eval_025`: `1.20584885`

## Hypothesis
If the remaining `eval_025` legality miss is materially driven by scorer-side per-row neural-stat extraction, then replacing repeated per-row `softmax` plus `log_softmax` work with one exact batched torch pass for `target_logp` and entropy will recover a meaningful fraction of the missing `14228ms` without materially changing BPB.

## Why It Might Work
- `eval_025` already removed most outer `batch_lookup()` overhead, but runtime still missed legality.
- The n-gram-specific timed sections in `eval_025` did not explain the full gap versus the locked no-ngram legal-TTT scorer.
- The validated leaderboard-style stack is already fixed here: eval-time backoff, entropy-adaptive mixing, score-first legality, and TTT. This round is not a motif search; it is a refinement-phase scorer cleanup.
- The cleanest remaining scorer-side lever was to tensorize exact neural-stat extraction after the already-validated forward pass and scorer-batch lookup path.

## Minimal Intervention
Copy the exact `eval_025` helper into a fresh run directory, add one default-off env switch, and change only `score_segments()` so exact `target_logp` and entropy are computed once per scorer batch in torch and then reused inside the existing row loop. Keep `NgramEvalCache`, cached context keys, sparse touched-bin updates, scorer-batch lookup batching, score-first legality, TTT settings, alpha math, chunking, tokenizer, dataset, and artifact lineage fixed.

## Variables To Change
- new env control: `NGRAM_EVAL_BATCH_TORCH_STATS`
- reviewed candidate setting: `1`
- scorer behavior when enabled:
  - after the batched forward pass, compute `log_probs = torch.log_softmax(logits.float(), dim=-1)` once for the scorer batch
  - compute exact `target_logp` for all rows with one batched gather
  - compute exact entropy for all rows from the same batched `log_probs`
  - reuse those exact per-row slices inside the existing n-gram mixing/accounting path
- minimal telemetry:
  - `ngram_torch_stats_batches`
  - `ngram_torch_stats_elapsed_ms`
  - `ngram_torch_stats_scored_positions_total`
  - inherited `ngram_batch_lookup_*`
  - inherited `ngram_update_batch_timing`
  - inherited `ngram_ctx_key_precompute`

## Variables To Hold Fixed
- exact saved seed-`1337` `final_model.pt` and `final_model.int6.ptz`
- exact `eval_025` helper outside the new scorer-stats switch
- exact `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1` behavior
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

## Exact Implementation Diff Versus `eval_025`
- added one env var in `Hyperparameters`:
  - `ngram_eval_batch_torch_stats = bool(int(os.environ.get("NGRAM_EVAL_BATCH_TORCH_STATS", "0")))`
- changed the legal scorer log line to expose `batch_torch_stats`
- added scorer-side torch-stats telemetry accumulators:
  - `torch_stats_batches`
  - `torch_stats_elapsed_ms`
  - `torch_stats_scored_positions_total`
- changed only `score_segments()` to:
  - preserve exact `eval_025` behavior when the switch is `0`
  - when the switch is `1`, compute `log_probs`, gathered `target_logp`, and entropy once for the full scorer batch in torch
  - reuse those exact tensors inside the existing row loop
  - keep alpha mixing, loss accounting, byte accounting, histogram updates, and `NgramEvalCache` unchanged
- added only the reviewed final torch-stats telemetry log line

## Identity Checks
- Source helper from `eval_025` before copy:
  - `train_gpt.py`: `116390` bytes
  - SHA-256 `2d32bdbf1d28834b12ec82da04860b4faccc019f599373ee4393b703b1be2cd2`
- New helper before launch and after all runs:
  - `runs/eval_026.../train_gpt.py`: `119346` bytes
  - SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`
- Saved artifact lineage stayed unchanged before and after all runs:
  - `final_model.pt`: `106178569` bytes, `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - `final_model.int6.ptz`: `15555121` bytes, `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

## Disabled Parity
- Full-val exact result:
  - `val_loss=1.88996957`
  - `val_bpb=1.11934940`
- Delta vs locked `eval_025` disabled-parity-equivalent baseline `1.11934793`: `+0.00000147`
- Script eval wallclock: `469094ms`
- Managed wallclock: `511s`
- Parity decision: `pass`

## Enabled Same-Helper Held-Out Control
- Frozen held-out exact result:
  - `val_loss=2.03663777`
  - `val_bpb=1.20585418`
- Delta vs locked `eval_025` held-out batching-on baseline `1.20584885`: `+0.00000533`
- Telemetry:
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=2019`
  - `ngram_batch_lookup_positions_total=2097152`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=0`
  - `ngram_torch_stats_elapsed_ms=0`
  - `ngram_torch_stats_scored_positions_total=0`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1172`
  - any-match fraction `0.52316141`
  - average alpha on matched positions `0.29492219`
- Script eval wallclock: `25567ms`
- Managed wallclock: `66s`
- Control decision: `pass`

## Enabled Held-Out Screen
- Frozen held-out exact result:
  - `val_loss=2.03662617`
  - `val_bpb=1.20584731`
- Delta vs same-helper control `1.20585418`: `-0.00000687`
- Telemetry:
  - `ngram_batch_lookup_call_count=1040`
  - `ngram_batch_lookup_elapsed_ms=2226`
  - `ngram_batch_lookup_positions_total=2097152`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=1040`
  - `ngram_torch_stats_elapsed_ms=489`
  - `ngram_torch_stats_scored_positions_total=2097152`
  - `ngram_update_batch_timing calls=3 elapsed_ms=1286`
  - any-match fraction `0.52316141`
  - average alpha on matched positions `0.29491858`
- Screen decision: `controlled, proceed to full eval`

## Enabled Full Official Eval
- Exact result:
  - `val_loss=0.49164521`
  - `val_bpb=0.29117999`
- Script eval wallclock: `606325ms`
- Managed wallclock: `647s`
- Telemetry:
  - context-key precompute `resident_bytes=1984692256 elapsed_ms=21311`
  - `ngram_batch_lookup_call_count=30770`
  - `ngram_batch_lookup_elapsed_ms=19874`
  - `ngram_batch_lookup_positions_total=62021632`
  - `ngram_batch_lookup_max_positions_per_call=4032`
  - `ngram_torch_stats_batches=30770`
  - `ngram_torch_stats_elapsed_ms=3257`
  - `ngram_torch_stats_scored_positions_total=62021632`
  - `ngram_update_batch_timing calls=63 elapsed_ms=32367`
  - any-match fraction `0.98387524`
  - average alpha on matched positions `0.64246912`
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
- Vs `eval_025`:
  - `val_bpb`: `+0.00000016`
  - script eval wallclock: `-7903ms`
  - managed wallclock: `-10s`
  - `ngram_batch_lookup_elapsed_ms`: `20386 -> 19874` (`-512ms`)
  - `ngram_ctx_key_precompute`: `21285 -> 21311` (`+26ms`)
  - `ngram_update_batch_timing`: `32269 -> 32367` (`+98ms`)
- Vs `eval_018`:
  - `val_bpb`: `+0.00000154`
  - script eval wallclock: `-24176ms`
  - managed wallclock: `-24s`
- Vs official target `0.4416`:
  - `val_bpb`: `-0.15042001`

## Bytes
- Artifact bytes: `15555121`
- Code bytes: `119346`
- Total bytes: `15674467`
- Headroom under `16,000,000`: `325533`

## Success Metric
Primary success criterion:
- script eval wallclock `<= 600000ms`

Secondary success criterion:
- managed wallclock `<= 600s`

Quality guardrails:
- disabled parity within `+-0.0002`
- enabled same-helper held-out control within `+-0.0001`
- enabled full-val within `+-0.0005` of `eval_025`
- still clearly below official `0.4416`

Outcome:
- disabled parity passed
- enabled same-helper held-out control passed
- enabled held-out torch-stats-on screen passed
- enabled full-val BPB stayed effectively locked to `eval_025`
- runtime improved materially but remained illegal
- scorer-side torch stats consumed nontrivial time but did not account for the entire remaining legality gap

## Expected Effect
- Reduce scorer-side neural-stat extraction overhead enough to recover legality
- Keep BPB near the locked `eval_025` line
- Show nontrivial batched torch-stats telemetry with lookup/update timings otherwise roughly locked

## Actual Result
- Semantics stayed controlled:
  - disabled parity delta `+0.00000147`
  - same-helper held-out control delta vs locked `eval_025` control `+0.00000533`
  - torch-stats-on held-out delta vs same-helper control `-0.00000687`
- Full quality stayed effectively locked:
  - `val_bpb 0.29117983 -> 0.29117999`
- Runtime improved materially but did not recover legality:
  - script time `614228ms -> 606325ms`
  - managed wallclock `657s -> 647s`
- New telemetry showed nontrivial scorer-side torch-stat work:
  - held-out `ngram_torch_stats_elapsed_ms=489`
  - full-val `ngram_torch_stats_elapsed_ms=3257`

## Interpretation
The required controls passed, so the helper edit is valid and directly comparable to `eval_025`. The hypothesis is supported in the narrower sense that scorer-side neural-stat extraction was a real remaining bottleneck: batched exact torch-side scorer stats recovered another `7903ms` of end-to-end runtime without moving BPB. But the gain was not large enough to clear the locked `10 min` script budget. This should be treated as a positive runtime probe that becomes the new legality baseline, not as a full legality recovery.

## Classification
`runtime-improved-but-still-illegal`

## Next Step
Keep `eval_026` as the active legality-recovery baseline instead of falling back to `eval_025`. The next controlled round should target a different non-overlapping runtime cost on top of this batched scorer plus batched torch-stats line rather than revisiting scorer-side neural-stat extraction.
