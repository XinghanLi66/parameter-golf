#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


LAB_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_command(command: list[str], timeout: int = 20) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, "", str(exc)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_memory_gib() -> float | None:
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return None
    total_kib = None
    for line in meminfo.read_text(encoding="utf-8").splitlines():
        if line.startswith("MemTotal:"):
            parts = line.split()
            if len(parts) >= 2:
                total_kib = int(parts[1])
                break
    if total_kib is None:
        return None
    return round(total_kib / 1024 / 1024, 2)


def parse_gpu_csv_line(line: str) -> dict[str, Any]:
    parts = [part.strip() for part in line.split(",")]
    if len(parts) < 5:
        return {"raw": line}
    return {
        "index": int(parts[0]),
        "name": parts[1],
        "memory_total_mib": int(parts[2]),
        "memory_free_mib": int(parts[3]),
        "utilization_gpu_percent": int(parts[4]),
    }


def get_hardware_snapshot() -> dict[str, Any]:
    code, stdout, stderr = run_command(
        [
            "nvidia-smi",
            "--query-gpu=index,name,memory.total,memory.free,utilization.gpu",
            "--format=csv,noheader,nounits",
        ]
    )
    gpus: list[dict[str, Any]] = []
    if code == 0 and stdout:
        gpus = [parse_gpu_csv_line(line) for line in stdout.splitlines() if line.strip()]
    return {
        "captured_at_utc": now_utc(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "cpu_count": os.cpu_count(),
        "memory_total_gib": get_memory_gib(),
        "gpu_visible_count": len(gpus),
        "gpus": gpus,
        "nvidia_smi_error": stderr if code != 0 else "",
    }


def check_executable(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    return {"found": bool(path), "path": path or ""}


def get_conda_env_list() -> list[str]:
    code, stdout, _ = run_command(["conda", "env", "list"], timeout=30)
    if code != 0 or not stdout:
        return []
    envs: list[str] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        env_name = stripped.split()[0]
        if env_name not in envs:
            envs.append(env_name)
    return envs


def inspect_conda_env(env_name: str) -> dict[str, Any]:
    envs = get_conda_env_list()
    result: dict[str, Any] = {"name": env_name, "exists": env_name in envs}
    if not result["exists"]:
        return result

    torch_code = (
        "import json, importlib.util; "
        "payload = {"
        "'torch': bool(importlib.util.find_spec(\"torch\")), "
        "'llamafactory_cli': bool(importlib.util.find_spec(\"llamafactory\")), "
        "'torchrun': __import__(\"shutil\").which(\"torchrun\") is not None"
        "}; print(json.dumps(payload))"
    )
    code, stdout, stderr = run_command(
        ["conda", "run", "--no-capture-output", "-n", env_name, "python", "-c", torch_code],
        timeout=60,
    )
    if code == 0 and stdout:
        try:
            result["package_probe"] = json.loads(stdout.splitlines()[-1])
        except json.JSONDecodeError:
            result["package_probe_raw"] = stdout
    else:
        result["package_probe_error"] = stderr or stdout

    cuda_code = """
import json

payload = {"cuda_backend": "none"}
try:
    import torch

    payload = {
        "cuda_backend": "torch",
        "torch_version": torch.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "device_count": int(torch.cuda.device_count()),
    }
    if torch.cuda.is_available():
        payload["device_names"] = [
            torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())
        ]
except Exception as exc:
    payload["cuda_probe_error"] = str(exc)

print(json.dumps(payload))
""".strip()
    code, stdout, stderr = run_command(
        ["conda", "run", "--no-capture-output", "-n", env_name, "python", "-c", cuda_code],
        timeout=90,
    )
    if code == 0 and stdout:
        try:
            result["cuda_probe"] = json.loads(stdout.splitlines()[-1])
        except json.JSONDecodeError:
            result["cuda_probe_raw"] = stdout
    else:
        result["cuda_probe_error"] = stderr or stdout
    return result


def get_tool_snapshot(experiment_conda_env: str | None) -> dict[str, Any]:
    code, codex_version, _ = run_command(["codex", "--version"])
    login_code, codex_login, codex_login_err = run_command(["codex", "login", "status"])
    snapshot = {
        "captured_at_utc": now_utc(),
        "executables": {
            name: check_executable(name)
            for name in [
                "codex",
                "python",
                "python3",
                "conda",
                "mamba",
                "uv",
                "nvidia-smi",
                "torchrun",
                "llamafactory-cli",
            ]
        },
        "codex_version": codex_version if code == 0 else "",
        "codex_login_status": codex_login or codex_login_err,
    }
    if experiment_conda_env:
        snapshot["experiment_conda_env"] = inspect_conda_env(experiment_conda_env)
    return snapshot


def analyze_proposal(text: str, source_path: Path) -> dict[str, Any]:
    lowered = text.lower()
    headings = len(re.findall(r"(?m)^#+\s+", text))
    words = len(re.findall(r"\S+", text))
    lines = len(text.splitlines())
    keywords = {
        "dataset": len(re.findall(r"\bdataset\b|数据集", lowered)),
        "baseline": len(re.findall(r"\bbaseline\b|基线", lowered)),
        "metric": len(re.findall(r"\bmetric\b|\bmetrics\b|指标", lowered)),
        "experiment": len(re.findall(r"\bexperiment\b|\bexperiments\b|实验", lowered)),
        "ablation": len(re.findall(r"\bablation\b|消融", lowered)),
        "hypothesis": len(re.findall(r"\bhypothesis\b|假设", lowered)),
        "train": len(re.findall(r"\btrain\b|\btraining\b|训练", lowered)),
        "infer": len(re.findall(r"\binference\b|推理", lowered)),
        "timeline": len(re.findall(r"\btimeline\b|时间线", lowered)),
    }
    signal_count = sum(1 for value in keywords.values() if value > 0)

    if words < 180 and signal_count <= 3:
        detail_level = "idea_only"
    elif words >= 450 and headings >= 4 and signal_count >= 5:
        detail_level = "detailed_plan"
    else:
        detail_level = "partial_plan"

    return {
        "source_path": str(source_path.resolve()),
        "analyzed_at_utc": now_utc(),
        "word_count": words,
        "line_count": lines,
        "heading_count": headings,
        "detail_level": detail_level,
        "keyword_hits": keywords,
        "recommended_focus": {
            "idea_only": [
                "clarify hypothesis",
                "define measurable success criteria",
                "pick minimal baselines",
                "run environment or smoke checks early",
            ],
            "partial_plan": [
                "fill missing experiment details",
                "implement a first baseline",
                "start a minimal executable study",
            ],
            "detailed_plan": [
                "execute the highest-value experiment",
                "collect evidence and ablations",
                "keep results reproducible",
            ],
        }[detail_level],
    }


def copy_tool_if_missing(source: Path, destination: Path) -> None:
    if not destination.exists():
        shutil.copy2(source, destination)
        destination.chmod(0o755)


def copy_reference_materials(extra_context_files: list[str], destination_dir: Path) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    used_names: set[str] = set()
    for raw_path in extra_context_files:
        source = Path(raw_path).resolve()
        if not source.exists() or not source.is_file():
            copied.append(
                {
                    "source_path": str(source),
                    "status": "missing",
                }
            )
            continue

        base_name = source.name
        candidate_name = base_name
        suffix = 2
        while candidate_name in used_names:
            candidate_name = f"{source.stem}_{suffix}{source.suffix}"
            suffix += 1
        used_names.add(candidate_name)

        destination = destination_dir / candidate_name
        shutil.copy2(source, destination)
        copied.append(
            {
                "source_path": str(source),
                "copied_path": str(destination),
                "status": "copied",
            }
        )
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a research proposal lab workspace.")
    parser.add_argument("--project-root", required=True, help="Project workspace root.")
    parser.add_argument("--proposal-file", required=True, help="Path to a proposal markdown file.")
    parser.add_argument(
        "--experiment-conda-env",
        default="",
        help="Preferred conda env for experiments, used for environment probing.",
    )
    parser.add_argument(
        "--extra-context-file",
        action="append",
        default=[],
        help="Optional reference material copied into context/reference_materials/.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    proposal_path = Path(args.proposal_file).resolve()

    if not proposal_path.exists():
        raise FileNotFoundError(f"Proposal file not found: {proposal_path}")

    inputs_dir = project_root / "inputs"
    context_dir = project_root / "context"
    reference_dir = context_dir / "reference_materials"
    planning_dir = project_root / "planning"
    experiments_dir = project_root / "experiments"
    reports_dir = project_root / "reports"
    code_dir = project_root / "code"
    artifacts_dir = project_root / "artifacts"
    logs_dir = project_root / "logs"
    tools_dir = project_root / "tools"
    runs_dir = project_root / "runs"
    round_plan_dir = planning_dir / "round_instructions"
    round_report_dir = reports_dir / "round_summaries"
    review_note_dir = planning_dir / "review_notes"

    for directory in [
        project_root,
        inputs_dir,
        context_dir,
        reference_dir,
        planning_dir,
        experiments_dir,
        reports_dir,
        code_dir,
        artifacts_dir,
        logs_dir,
        tools_dir,
        runs_dir,
        round_plan_dir,
        round_report_dir,
        review_note_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    proposal_text = read_text(proposal_path)
    copied_proposal = inputs_dir / "proposal.md"
    copied_proposal.write_text(proposal_text, encoding="utf-8")

    profile = analyze_proposal(proposal_text, proposal_path)
    hardware = get_hardware_snapshot()
    tools = get_tool_snapshot(args.experiment_conda_env or None)
    copied_reference_materials = copy_reference_materials(args.extra_context_file, reference_dir)

    write_json(context_dir / "proposal_profile.json", profile)
    write_json(context_dir / "hardware_snapshot.json", hardware)
    write_json(context_dir / "tool_snapshot.json", tools)
    write_json(
        context_dir / "reference_materials_index.json",
        {
            "captured_at_utc": now_utc(),
            "materials": copied_reference_materials,
        },
    )

    write_text_if_missing(
        planning_dir / "research_plan.md",
        """# Research Plan

This file should become the project-level working plan that the planner and worker keep refining.

Suggested sections:

1. Problem and hypothesis
2. Minimal baseline
3. Data / benchmarks
4. Metrics
5. Experiment order
6. Risks and fallback options
""",
    )
    write_text_if_missing(
        planning_dir / "next_experiment.md",
        """# Next Experiment Proposal

Fill this in before a substantive implementation or experiment run.

## Experiment ID

## Category
- architecture | optimization | evaluation | export

## Baseline / Comparison

## Hypothesis

## Why It Might Work

## Minimal Intervention

## Variables To Change

## Variables To Hold Fixed

## Success Metric

## Failure Interpretation

## Redundancy Check
- Similar prior experiments:
- Why this is still informative:

## Execution Plan

## Expected Effect
""",
    )
    write_text_if_missing(
        planning_dir / "assumptions.md",
        """# Assumptions

Use this file to record any assumptions inferred from a vague proposal, environment constraints, or missing details.
""",
    )
    write_text_if_missing(
        planning_dir / "experiment_ledger.md",
        """# Experiment Ledger

Use one row per meaningful experiment or proposal revision. Prefer short factual entries over prose.

| Date (UTC) | ID | Category | Baseline / Comparison | Hypothesis | Mechanism / Rationale | Changed Variables | Held Fixed | Expected Effect | Actual Result | Interpretation | Next Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
""",
    )
    write_text_if_missing(
        planning_dir / "research_memory.md",
        """# Research Memory

This file is the compact scientific memory for the project. Keep it updated so the planner can avoid redundant work.

## Confirmed Signals
- Add concise findings that appear reproducible.

## Negative Or Inconclusive Results
- Record ideas that failed or remain unclear, and why.

## Redundancy Watchlist
- Note experiments that should not be repeated unless a new variable or stronger rationale is introduced.

## Current Best Known Configuration
- architecture:
- optimization:
- evaluation:
- export:

## Open Hypotheses
- Add only hypotheses that are still decision-relevant.
""",
    )
    write_text_if_missing(
        reports_dir / "latest_status.md",
        """# Latest Status

Update this after each substantive round.

## Current Best Evidence

## Most Important Open Question

## Active Experiment ID

## Latest Result Summary

## Recommended Next Step
""",
    )
    write_text_if_missing(
        reports_dir / "comparison_summary.md",
        """# Comparison Summary

Use this file to keep apples-to-apples comparisons easy to scan.

| Comparison | Metric | Baseline | Candidate | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
""",
    )
    write_text_if_missing(
        experiments_dir / "README.md",
        """# Experiments

Put reusable experiment configs, launch scripts, and notebooks here.
""",
    )
    write_text_if_missing(
        code_dir / "README.md",
        """# Code

Put generated source code, training scripts, evaluators, and utilities here.
""",
    )
    write_text_if_missing(
        project_root / "README_PROJECT.md",
        f"""# Project Workspace

This workspace was initialized from:

- Proposal source: `{proposal_path}`
- Detected detail level: `{profile['detail_level']}`
- Preferred experiment conda env: `{args.experiment_conda_env or 'not set'}`

Important directories:

- `inputs/`: copied proposal and inputs
- `context/`: runtime snapshots such as hardware and tool probes
- `planning/`: plans, assumptions, and experiment ledger
- `experiments/`: configs and launch scripts
- `reports/`: round summaries and latest status
- `code/`: generated or edited project code
- `artifacts/`: checkpoints, predictions, figures, and other outputs
- `logs/`: experiment logs
- `tools/`: local helper scripts that Codex should use
- `context/reference_materials/`: copied external references such as SOTA reviews
""",
    )

    for tool_name in ["gpu_experiment_runner.py", "gpu_smoke_test.py"]:
        copy_tool_if_missing(SCRIPTS_DIR / tool_name, tools_dir / tool_name)

    print(f"Initialized project workspace at: {project_root}")
    print(f"Copied proposal to: {copied_proposal}")
    print(f"Detected proposal detail level: {profile['detail_level']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
