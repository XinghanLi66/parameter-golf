# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest completed local metric remains `eval_050_eval049_buckets1048576_operational_rerun_patched_7gpu` at `legal_ttt_exact val_bpb=0.14602989`, but this came from a candidate-only operational diagnosis and is **not** yet a promoted default.
- The active promoted 8-GPU anchor remains `eval_038_eval035_temperature_pair` at `0.19974237`, and the freshest admissible patched-helper `2097152` control on the `1..7` surrogate path is now `eval_051` at `0.19974343`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_051_eval050_buckets_pair_confirm_patched_7gpu`, which ran the reviewed fresh same-session patched-helper `2097152 -> 1048576` bucket confirmation pair on GPUs `1..7`.
- The helper/checkpoint/artifact guardrail stayed exact:
  - patched helper `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/train_gpt.py`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - source helper from `eval_049` and `eval_050`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- Fresh gate, control, and handoff result:
  - the initial gate passed at `2026-03-27T16:39:09Z`, with GPUs `1..7` clean at about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - the fresh `2097152` control launched under run directory timestamp `20260327T164002Z` and finished cleanly
  - the immediate post-control handoff sample also passed at `2026-03-27T16:51:56Z`
- Fresh control metrics:
  - `legal_ttt_exact val_loss=0.33725841`
  - `legal_ttt_exact val_bpb=0.19974343`
  - script wallclock `617197ms`
  - runner-managed wallclock `665584ms`
  - external wallclock `665.848s`
  - `runner_start_to_child_spawn_ms=649`
  - `child_runtime_ms=664935`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461559`
  - matched-order histogram:
    - `order_2=60166`
    - `order_3=346841`
    - `order_4=373090`
    - `order_5=332096`
    - `order_6=395043`
    - `order_7=644544`
    - `order_8=1634957`
    - `order_9=57234849`
  - `ngram_batch_lookup_elapsed_ms=17414`
  - `ngram_torch_stats_elapsed_ms=4366`
  - `ngram_postlookup_vectorized_elapsed_ms=1109722`
  - `ngram_update_batch_timing elapsed_ms=30758`
- Control admissibility:
  - versus `eval_049`, BPB was only `+0.00000027`
  - versus `eval_048`, BPB was only `+0.00000005`
  - any-match stayed identical to both, the matched-order histogram stayed identical, and the timing fields stayed in-family
- Candidate invalidation evidence:
  - the candidate launched cleanly at `2026-03-27T16:52:21Z`, but the first contamination sample arrived at `2026-03-27T16:53:37Z`
  - foreign PIDs `1873822..1873828` appeared on GPUs `1..7` alongside the candidate PIDs `1869880..1869886`
  - contamination escalated across later samples; by `2026-03-27T16:58:43Z` and `16:58:48Z`, GPUs `1..7` were at `100%` utilization with about `36.5..38.9 GiB` foreign memory plus about `5.3..5.6 GiB` candidate memory per GPU
  - I interrupted the candidate rather than allow a dirty final metric
  - latest captured candidate stdout only reached chunk `221/1893` at running `bpb=0.509815`, any-match `0.860559`, avg alpha `0.629725`, helper chunk-time `321.8s`
  - no candidate `metadata.json`, final `val_loss`, or final `val_bpb` was produced
- Interpretation:
  - this round is `invalid pair`
  - the fresh `2097152` control remains admissible on the patched `1..7` surrogate path
  - the `2097152 -> 1048576` bucket question is still unanswered because the candidate arm lost comparison cleanliness after a clean handoff
  - partial dirty candidate logs must not be treated as promotability evidence

## Most Important Open Question
Can a later fresh same-session patched-helper `2097152 -> 1048576` control/candidate pair be kept clean through both arms on the validated `1..7` path, so the bucket-geometry question can finally be answered without contamination?

## Active Experiment ID
`eval_051_eval050_buckets_pair_confirm_patched_7gpu`

## Latest Result Summary
- Completed the reviewed fresh same-session patched-helper bucket confirmation pair.
- Controlled intervention actually executed:
  - required file re-read
  - exact patched-helper reuse from `eval_049`
  - helper/checkpoint/artifact byte and SHA-256 verification
  - one fresh clean gate on GPUs `1..7`
  - one fresh `2097152` control through `tools/gpu_experiment_runner.py`
  - immediate admissibility check versus `eval_049` / `eval_048`
  - one immediate clean handoff sample
  - one immediate `1048576` candidate launch through `tools/gpu_experiment_runner.py`
  - separate external telemetry capture for both arms
  - on-disk recording of command, gate evidence, handoff evidence, telemetry, stdout, stderr, and runner metadata where available in `runs/eval_051_eval050_buckets_pair_confirm_patched_7gpu/`
- Managed control results:
  - environment `physicslm`
  - GPU allocation at launch: `7x NVIDIA L20Z`, specifically `1,2,3,4,5,6,7`
  - final control `legal_ttt_exact val_bpb=0.19974343`
  - final control `legal_ttt_exact val_loss=0.33725841`
  - artifact bytes stayed unchanged at `15555121`
  - patched helper code bytes stayed `126026`
  - total bytes on this evaluation-helper line stayed `15681147`
  - byte status remains under cap by `318853`
- Decision:
  - `invalid pair`
  - the fresh control was admissible, but the candidate arm became contaminated after a clean handoff
  - the bucket-geometry question remains open because no clean final candidate metric was allowed

## Recommended Next Step
If the bucket question remains important, require a later reviewed fresh same-session patched-helper `2097152 -> 1048576` control/candidate comparison on the validated `1..7` surrogate path only when GPUs `1..7` can remain isolated through both arms. Do not treat `eval_051` as evidence to promote or reject `1048576`; it is an invalidated pair with a valid control.
