# Proposal: Scientific Optimization Loop For Parameter Golf

## Goal

Use the planner-reviewer-worker system to improve the `parameter-golf` repository and **surpass the current SOTA on the Parameter Golf leaderboard**.

The target codebase is the repository root at:

- `/newcpfs/lxh/parameter-golf`

The primary objective is to close the gap to SOTA as fast as possible. The system should operate in two phases:
- **Aggressive phase** (local best BPB is more than ~0.02 above SOTA): reproduce and stack proven SOTA techniques from the leaderboard, even if multiple categories are touched together.
- **Refinement phase** (local best BPB is within ~0.02 of SOTA): switch to tight single-variable experiments to find improvements beyond the known SOTA stack.

Before every proposal, read `context/reference_materials/latest_sota_snapshot.md` to get the current leaderboard state. This snapshot is refreshed before every iteration run.

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

## Research task

Each round should advance the local BPB toward — and eventually past — the current SOTA. The system is past the initial setup phase.

In each round:

1. Read `context/reference_materials/latest_sota_snapshot.md` to get the freshest leaderboard state.
2. Determine the current phase (aggressive or refinement) based on the gap between local best BPB and current SOTA.
3. In **aggressive phase**: identify the highest-leverage technique(s) from the SOTA stack not yet applied locally. Implement them. It is acceptable to bundle multiple proven techniques.
4. In **refinement phase**: propose exactly one narrow, falsifiable experiment grounded in the SOTA review.
5. Always update the five scientific memory files after each experiment.

## What counts as a good experiment

A good experiment:

- has a named baseline (local BPB before the change),
- targets a specific SOTA technique or hypothesis,
- produces a measurable post-export `val_bpb` result,
- records what was changed and what was held fixed.

## Guidance for interacting with the target repo

- The main training script is `/newcpfs/lxh/parameter-golf/train_gpt.py`.
- Modifications to the training script are expected and encouraged when they implement SOTA techniques.
- Always validate with post-export `val_bpb`, not just pre-export train loss.

## Success criteria

A round is successful if it produces a measurable improvement in post-export `val_bpb`, or produces a clear negative result that eliminates a hypothesis and informs the next step.
