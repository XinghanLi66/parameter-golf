# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted 8-GPU anchor remains `eval_038_eval035_temperature_pair` at `0.19974237`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_049_eval048_buckets_pair_patched_7gpu`, which ran the reviewed same-session patched-helper `NGRAM_EVAL_BUCKETS=2097152 -> 1048576` pair on GPUs `1..7`.
- The helper/checkpoint/artifact guardrail stayed exact for both arms:
  - patched helper `runs/eval_049_eval048_buckets_pair_patched_7gpu/train_gpt.py`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - source helper from `eval_047`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- Fresh gate and launch result:
  - gate sample time `2026-03-27T15:21:54Z`
  - GPUs `1..7` all showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - no compute-app processes were present on the selected `1..7` subset
  - the fresh control then launched under run directory timestamp `20260327T152213Z`, finished cleanly, and passed admissibility versus both `eval_048` and `eval_047`
  - the immediate candidate launched under run directory timestamp `20260327T153346Z`, but failed late with a CUDA unspecified launch failure and never produced a final post-export metric
- Fresh control metrics:
  - `legal_ttt_exact val_loss=0.33725796`
  - `legal_ttt_exact val_bpb=0.19974316`
  - script wallclock `616057ms`
  - runner-managed wallclock `661647ms`
  - external wallclock `661.929s`
  - `runner_start_to_child_spawn_ms=390`
  - `child_runtime_ms=661256`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461727`
  - matched-order histogram identical to `eval_048`, `eval_047`, `eval_045`, and `eval_038`
  - `ngram_postlookup_vectorized_elapsed_ms=1112324`
- Control admissibility versus `eval_048=0.19974338`:
  - `val_bpb` delta `-0.00000022`
  - `val_loss` delta `-0.00000036`
  - script delta `-7745ms`
  - runner delta `-8262ms`
  - external delta `-8.212s`
  - avg alpha delta `+0.00000193`
  - histogram `unchanged`
  - postlookup delta `+6911ms`
  - decision `admissible`
- Control admissibility versus `eval_047=0.19974198`:
  - `val_bpb` delta `+0.00000118`
  - `val_loss` delta `+0.00000200`
  - script delta `-268ms`
  - runner delta `-1161ms`
  - external delta `-1.163s`
  - avg alpha delta `-0.00000017`
  - histogram `unchanged`
  - postlookup delta `+2158ms`
  - decision `admissible`
- Immediate candidate outcome:
  - no final `legal_ttt_exact` metric was produced
  - `stdout.log` reached chunk `1521/1893` at running `bpb=0.161550`, any-match `0.979712`, avg alpha `0.659670`, helper chunk-time `637.6s`
  - `stderr.log` then recorded `torch.AcceleratorError: CUDA error: unspecified launch failure`
  - torchrun hung in distributed teardown and never wrote candidate `metadata.json`
  - I interrupted the stuck runner at `2026-03-27T15:54:48Z` only after the failure had been captured so GPUs `1..7` were released back to `0 MiB` used / `81007 MiB` free / `0%` utilization
- Interpretation:
  - this round is `blocked`
  - the control arm was valid and admissible
  - the candidate arm is not scientifically admissible because it never produced final post-export BPB or final wallclocks
  - therefore round 24 is not evidence to `promote 1048576` and not evidence to `hold 2097152` as a bucket-geometry conclusion

## Most Important Open Question
Is the late `1048576` candidate failure on the patched `1..7` surrogate path worth a dedicated operational-diagnosis retry, or should the next reviewed refinement round move to a different single-variable evaluation question instead?

## Active Experiment ID
`eval_049_eval048_buckets_pair_patched_7gpu`

## Latest Result Summary
- Completed the reviewed same-session patched-helper bucket-count pair on the validated `1..7` surrogate path.
- Controlled intervention actually executed:
  - required file re-read
  - exact patched-helper reuse from `eval_047`
  - helper/checkpoint/artifact byte and SHA-256 verification
  - one fresh clean-idle gate sample on GPUs `1..7`
  - one fresh patched `NGRAM_EVAL_BUCKETS=2097152` control launch through `tools/gpu_experiment_runner.py`
  - admissibility checks against `eval_048` and `eval_047`
  - one immediate patched `NGRAM_EVAL_BUCKETS=1048576` candidate launch through `tools/gpu_experiment_runner.py`
  - on-disk recording of command, gate evidence, control runner metadata, and candidate failure logs in `runs/eval_049_eval048_buckets_pair_patched_7gpu/`
- Managed launch results:
  - environment `physicslm`
  - GPU allocation at launch: `7x NVIDIA L20Z`, specifically `1,2,3,4,5,6,7`
  - control `legal_ttt_exact val_bpb=0.19974316`
  - candidate `final val_bpb`: not produced because the run failed late
  - both artifacts stayed unchanged at `15555121` bytes
  - patched helper code bytes stayed `126026`
  - total bytes on this evaluation-helper line stayed `15681147`
  - byte status remains under cap by `318853`
- Decision:
  - `blocked`
  - the fresh control was admissible and reproducible
  - the immediate `1048576` candidate failed late with `CUDA error: unspecified launch failure`
  - because the candidate never finished, round 24 does not answer the intended bucket-geometry comparison

## Recommended Next Step
Do not infer a bucket conclusion from round 24. If the bucket question remains important, require a new reviewed brief for a focused operational diagnosis or controlled retry of the late `1048576` CUDA failure on the patched `1..7` path; otherwise move the next refinement round to a different single-variable evaluation question.
