# Research Proposal Lab For Parameter Golf

`research_lab_pg` is a vendored two-layer Codex workflow for turning a research proposal into an executable research workspace.

This copy keeps the original planner-worker structure, but adds a small set of scientific controls for Parameter Golf style research:

- structured experiment memory,
- hypothesis-first experiment proposals,
- controlled-variable execution guidance,
- a lightweight review pass before execution,
- optional copied reference material such as `docs/sota_review.md`.

It is modeled after the original proposal-lab loop, but the target here is different:

- accept proposals with very different detail levels
- let an upper-layer Codex re-plan each round
- let a lower-layer Codex actually write code, run experiments, and update artifacts
- let Codex use GPU resources through a reproducible local helper

## What it provides

- `scripts/codex_research_loop.sh`
  - the outer loop
  - each round runs `planner -> reviewer -> worker` when review is enabled
- `scripts/init_research_workspace.py`
  - bootstraps a project from a proposal file
  - creates context snapshots and reusable directories
- `scripts/gpu_experiment_runner.py`
  - selects GPUs, sets `CUDA_VISIBLE_DEVICES`, logs metadata, and runs a command
- `scripts/gpu_smoke_test.py`
  - verifies that a real CUDA backend can execute work
- prompt templates for planner and worker Codex roles
- `scripts/codex_research_review_prompt.txt`
  - lightweight critique of the planner output before execution
- two example proposal files

## Directory layout

```text
research_proposal_lab/
├── README.md
├── examples/
│   ├── proposal_brief.md
│   └── proposal_detailed.md
├── projects/                     # created at runtime
│   └── <project_name>/
│       ├── inputs/
│       ├── context/
│       ├── planning/
│       ├── experiments/
│       ├── reports/
│       ├── code/
│       ├── artifacts/
│       ├── logs/
│       ├── tools/
│       └── runs/
└── scripts/
```

## Quick start

1. Prepare a proposal markdown file.
2. Run one project:

```bash
cd /newcpfs/user/qixuan1/research_proposal_lab

PROPOSAL_FILE=examples/proposal_brief.md \
PROJECT_NAME=demo_brief \
EXPERIMENT_CONDA_ENV=loongflow_ml \
ROUNDS=3 \
scripts/codex_research_loop.sh
```

3. Inspect the generated project under `projects/demo_brief/`.

The most important scientific workspace files are:

- `planning/next_experiment.md`
- `planning/experiment_ledger.md`
- `planning/research_memory.md`
- `reports/latest_status.md`
- `reports/comparison_summary.md`
- `context/reference_materials/`

## Parameter Golf usage

To seed the loop with the local SOTA review from this repository:

```bash
cd /newcpfs/lxh/parameter-golf/research_lab_pg

PROPOSAL_FILE=examples/proposal_detailed.md \
PROJECT_NAME=parameter_golf_science \
ENABLE_REVIEW=1 \
EXTRA_CONTEXT_FILES=/newcpfs/lxh/parameter-golf/docs/sota_review.md \
RUN_STARTUP_GPU_SMOKE=0 \
scripts/codex_research_loop.sh
```

The loop should then use the copied SOTA review in `context/reference_materials/` and keep the scientific memory files updated after each round.

## Project-specific seeds

If a project needs extra planner steering, pass a custom `PLANNER_PROMPT_FILE` while keeping the generic worker prompt.

Example for the website-to-agent-native project inspired by CLI-Anything:

```bash
cd /newcpfs/user/qixuan1/research_proposal_lab

PROPOSAL_FILE=examples/proposal_web_agent_native.md \
PLANNER_PROMPT_FILE=examples/prompts/web_agent_native_planner_seed.txt \
PROJECT_NAME=web-agent-native \
RUN_STARTUP_GPU_SMOKE=0 \
EXTRA_ARGS="--add-dir /newcpfs/user/qixuan1/research_proposal_lab/CLI-Anything" \
scripts/codex_research_loop.sh
```

See `examples/web_agent_native_quickstart.md` for a fuller explanation of the parameters and the remaining user decisions.

## Proposal detail levels

The initializer writes `context/proposal_profile.json` and classifies the input roughly as:

- `idea_only`
- `partial_plan`
- `detailed_plan`

The planner prompt tells Codex to react differently:

- sparse proposal: operationalize assumptions, tasks, baselines, and success criteria first
- medium proposal: close missing pieces and start executing minimal experiments
- detailed proposal: prioritize implementation, experiments, ablations, and evidence

## GPU execution

All GPU jobs should go through `tools/gpu_experiment_runner.py` inside each project workspace.

Example:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 4 \
  --min-free-memory-gb 40 \
  --conda-env loongflow_ml \
  --log-dir logs/manual_runs \
  --run-name qwen_lora \
  -- torchrun --nproc_per_node 4 train.py
```

CPU-only commands can also use the same helper:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 0 \
  --log-dir logs/manual_runs \
  --run-name cpu_eval \
  -- python eval.py
```

## LLaMA-Factory example

If `llamafactory-cli` is installed in the selected environment, Codex can call it through the same helper:

```bash
python tools/gpu_experiment_runner.py \
  --gpus 2 \
  --conda-env loongflow_ml \
  --log-dir logs/manual_runs \
  --run-name llamafactory_lora \
  -- llamafactory-cli train examples/lora/qwen_lora.yaml
```

## Notes

- The current machine snapshot is discovered at runtime, so the code works even if the visible GPU count changes.
- On this machine, runtime detection may see fewer GPUs than the eventual 8-card deployment. The helper selects from the GPUs that are actually visible at execution time.
- `codex_research_loop.sh` can optionally run a startup GPU smoke test before the planner/worker loop.
- Review can be disabled with `ENABLE_REVIEW=0`, but it is enabled by default in this vendored copy because the goal is cleaner scientific iteration rather than maximum autonomy.
