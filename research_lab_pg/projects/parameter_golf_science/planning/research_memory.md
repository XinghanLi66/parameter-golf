# Research Memory

This file is the compact scientific memory for the project. Keep it updated so the planner can avoid redundant work.

## Working SOTA Anchor - 2026-03-27

**TARGET SOTA: PR #803 at `0.4416 BPB`** - Complementary Training + Backoff N-gram + TTT.  
PR `#809` at `0.2952` remains legality-pending and is not the official target.

This line is in **REFINEMENT phase**:
- strongest measured local run: `eval_015=0.19974202`
- promoted quality baseline on the locked legality line: `eval_035=0.20079980`
- freshest admissible runner-managed control on the promoted line: `eval_036 control=0.20079853`
- freshest attempted control on the promoted line: `eval_037 control=0.20079880`, but it failed the reviewed external-wallclock gate
- previous same-helper promoted anchor on the same helper lineage: `eval_035=0.20079980`
- previous legality baseline: `eval_027=0.29117839`
- newest refinement round: `eval_037 promoted-line temperature check -> drift-stop before candidate`
- newest comparison: `eval_037 control=0.20079880 vs promoted eval_035=0.20079980 with external drift +23201ms`
- official-anchor gap on the active legality line: `0.20079980 - 0.4416 = -0.24080020`
- open problem: launcher bypass, TTT epoch count, refreshed bucket geometry, and downward `TTT_LR` retuning are closed on this helper lineage, but promoted-line scorer-temperature testing remains unanswered because `eval_037` stopped on the fresh-control external gate. Until that question is rerun cleanly, hold `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152` fixed operationally.

`context/reference_materials/URGENT_ngram_backoff_breakthrough.md` remains authoritative for the n-gram mechanism family.  
`context/reference_materials/latest_sota_snapshot.md` remains authoritative for the official comparison target.

## Newest Critical Result - `eval_037_eval035_temperature_pair`

- The reviewed refinement-phase promoted-line temperature check executed cleanly through the required fresh-control gate with no code edits, but it stopped before the candidate because the control failed admissibility on external wallclock. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the control run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `TTT_LR=0.0025` fixed
  - kept `TTT_EPOCHS=4` fixed
  - kept `NGRAM_EVAL_BUCKETS=2097152` fixed
  - planned to change only `EVAL_LOGIT_TEMP` between `0.95` and `1.0`
  - actually ran only the fresh `0.95` control because the reviewed gate failed before candidate launch
- The fresh runner-managed control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.33904036`
  - `legal_ttt_exact val_bpb=0.20079880`
  - script eval wallclock `603417ms`
  - runner-managed wallclock `648159ms`
  - external top-level wallclock `648378ms`
- Required comparisons:
  - control vs promoted `eval_035`: `-0.00000100 BPB`, `+21145ms` script, `+23146ms` runner-managed, `+23201ms` external
  - control vs fresh `eval_036` control: `+0.00000027 BPB`, `+21405ms` script, `+22112ms` runner-managed, `+22331ms` external
  - control vs historical `eval_015`: `+0.00105678 BPB`
- Emitted telemetry stayed in-family with the promoted line:
  - any-match fraction `0.98387585`
  - avg alpha on matched `0.63990743`
  - order histogram identical to the promoted `2097152`-bucket pattern
- Decision label: `drift-stop`.
- Interpretation: semantics stayed in-family, but the fresh control exceeded the reviewed `+15000ms` external tolerance by `8201ms`, so the `EVAL_LOGIT_TEMP=1.0` candidate was not launched. This round is not evidence for or against changing the promoted-line temperature default; it is only evidence that fresh-control runtime drift prevented a clean answer.

## Previous Critical Result - `eval_036_eval035_ttt_lr_pair`

- The reviewed refinement-phase TTT-learning-rate pair executed cleanly on the promoted `eval_035` legality lineage with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - kept `NGRAM_EVAL_BUCKETS=2097152` fixed
  - changed only `TTT_LR` between `0.0025` and `0.0020`
  - changed only operational identifiers such as `RUN_ID`, runner log dir, and runner run name
- The fresh runner-managed control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.33903990`
  - `legal_ttt_exact val_bpb=0.20079853`
  - script eval wallclock `582012ms`
  - runner-managed wallclock `626047ms`
  - external top-level wallclock `626047ms` via runner-total proxy, with metadata UTC timestamps independently implying about `626000ms`
- The fresh control passed the reviewed admissibility gate versus promoted `eval_035`:
  - `val_bpb` drift `-0.00000127`
  - external wallclock drift `+870ms`
- The fresh runner-managed candidate with `TTT_LR=0.0020` scored:
  - `legal_ttt_exact val_loss=0.33907413`
  - `legal_ttt_exact val_bpb=0.20081880`
  - script eval wallclock `591247ms`
  - runner-managed wallclock `633936ms`
  - external top-level wallclock `634143ms`
- Required comparisons:
  - candidate vs fresh control: `+0.00002027 BPB`, `+9235ms` script, `+7889ms` runner-managed, `+8096ms` external
  - control vs promoted `eval_035`: `-0.00000127 BPB`, `-260ms` script, `+1034ms` runner-managed, `+870ms` external
  - candidate vs historical `eval_015`: `+0.00107678 BPB`
- Emitted telemetry stayed essentially flat across the pair:
  - any-match fraction `0.98387585 -> 0.98387585`
  - avg alpha on matched `0.63990797 -> 0.63995303`
- Decision label: `hold`.
- Interpretation: the promoted `2097152`-bucket legality line still prefers `TTT_LR=0.0025`. Downward TTT-LR retuning is now closed negatively on this helper lineage unless a future round changes the operating point materially.

## Previous Critical Result - `eval_035_eval031_bucket_geometry_pair`

- The reviewed refinement-phase bucket-geometry pair executed cleanly on the locked promoted `eval_031` legality lineage at `EVAL_LOGIT_TEMP=0.95` with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only `NGRAM_EVAL_BUCKETS` between `4194304` and `2097152`
  - changed only operational identifiers such as `RUN_ID`, runner log dir, and runner run name
- The fresh runner-managed control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49102809`
  - `legal_ttt_exact val_bpb=0.29081449`
  - script eval wallclock `591126ms`
  - runner-managed wallclock `634475ms`
  - external top-level wallclock `634633ms`
- The fresh control passed the reviewed admissibility gate versus `eval_033`:
  - `val_bpb` drift `+0.00000069`
  - external wallclock drift `+6494ms`
- The fresh runner-managed candidate with `NGRAM_EVAL_BUCKETS=2097152` scored:
  - `legal_ttt_exact val_loss=0.33904205`
  - `legal_ttt_exact val_bpb=0.20079980`
  - script eval wallclock `582272ms`
  - runner-managed wallclock `625013ms`
  - external top-level wallclock `625177ms`
- Required comparisons:
  - candidate vs fresh control: `-0.09001469 BPB`, `-8854ms` script, `-9462ms` runner-managed, `-9456ms` external
  - candidate vs promoted `eval_032`: `-0.09001291 BPB`, `-2604ms` script, `-2169ms` runner-managed, `-2244ms` external
  - candidate vs historical `eval_015`: `+0.00105778 BPB`, `-81685ms` script, roughly `-80s` runner-managed
- Emitted telemetry also shifted materially on the stronger line:
  - any-match fraction `0.98387524 -> 0.98387585`
  - avg alpha on matched `0.62766972 -> 0.63990334`
  - order histogram concentrated even more mass in `order_9`
- Decision label: `promote`.
- Interpretation: smaller bucket geometry transfers extremely strongly to the promoted `T=0.95` legality line and should now be the default on this helper lineage. `eval_015` still remains the absolute best same-family bucket result, but the promoted helper has now nearly matched it while preserving the newer scorer-path stack.

## Previous Critical Result - `eval_034_eval031_ttt_epochs3_candidate`

- The reviewed refinement-phase epoch-count ablation executed cleanly on the locked promoted `eval_031` legality lineage at `EVAL_LOGIT_TEMP=0.95` with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after the run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed
  - changed only `TTT_EPOCHS` from `4` to `3`
  - changed only operational identifiers such as `RUN_ID`, runner log dir, and runner run name
- The fresh runner-managed candidate in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49109611`
  - `legal_ttt_exact val_bpb=0.29085478`
  - script eval wallclock `514515ms`
  - runner-managed wallclock `558261ms`
  - external top-level wallclock `558444ms`
- Required comparisons:
  - candidate vs fresh `eval_033` runner control: `+0.00004098 BPB`, `-70937ms` script, `-69707ms` runner-managed, `-69695ms` external
  - candidate vs promoted `eval_032`: `+0.00004207 BPB`, `-70361ms` script, `-68921ms` runner-managed, `-68977ms` external
- Decision label: `runtime-only operational win`.
- Interpretation: reducing to `TTT_EPOCHS=3` buys a very large runtime gain of about `70s`, but the fourth epoch still buys a small quality gain on the promoted line. Keep `TTT_EPOCHS=4` as the quality default, remember `TTT_EPOCHS=3` as the runtime-optimized variant, and move the next refinement round to a different single-variable question.

## Previous Critical Result - `eval_033_eval031_direct_launch_pair`

- The reviewed refinement-phase launcher-path control pair executed cleanly on the locked promoted `eval_031` legality lineage at `EVAL_LOGIT_TEMP=0.95` with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - kept `EVAL_LOGIT_TEMP=0.95` fixed in both arms
  - changed only the outer launcher path between fresh control `runner` and fresh candidate `direct launch`
  - changed only operational identifiers such as `RUN_ID` and capture directories
- The fresh runner control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49102692`
  - `legal_ttt_exact val_bpb=0.29081380`
  - script eval wallclock `585452ms`
  - runner-managed wallclock `627968ms`
  - external top-level wallclock `628139ms`
- The fresh control passed the reviewed admissibility gate against `eval_032`:
  - `val_bpb` drift `+0.00000109` vs `0.29081271`
  - external wallclock drift `+718ms` vs `627421ms`
- The direct-launch candidate recovered the exact wrapped child command from the fresh control metadata and reused the same cwd, same `physicslm`, and same pinned GPUs via `CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7`. The only wrapped-command token difference was the allowed `RUN_ID`.
- The fresh direct-launch candidate scored:
  - `legal_ttt_exact val_loss=0.49102993`
  - `legal_ttt_exact val_bpb=0.29081558`
  - script eval wallclock `583370ms`
  - external top-level wallclock `625537ms`
- Required comparisons:
  - candidate vs fresh control: `+0.00000178 BPB`, `-2082ms` script, `-2602ms` external
  - fresh control vs `eval_032`: `+0.00000109 BPB`, `+718ms` external
  - candidate vs `eval_032`: `+0.00000287 BPB`, `-1884ms` external
- Decision label: `negative`.
- Interpretation: launcher bypass on the promoted `eval_031` `T=0.95` line preserves BPB but only saves `2.602s` externally, below the reviewed `<3s -> negative` threshold. Direct launch should therefore not become the new legality/runtime baseline on this line.

## Previous Critical Result - `eval_032_eval031_temperature_confirmation_pair`

- The reviewed refinement-phase fresh official confirmation pair executed cleanly on the locked `eval_031` legality lineage with no code edits. The helper stayed fixed at `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved checkpoint and artifact also stayed fixed before and after both runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed single-variable lane:
  - reused the exact locked `eval_031` helper with no edits
  - reused the exact same checkpoint, artifact, runner path, environment, tokenizer, dataset, stride, legal TTT settings, and PR809 vectorized n-gram settings
  - changed only `EVAL_LOGIT_TEMP` between fresh official control `1.0` and fresh official candidate `0.95`
  - changed only `RUN_ID`, log dir, and run name as operational bookkeeping
- Fresh same-helper full official control in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49164677`
  - `legal_ttt_exact val_bpb=0.29118091`
  - script eval wallclock `591399ms`
  - runner-managed wallclock `633253ms`
  - external top-level wallclock `633409ms`
- Fresh same-helper full official candidate at `EVAL_LOGIT_TEMP=0.95` on the same GPUs scored:
  - `legal_ttt_exact val_loss=0.49102508`
  - `legal_ttt_exact val_bpb=0.29081271`
  - script eval wallclock `584876ms`
  - runner-managed wallclock `627182ms`
  - external top-level wallclock `627421ms`
- Required comparisons:
  - fresh `T=0.95` vs fresh `T=1.0`: `0.29118091 -> 0.29081271` (`-0.00036820`)
  - fresh `T=0.95` vs prior `eval_031`: `0.29081485 -> 0.29081271` (`-0.00000214`)
  - fresh `T=1.0` vs `eval_027`: `0.29117839 -> 0.29118091` (`+0.00000252`)
  - fresh `T=1.0` vs `eval_030`: `0.29117961 -> 0.29118091` (`+0.00000130`)
  - runtime vs `eval_027`:
    - fresh `T=1.0`: `+17197ms` script, `+18253ms` runner-managed
    - fresh `T=0.95`: `+10674ms` script, `+12182ms` runner-managed
- Fresh-control admissibility passed cleanly because the fresh `T=1.0` control stayed far within the reviewed `0.0002` drift band against both `eval_027` and `eval_030`.
- Decision label: `promote`.
- Interpretation: this is a clean confirmatory result, not drift-limited and not another one-off selected run. `EVAL_LOGIT_TEMP=0.95` is now the promoted default on the locked `eval_031` PR809 legality line, and nearby scalar-temperature tuning should be considered closed on this line.

## Previous Critical Result - `eval_031_eval027_global_temperature_calibration`

- The reviewed refinement-phase temperature calibration ablation executed cleanly on the locked `eval_027` PR809 legality line. The exact source helper was verified first at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The copied edited `eval_031` helper changed only to `125663` bytes with SHA-256 `2dea839e4045da88c3e1ae4b6696fbe12d31e5697ace2812509b530dce1d16ce`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` stayed unchanged before and after all runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff stayed inside the reviewed single-variable evaluation lane:
  - copied `eval_027` into fresh `eval_031`
  - added one default-off env var `EVAL_LOGIT_TEMP`
  - applied it only to neural scoring logits immediately before `log_softmax` / `softmax` inside the PR809 scorer
  - left TTT adaptation loss, cache updates, n-gram alpha logic, training, export, checkpoint, and artifact untouched
- This round reused the exact frozen non-official held-out slice from `eval_009`:
  - source shard `/newcpfs/lxh/parameter-golf/data/datasets/fineweb10B_sp1024/fineweb_train_000000.bin`
  - source start token offset `8388608`
  - copied token count `2097153`
  - scored token count `2097152`
  - shard SHA-256 `8b5e92cca71fcfb03dff3a5b2cbf37b25e15a476e8218d253006f1bbcb4db556`
- Calibration sweep on that fixed slice in `physicslm` on GPUs `0,1,2,3,4,5,6,7` produced:
  - `T=0.95 -> 1.20029274`
  - `T=0.975 -> 1.20275434`
  - `T=1.00 -> 1.20587508`
  - `T=1.025 -> 1.20954568`
  - `T=1.05 -> 1.21377823`
- `T=1.0` parity stayed clean: the locked same-helper held-out control from `eval_027` was `1.20586072`, so the new `T=1.0` result drifted by only `+0.00001436`. The best non-`1.0` temperature was `T=0.95`, beating `T=1.0` on the fixed slice by `0.00558234`, which passed the reviewed `0.0002` gate by a wide margin.
- Exactly one full official candidate was then run at `T=0.95`. It scored:
  - `legal_ttt_exact val_loss=0.49102869`
  - `legal_ttt_exact val_bpb=0.29081485`
  - script eval wallclock `584865ms`
  - runner managed wallclock `628844ms`
  - external wallclock `629.130s`
- Official comparisons:
  - vs locked `eval_027`: `0.29117839 -> 0.29081485` (`-0.00036354`)
  - vs fresh `eval_030` control: `0.29117961 -> 0.29081485` (`-0.00036476`)
  - script runtime vs `eval_027`: `+10663ms`
  - managed runtime vs `eval_027`: `+13844ms`
- Decision: this is a controlled positive calibration result, not selector overfit. The selected `T=0.95` transferred from the fixed non-official slice to a real full official BPB improvement. The primary success criterion passed, but the more ambitious `>=0.0005` improvement target was not met. Treat `eval_031` as the new active single-seed legality baseline and do not retire the temperature motif on the PR809 line.

## Previous Controlled Negative Result - `eval_030_eval027_direct_launcher_ablation`

- The reviewed refinement-phase direct-launcher ablation was executable as written, but it stopped at the required fresh-control gate rather than reaching the candidate. The helper stayed unchanged at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged before and after the control run at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled experiment scope stayed exactly inside the reviewed evaluation-only lane:
  - no repo code edits
  - no helper edits
  - no scorer edits
  - no export edits
  - recovered the exact locked child command from prior `eval_029` metadata
  - reused one fresh shared `RUN_ID` and the exact `eval_027` helper path
  - measured top-level wallclock externally while also preserving runner metadata
- The fresh official control rerun in `physicslm` on GPUs `0,1,2,3,4,5,6,7` scored:
  - `legal_ttt_exact val_loss=0.49164458`
  - `legal_ttt_exact val_bpb=0.29117961`
  - script eval wallclock `583199ms`
  - runner managed wallclock `626554ms`
  - external top-level wallclock `626721ms`
- Gate check vs historical `eval_027`:
  - `val_bpb` drift `+0.00000122` -> pass
  - managed wallclock drift `+11554ms` -> fail
  - reviewed allowance was only `+10000ms`, so the control missed the gate by `1554ms`
- Per the reviewed brief, the direct-launch candidate was not run after that gate failure. This round must therefore be interpreted as environment drift rather than launcher evidence.
- Decision: keep `eval_027` as the active legality baseline, and do not treat `eval_030` as either a positive or a negative direct-launch result. The direct-launcher hypothesis remains unanswered.

## Previous Controlled Negative Result - `eval_029_eval027_runner_minpath_seed1337`

- The reviewed refinement-phase runner-path ablation is still answered directly on the exact `eval_027` helper/artifact lineage. The helper stayed unchanged at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff stayed inside the reviewed runner-only scope:
  - edited only `tools/gpu_experiment_runner.py`
  - added one default-off switch `--minimal-runner`
  - added the same runner timing fields in both arms:
    - `runner_start_to_child_spawn_ms`
    - `child_runtime_ms`
    - `child_exit_to_runner_exit_ms`
    - `runner_total_ms`
  - kept child command, env, cwd, stdout/stderr file capture, exit propagation, and artifact paths unchanged
  - allowed minimal mode to skip only console mirroring and the extra pre-query bookkeeping
- The fresh official control rerun answered the stability gate cleanly enough to compare:
  - `legal_ttt_exact val_loss=0.49164510`
  - `legal_ttt_exact val_bpb=0.29117992`
  - script eval wallclock `582051ms`
  - managed wallclock `624825ms`
  - drift vs historical `eval_027`: `+0.00000153 val_bpb`, `+9825ms` managed
- A first minimal-mode attempt with a different `RUN_ID` was discarded because the child command and helper log destination were not strictly identical. The final candidate reran with the exact same child command as control and changed only the outer runner switch.
- The corrected final candidate scored:
  - `legal_ttt_exact val_loss=0.49164536`
  - `legal_ttt_exact val_bpb=0.29118007`
  - script eval wallclock `583407ms`
  - managed wallclock `625998ms`
- Final control-vs-candidate deltas were:
  - `val_bpb`: `+0.00000015`
  - script eval wallclock: `+1356ms`
  - managed wallclock: `+1173ms`
  - `runner_start_to_child_spawn_ms`: `427 -> 180` (`-247ms`)
  - `child_runtime_ms`: `624397 -> 625818` (`+1421ms`)
  - `child_exit_to_runner_exit_ms`: `0 -> 0`
- The exact `eval_027` helper intentionally remained untouched, so the fresh arms do not emit helper-local `process_total_ms`. The closest helper-timed historical anchor remains `eval_028`, which measured `process_total_ms=594842` and inferred outside-helper residual `21158ms`.
- Decision: do not promote the new minimal runner mode. This is a controlled negative result for the repo-controlled runner-path hypothesis inside the runner itself.

## Previous Positive Baseline Result - `eval_027_arch010_pr809_chunk_ngram_ttt_vectorized_postlookup_seed1337`

- The reviewed refinement-phase scorer-side post-lookup vectorization follow-up is now answered directly on the exact `eval_026` helper/artifact lineage. The copied source helper from `eval_026` was `119346` bytes with SHA-256 `62c19517ea4278a89f4b89f93277f176452a72e55edd315db352df36b4ea25ba`. The new `eval_027` helper stayed fixed before and after launch at `125178` bytes with SHA-256 `bbfe961cf13ad485c4e2a335b6e2cbe0b9523882dc88a35dcbfcb20e20b7bc8b`. The saved seed-`1337` `final_model.pt` and `final_model.int6.ptz` also stayed unchanged before and after all runs at `106178569` bytes / `b8291ad1...` and `15555121` bytes / `eb062c96...`.
- The controlled code diff versus `eval_026` stayed inside the reviewed single-variable scope:
  - added one env var: `NGRAM_EVAL_VECTORIZE_POSTLOOKUP`
  - preserved exact `eval_026` behavior when the switch is `0`
  - changed only `score_segments()` so the switch `1` path vectorizes the remaining matched-order, alpha, probability-mixing, byte-accounting, and histogram work across the scorer batch after the already-validated batch-lookup and batch-torch-stats paths
  - left `NgramEvalCache`, scorer-batch lookup batching, TTT, and all other accounting semantics untouched
  - added only the requested vectorized-postlookup telemetry
- The required disabled parity gate passed cleanly. With `NGRAM_EVAL_ENABLED=0`, the copied helper scored `legal_ttt_exact val_bpb=1.11934901`, only `-0.00000039` versus the locked `eval_026` disabled-parity reference `1.11934940`, at `468349ms` script wallclock and `511s` managed.
- The required same-helper held-out control passed cleanly on the frozen `eval_009` slice. With `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=0`, the helper scored `legal_ttt_exact val_bpb=1.20586072`, with `ngram_batch_lookup_call_count=1040`, `ngram_batch_lookup_elapsed_ms=1769`, `ngram_torch_stats_elapsed_ms=469`, `ngram_postlookup_vectorized_elapsed_ms=0`, and `ngram_update_batch_timing calls=3 elapsed_ms=1139`.
- The enabled held-out candidate also stayed fully controlled. With `NGRAM_EVAL_VECTORIZE_POSTLOOKUP=1`, it scored `legal_ttt_exact val_bpb=1.20586294`, only `+0.00000222` versus the same-helper control, with `ngram_postlookup_vectorized_batches=1040`, `ngram_postlookup_vectorized_positions_total=2097152`, and `ngram_postlookup_vectorized_elapsed_ms=40753`, so the reviewed stop gate did not trigger.
- The enabled full official run scored `legal_ttt_exact val_loss=0.49164251`, `legal_ttt_exact val_bpb=0.29117839`, with script eval wallclock `574202ms` and managed wallclock `615s`. That keeps BPB effectively locked to `eval_026` (`-0.00000160 val_bpb`) while improving runtime materially (`-32123ms` script, `-32s` managed) and, critically, making the script path legal.
- Final enabled full-val telemetry stayed nearly locked in the pre-existing measured blocks:
  - `ngram_ctx_key_precompute resident_bytes=1984692256 elapsed_ms=20904`
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
- Final matched-order behavior stayed on the validated `eval_026` line: any-match fraction `0.98387524`, average alpha `0.64247077`, and histogram `order_2=120864`, `order_3=808024`, `order_4=915947`, `order_5=767349`, `order_6=844813`, `order_7=1317753`, `order_8=3289964`, `order_9=52956834`.
- The run remained under the byte cap at `15555121` artifact bytes, `125178` code bytes, `15680299` total, leaving `319701` bytes of headroom.
- Decision: promote `eval_027` as the new active legality baseline. The controls passed, BPB stayed locked, and the official script wallclock is now legal by `25798ms`. Managed wallclock still sits `15s` above `600s`, so any next runtime round should target extra headroom or managed-path overhead rather than scorer-side post-lookup bookkeeping again.

## What Is Already Answered On The Locked PR `#809` Legality Line

- `eval_014`: lowering max order helped runtime only modestly and cost too much BPB.
- `eval_015`: halving buckets changed semantics strongly and stayed runtime-illegal.
- `eval_016`: coarser chunk updates barely helped runtime and regressed BPB.
- `eval_017`: cached context-key reuse was a real runtime win and preserved BPB.
- `eval_018`: sparse touched-bin `update_batch()` preserved BPB and recovered another `15494ms` script time.
- `eval_019`: exact deduplicated lookup gathers preserved BPB but made runtime worse than `eval_018`.
- `eval_020`: exact cached full-key reuse preserved BPB and sped up the hot path, but the added `1.98 GB` tables plus precompute cost erased the gain and left the full run slightly slower than `eval_018`.
- `eval_021`: exact fused scratch-backed `batch_lookup()` preserved BPB and passed both gates, but the full run still regressed versus `eval_018`.
- `eval_022`: exact CUDA-resident tables plus exact CUDA lookup/update execution preserved BPB and passed both gates, but the full run regressed sharply versus `eval_018`, so backend locality was answered negatively.
- `eval_023`: same-helper gate-off control passed, but a global `seg_entropy >= 3.0` pre-lookup gate collapsed full-val BPB to `0.59711635` while still missing runtime legality, so simple global lookup eligibility should be considered answered negatively.
- `eval_024`: saturating `uint16` tables preserved the held-out controls and full-val BPB, but full runtime worsened slightly and full-val saturation telemetry was nontrivial, so count-table precision should be considered answered negatively as a legality lever.
- `eval_025`: scorer-side lookup batching preserved the held-out controls and full-val BPB, slashed lookup call count and lookup elapsed time, and improved end-to-end runtime materially, but still missed the script budget by `14228ms`; this line should be kept as the new active runtime baseline rather than closed as a negative.
- `eval_026`: scorer-side batched exact torch stats preserved the held-out controls and full-val BPB, recovered another `7903ms` script time on top of `eval_025`, and measured `ngram_torch_stats_elapsed_ms=3257`, but still missed the script budget by `6325ms`; it is now superseded by `eval_027`.
- `eval_027`: scorer-side post-lookup vectorization preserved the held-out controls and full-val BPB, recovered `32123ms` script time on top of `eval_026`, and brought the official script eval to `574202ms`; this was the prior active legality baseline before `eval_031`.
- `eval_028`: helper-only official-eval orchestration trimming preserved full-val BPB and reduced helper-local pre/post overhead to about `15.5s`, but managed wallclock stayed `616s` because about `21.2s` now localizes outside the helper in the managed runner path; do not promote it over `eval_027`.
- `eval_029`: a default-off minimal runner mode preserved the exact child command and full official BPB but reduced pre-spawn time by only `247ms` and still worsened managed wallclock by `1173ms`; do not spend another immediate round on nearby repo-controlled runner micro-trims.
- `eval_030`: the direct-launcher ablation did not reach its candidate because the fresh control missed the reviewed managed-wallclock gate by `1554ms`; treat this as drift, not as evidence for or against direct launch.
- `eval_031`: scoring-only neural-logit temperature scaling on the locked PR809 legality line was locally positive and selected `T=0.95`; it is now superseded by `eval_032`, which cleanly confirmed the same setting on a fresh full official control/candidate pair.
- `eval_032`: fresh same-helper full official control/candidate confirmation on the locked `eval_031` line promoted `EVAL_LOGIT_TEMP=0.95` as the default. The fresh control stayed admissible, the fresh candidate won by `0.00036820 BPB`, and nearby scalar-temperature tuning on this line should now be treated as closed.
- `eval_033`: fresh admissible runner control plus direct-launch candidate on the promoted `eval_031` `T=0.95` line preserved BPB but saved only `2602ms` externally, which is below the reviewed `3s` floor; launcher bypass should now be treated as answered negatively on this line.
- `eval_034`: fresh runner-managed `TTT_EPOCHS=3` on the promoted `eval_031` `T=0.95` line worsened BPB by `+0.00004098` versus fresh `eval_033` but saved about `70s` end-to-end, so epoch count is now closed as quality-default `4` versus runtime-optimized `3`.

## Best Next Step

Keep the promoted `eval_035` legality line as the active baseline with `EVAL_LOGIT_TEMP=0.95`, `TTT_EPOCHS=4`, `TTT_LR=0.0025`, and `NGRAM_EVAL_BUCKETS=2097152`.  
Remember `TTT_EPOCHS=3` only as a runtime-optimized operational variant, and remember that downward `TTT_LR` retuning and launcher-path reruns are already answered on this lineage. The one still-open nearby question is the promoted-line temperature check `0.95 -> 1.0`, but it must be retried only after obtaining a fresh in-gate control.
