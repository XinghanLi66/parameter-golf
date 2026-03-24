#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_command(command: list[str], cwd: Path | None = None, timeout: int = 60) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return 1, "", str(exc)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def executable_status(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    return {"found": bool(path), "path": path or ""}


def python_module_status(python_bin: str, module: str, conda_env: str = "") -> dict[str, Any]:
    code = (
        "import importlib.util, json; "
        f"print(json.dumps({{'module': '{module}', 'found': bool(importlib.util.find_spec('{module}'))}}))"
    )
    command = [python_bin, "-c", code]
    if conda_env:
        command = ["conda", "run", "--no-capture-output", "-n", conda_env, python_bin, "-c", code]
    exit_code, stdout, stderr = run_command(command, timeout=30)
    result: dict[str, Any] = {"module": module, "ok": False}
    if exit_code == 0 and stdout:
        try:
            parsed = json.loads(stdout.splitlines()[-1])
            result["ok"] = bool(parsed.get("found"))
        except json.JSONDecodeError:
            result["error"] = stdout
    else:
        result["error"] = stderr or stdout
    return result


def path_summary(path: Path, glob_pattern: str) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "count": 0, "examples": []}
    matches = sorted(path.glob(glob_pattern))
    return {
        "exists": True,
        "count": len(matches),
        "examples": [str(match) for match in matches[:5]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the Parameter Golf research environment for autonomous iteration.")
    parser.add_argument("--repo-root", required=True, help="Path to the main parameter-golf repo root.")
    parser.add_argument("--project-root", required=True, help="Path to the research_lab_pg project root.")
    parser.add_argument("--python-bin", default=sys.executable, help="Python binary to use for module checks.")
    parser.add_argument("--conda-env", default="", help="Optional conda env to use for Python module checks.")
    parser.add_argument("--output", default="", help="Optional JSON output path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    project_root = Path(args.project_root).resolve()
    data_root = repo_root / "data"
    datasets_root = data_root / "datasets"
    tokenizers_root = data_root / "tokenizers"

    report: dict[str, Any] = {
        "generated_at_utc": now_utc(),
        "repo_root": str(repo_root),
        "project_root": str(project_root),
        "executables": {name: executable_status(name) for name in ["codex", "python", "python3", "torchrun", "nvidia-smi"]},
        "python_modules": {},
        "codex": {},
        "git_status": {},
        "data": {},
        "project": {},
        "python_context": {"python_bin": args.python_bin, "conda_env": args.conda_env},
    }

    for module in ["torch", "numpy", "sentencepiece", "huggingface_hub", "datasets", "tqdm"]:
        report["python_modules"][module] = python_module_status(args.python_bin, module, args.conda_env)

    codex_code, codex_version, codex_version_err = run_command(["codex", "--version"], cwd=repo_root, timeout=30)
    login_code, login_out, login_err = run_command(["codex", "login", "status"], cwd=repo_root, timeout=30)
    report["codex"] = {
        "version_ok": codex_code == 0,
        "version": codex_version or codex_version_err,
        "login_ok": login_code == 0,
        "login_status": login_out or login_err,
    }

    git_code, git_out, git_err = run_command(["git", "status", "--short"], cwd=repo_root, timeout=30)
    report["git_status"] = {
        "ok": git_code == 0,
        "summary": git_out or git_err,
    }

    train_shards = path_summary(datasets_root / "fineweb10B_sp1024", "fineweb_train_*.bin")
    val_shards = path_summary(datasets_root / "fineweb10B_sp1024", "fineweb_val_*.bin")
    tokenizer_file = tokenizers_root / "fineweb_1024_bpe.model"
    report["data"] = {
        "datasets_root_exists": datasets_root.exists(),
        "tokenizers_root_exists": tokenizers_root.exists(),
        "sp1024_train_shards": train_shards,
        "sp1024_val_shards": val_shards,
        "tokenizer_model_exists": tokenizer_file.exists(),
        "tokenizer_model_path": str(tokenizer_file),
    }

    required_files = [
        project_root / "planning" / "next_experiment.md",
        project_root / "planning" / "experiment_ledger.md",
        project_root / "planning" / "research_memory.md",
        project_root / "reports" / "latest_status.md",
        project_root / "reports" / "comparison_summary.md",
    ]
    report["project"] = {
        "exists": project_root.exists(),
        "required_files": {str(path): path.exists() for path in required_files},
    }

    report["summary"] = {
        "ready_for_real_iteration": all(
            [
                report["codex"]["version_ok"],
                report["codex"]["login_ok"],
                train_shards["count"] > 0,
                val_shards["count"] > 0,
                tokenizer_file.exists(),
            ]
        )
    }

    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
