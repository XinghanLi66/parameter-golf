# Proposal: Lightweight Verifier-Guided Self-Refinement for Research Coding Agents

## Goal

Evaluate whether a lightweight verifier can improve the stability of multi-step research coding agents on small reproduction tasks.

## Main hypothesis

Compared with a plain iterative coding agent, a verifier-guided agent will:

1. reduce invalid experiment launches
2. improve first-valid-run rate
3. improve final task success on small research coding tasks

## Task setting

- Build 3 to 5 small research-style tasks
- Each task should require code changes plus at least one experiment
- Tasks may include:
  - toy model training
  - result reproduction from a paper appendix
  - ablation script repair

## Baselines

1. Plain iterative coding agent
2. Planner-worker agent without verifier
3. Planner-worker agent with verifier

## Metrics

- first executable run rate
- final task success rate
- number of experiment retries
- wall-clock time
- token usage if available

## Experimental plan

1. Build a minimal task set and evaluation harness
2. Implement the plain iterative baseline
3. Implement the planner-worker baseline
4. Add a lightweight verifier that checks:
   - command validity
   - missing files
   - obvious metric mismatch
5. Compare all methods on the task set
6. Run an ablation on verifier strictness

## Compute notes

- Prefer CPU for the smallest harness checks
- Use GPU if a task actually benefits from model training or inference
- If LLaMA-Factory is available, allow LoRA experiments for a compact open model

## Deliverables

- runnable workspace
- experiment scripts
- result summaries
- notes on threats to validity and next steps
