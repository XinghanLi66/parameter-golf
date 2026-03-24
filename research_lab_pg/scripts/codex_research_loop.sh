#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_PROJECTS_DIR="${LAB_ROOT}/projects"

PLANNER_PROMPT_FILE="${PLANNER_PROMPT_FILE:-${PROMPT_FILE:-${SCRIPT_DIR}/codex_research_prompt.txt}}"
WORKER_PROMPT_FILE="${WORKER_PROMPT_FILE:-${SCRIPT_DIR}/codex_research_worker_prompt.txt}"
REVIEWER_PROMPT_FILE="${REVIEWER_PROMPT_FILE:-${SCRIPT_DIR}/codex_research_review_prompt.txt}"
SKILLS_DIR="${SKILLS_DIR:-${LAB_ROOT}/skills}"
PROJECT_NAME="${PROJECT_NAME:-}"
PROJECT_ROOT="${PROJECT_ROOT:-}"
PROPOSAL_FILE="${PROPOSAL_FILE:-}"
ROUNDS="${ROUNDS:-5}"
SLEEP_SECONDS="${SLEEP_SECONDS:-3}"
MODEL="${MODEL:-gpt-5.4}"
ENABLE_SEARCH="${ENABLE_SEARCH:-1}"
WEB_SEARCH_MODE="${WEB_SEARCH_MODE:-live}"
BYPASS_ALL_GUARDRAILS="${BYPASS_ALL_GUARDRAILS:-1}"
USE_FULL_AUTO="${USE_FULL_AUTO:-0}"
SANDBOX_MODE="${SANDBOX_MODE:-danger-full-access}"
USE_EPHEMERAL="${USE_EPHEMERAL:-0}"
CONTINUE_ON_ERROR="${CONTINUE_ON_ERROR:-0}"
EXTRA_ARGS="${EXTRA_ARGS:-}"
COLOR="${COLOR:-never}"
EXPERIMENT_CONDA_ENV="${EXPERIMENT_CONDA_ENV:-loongflow_ml}"
RUN_STARTUP_GPU_SMOKE="${RUN_STARTUP_GPU_SMOKE:-1}"
STARTUP_SMOKE_REQUIRED="${STARTUP_SMOKE_REQUIRED:-1}"
STARTUP_SMOKE_GPUS="${STARTUP_SMOKE_GPUS:-1}"
STARTUP_SMOKE_MIN_FREE_MEMORY_GB="${STARTUP_SMOKE_MIN_FREE_MEMORY_GB:-10}"
STARTUP_SMOKE_MATRIX_SIZE="${STARTUP_SMOKE_MATRIX_SIZE:-768}"
ENABLE_REVIEW="${ENABLE_REVIEW:-1}"
EXTRA_CONTEXT_FILES="${EXTRA_CONTEXT_FILES:-}"

PHASE_EXIT_CODE=0
PHASE_LAST_MESSAGE=""
PHASE_STDOUT_LOG=""
PHASE_STDERR_LOG=""
PHASE_META_FILE=""

usage() {
  cat <<'EOF'
Usage:
  scripts/codex_research_loop.sh

Required environment:
  PROPOSAL_FILE=/path/to/proposal.md

Optional overrides:
  PROJECT_NAME=my_project
  PROJECT_ROOT=/abs/path/to/project_root
  ROUNDS=5
  EXPERIMENT_CONDA_ENV=loongflow_ml
  ENABLE_REVIEW=1
  REVIEWER_PROMPT_FILE=/path/to/review_prompt.txt
  EXTRA_CONTEXT_FILES=/path/to/sota_review.md:/path/to/notes.md
  RUN_STARTUP_GPU_SMOKE=1
  STARTUP_SMOKE_REQUIRED=1
  STARTUP_SMOKE_GPUS=1
  MODEL=gpt-5.4
  ENABLE_SEARCH=1
  EXTRA_ARGS='--add-dir /some/path'

Examples:
  PROPOSAL_FILE=examples/proposal_brief.md scripts/codex_research_loop.sh
  PROPOSAL_FILE=examples/proposal_detailed.md PROJECT_NAME=verifier_study ROUNDS=3 scripts/codex_research_loop.sh
EOF
}

sanitize_name() {
  local raw="$1"
  raw="${raw,,}"
  raw="${raw// /-}"
  raw="$(printf '%s' "$raw" | tr -cs 'a-z0-9._-' '-')"
  raw="${raw#-}"
  raw="${raw%-}"
  if [[ -z "$raw" ]]; then
    raw="project"
  fi
  printf '%s\n' "$raw"
}

append_section() {
  local title="$1"
  local file_path="$2"
  local output_file="$3"

  if [[ -f "$file_path" ]]; then
    {
      echo
      echo "===== $title ====="
      cat "$file_path"
      echo
    } >> "$output_file"
  fi
}

append_directory_sections() {
  local title_prefix="$1"
  local directory_path="$2"
  local output_file="$3"
  local file_path
  local file_list=()

  if [[ ! -d "$directory_path" ]]; then
    return 0
  fi

  shopt -s nullglob
  file_list=("$directory_path"/*)
  shopt -u nullglob

  for file_path in "${file_list[@]}"; do
    if [[ -f "$file_path" ]]; then
      append_section "${title_prefix}: $(basename "$file_path")" "$file_path" "$output_file"
    fi
  done
}

run_startup_gpu_smoke() {
  local smoke_output_json="$WORKDIR/context/startup_gpu_smoke.json"
  local smoke_runner_json="$WORKDIR/context/startup_gpu_smoke_runner.json"
  local exit_code

  set +e
  python "$WORKDIR/tools/gpu_experiment_runner.py" \
    --gpus "$STARTUP_SMOKE_GPUS" \
    --min-free-memory-gb "$STARTUP_SMOKE_MIN_FREE_MEMORY_GB" \
    --conda-env "$EXPERIMENT_CONDA_ENV" \
    --cwd "$WORKDIR" \
    --log-dir "$WORKDIR/logs/gpu_smoke" \
    --run-name startup_gpu_smoke \
    --metadata-file "$smoke_runner_json" \
    -- python "$WORKDIR/tools/gpu_smoke_test.py" \
      --output "$smoke_output_json" \
      --matrix-size "$STARTUP_SMOKE_MATRIX_SIZE" \
      --tag startup_gpu_smoke
  exit_code=$?
  set -e

  if [[ "$exit_code" -ne 0 ]]; then
    echo "Startup GPU smoke test failed with exit code $exit_code" >&2
    if [[ "$STARTUP_SMOKE_REQUIRED" == "1" ]]; then
      exit "$exit_code"
    fi
  fi
}

build_planner_prompt() {
  local round="$1"
  local output_file="$2"
  local previous_instructions="$3"
  local previous_worker_summary="$4"

  cat > "$output_file" <<EOF
You are the planner agent. This is round ${round}.

Your job is to propose the next scientifically useful step for a research coding workspace.

Hard requirements:
- Read proposal, context, planning, reports, and prior memory before proposing work.
- Prefer one primary experiment or one tightly scoped implementation step that enables a specific experiment.
- Every experiment must be hypothesis-driven, minimally invasive, and easy to compare against a clear baseline.
- Avoid proposing broad bundles of architecture + optimization + evaluation + export changes together unless the memory shows that bundling is necessary and you justify it explicitly.
- Use the experiment memory to avoid redundant experiments. If repeating a similar idea, explain what new variable or stronger rationale makes it informative.
- Distinguish the experiment category clearly: architecture, optimization, evaluation, or export.
- If no real experiment has run yet, prioritize the smallest executable baseline or smoke check that unlocks evidence.
- If GPU is helpful, instruct the worker to use 'tools/gpu_experiment_runner.py'.
- Your final response must be directly usable by the worker. Do not include chain-of-thought. Do not wrap the answer in code fences.

Your final response must use these headings exactly:
1. Stage Diagnosis
2. Primary Experiment
3. Experiment Category
4. Baseline / Comparison
5. Hypothesis
6. Why It Might Work
7. Minimal Intervention
8. Variables To Change
9. Variables To Hold Fixed
10. Success Metric
11. Failure Interpretation
12. Redundancy Check
13. Required Files To Read
14. Execution Steps
15. Validation And Comparison Requirements
16. GPU / Compute Guidance
17. Completion Criteria
18. What To Report Back To The User
EOF

  append_section "AVAILABLE SKILLS INDEX" "${SKILLS_DIR}/README.md" "$output_file"
  append_section "PLANNER SEED PROMPT" "$PLANNER_PROMPT_FILE" "$output_file"
  append_section "COPIED PROPOSAL" "$WORKDIR/inputs/proposal.md" "$output_file"
  append_section "PROPOSAL PROFILE" "$WORKDIR/context/proposal_profile.json" "$output_file"
  append_section "HARDWARE SNAPSHOT" "$WORKDIR/context/hardware_snapshot.json" "$output_file"
  append_section "TOOL SNAPSHOT" "$WORKDIR/context/tool_snapshot.json" "$output_file"
  append_section "STARTUP GPU SMOKE TEST" "$WORKDIR/context/startup_gpu_smoke.json" "$output_file"
  append_section "RESEARCH PLAN" "$WORKDIR/planning/research_plan.md" "$output_file"
  append_section "NEXT EXPERIMENT PROPOSAL" "$WORKDIR/planning/next_experiment.md" "$output_file"
  append_section "ASSUMPTIONS" "$WORKDIR/planning/assumptions.md" "$output_file"
  append_section "EXPERIMENT LEDGER" "$WORKDIR/planning/experiment_ledger.md" "$output_file"
  append_section "RESEARCH MEMORY" "$WORKDIR/planning/research_memory.md" "$output_file"
  append_section "LATEST STATUS" "$WORKDIR/reports/latest_status.md" "$output_file"
  append_section "COMPARISON SUMMARY" "$WORKDIR/reports/comparison_summary.md" "$output_file"
  append_section "PREVIOUS PLANNER INSTRUCTIONS" "$previous_instructions" "$output_file"
  append_section "PREVIOUS WORKER SUMMARY" "$previous_worker_summary" "$output_file"
  append_directory_sections "REFERENCE MATERIAL" "$WORKDIR/context/reference_materials" "$output_file"
}

build_review_prompt() {
  local round="$1"
  local output_file="$2"
  local planner_instructions="$3"

  cat > "$output_file" <<EOF
You are a lightweight scientific reviewer. This is round ${round}.

Your only job is to critique and tighten the planner's proposed experiment before execution.

Review checklist:
- Is the proposal redundant given experiment memory or prior rounds?
- Is the hypothesis explicit and falsifiable?
- Are the changed variables small in number and clearly separated from held-constant variables?
- Is the category clear: architecture, optimization, evaluation, or export?
- If categories are mixed, is the justification strong enough?
- Will the result be interpretable even if the experiment fails?
- Is the requested validation sufficient for comparison against a baseline?

Output requirements:
- If the proposal is already strong, lightly rewrite it for clarity and control.
- If the proposal is weak, rewrite it into the smallest useful experiment that still advances the research question.
- Keep the final output directly usable by the worker.
- Preserve the same headings as the planner format.
- Add one extra final section called "Review Notes" with a short critique summary.
- Do not include chain-of-thought. Do not use code fences.
EOF

  append_section "REVIEWER BASE PROMPT" "$REVIEWER_PROMPT_FILE" "$output_file"
  append_section "PLANNER PROPOSAL FOR REVIEW" "$planner_instructions" "$output_file"
  append_section "NEXT EXPERIMENT PROPOSAL" "$WORKDIR/planning/next_experiment.md" "$output_file"
  append_section "EXPERIMENT LEDGER" "$WORKDIR/planning/experiment_ledger.md" "$output_file"
  append_section "RESEARCH MEMORY" "$WORKDIR/planning/research_memory.md" "$output_file"
  append_section "LATEST STATUS" "$WORKDIR/reports/latest_status.md" "$output_file"
  append_section "COMPARISON SUMMARY" "$WORKDIR/reports/comparison_summary.md" "$output_file"
  append_directory_sections "REFERENCE MATERIAL" "$WORKDIR/context/reference_materials" "$output_file"
}

build_worker_prompt() {
  local round="$1"
  local output_file="$2"
  local planner_instructions="$3"

  cat > "$output_file" <<EOF
You are the executor agent. This is round ${round}.

Your job is to execute the reviewed experiment brief in a disciplined, scientific way.

Execution rules:
1. Read the reviewed experiment brief first, then read the cited files before changing anything.
2. Prefer the smallest intervention that cleanly tests the stated hypothesis.
3. When possible, change only a small number of factors. Do not silently mix architecture, optimization, evaluation, and export changes.
4. If the reviewed brief is still too broad, narrow it to a controlled version and explain that choice in the final summary.
5. If GPU is needed, prefer 'tools/gpu_experiment_runner.py' so commands and resources are logged.
6. For every substantive experiment, update:
   - 'planning/next_experiment.md'
   - 'planning/experiment_ledger.md'
   - 'planning/research_memory.md'
   - 'reports/latest_status.md'
   - 'reports/comparison_summary.md' when there is a comparison to record
7. Make outputs easy to compare against the stated baseline.
8. Do not do destructive cleanup.

Before concluding, make sure the recorded result includes:
- hypothesis,
- mechanism / rationale,
- changed variables,
- held-fixed variables,
- expected effect,
- actual result,
- interpretation,
- next step.
EOF

  append_section "AVAILABLE SKILLS INDEX" "${SKILLS_DIR}/README.md" "$output_file"
  append_section "WORKER BASE PROMPT" "$WORKER_PROMPT_FILE" "$output_file"
  append_section "REVIEWED INSTRUCTIONS FOR THIS ROUND" "$planner_instructions" "$output_file"
  append_section "NEXT EXPERIMENT PROPOSAL" "$WORKDIR/planning/next_experiment.md" "$output_file"
  append_section "EXPERIMENT LEDGER" "$WORKDIR/planning/experiment_ledger.md" "$output_file"
  append_section "RESEARCH MEMORY" "$WORKDIR/planning/research_memory.md" "$output_file"
  append_section "LATEST STATUS" "$WORKDIR/reports/latest_status.md" "$output_file"
  append_section "COMPARISON SUMMARY" "$WORKDIR/reports/comparison_summary.md" "$output_file"
  append_directory_sections "REFERENCE MATERIAL" "$WORKDIR/context/reference_materials" "$output_file"
}

run_codex_phase() {
  local phase="$1"
  local round="$2"
  local prompt_file="$3"
  local phase_tag
  local stdout_log
  local stderr_log
  local last_message
  local meta_file
  local start_time
  local end_time
  local exit_code

  phase_tag="$(printf 'round_%03d.%s' "$round" "$phase")"
  stdout_log="$RUN_ROOT/${phase_tag}.stdout.log"
  stderr_log="$RUN_ROOT/${phase_tag}.stderr.log"
  last_message="$RUN_ROOT/${phase_tag}.final.txt"
  meta_file="$RUN_ROOT/${phase_tag}.meta"
  start_time="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  echo "[$start_time] Starting ${phase_tag}"
  set +e
  "${BASE_CMD[@]}" -o "$last_message" - < "$prompt_file" \
    > >(tee "$stdout_log") \
    2> >(tee "$stderr_log" >&2)
  exit_code=$?
  set -e
  end_time="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  {
    echo "phase=$phase"
    echo "round=$round"
    echo "start_time=$start_time"
    echo "end_time=$end_time"
    echo "exit_code=$exit_code"
    echo "prompt_file=$prompt_file"
    echo "stdout_log=$stdout_log"
    echo "stderr_log=$stderr_log"
    echo "last_message=$last_message"
  } > "$meta_file"

  if [[ "$exit_code" -ne 0 ]]; then
    echo "[$end_time] ${phase_tag} failed with exit code $exit_code" >&2
  else
    echo "[$end_time] ${phase_tag} completed"
  fi

  PHASE_EXIT_CODE="$exit_code"
  PHASE_LAST_MESSAGE="$last_message"
  PHASE_STDOUT_LOG="$stdout_log"
  PHASE_STDERR_LOG="$stderr_log"
  PHASE_META_FILE="$meta_file"
}

run_round() {
  local round="$1"
  local round_tag
  local planner_prompt_path
  local planner_instructions_path
  local review_prompt_path
  local review_instructions_path=""
  local worker_prompt_path
  local worker_summary_path
  local worker_instruction_source
  local planner_exit_code
  local review_exit_code=0
  local worker_exit_code

  round_tag="$(printf 'round_%03d' "$round")"
  planner_prompt_path="$RUN_ROOT/${round_tag}.planner.prompt.txt"
  review_prompt_path="$RUN_ROOT/${round_tag}.review.prompt.txt"
  worker_prompt_path="$RUN_ROOT/${round_tag}.worker.prompt.txt"

  build_planner_prompt \
    "$round" \
    "$planner_prompt_path" \
    "$RUN_ROOT/planner_current_instructions.txt" \
    "$RUN_ROOT/worker_last_summary.txt"

  run_codex_phase "planner" "$round" "$planner_prompt_path"
  planner_exit_code="$PHASE_EXIT_CODE"
  planner_instructions_path="$PHASE_LAST_MESSAGE"

  if [[ "$planner_exit_code" -ne 0 ]]; then
    {
      echo "round=$round"
      echo "planner_prompt=$planner_prompt_path"
      echo "planner_instructions=$planner_instructions_path"
      echo "planner_exit_code=$planner_exit_code"
      echo "worker_skipped=1"
    } > "$RUN_ROOT/${round_tag}.meta"

    if [[ "$CONTINUE_ON_ERROR" != "1" ]]; then
      return "$planner_exit_code"
    fi

    return 0
  fi

  cp "$planner_instructions_path" "$RUN_ROOT/planner_current_instructions.txt"
  cp "$planner_instructions_path" "$WORKDIR/planning/round_instructions/${round_tag}.planner.md"
  worker_instruction_source="$planner_instructions_path"

  if [[ "$ENABLE_REVIEW" == "1" ]]; then
    build_review_prompt \
      "$round" \
      "$review_prompt_path" \
      "$planner_instructions_path"

    run_codex_phase "review" "$round" "$review_prompt_path"
    review_exit_code="$PHASE_EXIT_CODE"
    review_instructions_path="$PHASE_LAST_MESSAGE"

    if [[ "$review_exit_code" -ne 0 ]]; then
      {
        echo "round=$round"
        echo "planner_prompt=$planner_prompt_path"
        echo "planner_instructions=$planner_instructions_path"
        echo "planner_exit_code=$planner_exit_code"
        echo "review_prompt=$review_prompt_path"
        echo "review_instructions=$review_instructions_path"
        echo "review_exit_code=$review_exit_code"
        echo "worker_skipped=1"
      } > "$RUN_ROOT/${round_tag}.meta"

      if [[ "$CONTINUE_ON_ERROR" != "1" ]]; then
        return "$review_exit_code"
      fi
    else
      worker_instruction_source="$review_instructions_path"
      cp "$review_instructions_path" "$WORKDIR/planning/review_notes/${round_tag}.md"
      cp "$review_instructions_path" "$RUN_ROOT/reviewer_current_instructions.txt"
    fi
  fi

  cp "$worker_instruction_source" "$WORKDIR/planning/round_instructions/${round_tag}.md"

  build_worker_prompt \
    "$round" \
    "$worker_prompt_path" \
    "$worker_instruction_source"

  run_codex_phase "worker" "$round" "$worker_prompt_path"
  worker_exit_code="$PHASE_EXIT_CODE"
  worker_summary_path="$PHASE_LAST_MESSAGE"

  if [[ "$worker_exit_code" -eq 0 ]]; then
    cp "$worker_summary_path" "$RUN_ROOT/worker_last_summary.txt"
    cp "$worker_summary_path" "$WORKDIR/reports/round_summaries/${round_tag}.md"
  fi

  {
    echo "round=$round"
    echo "planner_prompt=$planner_prompt_path"
    echo "planner_instructions=$planner_instructions_path"
    echo "planner_exit_code=$planner_exit_code"
    echo "review_enabled=$ENABLE_REVIEW"
    echo "review_prompt=$review_prompt_path"
    echo "review_instructions=$review_instructions_path"
    echo "review_exit_code=$review_exit_code"
    echo "worker_prompt=$worker_prompt_path"
    echo "worker_summary=$worker_summary_path"
    echo "worker_exit_code=$worker_exit_code"
  } > "$RUN_ROOT/${round_tag}.meta"

  if [[ "$worker_exit_code" -ne 0 ]] && [[ "$CONTINUE_ON_ERROR" != "1" ]]; then
    return "$worker_exit_code"
  fi
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -z "$PROPOSAL_FILE" ]]; then
  echo "Error: PROPOSAL_FILE is required." >&2
  exit 1
fi

if [[ ! -f "$PROPOSAL_FILE" ]]; then
  echo "Error: PROPOSAL_FILE does not exist: $PROPOSAL_FILE" >&2
  exit 1
fi

if [[ -z "$PROJECT_NAME" ]]; then
  PROJECT_NAME="$(sanitize_name "$(basename "${PROPOSAL_FILE%.*}")")"
fi

if [[ -z "$PROJECT_ROOT" ]]; then
  PROJECT_ROOT="${DEFAULT_PROJECTS_DIR}/${PROJECT_NAME}"
fi

WORKDIR="$PROJECT_ROOT"
LOG_BASE_DIR="${LOG_BASE_DIR:-$WORKDIR/runs/codex_research_loop}"

if [[ ! -f "$PLANNER_PROMPT_FILE" ]]; then
  echo "Error: PLANNER_PROMPT_FILE does not exist: $PLANNER_PROMPT_FILE" >&2
  exit 1
fi

if [[ ! -f "$WORKER_PROMPT_FILE" ]]; then
  echo "Error: WORKER_PROMPT_FILE does not exist: $WORKER_PROMPT_FILE" >&2
  exit 1
fi

if [[ "$ENABLE_REVIEW" == "1" ]] && [[ ! -f "$REVIEWER_PROMPT_FILE" ]]; then
  echo "Error: REVIEWER_PROMPT_FILE does not exist: $REVIEWER_PROMPT_FILE" >&2
  exit 1
fi

if [[ ! "$ROUNDS" =~ ^[0-9]+$ ]]; then
  echo "Error: ROUNDS must be a non-negative integer: $ROUNDS" >&2
  exit 1
fi

if [[ ! "$SLEEP_SECONDS" =~ ^[0-9]+$ ]]; then
  echo "Error: SLEEP_SECONDS must be a non-negative integer: $SLEEP_SECONDS" >&2
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "Error: python is required." >&2
  exit 1
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "Error: codex CLI not found. Install it first." >&2
  exit 1
fi

if ! codex login status >/dev/null 2>&1; then
  echo "Error: Codex is not logged in. Run 'codex login' first." >&2
  exit 1
fi

declare -a INIT_CMD
declare -a EXTRA_CONTEXT_FILE_ARRAY
INIT_CMD=(
  python "$SCRIPT_DIR/init_research_workspace.py"
  --project-root "$WORKDIR"
  --proposal-file "$PROPOSAL_FILE"
  --experiment-conda-env "$EXPERIMENT_CONDA_ENV"
)

if [[ -n "$EXTRA_CONTEXT_FILES" ]]; then
  IFS=':' read -r -a EXTRA_CONTEXT_FILE_ARRAY <<< "$EXTRA_CONTEXT_FILES"
  for extra_context_file in "${EXTRA_CONTEXT_FILE_ARRAY[@]}"; do
    if [[ -n "$extra_context_file" ]]; then
      INIT_CMD+=(--extra-context-file "$extra_context_file")
    fi
  done
fi

"${INIT_CMD[@]}"

if [[ "$RUN_STARTUP_GPU_SMOKE" == "1" ]]; then
  run_startup_gpu_smoke
fi

RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_ROOT="${LOG_BASE_DIR}/${RUN_ID}"
mkdir -p "$RUN_ROOT"
cp "$PLANNER_PROMPT_FILE" "$RUN_ROOT/planner_seed_prompt_snapshot.txt"
cp "$WORKER_PROMPT_FILE" "$RUN_ROOT/worker_prompt_snapshot.txt"
if [[ "$ENABLE_REVIEW" == "1" ]]; then
  cp "$REVIEWER_PROMPT_FILE" "$RUN_ROOT/reviewer_prompt_snapshot.txt"
fi
cp "$WORKDIR/inputs/proposal.md" "$RUN_ROOT/proposal_snapshot.md"

declare -a BASE_CMD
BASE_CMD=(codex exec --cd "$WORKDIR" --color "$COLOR")

if ! git -C "$WORKDIR" rev-parse --show-toplevel >/dev/null 2>&1; then
  BASE_CMD+=(--skip-git-repo-check)
fi

if [[ "$BYPASS_ALL_GUARDRAILS" == "1" ]]; then
  BASE_CMD+=(--dangerously-bypass-approvals-and-sandbox)
elif [[ "$USE_FULL_AUTO" == "1" ]]; then
  BASE_CMD+=(--full-auto)
else
  BASE_CMD+=(-s "$SANDBOX_MODE")
fi

if [[ -n "$MODEL" ]]; then
  BASE_CMD+=(-m "$MODEL")
fi

if [[ "$ENABLE_SEARCH" == "1" ]]; then
  BASE_CMD+=(-c "web_search=\"$WEB_SEARCH_MODE\"")
fi

if [[ "$USE_EPHEMERAL" == "1" ]]; then
  BASE_CMD+=(--ephemeral)
fi

if [[ -n "$EXTRA_ARGS" ]]; then
  # shellcheck disable=SC2206
  EXTRA_ARG_ARRAY=($EXTRA_ARGS)
  BASE_CMD+=("${EXTRA_ARG_ARRAY[@]}")
fi

print_config() {
  cat <<EOF
Run root: $RUN_ROOT
Project root: $WORKDIR
Proposal file: $PROPOSAL_FILE
Planner prompt: $PLANNER_PROMPT_FILE
Worker prompt: $WORKER_PROMPT_FILE
Reviewer prompt: ${REVIEWER_PROMPT_FILE:-<disabled>}
Rounds: $ROUNDS
Sleep seconds: $SLEEP_SECONDS
Model: ${MODEL:-<default>}
Search: $ENABLE_SEARCH
Web search mode: ${WEB_SEARCH_MODE:-<config default>}
Bypass approvals and sandbox: $BYPASS_ALL_GUARDRAILS
Use full auto: $USE_FULL_AUTO
Sandbox mode: $SANDBOX_MODE
Ephemeral: $USE_EPHEMERAL
Continue on error: $CONTINUE_ON_ERROR
Experiment conda env: $EXPERIMENT_CONDA_ENV
Enable review: $ENABLE_REVIEW
Extra context files: ${EXTRA_CONTEXT_FILES:-<none>}
Run startup GPU smoke: $RUN_STARTUP_GPU_SMOKE
Startup smoke required: $STARTUP_SMOKE_REQUIRED
Startup smoke GPUs: $STARTUP_SMOKE_GPUS
Color: $COLOR
Base command: ${BASE_CMD[*]}
EOF
}

print_config | tee "$RUN_ROOT/run_config.txt"

if [[ "$ROUNDS" -gt 0 ]]; then
  for ((round = 1; round <= ROUNDS; round++)); do
    run_round "$round"
    if [[ "$round" -lt "$ROUNDS" ]] && [[ "$SLEEP_SECONDS" -gt 0 ]]; then
      sleep "$SLEEP_SECONDS"
    fi
  done
else
  round=1
  while true; do
    run_round "$round"
    round=$((round + 1))
    if [[ "$SLEEP_SECONDS" -gt 0 ]]; then
      sleep "$SLEEP_SECONDS"
    fi
  done
fi

echo "All runs finished. Logs saved in: $RUN_ROOT"
