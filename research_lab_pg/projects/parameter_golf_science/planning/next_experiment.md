# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Status
Completed on `2026-03-27` as the reviewed refinement-phase orchestration-only follow-up on top of the locked `eval_027` PR `#809` legality line.

- Executed the reviewed brief materially as written:
  - created `runs/eval_028_arch010_pr809_chunk_ngram_ttt_official_eval_only_seed1337`
  - copied the exact `eval_027` helper into the new run directory
  - added one default-off top-level env switch `NGRAM_EVAL_OFFICIAL_ONLY=1`
  - changed only top-level orchestration/reporting inside `main()`
  - kept the saved seed-`1337` checkpoint/export lineage unchanged
  - ran one full official candidate in `physicslm` on `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`
  - recorded coarse helper phase timings around the single official `legal_ttt_exact` eval

## Experiment ID
`eval_028_arch010_pr809_chunk_ngram_ttt_official_eval_only_seed1337`

## Category
- evaluation

Operational subtype: `runtime-only helper-orchestration trim on locked PR #809 legality line`

## Baseline / Comparison
Primary runtime baseline:
- `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`
  - `val_bpb=0.29117839`
  - script eval wallclock `574202ms`
  - managed wallclock `615s`
  - managed minus script overhead `40.798s`

External comparison:
- official snapshot target `PR #803`: `0.4416`
- legality-pending reference `PR #809`: `0.2952`

## Hypothesis
If the remaining `15s` managed overrun after `eval_027` is mostly outside the locked scorer path, then an official-eval-only fast path will reduce managed wallclock to `<=600s` while keeping `val_bpb` within `±0.0001` of `eval_027` and leaving script eval roughly unchanged.

## Why It Might Work
- `eval_026 -> eval_027` recovered `32123ms` of script time while managed minus script overhead stayed large.
- That pointed away from the locked scorer hot path and toward helper startup, teardown, or inherited run-local work around the single scored official call.

## Minimal Intervention
Copy the exact `eval_027` helper into a fresh run directory, add one default-off env switch, and change only top-level orchestration/reporting so the enabled path runs only the final official `legal_ttt_exact` evaluation on the saved artifact and emits coarse pre/eval/post timings.

## Variables To Change
- new env control: `NGRAM_EVAL_OFFICIAL_ONLY`
- reviewed candidate setting: `1`
- top-level behavior when enabled:
  - skip full code dump to log
  - skip `nvidia-smi` logging
  - skip training-shard counting/logging
  - keep only the saved-artifact load plus final official eval path
  - emit:
    - `process_to_official_eval_start_ms`
    - `official_eval_duration_ms`
    - `official_eval_end_to_process_exit_ms`
    - `process_total_ms`

## Variables To Hold Fixed
- exact `eval_027` scorer code and n-gram mechanism
- exact saved seed-`1337` `final_model.pt` and `final_model.int6.ptz`
- exact `NGRAM_EVAL_BATCH_LOOKUP_BY_BATCH=1`
- exact `NGRAM_EVAL_BATCH_TORCH_STATS=1`
- exact `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`
- exact `NGRAM_EVAL_MIN_ORDER=2`
- exact `NGRAM_EVAL_MAX_ORDER=9`
- exact `NGRAM_EVAL_BUCKETS=4194304`
- exact `NGRAM_EVAL_MIN_COUNT=2`
- exact `NGRAM_EVAL_CHUNK_TOKENS=1000000`
- locked alpha / entropy / order-mult settings
- locked legal TTT settings
- tokenizer, dataset, stride `64`, export bytes
- no retraining
- no export rewrite
- no scorer-side algorithm change

## Exact Implementation Diff Versus `eval_027`
- added one env var in `Hyperparameters`:
  - `ngram_eval_official_only = bool(int(os.environ.get("NGRAM_EVAL_OFFICIAL_ONLY", "0")))`
- changed only `main()` / top-level eval-only orchestration so the official-only path:
  - suppresses inherited code-dump / `nvidia-smi` / train-shard logs
  - keeps only val-token setup, artifact load, and the locked final official eval
  - records coarse helper phase timing around the single official eval
- left `score_segments()`, `NgramEvalCache`, TTT math, lookup/update semantics, tokenizer, dataset, and artifact handling unchanged

## Identity Checks
- Source helper before copy:
  - `runs/eval_027.../train_gpt.py`: `125178` bytes
  - SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`
- New helper after edit:
  - `runs/eval_028.../train_gpt.py`: `126904` bytes
  - SHA-256 `e1e55335df5a188738545811fe6a03516a4629bb343ebd3e57f847598eb0d5b3`
- Saved artifact lineage stayed unchanged:
  - `final_model.pt`: `106178569` bytes, `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - `final_model.int6.ptz`: `15555121` bytes, `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`

## Enabled Full Official Eval
- Exact result:
  - `val_loss=0.49164748`
  - `val_bpb=0.29118133`
- Script eval wallclock: `579356ms`
- Managed wallclock: `616s`
- Managed minus script overhead: `36.644s`
- Helper-local phase timings:
  - process start to official-eval start: `14940ms`
  - official-eval duration: `579356ms`
  - official-eval end to process exit: `547ms`
  - helper total process time: `594842ms`
- Inferred runner-managed overhead outside helper:
  - `616000ms - 594842ms = 21158ms`
- Reused scorer telemetry:
  - `ngram_ctx_key_precompute resident_bytes=1984692256 elapsed_ms=20645`
  - `ngram_batch_lookup_call_count=30770`
  - `ngram_batch_lookup_elapsed_ms=20226`
  - `ngram_torch_stats_batches=30770`
  - `ngram_torch_stats_elapsed_ms=3297`
  - `ngram_postlookup_vectorized_batches=30770`
  - `ngram_postlookup_vectorized_elapsed_ms=1171231`
  - `ngram_update_batch_timing calls=63 elapsed_ms=32505`
  - any-match fraction `0.98387524`
  - average alpha on matched positions `0.64246944`

## Delta Summary
- Vs `eval_027`:
  - `val_bpb`: `+0.00000294`
  - script eval wallclock: `+5154ms`
  - managed wallclock: `+1s`
  - managed minus script overhead: `-4.154s`
- Vs managed budget:
  - `600s -> 616s` (`+16s`, still illegal)
- Vs helper-local `600000ms` process budget:
  - `594842ms` (`-5158ms`, helper itself is now under budget)
- Vs official target `0.4416`:
  - `val_bpb`: `-0.15041867`

## Bytes
- Artifact bytes: `15555121`
- Code bytes: `126904`
- Total bytes: `15682025`
- Headroom under `16,000,000`: `317975`

## Success Metric
Primary success criterion:
- managed wallclock `<=600s`

Quality guardrail:
- full official `val_bpb` within `±0.0001` of `eval_027`

Secondary runtime guardrails:
- script eval wallclock no worse than `eval_027` by more than `5000ms`
- managed minus script overhead reduced to `<=26s`

Outcome:
- quality guardrail passed
- managed wallclock target failed
- script eval stayed close but missed the `+5000ms` tolerance by `154ms`
- helper-local total process time fell below `600s`
- remaining miss localizes mostly to managed-path overhead outside the helper rather than more scorer or helper-harness trimming

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
