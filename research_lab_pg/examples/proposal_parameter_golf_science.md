# Proposal: Scientific Optimization Loop For Parameter Golf

## Goal

Use the upgraded planner-reviewer-worker system to improve the `parameter-golf` repository in a disciplined, hypothesis-driven way for the Parameter Golf competition.

The target codebase is the repository root at:

- `/newcpfs/lxh/parameter-golf`

The immediate objective is not to make broad model changes blindly. The immediate objective is to build a clean experimental program that can produce high-quality, non-redundant optimization steps.

## Competition objective

Optimize for the main contest metric under the actual competition constraints:

- primary metric: post-export `val_bpb`
- hard artifact cap: `16,000,000` bytes
- training budget: under 10 minutes on `8xH100 SXM`
- evaluation budget: under 10 minutes

Secondary metrics that should be tracked whenever possible:

- pre-export metric
- quantization gap
- artifact bytes
- evaluation protocol used
- approximate train time and eval time

## Scientific operating principles

1. Every proposed experiment must have a clear hypothesis.
2. Every experiment should change only a small number of factors when possible.
3. The system should accumulate knowledge and avoid redundant experiments.
4. The system must distinguish among:
   - architecture changes
   - optimization changes
   - evaluation changes
   - export / compression changes
5. The system should prefer informative experiments over flashy ones.

## Available context

The repository already contains:

- the main competition README and leaderboard
- recent top record submissions under `records/`
- `docs/sota_review.md`
- `docs/scientific_research_loop.md`

These should be treated as required context, especially for avoiding repeated exploration of already obvious ideas.

## Initial research task

For the first round, do **not** launch into broad optimization work.

Instead, use the first round to establish a scientific starting point:

1. Inspect the current root-level baseline and relevant record folders.
2. Populate the scientific memory files with:
   - best known external patterns,
   - current local baseline understanding,
   - open questions,
   - redundancy watchlist.
3. Define a clean experiment taxonomy:
   - architecture
   - optimization
   - evaluation
   - export
4. Propose exactly one high-value next experiment that is:
   - narrow,
   - falsifiable,
   - easy to compare,
   - grounded in the SOTA review.
5. Prefer not to modify the main training code in this first round unless a tiny instrumentation or bookkeeping change is strictly necessary to support the scientific loop.

## What counts as a good first experiment

A good first experiment:

- has a named baseline,
- has one primary hypothesis,
- controls non-target variables,
- produces interpretable success and failure,
- helps decide what class of optimization should come next.

Bad first experiments include:

- stacking many improvements at once,
- changing architecture and optimization and evaluation together,
- repeating a known SOTA recipe without a local question,
- proposing work that cannot be compared against a stable baseline.

## Preferred first-round deliverables

By the end of the first round, the workspace should contain:

- a filled or partially filled `planning/research_memory.md`
- a structured `planning/next_experiment.md`
- a more useful `planning/experiment_ledger.md`
- a concise `reports/latest_status.md`
- a concise `reports/comparison_summary.md`
- a single recommended next experiment for the main repo

## Guidance for interacting with the target repo

- You may inspect files in `/newcpfs/lxh/parameter-golf`.
- Avoid invasive edits to the target repo in the first round.
- If you identify a tiny instrumentation change that would materially improve scientific comparison quality, justify it explicitly before making it.

## Success criteria for this proposal

The first round is successful if it leaves behind a cleaner scientific decision process for future optimization and surfaces one concrete next experiment that should be run next on the contest model.
