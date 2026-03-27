# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest completed local metric is now `eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu` at `legal_ttt_exact val_bpb=0.14602989`, but this came from a candidate-only operational diagnosis and is **not** yet a promoted default.
- The active promoted 8-GPU anchor remains `eval_038_eval035_temperature_pair` at `0.19974237`, and the last completed validated patched-helper `2097152` control on the `1..7` surrogate path remains `eval_049` at `0.19974316`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu`, which ran the reviewed candidate-only operational diagnosis of the patched-helper `NGRAM_EVAL_BUCKETS=1048576` path on GPUs `1..7`.
- The helper/checkpoint/artifact guardrail stayed exact:
  - patched helper `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/train_gpt.py`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - source helper from `eval_049` and `eval_047`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- Fresh gate and launch result:
  - the first fresh gate sample at `2026-03-27T16:10:03Z` failed because a foreign 8-GPU workload occupied GPUs `1..7`
  - the bounded gate watch then passed at `2026-03-27T16:10:35Z`, with GPUs `1..7` clean at about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - the candidate launched under run directory timestamp `20260327T161117Z` and finished cleanly
- Completed candidate metrics:
  - `legal_ttt_exact val_loss=0.24656535`
  - `legal_ttt_exact val_bpb=0.14602989`
  - script wallclock `618438ms`
  - runner-managed wallclock `666370ms`
  - external wallclock `666.594s`
  - `runner_start_to_child_spawn_ms=395`
  - `child_runtime_ms=665975`
  - any-match fraction `0.98387635`
  - avg alpha `0.66088724`
  - matched-order histogram:
    - `order_2=17786`
    - `order_3=95312`
    - `order_4=113192`
    - `order_5=124743`
    - `order_6=175760`
    - `order_7=309994`
    - `order_8=810348`
    - `order_9=59374482`
  - `ngram_batch_lookup_elapsed_ms=14132`
  - `ngram_torch_stats_elapsed_ms=4303`
  - `ngram_postlookup_vectorized_elapsed_ms=1108473`
  - `ngram_update_batch_timing elapsed_ms=29799`
- Comparison against the prior failed `eval_049` candidate:
  - `eval_049` failed late at chunk `1521/1893` with `torch.AcceleratorError: CUDA error: unspecified launch failure` inside `score_segments()` and never wrote `metadata.json`
  - `eval_050` reached the same chunk with the same running `bpb=0.161550`, the same any-match `0.979712`, and nearly identical avg alpha `0.659664`, but did so at `487.0s` instead of `637.6s`, then finished cleanly and wrote `metadata.json`
  - the prior crash therefore did not reproduce on the exact rerun path
- External telemetry result:
  - near the end of the run at `2026-03-27T16:22:19Z`, GPUs `1..7` were using about `5367..5627 MiB` with `68..82%` utilization
  - after completion, telemetry at `16:22:24Z` and `16:22:30Z` showed GPUs `1..7` back at `0 MiB` used, about `81007 MiB` free, and `subset_apps=none`
- Interpretation:
  - this round is `operationally viable`
  - the late `1048576` crash from `eval_049` is not reproducible enough to close the setting as unstable on the patched `1..7` path
  - promotability is still unanswered because this round intentionally omitted a fresh same-session `2097152` control arm
  - the unexpectedly large completed BPB shift makes a later reviewed same-session control/candidate rerun more valuable, not less

## Most Important Open Question
Does a later fresh same-session patched-helper `2097152 -> 1048576` control/candidate pair confirm the dramatic completed `eval_050` metric on the validated `1..7` path, or does that candidate-only operational completion turn out to be non-promotable under comparison-clean conditions?

## Active Experiment ID
`eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu`

## Latest Result Summary
- Completed the reviewed candidate-only operational diagnosis on the patched-helper `NGRAM_EVAL_BUCKETS=1048576` path.
- Controlled intervention actually executed:
  - required file re-read
  - exact patched-helper reuse from `eval_049`
  - helper/checkpoint/artifact byte and SHA-256 verification
  - one fresh gate sample plus a bounded clean launch watch on GPUs `1..7`
  - full external GPU telemetry capture during the attempt
  - one exact candidate-only `NGRAM_EVAL_BUCKETS=1048576` rerun through `tools/gpu_experiment_runner.py`
  - on-disk recording of command, gate evidence, telemetry, stdout, stderr, and runner metadata in `runs/eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu/`
- Managed launch results:
  - environment `physicslm`
  - GPU allocation at launch: `7x NVIDIA L20Z`, specifically `1,2,3,4,5,6,7`
  - final `legal_ttt_exact val_bpb=0.14602989`
  - final `legal_ttt_exact val_loss=0.24656535`
  - artifact bytes stayed unchanged at `15555121`
  - patched helper code bytes stayed `126026`
  - total bytes on this evaluation-helper line stayed `15681147`
  - byte status remains under cap by `318853`
- Decision:
  - `1048576 operationally viable but needs fresh same-session comparison`
  - the prior late crash did not reproduce
  - the setting can now be evaluated in a later comparison-clean promotability round

## Recommended Next Step
If the bucket question remains important, require a later reviewed fresh same-session patched-helper `2097152 -> 1048576` control/candidate comparison on the validated `1..7` surrogate path. If not, move the next refinement round to a different single-variable evaluation question and keep `eval_050` classified as operational evidence rather than a promotion.
