# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line remains `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest controlled runtime-only result is now `eval_028_arch010_pr809_chunk_ngram_ttt_official_eval_only_seed1337`.
- The `eval_028` helper/artifact guardrail stayed clean. The copied `eval_027` helper was `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`; the edited `eval_028` helper was `126904` bytes with SHA-256 `e1e55335df5a188738545811fe6a03516a4629bb343ebd3e57f847598eb0d5b3`; the saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` stayed unchanged at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The exact implementation diff versus `eval_027` stayed within the reviewed orchestration-only scope:
  - added one env var `NGRAM_EVAL_OFFICIAL_ONLY`
  - changed only top-level `main()` / eval-only orchestration
  - suppressed inherited code-dump / `nvidia-smi` / train-shard logging on the official-only path
  - added one coarse `official_eval_only_phase_timing` log
  - left scorer, TTT, n-gram lookup/update, tokenizer, dataset, checkpoint lineage, and artifact bytes unchanged
- The full official `eval_028` run scored `legal_ttt_exact val_loss=0.49164748`, `legal_ttt_exact val_bpb=0.29118133`.
- Delta summary for `eval_028` vs active baseline `eval_027`:
  - `val_bpb`: `+0.00000294`
  - script eval wallclock: `574202ms -> 579356ms` (`+5154ms`)
  - managed wallclock: `615s -> 616s` (`+1s`)
  - managed minus script overhead: `40.798s -> 36.644s` (`-4.154s`)
- The new helper-local phase split for `eval_028` was:
  - process start to official-eval start: `14940ms`
  - official-eval duration: `579356ms`
  - official-eval end to process exit: `547ms`
  - helper total process time: `594842ms`
  - inferred runner-managed overhead outside helper: `21158ms`
- Interpretation: the orchestration-only fast path reduced helper-local pre/post work to about `15.5s`, but managed legality still failed because a larger residual remains outside the helper in the managed runner path. `eval_028` is therefore informative but non-promotable.

## Most Important Open Question
If managed legality is still worth pursuing on the already script-legal `eval_027` line, can the remaining roughly `21s` of runner-managed overhead outside the helper be reduced without touching the locked scorer path?

## Active Experiment ID
`eval_028_arch010_pr809_chunk_ngram_ttt_official_eval_only_seed1337`

## Latest Result Summary
- Completed `eval_028_arch010_pr809_chunk_ngram_ttt_official_eval_only_seed1337` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_028_arch010_pr809_chunk_ngram_ttt_official_eval_only_seed1337/summary.md).
- Controlled intervention actually executed:
  - copied the exact `eval_027` helper into a fresh `eval_028` run directory
  - reused the exact saved seed-`1337` `arch_010` checkpoint/export lineage unchanged
  - added only one default-off orchestration switch `NGRAM_EVAL_OFFICIAL_ONLY`
  - changed only top-level logging/setup on the `EVAL_ONLY` path and added coarse pre/eval/post timings
  - ran one enabled managed full official candidate on `8x NVIDIA L20Z` in `physicslm`
- Managed run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z` via `tools/gpu_experiment_runner.py`
  - final enabled result: `legal_ttt_exact val_bpb=0.29118133`, `val_loss=0.49164748`
  - bytes: artifact `15555121`, code `126904`, total `15682025`
  - byte status: under cap by `317975`
- Timing:
  - final script eval wallclock: `579356ms`
  - final managed wallclock: `616s`
  - final managed minus script overhead: `36.644s`
  - helper-local phase split:
    - pre-eval `14940ms`
    - official eval `579356ms`
    - post-eval `547ms`
    - helper total `594842ms`
  - inferred runner-managed overhead outside helper: `21158ms`
- Decision:
  - BPB stayed within the reviewed guardrail, so the result is scientifically comparable to `eval_027`
  - helper-local orchestration trimming was real but insufficient
  - `eval_028` should not replace `eval_027` as the active legality baseline
  - the remaining runtime target, if pursued, is runner-managed overhead outside the helper rather than more scorer or helper-harness trimming

## Recommended Next Step
Keep `eval_027` fixed as the active legality baseline. If another runtime round is still necessary, target runner-managed overhead outside the helper rather than revisiting scorer-side code or another top-level helper-orchestration trim.
