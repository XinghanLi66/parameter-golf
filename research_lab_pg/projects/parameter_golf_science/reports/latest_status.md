# Latest Status

Update this after each substantive round.

## Current Best Evidence
- The strongest measured local BPB is still `eval_015_arch010_pr809_chunk_ngram_ttt_buckets2097152_seed1337` at `0.19974202`, but the active promoted legality line is now `eval_038_eval035_temperature_pair` at `0.19974237`, only `+0.00000035` behind that historical same-family anchor.
- Official anchor handling stays explicit and correct: `0.4416` from the 2026-03-27 snapshot remains the authoritative comparison target, while PR `#809` `0.2952` remains only a legality-pending reference.
- The newest refinement round is `eval_040_eval038_duplicate_control`, and it completed the reviewed same-session duplicate-control runtime probe on the promoted `eval_038` line.
- The helper/artifact guardrail stayed clean before and after the round:
  - helper `runs/eval_031_eval027_global_temperature_calibration/train_gpt.py`: `125663` bytes, SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`
  - checkpoint `final_model.pt`: `106178569` bytes, SHA-256 `b8291ad1608f3ad86fc6dcbbfa9753b1f0bc376935bde8b17af34acc178df63a`
  - artifact `final_model.int6.ptz`: `15555121` bytes, SHA-256 `eb062c96a4151946160731add43800617ce7fc47eb31934123a7283f8e9587e3`
- The exact experiment scope stayed within the reviewed evaluation-only duplicate-control lane:
  - no code edits
  - no export edits
  - no runner edits
  - reused the locked `eval_031` helper exactly
  - reused promoted `EVAL_LOGIT_TEMP=1.0`, `TTT_LR=0.0025`, `TTT_EPOCHS=4`, and `NGRAM_EVAL_BUCKETS=2097152`
  - changed only `RUN_ID`, runner log dir, and runner run name between `control A` and `control B`
- Fresh controls on GPUs `0,1,2,3,4,5,6,7`:
  - control A: `val_loss=0.33725588`, `val_bpb=0.19974193`, script `1316129ms`, runner `1364893ms`, external `1365195ms`
  - control B: `val_loss=0.33725882`, `val_bpb=0.19974367`, script `1249634ms`, runner `1298509ms`, external `1298755ms`
  - any-match `0.98387585`
  - control A avg alpha on matched `0.65459876`
  - control B avg alpha on matched `0.65459430`
- Decision comparisons:
  - control A vs promoted `eval_038`: `-0.00000044 BPB`, `-0.00000075 val_loss`, `+727316ms` script, `+730208ms` runner, `+730269ms` external
  - control B vs promoted `eval_038`: `+0.00000130 BPB`, `+0.00000219 val_loss`, `+660821ms` script, `+663824ms` runner, `+663829ms` external
  - control B vs control A: `+0.00000174 BPB`, `+0.00000294 val_loss`, `-66495ms` script, `-66384ms` runner, `-66440ms` external
  - control A vs drifted `eval_039`: `+127701ms` external
  - control B vs drifted `eval_039`: `+61261ms` external
- Interpretation:
  - both fresh controls stayed semantically in-family with the promoted line on BPB and telemetry
  - both fresh controls stayed in the slowdown regime rather than returning to promoted runtime
  - control A also suffered observed overlap from an external root-owned Humaneval/VLLM workload on GPU `0`, but control B ran after that overlap cleared and was still catastrophically slow
  - conclusion label is `persistent-runtime-shift`
  - `TTT_EPOCHS=3` remains unanswered on the promoted `EVAL_LOGIT_TEMP=1.0` line because the comparison is still inadmissible

## Most Important Open Question
What changed in the promoted `eval_038` runtime regime, given that exact same-session controls still reproduce BPB and telemetry but remain `~61s` to `~128s` slower than the already-drifted `eval_039` anchor and `~664s` to `~730s` slower than promoted runtime? The next round should diagnose the runtime shift itself rather than returning to `TTT_EPOCHS=4 -> 3`.

## Active Experiment ID
`eval_040_eval038_duplicate_control`

## Latest Result Summary
- Completed the reviewed duplicate-control reproducibility check on the promoted `eval_038` legality line; both exact controls finished successfully.
- Controlled intervention actually executed:
  - two fresh runner-managed exact controls at the promoted settings with `TTT_EPOCHS=4`
  - no candidate arm in this round
  - same helper, checkpoint, artifact, runner path, environment, stride, legal TTT settings, and PR809 vectorized n-gram settings as the promoted line in both successful launches
- Managed run:
  - environment: `physicslm`
  - GPU allocation: `8x NVIDIA L20Z`, specifically `0,1,2,3,4,5,6,7`
  - control A result: `legal_ttt_exact val_bpb=0.19974193`, `val_loss=0.33725588`
  - control B result: `legal_ttt_exact val_bpb=0.19974367`, `val_loss=0.33725882`
  - artifact bytes stayed unchanged at `15555121`
  - helper code bytes are `125663`
  - total bytes on the locked evaluation-helper line: `15680784`
  - byte status: under cap by `319216`
- Timing:
  - control A: `1316129ms` script, `1364893ms` runner, `1365195ms` external
  - control B: `1249634ms` script, `1298509ms` runner, `1298755ms` external
- Decision:
  - both fresh controls remained in-family on BPB and telemetry but failed runtime admissibility by about `+730.3s` and `+663.8s` external versus promoted `eval_038`
  - both fresh controls also stayed near the `eval_039` slowdown regime rather than restoring the promoted runtime band
  - control A had a visible external GPU `0` overlap, but control B still failed badly after that overlap cleared
  - label: `persistent-runtime-shift`

## Recommended Next Step
Keep `EVAL_LOGIT_TEMP=1.0` fixed as the promoted default on this helper lineage, but do not return to the `TTT_EPOCHS=4 -> 3` pair next round. First isolate the runtime-shift cause on the exact promoted line, because the dedicated epoch-count comparison is still not admissible.
