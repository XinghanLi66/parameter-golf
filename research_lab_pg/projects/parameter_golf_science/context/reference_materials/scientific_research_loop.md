# Scientific Research Loop Upgrade

## What Changed

The original two-agent reference loop has been copied into `research_lab_pg/` and upgraded with a small set of scientific controls rather than a broad redesign.

Key changes:

- Added a vendored framework copy under `research_lab_pg/`.
- Upgraded workspace initialization in `research_lab_pg/scripts/init_research_workspace.py`.
- Upgraded the planner and executor contracts in:
  - `research_lab_pg/scripts/codex_research_loop.sh`
  - `research_lab_pg/scripts/codex_research_prompt.txt`
  - `research_lab_pg/scripts/codex_research_worker_prompt.txt`
- Added a lightweight pre-execution reviewer:
  - `research_lab_pg/scripts/codex_research_review_prompt.txt`
- Added support for copying external reference material such as `docs/sota_review.md` into each workspace.

## Main Weaknesses In The Original Loop

The original planner-executor workflow was useful, but not yet scientific enough for Parameter Golf iteration:

1. Memory was too weak.
   - The old ledger was only a thin table and did not consistently capture hypothesis, mechanism, changed variables, held-fixed variables, interpretation, or next step.

2. Planning was too free-form.
   - The planner was told to make progress, but not forced to produce a falsifiable experiment brief with explicit controls and failure interpretation.

3. Execution control was too loose.
   - The worker was encouraged to do real work, but not strongly constrained to isolate factors or keep change categories separate.

4. There was no critique step.
   - Nothing checked whether a proposed experiment was redundant, too bundled, or too vague before execution.

## Why These Changes Improve Scientific Quality

### Structured memory

Each workspace now starts with:

- `planning/next_experiment.md`
- `planning/experiment_ledger.md`
- `planning/research_memory.md`
- `reports/comparison_summary.md`

These files make the loop explicitly record:

- hypothesis,
- mechanism / rationale,
- changed variables,
- held-fixed variables,
- expected effect,
- actual result,
- interpretation,
- next step.

This gives the planner a compact memory that can be reused to avoid repeating already-answered experiments.

### Hypothesis-first planning

The planner is now required to output a structured experiment brief with:

- experiment category,
- baseline / comparison,
- hypothesis,
- why it might work,
- minimal intervention,
- variables to change,
- variables to hold fixed,
- success metric,
- failure interpretation,
- redundancy check.

This pushes the loop toward small, falsifiable experiments instead of generic "try a few improvements" instructions.

### Controlled execution

The executor is now explicitly told to:

- prefer the smallest justified intervention,
- avoid silently mixing architecture, optimization, evaluation, and export changes,
- narrow broad plans into controlled tests when needed,
- write structured results back into the workspace.

### Lightweight review

The loop now supports a lightweight review pass before execution.

Default flow:

`planner -> reviewer -> worker`

The reviewer does not redesign the agenda. It tightens the planner proposal by checking:

- redundancy,
- hypothesis clarity,
- variable control,
- category clarity,
- usefulness of the likely result.

## How To Use The New Workflow

Typical usage:

```bash
cd /newcpfs/lxh/parameter-golf/research_lab_pg

PROPOSAL_FILE=examples/proposal_detailed.md \
PROJECT_NAME=parameter_golf_science \
ENABLE_REVIEW=1 \
EXTRA_CONTEXT_FILES=/newcpfs/lxh/parameter-golf/docs/sota_review.md \
RUN_STARTUP_GPU_SMOKE=0 \
scripts/codex_research_loop.sh
```

Recommended workflow:

1. Put the project goal in the proposal file.
2. Pass relevant static context through `EXTRA_CONTEXT_FILES`, especially `docs/sota_review.md`.
3. Let the planner propose one primary experiment.
4. Let the reviewer reduce redundancy and tighten controls.
5. Let the worker execute the smallest informative version of that experiment.
6. Inspect:
   - `planning/experiment_ledger.md`
   - `planning/research_memory.md`
   - `reports/latest_status.md`
   - `reports/comparison_summary.md`

## Key Logic Locations

- Loop orchestration and review step:
  - `research_lab_pg/scripts/codex_research_loop.sh`
- Workspace templates and copied reference materials:
  - `research_lab_pg/scripts/init_research_workspace.py`
- Planner behavior:
  - `research_lab_pg/scripts/codex_research_prompt.txt`
- Executor behavior:
  - `research_lab_pg/scripts/codex_research_worker_prompt.txt`
- Review behavior:
  - `research_lab_pg/scripts/codex_research_review_prompt.txt`

## Example Next Experiment After Reading `docs/sota_review.md`

Below is the kind of next experiment the improved system should propose. It is intentionally narrow and falsifiable.

### Stage Diagnosis

The SOTA review suggests that current wins come from compression-aware capacity allocation, not generic tuning. A strong unanswered question for a baseline near `~1.18` is whether mixed low-bit export can save enough bytes to fund later capacity increases without immediately damaging roundtrip quality too much.

### Primary Experiment

Run a controlled export-focused ablation of `uniform int6` versus `mixed int5/int6`, changing only MLP export precision.

### Experiment Category

`export`

### Baseline / Comparison

Current best local baseline with training, evaluation mode, and architecture fixed.

### Hypothesis

Quantizing MLP weights to `int5` while keeping attention weights at `int6` will save meaningful artifact bytes with only a small roundtrip `val_bpb` penalty, making later depth or width increases feasible.

### Why It Might Work

The SOTA review shows that top runs repeatedly use more aggressive compression on the MLP side because MLP weights compress better than attention weights.

### Minimal Intervention

Change only export precision for MLP weights from `int6` to `int5`. Keep architecture, training hyperparameters, evaluation protocol, and non-MLP export rules fixed.

### Variables To Change

- MLP export precision: `int6 -> int5`

### Variables To Hold Fixed

- model depth
- MLP width
- optimizer
- warmdown
- weight decay
- evaluation protocol
- attention export precision

### Success Metric

- artifact bytes saved,
- post-export `val_bpb`,
- quantization gap versus pre-export metric.

### Failure Interpretation

If roundtrip quality degrades too much, then the current recipe is not yet quantization-friendly enough for mixed `int5/int6`, and the next step should be to improve training-for-export first rather than buying extra capacity immediately.

### Why This Is Scientifically Useful

Even a negative result is informative: it tells the system whether byte reallocation is currently bottlenecked by export precision or by training robustness.
