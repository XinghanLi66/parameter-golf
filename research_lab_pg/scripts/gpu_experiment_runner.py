#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any


def run_query(command: list[str], timeout: int = 15) -> tuple[int, str, str]:
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


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def sanitize_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in value)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "run"


def parse_gpu_line(line: str) -> dict[str, Any]:
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


def query_gpus() -> list[dict[str, Any]]:
    code, stdout, _ = run_query(
        [
            "nvidia-smi",
            "--query-gpu=index,name,memory.total,memory.free,utilization.gpu",
            "--format=csv,noheader,nounits",
        ]
    )
    if code != 0 or not stdout:
        return []
    return [parse_gpu_line(line) for line in stdout.splitlines() if line.strip()]


def pick_gpus(
    available: list[dict[str, Any]],
    requested_count: int,
    explicit_indices: list[int] | None,
    min_free_memory_mib: int,
    strategy: str,
) -> list[dict[str, Any]]:
    pool = [gpu for gpu in available if isinstance(gpu.get("index"), int)]
    if explicit_indices:
        index_map = {gpu["index"]: gpu for gpu in pool}
        selected = []
        for index in explicit_indices:
            gpu = index_map.get(index)
            if gpu and gpu["memory_free_mib"] >= min_free_memory_mib:
                selected.append(gpu)
        return selected

    eligible = [gpu for gpu in pool if gpu["memory_free_mib"] >= min_free_memory_mib]
    if strategy == "most-free":
        eligible.sort(key=lambda item: (item["memory_free_mib"], -item["utilization_gpu_percent"]), reverse=True)
    else:
        eligible.sort(key=lambda item: item["index"])
    return eligible[:requested_count]


def stream_pipe(pipe: Any, log_path: Path, sink: Any) -> None:
    with log_path.open("w", encoding="utf-8") as handle:
        for line in iter(pipe.readline, ""):
            handle.write(line)
            handle.flush()
            sink.write(line)
            sink.flush()
    pipe.close()


def build_command(command: list[str], conda_env: str | None) -> list[str]:
    if not command:
        raise ValueError("No command provided to execute.")
    if conda_env:
        return ["conda", "run", "--no-capture-output", "-n", conda_env, *command]
    return command


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Select GPUs, set CUDA_VISIBLE_DEVICES, and run an experiment command with metadata logging."
    )
    parser.add_argument("--gpus", type=int, default=1, help="Number of GPUs to request. Use 0 for CPU-only.")
    parser.add_argument("--gpu-indices", default="", help="Explicit comma-separated GPU indices to use.")
    parser.add_argument("--min-free-memory-gb", type=float, default=10.0, help="Minimum free memory per GPU.")
    parser.add_argument(
        "--strategy",
        choices=["most-free", "first-fit"],
        default="most-free",
        help="GPU selection strategy when indices are not pinned.",
    )
    parser.add_argument("--wait-seconds", type=int, default=0, help="How long to wait for enough GPUs.")
    parser.add_argument("--poll-interval-seconds", type=int, default=20, help="Polling interval while waiting.")
    parser.add_argument("--allow-cpu-fallback", action="store_true", help="Run on CPU if GPU selection fails.")
    parser.add_argument("--conda-env", default="", help="Run the command inside this conda environment.")
    parser.add_argument("--cwd", default="", help="Working directory for the command.")
    parser.add_argument("--log-dir", default="logs/experiment_runs", help="Base directory for logs.")
    parser.add_argument("--run-name", default="experiment", help="Human-friendly run name.")
    parser.add_argument("--timeout-seconds", type=int, default=0, help="Optional timeout for the command.")
    parser.add_argument("--metadata-file", default="", help="Optional extra JSON metadata output path.")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute after '--'.")
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("You must provide a command after '--'.")

    explicit_indices = [int(item) for item in args.gpu_indices.split(",") if item.strip()]
    min_free_memory_mib = int(args.min_free_memory_gb * 1024)
    log_dir = Path(args.log_dir).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    run_dir = log_dir / f"{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}_{sanitize_name(args.run_name)}"
    run_dir.mkdir(parents=True, exist_ok=True)
    stdout_log = run_dir / "stdout.log"
    stderr_log = run_dir / "stderr.log"
    metadata_path = run_dir / "metadata.json"

    selected_gpus: list[dict[str, Any]] = []
    visible_before = query_gpus()
    selection_error = ""

    if args.gpus > 0:
        deadline = time.time() + args.wait_seconds
        while True:
            visible_now = query_gpus()
            selected_gpus = pick_gpus(
                visible_now,
                args.gpus,
                explicit_indices if explicit_indices else None,
                min_free_memory_mib,
                args.strategy,
            )
            if len(selected_gpus) >= args.gpus:
                visible_before = visible_now
                break
            if time.time() >= deadline:
                selection_error = (
                    f"Requested {args.gpus} GPU(s), but only found {len(selected_gpus)} meeting the requirement "
                    f"of {args.min_free_memory_gb:.1f} GiB free memory."
                )
                break
            time.sleep(max(args.poll_interval_seconds, 1))

        if selection_error and not args.allow_cpu_fallback:
            metadata = {
                "captured_at_utc": now_utc(),
                "hostname": platform.node(),
                "requested_gpus": args.gpus,
                "selected_gpus": selected_gpus,
                "visible_gpus": visible_before,
                "selection_error": selection_error,
                "command": command,
                "conda_env": args.conda_env,
            }
            metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            if args.metadata_file:
                Path(args.metadata_file).write_text(
                    json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            print(selection_error, file=sys.stderr)
            print(f"Metadata written to: {metadata_path}", file=sys.stderr)
            return 1

    execution_mode = "gpu" if args.gpus > 0 and len(selected_gpus) >= args.gpus else "cpu"
    env = os.environ.copy()
    if execution_mode == "gpu":
        selected_indices = [str(gpu["index"]) for gpu in selected_gpus[: args.gpus]]
        env["CUDA_VISIBLE_DEVICES"] = ",".join(selected_indices)
        env["PROPOSAL_LAB_SELECTED_GPUS"] = env["CUDA_VISIBLE_DEVICES"]
    else:
        env["CUDA_VISIBLE_DEVICES"] = ""
        env["PROPOSAL_LAB_SELECTED_GPUS"] = ""
    env["PROPOSAL_LAB_DEVICE"] = execution_mode

    final_command = build_command(command, args.conda_env or None)
    cwd = Path(args.cwd).resolve() if args.cwd else Path.cwd()
    started_at = now_utc()

    metadata: dict[str, Any] = {
        "started_at_utc": started_at,
        "hostname": platform.node(),
        "cwd": str(cwd),
        "requested_gpus": args.gpus,
        "explicit_gpu_indices": explicit_indices,
        "execution_mode": execution_mode,
        "selected_gpus": selected_gpus[: args.gpus],
        "visible_gpus": visible_before,
        "selection_error": selection_error,
        "conda_env": args.conda_env,
        "command": command,
        "wrapped_command": final_command,
        "stdout_log": str(stdout_log),
        "stderr_log": str(stderr_log),
    }

    process = subprocess.Popen(
        final_command,
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    stdout_thread = threading.Thread(target=stream_pipe, args=(process.stdout, stdout_log, sys.stdout), daemon=True)
    stderr_thread = threading.Thread(target=stream_pipe, args=(process.stderr, stderr_log, sys.stderr), daemon=True)
    stdout_thread.start()
    stderr_thread.start()

    try:
        process.wait(timeout=args.timeout_seconds if args.timeout_seconds > 0 else None)
        exit_code = process.returncode
        timed_out = False
    except subprocess.TimeoutExpired:
        process.kill()
        exit_code = 124
        timed_out = True

    stdout_thread.join()
    stderr_thread.join()

    metadata["ended_at_utc"] = now_utc()
    metadata["exit_code"] = exit_code
    metadata["timed_out"] = timed_out
    metadata["run_dir"] = str(run_dir)

    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.metadata_file:
        Path(args.metadata_file).write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Run directory: {run_dir}", file=sys.stderr)
    print(f"Metadata written to: {metadata_path}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
