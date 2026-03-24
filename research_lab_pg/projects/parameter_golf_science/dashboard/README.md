# How To Read This Dashboard

This dashboard tracks the `parameter_golf_science` research loop at three different levels:

## 1. Run batches

`Run Batches` shows each invocation of the outer research loop, for example:

- `20260324T035545Z`: one 10-round optimization batch
- `1 / 10`, `2 / 10`, ...: progress within that batch

Different batches can coexist on the page. A later 10-round batch does not erase an earlier 1-round batch.

## 2. Experiments

Experiment IDs describe the *type* of intervention:

- `eval_001`: an evaluation-protocol experiment
- `opt_001`: an optimization/training recipe experiment
- `arch_001`: an architecture experiment
- `export_001`: an export / quantization / compression experiment

The numeric suffix is just the sequence number within that category.

Examples in the current project:

- `eval_001` trained and evaluated a real checkpoint, so it can appear in both comparisons and training-job charts.
- `export_001`, `export_002`, `export_003` are export-side experiments built on top of an existing checkpoint, so they usually appear in experiment summaries and comparison tables, but not in training-job loss curves unless they also launch a fresh training run.

## 3. Metrics sections

The most important sections are:

- `Real Local Best BPB`: the best *successful local* `val_bpb` seen so far from structured comparison rows. Lower is better.
- `Local BPB Curve`: blue is each successful real candidate value; green is the best-so-far envelope. Smoke runs, failed rows, and non-`val_bpb` metrics such as quantization-gap helper rows are skipped.
- `Experiment Highlights`: short recent takeaways from the experiment ledger.
- `Comparison Highlights`: short recent metric deltas from the structured comparison summary.
- `Training Job Curves`: only logs produced by actual `train_gpt.py` training jobs.
- `Latest SOTA Snapshot`: live summary of the current public leaderboard and recurring motifs, refreshed from the latest Parameter Golf repo state before iteration starts.

## Comparison categories

`Full Comparison Summary` now uses both colored badges and tab-style filters.

The category split is:

- `External`: published repo references and leaderboard context
- `Eval`: evaluation-protocol comparisons such as `non_overlapping` vs `sliding_window`
- `Export`: quantization, artifact size, and post-export quality comparisons
- `Optimization`: training recipe changes such as warmdown or scheduler adjustments
- `Infra`: asset audits, blocker checks, and storage/discovery diagnostics
- `Other`: anything that does not fit the main buckets cleanly

In this project, `Export` specifically means post-training artifact-side optimization, for example:

- changing the outer container, such as `zlib-9` vs `zstd-22`
- changing quantization precision, such as `uniform int8` vs `uniform int6`
- using selective precision policies, such as `mlp_int6_else_int8`
- measuring the byte / quality tradeoff after export on a fixed checkpoint

So `Export` is not "train a different model". It is "keep the checkpoint fixed, then change how the submission artifact is serialized / quantized / compressed and measure the resulting bytes and post-export `val_bpb`".

## Why `Training Job Curves` may still only show `eval_001`

That section is intentionally narrow: it only renders runs that produced real step-by-step training logs.

So if later experiments only:

- export an existing checkpoint,
- change quantization,
- compare artifact size,
- or rerun evaluation without retraining,

they will not create a new training-loss plot. They still show up elsewhere on the dashboard.

## Where to inspect raw details

If you want the full record behind a card or curve, inspect:

- `records/experiment_ledger.md`: hypothesis, actual result, interpretation, next step
- `records/comparison_summary.md`: structured metric deltas
- `runs/`: per-run stdout/stderr, training logs, proposal snapshots, reviewer notes

## Watcher and README maintenance

The dashboard is expected to be kept live by a single watcher process that regenerates `index.html` and `status.json`.

Rules:

- keep exactly one active dashboard watcher for this project
- prefer a moderate watcher cadence such as `60s` unless actively debugging the dashboard
- before restarting the watcher, kill older `generate_progress_dashboard.py` watchers for `parameter_golf_science`
- after changing dashboard rendering logic, regenerate the dashboard immediately instead of waiting for a stale file to refresh
- when dashboard semantics change, update this README in the same edit so the page and the docs stay aligned
- if a metric or section label changes, document what it now means here

## Publishing

There are now two ways to share this dashboard:

- temporary tunnel sharing from the research machine
- GitHub Pages deployment from the repository

GitHub Pages setup in this repo:

- workflow file: `.github/workflows/deploy-parameter-golf-dashboard.yml`
- published directory: `research_lab_pg/projects/parameter_golf_science/dashboard/`
- trigger: push to `main` when the dashboard files change, or manual workflow dispatch

Expected public URL for this repo:

- `https://xinghanli66.github.io/parameter-golf/`

Important note:

- GitHub Pages serves the last pushed dashboard snapshot, not the live local filesystem
- so the local watcher can keep updating `index.html`, but the public Pages site only changes after you push the updated dashboard files to GitHub

## Reading the curve correctly

The top BPB chart is not "one point per round no matter what". It is "one point per successful real local `val_bpb` comparison row".

That means:

- a round can contribute zero points if it crashes or never produces a usable `val_bpb`
- one round can contribute multiple points if it records multiple real local comparisons
- best-so-far can stay flat while the blue line gets worse, which means the new attempt failed to beat the current best
- the curve uses the full comparison history, even though the expanded comparison table on the page only shows the most recent rows

## Clickable chart points

The main BPB chart and the per-run loss/BPB charts support point inspection:

- hover a point to enlarge it and see a tooltip
- click a point to pin the tooltip and keep the point highlighted
- press `Enter` or space on a focused point for the same behavior
- clicking a `Local BPB Curve` point also scrolls to the matching row in `Full Comparison Summary`
- clicking a `Loss Curve` or `BPB Curve` point also scrolls to the parent training-run card
