# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active legality baseline on the locked PR `#809` line is now `eval_031_eval027_global_temperature_calibration`.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest scored refinement round is `eval_031_eval027_global_temperature_calibration`.
- The `eval_031` helper/artifact guardrail stayed clean. The exact source `eval_027` helper was `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`; the copied edited `eval_031` helper is `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`; the saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` stayed unchanged before and after all runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The exact experiment scope stayed within the reviewed evaluation-only calibration lane:
  - copied the locked `eval_027` helper into fresh `eval_031`
  - added one default-off scoring knob `EVAL_LOGIT_TEMP`
  - applied it only to neural scoring logits before probability computation and before neural-to-n-gram mixing
  - changed no training, export, cache update, or runner-path logic
  - reused one fixed non-official calibration slice from the frozen `eval_009` held-out train shard
  - ran the five-point calibration grid and then exactly one full official candidate
- Calibration-slice summary on the fixed `2097152`-token held-out shard:
  - `T=0.95 -> 1.20029274`
  - `T=0.975 -> 1.20275434`
  - `T=1.00 -> 1.20587508`
  - `T=1.025 -> 1.20954568`
  - `T=1.05 -> 1.21377823`
  - locked same-helper held-out control from `eval_027`: `1.20586072`
  - `T=1.0` parity drift vs locked same-helper control: `+0.00001436`
  - selected temperature: `0.95`
  - held-out gain of selected `0.95` vs `1.0`: `-0.00558234`
- The single full official run at `EVAL_LOGIT_TEMP=0.95` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49102869`
  - `legal_ttt_exact val_bpb=0.29081485`
  - script eval wallclock `584865ms`
  - runner managed wallclock `628844ms`
  - external top-level wallclock `629.130s`
- Official comparison summary:
  - vs locked `eval_027`: `0.29117839 -> 0.29081485` (`-0.00036354`)
  - vs fresh `eval_030`: `0.29117961 -> 0.29081485` (`-0.00036476`)
  - vs `eval_027` runtime: `+10663ms` script, `+13844ms` managed
  - the primary success criterion passed because full official `val_bpb` is below `0.29117839`
  - the more ambitious `>=0.0005` gain target did not pass
- Interpretation: this is a real calibration win on the PR809 legality line, not selector overfit and not parity failure. `EVAL_LOGIT_TEMP=0.95` is conditionally promotable on this line and `eval_031` becomes the new active single-seed legality baseline.

## Most Important Open Question
Does the new `EVAL_LOGIT_TEMP=0.95` improvement on the locked PR809 legality line remain stable on a fresh full official confirmation against `T=1.0`, or is a second full-val rerun needed before promoting this calibration as the default evaluation setting?

## Active Experiment ID
`eval_031_eval027_global_temperature_calibration`

## Latest Result Summary
- Completed `eval_031_eval027_global_temperature_calibration` in [summary.md](/newcpfs/lxh/parameter-golf/research_lab_pg/projects/parameter_golf_science/runs/eval_031_eval027_global_temperature_calibration/summary.md).
- Controlled intervention actually executed:
  - edited only the copied `eval_031` helper
  - added one default-off `EVAL_LOGIT_TEMP`
  - calibrated only on the fixed non-official `eval_009` held-out slice
  - launched exactly one full official candidate after the slice gate passed
- Managed runs:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - selected official candidate: `EVAL_LOGIT_TEMP=0.95`
  - selected official result: `legal_ttt_exact val_bpb=0.29081485`, `val_loss=0.49102869`
  - artifact bytes stayed unchanged at `15555121`
  - copied helper code bytes are `125663`
  - total bytes on the edited evaluation helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - official script eval wallclock: `584865ms`
  - official managed wallclock: `628844ms`
  - official external top-level wallclock: `629.130s`
- Decision:
  - the fixed calibration slice selected `T=0.95`
  - the selected temperature transferred to a full official improvement
  - `eval_031` is the new active single-seed legality baseline
  - nearby scalar-temperature sweeps should stop until a fresh confirmation is run or promotion is accepted

## Recommended Next Step
Keep the locked PR809 legality stack fixed and, if promotion confidence is needed, run one fresh full official confirmation of `EVAL_LOGIT_TEMP=0.95` against `T=1.0` on the same saved artifact and pinned GPUs. If that confirms, lock `T=0.95` as the default on this line and move the next refinement round to a genuinely different single-variable question rather than another nearby scalar calibration.
