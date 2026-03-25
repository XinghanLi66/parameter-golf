#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="${REPO_ROOT:-$(cd "${LAB_ROOT}/.." && pwd)}"
PROJECT_NAME="${PROJECT_NAME:-parameter_golf_science}"
PROJECT_ROOT="${PROJECT_ROOT:-${LAB_ROOT}/projects/${PROJECT_NAME}}"
PROPOSAL_FILE="${PROPOSAL_FILE:-${LAB_ROOT}/examples/proposal_parameter_golf_science.md}"
EXPERIMENT_CONDA_ENV="${EXPERIMENT_CONDA_ENV:-loongflow_ml}"
ROUNDS="${ROUNDS:-2}"
WAIT_FOR_DATA="${WAIT_FOR_DATA:-1}"
WAIT_SECONDS="${WAIT_SECONDS:-30}"
RUN_STARTUP_GPU_SMOKE="${RUN_STARTUP_GPU_SMOKE:-0}"
DATASET_DIR="${REPO_ROOT}/data/datasets/fineweb10B_sp1024"
TOKENIZER_FILE="${REPO_ROOT}/data/tokenizers/fineweb_1024_bpe.model"
LIVE_SOTA_FILE="${LIVE_SOTA_FILE:-${REPO_ROOT}/docs/latest_sota_snapshot.md}"
SOTA_RECORDS_DIR="${SOTA_RECORDS_DIR:-${REPO_ROOT}/docs/sota_records}"
SOTA_RECORDS_TOP_N="${SOTA_RECORDS_TOP_N:-5}"
EXTRA_CONTEXT_FILES="${EXTRA_CONTEXT_FILES:-${REPO_ROOT}/docs/sota_review.md:${LIVE_SOTA_FILE}:${REPO_ROOT}/docs/scientific_research_loop.md}"

wait_for_assets() {
  while true; do
    if [[ -d "$DATASET_DIR" ]] && [[ -f "$TOKENIZER_FILE" ]]; then
      break
    fi
    echo "Waiting for dataset/tokenizer assets..."
    sleep "$WAIT_SECONDS"
  done
}

if [[ "$WAIT_FOR_DATA" == "1" ]]; then
  wait_for_assets
fi

python "${LAB_ROOT}/scripts/refresh_parameter_golf_sota_context.py" \
  --repo-root "$REPO_ROOT" \
  --output "$LIVE_SOTA_FILE" \
  --output "${PROJECT_ROOT}/context/reference_materials/latest_sota_snapshot.md"

echo "Fetching top ${SOTA_RECORDS_TOP_N} SOTA training scripts..."
python "${LAB_ROOT}/scripts/fetch_sota_records.py" \
  --repo-root "$REPO_ROOT" \
  --output-dir "$SOTA_RECORDS_DIR" \
  --top-n "$SOTA_RECORDS_TOP_N" || echo "Warning: fetch_sota_records failed, continuing without updated SOTA codes."

# Append all fetched SOTA record files to EXTRA_CONTEXT_FILES
if [[ -d "$SOTA_RECORDS_DIR" ]]; then
  while IFS= read -r -d '' record_file; do
    EXTRA_CONTEXT_FILES="${EXTRA_CONTEXT_FILES}:${record_file}"
  done < <(find "$SOTA_RECORDS_DIR" -maxdepth 1 -name "*.md" -type f -print0 | sort -z)
fi

python "${LAB_ROOT}/scripts/verify_parameter_golf_env.py" \
  --repo-root "$REPO_ROOT" \
  --project-root "$PROJECT_ROOT" \
  --python-bin python \
  --conda-env "$EXPERIMENT_CONDA_ENV" \
  --output "${PROJECT_ROOT}/context/verifier_env.json"

PROPOSAL_FILE="$PROPOSAL_FILE" \
PROJECT_NAME="$PROJECT_NAME" \
ENABLE_REVIEW=1 \
EXPERIMENT_CONDA_ENV="$EXPERIMENT_CONDA_ENV" \
EXTRA_CONTEXT_FILES="$EXTRA_CONTEXT_FILES" \
RUN_STARTUP_GPU_SMOKE="$RUN_STARTUP_GPU_SMOKE" \
ROUNDS="$ROUNDS" \
EXTRA_ARGS="--add-dir ${REPO_ROOT}" \
bash "${LAB_ROOT}/scripts/codex_research_loop.sh"
