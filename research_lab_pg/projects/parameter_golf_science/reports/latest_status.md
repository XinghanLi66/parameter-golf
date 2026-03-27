# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, and the active promoted 8-GPU anchor remains `eval_038_eval035_temperature_pair` at `0.19974237`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_047_eval045_patched_helper_7gpu_control`, which patched only the copied helper’s eval-only non-divisor startup path, then ran one fresh 7-GPU promoted-line control on GPUs `1..7`.
- The fresh 7-GPU control finished with `legal_ttt_exact val_bpb=0.19974198`, which is:
  - `+0.00000012` versus fresh admissible 8-GPU control `eval_045=0.19974186`
  - `-0.00000039` versus promoted 8-GPU anchor `eval_038=0.19974237`
- The helper/checkpoint/artifact guardrail for this round:
  - patched helper `runs/eval_047_eval045_patched_helper_7gpu_control/train_gpt.py`: `126026` bytes, SHA-256 `c4a687b680df9eaff7f23c259f7e07e1da5446fab9319e3c72e3c4b59706b2ed`
  - locked source helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed controlled:
  - copied the locked helper into a fresh run directory
  - changed only the eval-only non-divisor `WORLD_SIZE` startup path
  - preserved training behavior and non-eval behavior
  - held checkpoint, artifact, scorer math, TTT hyperparameters, n-gram settings, tokenizer, dataset, export path, and runner fixed
  - changed operational subset to GPUs `1..7`, runner request count to `7`, and `torchrun --nproc_per_node=7`
- 7-GPU gate and launch result:
  - gate sample time `2026-03-27T14:12:53Z`
  - GPUs `1..7` all showed about `81007 MiB` free, `0 MiB` used, and `0%` utilization
  - GPU `0` stayed occupied by a foreign process at about `74486 MiB`, but it was outside the reviewed gate set
  - the runner then selected GPUs `1,2,3,4,5,6,7` successfully and launched the fresh control at `2026-03-27T14:13:16Z`
  - the helper emitted `eval_only_nondivisor_world_size:enabled world_size:7 forced_grad_accum_steps:1`
- Final control timing and telemetry:
  - `legal_ttt_exact val_loss=0.33725596`
  - `legal_ttt_exact val_bpb=0.19974198`
  - script wallclock `616325ms`
  - runner-managed wallclock `662808ms`
  - external wallclock `663.092s`
  - `runner_start_to_child_spawn_ms=428`
  - `child_runtime_ms=662380`
  - any-match fraction `0.98387585`
  - avg alpha `0.65461744`
  - matched-order histogram identical to `eval_045` and `eval_038`
  - `ngram_postlookup_vectorized_elapsed_ms=1110166`
- Interpretation:
  - this round is `7-GPU surrogate admissible`
  - the patched eval-only `1..7` path is now a valid surrogate regime for the promoted 8-GPU control
  - the `TTT_EPOCHS=4 -> 3` scientific question is reopened on this patched path

## Most Important Open Question
On the now-validated patched `1..7` surrogate path, does changing only `TTT_EPOCHS` from `4` to `3` preserve BPB closely enough to justify promotion as the runtime-optimized setting on the promoted legal-TTT line?

## Active Experiment ID
`eval_047_eval045_patched_helper_7gpu_control`

## Latest Result Summary
- Completed the reviewed eval-only launch-path compatibility and surrogate-validity check on the promoted legal-TTT line.
- Controlled intervention actually executed:
  - required file re-read
  - copied-helper creation
  - minimal eval-only startup patch
  - helper/checkpoint/artifact byte and SHA-256 verification
  - one clean-idle gate sample on GPUs `1..7`
  - one fresh patched 7-GPU control launch through `tools/gpu_experiment_runner.py`
  - on-disk recording of command, gate evidence, and runner logs in `runs/eval_047_eval045_patched_helper_7gpu_control/`
- Managed launch result:
  - environment `physicslm`
  - GPU allocation at launch: `7x NVIDIA L20Z`, specifically `1,2,3,4,5,6,7`
  - `legal_ttt_exact val_bpb=0.19974198`
  - script wallclock `616325ms`
  - runner-managed wallclock `662808ms`
  - external wallclock `663.092s`
  - `runner_start_to_child_spawn_ms=428`
  - `child_runtime_ms=662380`
  - any-match `0.98387585`
  - avg alpha `0.65461744`
  - `ngram_postlookup_vectorized_elapsed_ms=1110166`
  - artifact bytes stayed unchanged at `15555121`
  - patched helper code bytes were `126026`
  - total bytes on the patched evaluation-helper line are `15681147`
  - byte status remains under cap by `318853`
- Decision:
  - this round is `7-GPU surrogate admissible`
  - it answers the surrogate-validity question positively
  - it does not answer `TTT_EPOCHS=3`, because that candidate was intentionally not run in this round

## Recommended Next Step
Run the exact same-session promoted-line `TTT_EPOCHS=4 -> 3` pair on the patched `1..7` path, keeping the patched helper, checkpoint, artifact, scorer settings, and all non-epoch variables fixed.
