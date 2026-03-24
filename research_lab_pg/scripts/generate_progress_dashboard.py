#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
import time
from pathlib import Path
from typing import Any


BPB_PATTERNS = [
    re.compile(r"final_int8_zlib_roundtrip_exact[^\n]*val_bpb[:=]\s*([0-9]+\.[0-9]+)"),
    re.compile(r"\bval_bpb[:=]\s*([0-9]+\.[0-9]+)"),
]
TRAIN_LOSS_PATTERN = re.compile(r"step:(\d+)/(\d+)\s+train_loss:([0-9]+\.[0-9]+)")
VAL_METRIC_PATTERN = re.compile(
    r"step:(\d+)/(\d+)\s+eval_mode:([a-z_]+)\s+stride:(\d+)\s+val_loss:([0-9]+\.[0-9]+)\s+val_bpb:([0-9]+\.[0-9]+)"
)
RUN_PHASE_ORDER = {"planner": 1, "review": 2, "worker": 3}


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def run_command(command: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        return 1, "", str(exc)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def safe_read_text(path: Path) -> str:
    try:
        return read_text(path)
    except Exception:
        return ""


def list_run_roots(project_root: Path) -> list[Path]:
    run_base = project_root / "runs" / "codex_research_loop"
    if not run_base.exists():
        return []
    return sorted([path for path in run_base.iterdir() if path.is_dir()])


def parse_meta_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in safe_read_text(path).splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def parse_latest_run(project_root: Path) -> dict[str, Any]:
    run_roots = list_run_roots(project_root)
    if not run_roots:
        return {}
    latest = run_roots[-1]
    phase_meta: dict[str, dict[str, str]] = {}
    for meta_path in sorted(latest.glob("round_*.meta")):
        meta = parse_meta_file(meta_path)
        if "worker_prompt" in meta or "review_prompt" in meta or "planner_prompt" in meta:
            phase_meta[meta_path.name] = meta
    standalone_phase_meta: dict[str, dict[str, str]] = {}
    for meta_path in sorted(latest.glob("round_*.*.meta")):
        meta = parse_meta_file(meta_path)
        phase = meta.get("phase")
        if phase:
            standalone_phase_meta[phase] = meta
    return {
        "run_root": str(latest),
        "round_summary": phase_meta,
        "phase_meta": standalone_phase_meta,
    }


def parse_run_batch(run_root: Path) -> dict[str, Any]:
    run_config = safe_read_text(run_root / "run_config.txt")
    rounds_match = re.search(r"^Rounds:\s*(\d+)", run_config, re.MULTILINE)
    configured_rounds = int(rounds_match.group(1)) if rounds_match else 0

    round_phase_meta: dict[str, dict[str, dict[str, str]]] = {}
    for meta_path in sorted(run_root.glob("round_*.*.meta")):
        meta = parse_meta_file(meta_path)
        round_id = meta.get("round")
        phase = meta.get("phase")
        if round_id and phase:
            round_phase_meta.setdefault(round_id, {})[phase] = meta

    round_numbers = sorted((int(round_id) for round_id in round_phase_meta), reverse=True)
    latest_round = str(round_numbers[0]) if round_numbers else ""
    latest_phase = ""
    latest_phase_meta = round_phase_meta.get(latest_round, {})
    if latest_phase_meta:
        latest_phase = sorted(latest_phase_meta, key=lambda phase: RUN_PHASE_ORDER.get(phase, 99))[-1]

    completed_rounds = sum(
        1 for phases in round_phase_meta.values() if phases.get("worker", {}).get("exit_code") == "0"
    )
    state = "complete" if configured_rounds and completed_rounds >= configured_rounds else "in progress"
    timestamps = [
        meta.get("end_time") or meta.get("start_time") or ""
        for phases in round_phase_meta.values()
        for meta in phases.values()
    ]
    latest_timestamp = max((timestamp for timestamp in timestamps if timestamp), default="")
    return {
        "run_root": str(run_root),
        "configured_rounds": configured_rounds,
        "completed_rounds": completed_rounds,
        "latest_round": latest_round,
        "latest_phase": latest_phase,
        "state": state,
        "latest_timestamp": latest_timestamp,
    }


def parse_run_batches(project_root: Path, limit: int = 6) -> list[dict[str, Any]]:
    run_roots = list_run_roots(project_root)
    return [parse_run_batch(path) for path in reversed(run_roots[-limit:])]


def list_training_logs(project_root: Path) -> list[Path]:
    candidates: dict[Path, float] = {}
    for pattern in ["runs/**/logs/*.txt", "logs/**/*.txt"]:
        for path in project_root.glob(pattern):
            if path.is_file():
                try:
                    candidates[path] = path.stat().st_mtime
                except OSError:
                    continue
    return [path for path, _ in sorted(candidates.items(), key=lambda item: item[1], reverse=True)]


def parse_markdown_table(path: Path) -> list[dict[str, str]]:
    lines = safe_read_text(path).splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return []
    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells, strict=True)))
    return rows


def extract_numeric_values(text: str) -> list[float]:
    return [float(match) for match in re.findall(r"([0-9]+\.[0-9]+)", text)]


def is_valid_local_bpb_row(row: dict[str, str]) -> bool:
    comparison = row.get("Comparison", "").lower()
    metric = row.get("Metric", "").lower()
    row_text = " ".join(
        [
            comparison,
            row.get("Baseline", "").lower(),
            row.get("Candidate", "").lower(),
            row.get("Delta", "").lower(),
            row.get("Notes", "").lower(),
        ]
    )
    if not comparison.startswith("local"):
        return False
    if "smoke" in comparison:
        return False
    if any(token in row_text for token in ("failed", "crash", "error", "oom", "nan")):
        return False
    return "val_bpb" in metric and "gap" not in metric


def best_local_bpb_from_comparisons(rows: list[dict[str, str]], source_path: Path) -> dict[str, Any]:
    best_value: float | None = None
    best_text = ""
    for row in rows:
        if not is_valid_local_bpb_row(row):
            continue
        for field in ["Baseline", "Candidate"]:
            for value in extract_numeric_values(row.get(field, "")):
                if best_value is None or value < best_value:
                    best_value = value
                    best_text = f"{row.get('Comparison', '')} | {field}: {row.get(field, '')}"
    if best_value is None:
        return {}
    return {
        "val_bpb": best_value,
        "path": str(source_path),
        "matched_text": best_text,
    }


def parse_section_map(path: Path) -> dict[str, str]:
    section_map: dict[str, str] = {}
    current = ""
    chunks: list[str] = []
    for line in safe_read_text(path).splitlines():
        if line.startswith("## "):
            if current:
                section_map[current] = "\n".join(chunks).strip()
            current = line[3:].strip()
            chunks = []
        else:
            chunks.append(line)
    if current:
        section_map[current] = "\n".join(chunks).strip()
    return section_map


def parse_training_run(path: Path) -> dict[str, Any]:
    text = safe_read_text(path)
    if not text:
        return {}

    train_points: list[dict[str, float]] = []
    val_by_mode: dict[str, list[dict[str, float]]] = {}
    total_steps = 0
    for match in TRAIN_LOSS_PATTERN.finditer(text):
        step = int(match.group(1))
        total_steps = max(total_steps, int(match.group(2)))
        train_points.append({"step": step, "value": float(match.group(3))})
    for match in VAL_METRIC_PATTERN.finditer(text):
        step = int(match.group(1))
        total_steps = max(total_steps, int(match.group(2)))
        eval_mode = match.group(3)
        val_by_mode.setdefault(eval_mode, []).append(
            {
                "step": step,
                "val_loss": float(match.group(5)),
                "val_bpb": float(match.group(6)),
            }
        )

    latest_step = train_points[-1]["step"] if train_points else 0
    if not latest_step:
        for points in val_by_mode.values():
            if points:
                latest_step = max(latest_step, int(points[-1]["step"]))
    stop_match = re.search(r"stopping_early:[^\n]*step:(\d+)/(\d+)", text)
    stop_reason = ""
    if stop_match:
        latest_step = max(latest_step, int(stop_match.group(1)))
        total_steps = max(total_steps, int(stop_match.group(2)))
        stop_reason = "wallclock cap"
    is_complete = "final_int8_zlib_roundtrip_exact" in text
    latest_metrics = {
        mode: {
            "val_loss": points[-1]["val_loss"],
            "val_bpb": points[-1]["val_bpb"],
            "step": int(points[-1]["step"]),
        }
        for mode, points in val_by_mode.items()
        if points
    }
    try:
        mtime = dt.datetime.fromtimestamp(path.stat().st_mtime, dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    except OSError:
        mtime = ""
    return {
        "name": path.stem,
        "path": str(path),
        "updated_at_utc": mtime,
        "latest_step": latest_step,
        "total_steps": total_steps,
        "is_complete": is_complete,
        "stop_reason": stop_reason,
        "train_points": train_points,
        "val_by_mode": val_by_mode,
        "latest_metrics": latest_metrics,
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def parse_external_sota(repo_root: Path) -> float | None:
    readme = safe_read_text(repo_root / "README.md")
    match = re.search(r"\|\s*[^|]+\|\s*([0-9]+\.[0-9]+)\s*\|", readme)
    return float(match.group(1)) if match else None


def parse_latest_sota_snapshot(path: Path) -> dict[str, Any]:
    text = safe_read_text(path)
    if not text:
        return {}
    sections = parse_section_map(path)
    top_match = re.search(
        r"Current top leaderboard entry:\s*`([^`]+)` by `([^`]+)` at `([0-9]+\.[0-9]+)`",
        text,
    )
    source_match = re.search(r"Source:\s*`([^`]+)`", text)
    entries = [line[2:].strip() for line in sections.get("Current top leaderboard entries", "").splitlines() if line.startswith("- ")]
    motifs = [line[2:].strip() for line in sections.get("Recurring motifs in the current top entries", "").splitlines() if line.startswith("- ")]
    return {
        "source": source_match.group(1) if source_match else "",
        "top_run": top_match.group(1) if top_match else "",
        "top_author": top_match.group(2) if top_match else "",
        "top_score": float(top_match.group(3)) if top_match else None,
        "entries": entries[:4],
        "motifs": motifs[:4],
    }


def should_scan_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in {".log", ".txt", ".md", ".json", ".jsonl"}:
        return False
    excluded_parts = {"records", ".git", "reference_materials", "dashboard"}
    return not any(part in excluded_parts for part in path.parts)


def scan_best_bpb(repo_root: Path, project_root: Path) -> dict[str, Any]:
    best: dict[str, Any] = {}
    seen: set[Path] = set()
    candidate_files: list[Path] = []

    candidate_files.extend(
        [
            project_root / "planning" / "experiment_ledger.md",
            project_root / "reports" / "comparison_summary.md",
            project_root / "reports" / "latest_status.md",
        ]
    )

    runs_root = project_root / "runs" / "codex_research_loop"
    if runs_root.exists():
        candidate_files.extend(sorted(runs_root.glob("**/round_*.worker.final.txt")))
        candidate_files.extend(sorted(runs_root.glob("**/round_*.worker.stdout.log")))

    for pattern in ["*.log", "*.txt", "*.jsonl"]:
        candidate_files.extend(path for path in repo_root.glob(pattern) if should_scan_file(path))

    for path in candidate_files:
        if not path.exists() or not should_scan_file(path):
            continue
        if path in seen:
            continue
        seen.add(path)
        text = safe_read_text(path)
        if not text:
            continue
        for pattern in BPB_PATTERNS:
            for match in pattern.finditer(text):
                value = float(match.group(1))
                if not best or value < best["val_bpb"]:
                    best = {
                        "val_bpb": value,
                        "path": str(path),
                        "matched_text": match.group(0),
                    }
    return best


def git_change_summary(repo_root: Path) -> dict[str, Any]:
    status_code, status_out, _ = run_command(["git", "status", "--short"], cwd=repo_root)
    diff_code, diff_out, _ = run_command(["git", "diff", "--stat"], cwd=repo_root)
    changed_files = [line.strip() for line in status_out.splitlines() if line.strip()] if status_code == 0 else []
    diff_lines = [line.strip() for line in diff_out.splitlines() if line.strip()] if diff_code == 0 else []
    return {
        "changed_files": changed_files,
        "diff_stat": diff_lines,
    }


def build_status(project_root: Path, repo_root: Path) -> dict[str, Any]:
    latest_status_sections = parse_section_map(project_root / "reports" / "latest_status.md")
    next_experiment_sections = parse_section_map(project_root / "planning" / "next_experiment.md")
    experiment_rows = parse_markdown_table(project_root / "planning" / "experiment_ledger.md")
    comparison_rows = parse_markdown_table(project_root / "reports" / "comparison_summary.md")
    latest_sota = parse_latest_sota_snapshot(project_root / "context" / "reference_materials" / "latest_sota_snapshot.md")
    if not latest_sota:
        latest_sota = parse_latest_sota_snapshot(repo_root / "docs" / "latest_sota_snapshot.md")
    latest_run = parse_latest_run(project_root)
    run_batches = parse_run_batches(project_root)
    training_runs = [run for run in (parse_training_run(path) for path in list_training_logs(project_root)[:6]) if run]
    best_bpb = best_local_bpb_from_comparisons(
        comparison_rows,
        project_root / "reports" / "comparison_summary.md",
    )
    external_sota = latest_sota.get("top_score")
    if external_sota is None:
        external_sota = parse_external_sota(repo_root)
    verifier = read_json(project_root / "context" / "verifier_env.json")
    gap_to_sota = None
    if external_sota is not None and best_bpb:
        gap_to_sota = round(best_bpb["val_bpb"] - external_sota, 6)
    return {
        "generated_at_utc": now_utc(),
        "project_root": str(project_root),
        "repo_root": str(repo_root),
        "external_sota_bpb": external_sota,
        "latest_sota": latest_sota,
        "local_best_bpb": best_bpb or None,
        "gap_to_sota": gap_to_sota,
        "latest_status_sections": latest_status_sections,
        "next_experiment_sections": next_experiment_sections,
        "experiment_rows": experiment_rows[-12:],
        "comparison_rows": comparison_rows[-12:],
        "comparison_rows_all": comparison_rows,
        "latest_run": latest_run,
        "run_batches": run_batches,
        "training_runs": training_runs,
        "verifier": verifier,
        "git": git_change_summary(repo_root),
    }


def html_list(items: list[str]) -> str:
    if not items:
        return "<p class='muted'>None</p>"
    return "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


def truncate_text(text: str, limit: int = 180) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else compact[: limit - 1].rstrip() + "..."


def classify_comparison_row(row: dict[str, str]) -> str:
    comparison = row.get("Comparison", "").lower()
    metric = row.get("Metric", "").lower()
    notes = row.get("Notes", "").lower()
    text = " ".join([comparison, metric, notes])
    if comparison.startswith("external"):
        return "external"
    if any(token in text for token in ("audit", "blocker", "storage", "asset pair", "none found")):
        return "infra"
    if comparison.startswith("local optimization") or "optimization locked recipe" in comparison:
        return "optimization"
    if any(token in text for token in ("export-only", "artifact bytes", "quantization gap", "selective-export", "zstd", "int6", "int8")):
        return "export"
    if any(token in text for token in ("sliding-window", "non-overlapping", "checkpoint `val_bpb`", "real pair", "eval")):
        return "evaluation"
    return "other"


def comparison_category_label(category: str) -> str:
    return {
        "external": "External",
        "evaluation": "Eval",
        "export": "Export",
        "optimization": "Optimization",
        "infra": "Infra",
        "other": "Other",
    }.get(category, "Other")


def render_comparison_badge(category: str) -> str:
    return f"<span class='badge badge-{html.escape(category)}'>{html.escape(comparison_category_label(category))}</span>"


def render_phase_cards(phase_meta: dict[str, dict[str, str]]) -> str:
    if not phase_meta:
        return "<p class='muted'>No run phases yet.</p>"
    cards = []
    for phase in ["planner", "review", "worker"]:
        meta = phase_meta.get(phase, {})
        if not meta:
            cards.append(
                "<div class='card'><h3>{}</h3><p class='muted'>Not available yet.</p></div>".format(html.escape(phase))
            )
            continue
        cards.append(
            "<div class='card'>"
            f"<h3>{html.escape(phase)}</h3>"
            f"<p><strong>Exit:</strong> {html.escape(meta.get('exit_code', '?'))}</p>"
            f"<p><strong>Start:</strong> {html.escape(meta.get('start_time', ''))}</p>"
            f"<p><strong>End:</strong> {html.escape(meta.get('end_time', ''))}</p>"
            f"<p class='break'><strong>Final file:</strong> {html.escape(meta.get('last_message', ''))}</p>"
            "</div>"
        )
    return "<div class='grid three'>" + "".join(cards) + "</div>"


def render_run_batch_cards(run_batches: list[dict[str, Any]]) -> str:
    if not run_batches:
        return "<p class='muted'>No run batches yet.</p>"
    cards = []
    for batch in run_batches:
        cards.append(
            "<div class='card'>"
            f"<h3>{html.escape(Path(batch['run_root']).name)}</h3>"
            f"<p class='muted break mono'>{html.escape(batch['run_root'])}</p>"
            f"<p><strong>Status:</strong> {html.escape(batch.get('state', 'unknown'))}</p>"
            f"<p><strong>Rounds:</strong> {batch.get('completed_rounds', 0)} / {batch.get('configured_rounds', 0)}</p>"
            f"<p><strong>Latest:</strong> round {html.escape(batch.get('latest_round', '?'))} {html.escape(batch.get('latest_phase', ''))}</p>"
            f"<p><strong>Updated:</strong> {html.escape(batch.get('latest_timestamp', ''))}</p>"
            "</div>"
        )
    return "<div class='grid three'>" + "".join(cards) + "</div>"


def render_table(rows: list[dict[str, str]], row_id_prefix: str = "") -> str:
    if not rows:
        return "<p class='muted'>No rows yet.</p>"
    headers = list(rows[0].keys())
    thead = "<tr>" + "".join(f"<th>{html.escape(header)}</th>" for header in headers) + "</tr>"
    body_rows = []
    for index, row in enumerate(rows, start=1):
        row_id_attr = f" id='{row_id_prefix}-{index}'" if row_id_prefix else ""
        body_rows.append(
            f"<tr{row_id_attr}>" + "".join(f"<td>{html.escape(row.get(header, ''))}</td>" for header in headers) + "</tr>"
        )
    return "<div class='table-wrap'><table><thead>{}</thead><tbody>{}</tbody></table></div>".format(
        thead, "".join(body_rows)
    )


def local_progress_points(comparison_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    best_so_far: float | None = None
    for index, row in enumerate(comparison_rows, start=1):
        comparison = row.get("Comparison", "")
        if not is_valid_local_bpb_row(row):
            continue
        candidate_vals = extract_numeric_values(row.get("Candidate", ""))
        if not candidate_vals:
            continue
        actual = candidate_vals[-1]
        if best_so_far is None or actual < best_so_far:
            best_so_far = actual
        points.append(
            {
                "label": comparison,
                "attempt_bpb": actual,
                "best_bpb": best_so_far,
                "target_id": f"comparison-row-{index}",
            }
        )
    return points


def render_progress_curve(points: list[dict[str, Any]]) -> str:
    if not points:
        return "<p class='muted'>No local BPB curve yet. No real local metric run has been recorded.</p>"

    width = 920
    height = 280
    left = 88
    right = 18
    top = 18
    bottom = 42
    values = [point["attempt_bpb"] for point in points] + [point["best_bpb"] for point in points]
    min_v = min(values)
    max_v = max(values)
    if abs(max_v - min_v) < 1e-9:
        max_v = min_v + 1e-6

    def x_at(i: int) -> float:
        usable = max(len(points) - 1, 1)
        return left + (width - left - right) * (i / usable)

    def y_at(v: float) -> float:
        frac = (v - min_v) / (max_v - min_v)
        return top + (height - top - bottom) * frac

    attempt_pts = " ".join(f"{x_at(i):.1f},{y_at(point['attempt_bpb']):.1f}" for i, point in enumerate(points))
    best_pts = " ".join(f"{x_at(i):.1f},{y_at(point['best_bpb']):.1f}" for i, point in enumerate(points))

    circles = []
    labels = []
    for i, point in enumerate(points):
        x = x_at(i)
        y = y_at(point["attempt_bpb"])
        safe_label = html.escape(point["label"], quote=True)
        circles.append(
            f"<circle class='chart-point progress-point' cx='{x:.1f}' cy='{y:.1f}' r='4' fill='#58a6ff' "
            f"tabindex='0' role='button' "
            f"data-tip-title='Attempt {i + 1}' "
            f"data-tip-line1='{safe_label}' "
            f"data-tip-line2='actual bpb: {point['attempt_bpb']:.8f}' "
            f"data-tip-line3='best so far: {point['best_bpb']:.8f}' "
            f"data-tip-line4='click to jump to the matching comparison row' "
            f"data-target-id='{html.escape(point.get('target_id', ''), quote=True)}'>"
            f"<title>{html.escape(point['label'])}: {point['attempt_bpb']:.8f}</title>"
            "</circle>"
        )
        labels.append(
            f"<text x='{x:.1f}' y='{height - 12:.1f}' text-anchor='middle' fill='#9da7b3' font-size='11'>"
            f"{i + 1}</text>"
        )

    y_ticks = []
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        value = min_v + (max_v - min_v) * frac
        y = y_at(value)
        y_ticks.append(
            f"<line x1='{left}' y1='{y:.1f}' x2='{width - right}' y2='{y:.1f}' stroke='#30363d' stroke-dasharray='4 4' />"
            f"<text x='{left - 8}' y='{y + 4:.1f}' text-anchor='end' fill='#9da7b3' font-size='11'>{value:.6f}</text>"
        )

    return (
        "<div class='card'>"
        "<h3>Local BPB Curve</h3>"
        "<p class='muted'>Blue = actual candidate BPB for each successful real local comparison. Green = best-so-far BPB. Failed or smoke-only rows are skipped.</p>"
        "<div class='chart-shell'>"
        f"<svg class='progress-curve-svg' viewBox='0 0 {width} {height}' width='100%' height='auto' role='img' aria-label='Local BPB progress curve'>"
        f"{''.join(y_ticks)}"
        f"<polyline fill='none' stroke='#58a6ff' stroke-width='3' points='{attempt_pts}' />"
        f"<polyline fill='none' stroke='#3fb950' stroke-width='3' points='{best_pts}' />"
        f"{''.join(circles)}"
        f"{''.join(labels)}"
        f"<text x='{left}' y='{height - 24}' fill='#9da7b3' font-size='11'>attempt index</text>"
        "</svg>"
        "<div class='chart-tooltip' hidden></div>"
        "</div>"
        "</div>"
    )


def render_line_chart(
    title: str,
    subtitle: str,
    series: list[dict[str, Any]],
    x_label: str = "step",
    target_id: str = "",
) -> str:
    non_empty_series = [item for item in series if item.get("points")]
    if not non_empty_series:
        return (
            "<div class='card'>"
            f"<h3>{html.escape(title)}</h3>"
            f"<p class='muted'>{html.escape(subtitle)}</p>"
            "<p class='muted'>No points logged yet.</p>"
            "</div>"
        )

    width = 920
    height = 260
    left = 88
    right = 18
    top = 18
    bottom = 42
    max_x = max(point["x"] for item in non_empty_series for point in item["points"])
    values = [point["y"] for item in non_empty_series for point in item["points"]]
    min_v = min(values)
    max_v = max(values)
    if abs(max_v - min_v) < 1e-9:
        max_v = min_v + 1e-6

    def x_at(v: float) -> float:
        return left + (width - left - right) * (v / max(max_x, 1))

    def y_at(v: float) -> float:
        frac = (v - min_v) / (max_v - min_v)
        return top + (height - top - bottom) * frac

    lines: list[str] = []
    legend: list[str] = []
    point_titles: list[str] = []
    for item in non_empty_series:
        pts = " ".join(f"{x_at(point['x']):.1f},{y_at(point['y']):.1f}" for point in item["points"])
        lines.append(f"<polyline fill='none' stroke='{item['color']}' stroke-width='3' points='{pts}' />")
        legend.append(
            f"<span style='display:inline-block;margin-right:14px;'>"
            f"<span style='display:inline-block;width:10px;height:10px;background:{item['color']};border-radius:999px;margin-right:6px;'></span>"
            f"{html.escape(item['label'])}</span>"
        )
        for point in item["points"]:
            point_titles.append(
                f"<circle class='chart-point' cx='{x_at(point['x']):.1f}' cy='{y_at(point['y']):.1f}' "
                f"r='3.5' fill='{item['color']}' tabindex='0' role='button' "
                f"data-tip-title='{html.escape(title, quote=True)}' "
                f"data-tip-line1='{html.escape(item['label'], quote=True)}' "
                f"data-tip-line2='{html.escape(x_label, quote=True)}: {int(point['x'])}' "
                f"data-tip-line3='value: {point['y']:.6f}' "
                f"data-tip-line4='click to jump to the parent training run' "
                f"data-target-id='{html.escape(target_id, quote=True)}'>"
                f"<title>{html.escape(item['label'])}: step {int(point['x'])}, value {point['y']:.6f}</title>"
                "</circle>"
            )

    y_ticks = []
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        value = min_v + (max_v - min_v) * frac
        y = y_at(value)
        y_ticks.append(
            f"<line x1='{left}' y1='{y:.1f}' x2='{width - right}' y2='{y:.1f}' stroke='#30363d' stroke-dasharray='4 4' />"
            f"<text x='{left - 8}' y='{y + 4:.1f}' text-anchor='end' fill='#9da7b3' font-size='11'>{value:.4f}</text>"
        )
    x_ticks = []
    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
        value = round(max_x * frac)
        x = x_at(value)
        x_ticks.append(
            f"<text x='{x:.1f}' y='{height - 12:.1f}' text-anchor='middle' fill='#9da7b3' font-size='11'>{value}</text>"
        )

    return (
        "<div class='card'>"
        f"<h3>{html.escape(title)}</h3>"
        f"<p class='muted'>{html.escape(subtitle)}</p>"
        f"<p class='muted'>{''.join(legend)}</p>"
        "<div class='chart-shell'>"
        f"<svg viewBox='0 0 {width} {height}' width='100%' height='auto' role='img' aria-label='{html.escape(title)}'>"
        f"{''.join(y_ticks)}"
        f"{''.join(lines)}"
        f"{''.join(point_titles)}"
        f"{''.join(x_ticks)}"
        f"<text x='{left}' y='{height - 24}' fill='#9da7b3' font-size='11'>{html.escape(x_label)}</text>"
        "</svg>"
        "<div class='chart-tooltip' hidden></div>"
        "</div>"
        "</div>"
    )


def render_training_runs(training_runs: list[dict[str, Any]]) -> str:
    if not training_runs:
        return "<p class='muted'>No training-run logs detected yet.</p>"

    blocks: list[str] = []
    loss_colors = ["#58a6ff", "#3fb950", "#d29922", "#f778ba"]
    bpb_colors = ["#3fb950", "#d29922", "#f778ba", "#a371f7"]
    for run_index, run in enumerate(training_runs, start=1):
        run_target_id = f"training-run-{run_index}"
        loss_series = []
        if run.get("train_points"):
            loss_series.append(
                {
                    "label": "train_loss",
                    "color": loss_colors[0],
                    "points": [{"x": point["step"], "y": point["value"]} for point in run["train_points"]],
                }
            )
        for idx, eval_mode in enumerate(sorted(run.get("val_by_mode", {}).keys())):
            points = run["val_by_mode"][eval_mode]
            loss_series.append(
                {
                    "label": f"val_loss:{eval_mode}",
                    "color": loss_colors[(idx + 1) % len(loss_colors)],
                    "points": [{"x": point["step"], "y": point["val_loss"]} for point in points],
                }
            )
        bpb_series = []
        for idx, eval_mode in enumerate(sorted(run.get("val_by_mode", {}).keys())):
            points = run["val_by_mode"][eval_mode]
            bpb_series.append(
                {
                    "label": f"val_bpb:{eval_mode}",
                    "color": bpb_colors[idx % len(bpb_colors)],
                    "points": [{"x": point["step"], "y": point["val_bpb"]} for point in points],
                }
            )

        latest_metric_bits = []
        for eval_mode, metric in sorted(run.get("latest_metrics", {}).items()):
            latest_metric_bits.append(
                f"{eval_mode}: val_loss {metric['val_loss']:.4f}, val_bpb {metric['val_bpb']:.4f} @ step {metric['step']}"
            )
        status_text = "complete" if run.get("is_complete") else "in progress"
        if run.get("stop_reason"):
            status_text += f" ({run['stop_reason']})"
        blocks.append(
            f"<div class='card' id='{run_target_id}'>"
            f"<h3>{html.escape(run['name'])}</h3>"
            f"<p class='muted mono break'>{html.escape(run['path'])}</p>"
            f"<p class='muted'>Status: {html.escape(status_text)}. "
            f"Latest step: {run.get('latest_step', 0)} / {run.get('total_steps', 0)}. "
            f"Updated: {html.escape(run.get('updated_at_utc', ''))}</p>"
            f"<p class='muted'>{html.escape(' | '.join(latest_metric_bits) if latest_metric_bits else 'Validation metrics not logged yet.')}</p>"
            "<div class='grid two'>"
            f"{render_line_chart('Loss Curve', 'Blue = training loss. Other lines = validation loss by eval mode.', loss_series, target_id=run_target_id)}"
            f"{render_line_chart('BPB Curve', 'Validation BPB over time, split by eval mode.', bpb_series, target_id=run_target_id)}"
            "</div>"
            "</div>"
        )
    return "".join(blocks)


def render_experiment_highlights(experiment_rows: list[dict[str, str]]) -> str:
    if not experiment_rows:
        return "<p class='muted'>No experiments yet.</p>"
    cards = []
    for row in reversed(experiment_rows[-4:]):
        cards.append(
            "<div class='card'>"
            f"<h3>{html.escape(row.get('ID', ''))}</h3>"
            f"<p class='muted'>{html.escape(row.get('Category', ''))}</p>"
            f"<p><strong>Result:</strong> {html.escape(truncate_text(row.get('Actual Result', ''), 220))}</p>"
            f"<p><strong>Interpretation:</strong> {html.escape(truncate_text(row.get('Interpretation', ''), 180))}</p>"
            f"<p><strong>Next:</strong> {html.escape(truncate_text(row.get('Next Step', ''), 140))}</p>"
            "</div>"
        )
    return "<div class='grid two'>" + "".join(cards) + "</div>"


def render_comparison_highlights(comparison_rows: list[dict[str, str]]) -> str:
    if not comparison_rows:
        return "<p class='muted'>No comparisons yet.</p>"
    preferred_rows = [row for row in comparison_rows if row.get("Comparison", "").lower().startswith("local")]
    rows = preferred_rows[-4:] if preferred_rows else comparison_rows[-4:]
    cards = []
    for row in reversed(rows):
        category = classify_comparison_row(row)
        cards.append(
            "<div class='card'>"
            f"<h3>{render_comparison_badge(category)} {html.escape(truncate_text(row.get('Comparison', ''), 90))}</h3>"
            f"<p class='muted'>{html.escape(row.get('Metric', ''))}</p>"
            f"<p><strong>Baseline:</strong> {html.escape(row.get('Baseline', ''))}</p>"
            f"<p><strong>Candidate:</strong> {html.escape(row.get('Candidate', ''))}</p>"
            f"<p><strong>Delta:</strong> {html.escape(row.get('Delta', ''))}</p>"
            f"<p><strong>Notes:</strong> {html.escape(truncate_text(row.get('Notes', ''), 160))}</p>"
            "</div>"
        )
    return "<div class='grid two'>" + "".join(cards) + "</div>"


def render_comparison_summary(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "<p class='muted'>No comparison rows yet.</p>"
    categories = ["all", "external", "evaluation", "export", "optimization", "infra", "other"]
    counts = {category: 0 for category in categories}
    prepared: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        category = classify_comparison_row(row)
        prepared.append({"index": index, "category": category, "row": row})
        counts["all"] += 1
        counts[category] += 1

    buttons = []
    for category in categories:
        if category != "all" and counts[category] == 0:
            continue
        label = "All" if category == "all" else comparison_category_label(category)
        active = " is-active" if category == "all" else ""
        buttons.append(
            f"<button class='tab-button{active}' type='button' data-comparison-filter='{html.escape(category)}'>"
            f"{html.escape(label)} <span class='tab-count'>{counts[category]}</span>"
            "</button>"
        )

    headers = ["Category", "Comparison", "Metric", "Baseline", "Candidate", "Delta", "Notes"]
    thead = "<tr>" + "".join(f"<th>{html.escape(header)}</th>" for header in headers) + "</tr>"
    body_rows = []
    for item in prepared:
        row = item["row"]
        category = item["category"]
        body_rows.append(
            f"<tr id='comparison-row-{item['index']}' data-comparison-category='{html.escape(category)}'>"
            f"<td>{render_comparison_badge(category)}</td>"
            f"<td>{html.escape(row.get('Comparison', ''))}</td>"
            f"<td>{html.escape(row.get('Metric', ''))}</td>"
            f"<td>{html.escape(row.get('Baseline', ''))}</td>"
            f"<td>{html.escape(row.get('Candidate', ''))}</td>"
            f"<td>{html.escape(row.get('Delta', ''))}</td>"
            f"<td>{html.escape(row.get('Notes', ''))}</td>"
            "</tr>"
        )
    table_html = "<div class='table-wrap'><table><thead>{}</thead><tbody>{}</tbody></table></div>".format(
        thead, "".join(body_rows)
    )
    return (
        "<div class='comparison-summary'>"
        "<p class='muted'>Filter by comparison type. The same row IDs are preserved, so chart jumps still land on the correct comparison.</p>"
        f"<div class='tab-bar'>{''.join(buttons)}</div>"
        f"{table_html}"
        "</div>"
    )


def render_latest_sota_summary(latest_sota: dict[str, Any]) -> str:
    if not latest_sota:
        return "<p class='muted'>No live SOTA snapshot found yet.</p>"
    score = latest_sota.get("top_score")
    score_text = f"{score:.4f}" if score is not None else "unknown"
    cards = [
        "<div class='card'>"
        "<h3>Current Top Run</h3>"
        f"<p><strong>Run:</strong> {html.escape(latest_sota.get('top_run', 'unknown'))}</p>"
        f"<p><strong>Author:</strong> {html.escape(latest_sota.get('top_author', 'unknown'))}</p>"
        f"<p><strong>Score:</strong> {html.escape(score_text)}</p>"
        f"<p class='muted break mono'>{html.escape(latest_sota.get('source', ''))}</p>"
        "</div>",
        "<div class='card'>"
        "<h3>Recent Top Entries</h3>"
        f"{html_list(latest_sota.get('entries', []))}"
        "</div>",
        "<div class='card'>"
        "<h3>Recurring Motifs</h3>"
        f"{html_list(latest_sota.get('motifs', []))}"
        "</div>",
    ]
    return "<div class='grid three'>" + "".join(cards) + "</div>"


def render_dashboard(status: dict[str, Any], refresh_seconds: int) -> str:
    local_best = status.get("local_best_bpb")
    local_best_display = "No real local result yet"
    local_best_path = ""
    if local_best:
        local_best_display = f"{local_best['val_bpb']:.6f}"
        local_best_path = local_best["path"]
    latest_sota = status.get("latest_sota", {})
    external_display = (
        f"{status['external_sota_bpb']:.4f}" if status.get("external_sota_bpb") is not None else "Unknown"
    )
    gap_display = "Unknown" if status.get("gap_to_sota") is None else f"{status['gap_to_sota']:+.6f}"
    current_question = status.get("latest_status_sections", {}).get("Most Important Open Question", "")
    recommended_next = status.get("latest_status_sections", {}).get("Recommended Next Step", "")
    current_experiment = status.get("latest_status_sections", {}).get("Active Experiment ID", "")
    verifier = status.get("verifier", {})
    ready = verifier.get("summary", {}).get("ready_for_real_iteration")
    data_info = verifier.get("data", {})
    train_count = data_info.get("sp1024_train_shards", {}).get("count", 0)
    val_count = data_info.get("sp1024_val_shards", {}).get("count", 0)
    tokenizer_ok = data_info.get("tokenizer_model_exists", False)
    latest_run = status.get("latest_run", {})
    run_batches = status.get("run_batches", [])
    phase_meta = latest_run.get("phase_meta", {})
    changed_files = status.get("git", {}).get("changed_files", [])
    diff_stat = status.get("git", {}).get("diff_stat", [])
    progress_curve = render_progress_curve(local_progress_points(status.get("comparison_rows_all", [])))
    training_runs_html = render_training_runs(status.get("training_runs", []))
    experiment_highlights = render_experiment_highlights(status.get("experiment_rows", []))
    comparison_highlights = render_comparison_highlights(status.get("comparison_rows", []))
    latest_sota_html = render_latest_sota_summary(latest_sota)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Parameter Golf Research Dashboard</title>
  <meta http-equiv="refresh" content="{refresh_seconds}">
  <style>
    :root {{
      --bg: #0d1117;
      --panel: #161b22;
      --panel-2: #1f2630;
      --text: #e6edf3;
      --muted: #9da7b3;
      --accent: #58a6ff;
      --good: #3fb950;
      --warn: #d29922;
      --border: #30363d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 24px;
      background: var(--bg);
      color: var(--text);
      font: 14px/1.5 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    h1, h2, h3 {{ margin: 0 0 12px 0; }}
    .muted {{ color: var(--muted); }}
    .break {{ overflow-wrap: anywhere; word-break: break-word; white-space: normal; }}
    .grid {{
      display: grid;
      gap: 16px;
      margin: 16px 0 24px;
    }}
    .grid > * {{
      min-width: 0;
    }}
    .grid.three {{ grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
    .grid.two {{ grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }}
    .card {{
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      min-width: 0;
    }}
    .card h3, .card p, .card li {{
      overflow-wrap: anywhere;
      word-break: break-word;
    }}
    .metric {{
      font-size: 28px;
      font-weight: 700;
      color: var(--accent);
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      border: 1px solid transparent;
      vertical-align: middle;
      margin-right: 8px;
      white-space: nowrap;
    }}
    .badge-external {{ background: rgba(163, 113, 247, 0.14); color: #c297ff; border-color: rgba(163, 113, 247, 0.35); }}
    .badge-evaluation {{ background: rgba(88, 166, 255, 0.14); color: #7cc0ff; border-color: rgba(88, 166, 255, 0.35); }}
    .badge-export {{ background: rgba(63, 185, 80, 0.14); color: #71d485; border-color: rgba(63, 185, 80, 0.35); }}
    .badge-optimization {{ background: rgba(242, 153, 34, 0.14); color: #f2bb68; border-color: rgba(242, 153, 34, 0.35); }}
    .badge-infra {{ background: rgba(247, 120, 186, 0.14); color: #ff9acc; border-color: rgba(247, 120, 186, 0.35); }}
    .badge-other {{ background: rgba(157, 167, 179, 0.14); color: #c6d0db; border-color: rgba(157, 167, 179, 0.35); }}
    .section {{
      margin: 24px 0;
      scroll-margin-top: 16px;
    }}
    .tab-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 12px 0 16px;
    }}
    .tab-button {{
      border: 1px solid var(--border);
      background: #11161d;
      color: var(--muted);
      border-radius: 999px;
      padding: 8px 12px;
      font: inherit;
      font-weight: 600;
      cursor: pointer;
    }}
    .tab-button.is-active {{
      background: rgba(88, 166, 255, 0.16);
      color: var(--text);
      border-color: rgba(88, 166, 255, 0.45);
    }}
    .tab-count {{
      color: var(--accent);
      margin-left: 4px;
    }}
    .table-wrap {{
      overflow-x: auto;
    }}
    .chart-shell {{
      position: relative;
    }}
    .chart-tooltip {{
      position: absolute;
      z-index: 5;
      min-width: 220px;
      max-width: min(320px, calc(100% - 16px));
      pointer-events: none;
      background: rgba(17, 22, 29, 0.98);
      border: 1px solid var(--border);
      border-radius: 10px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
      padding: 10px 12px;
      color: var(--text);
    }}
    .chart-tooltip p {{
      margin: 4px 0;
    }}
    .chart-tooltip .tooltip-title {{
      font-weight: 700;
      color: #e6edf3;
    }}
    .chart-tooltip .tooltip-metric {{
      color: var(--accent);
      font-weight: 600;
    }}
    .chart-point {{
      cursor: pointer;
      transform-box: fill-box;
      transform-origin: center;
      transition: transform 120ms ease, stroke 120ms ease, stroke-width 120ms ease;
    }}
    .chart-point:hover,
    .chart-point:focus-visible {{
      transform: scale(1.7);
      stroke: #e6edf3;
      stroke-width: 1.5;
      outline: none;
    }}
    .chart-point.is-active {{
      transform: scale(1.9);
      stroke: #f2cc60;
      stroke-width: 2;
    }}
    .flash-target {{
      box-shadow: 0 0 0 2px #f2cc60 inset, 0 0 0 1px #f2cc60;
      transition: box-shadow 180ms ease;
    }}
    tr.flash-target {{
      background: rgba(242, 204, 96, 0.12);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #11161d;
      font-weight: 600;
    }}
    code {{
      background: #11161d;
      border: 1px solid var(--border);
      padding: 2px 6px;
      border-radius: 6px;
    }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    details {{
      margin-top: 12px;
    }}
    summary {{
      cursor: pointer;
      color: var(--accent);
      font-weight: 600;
      margin-bottom: 12px;
    }}
  </style>
</head>
<body>
  <h1>Parameter Golf Research Dashboard</h1>
  <p class="muted">Inspired by the lightweight experiment-tracking spirit of Karpathy's <a href="https://github.com/karpathy/autoresearch">`autoresearch`</a>. Generated at {html.escape(status["generated_at_utc"])}.</p>

  <div class="grid three">
    <div class="card">
      <h3>Real Local Best BPB</h3>
      <div class="metric">{html.escape(local_best_display)}</div>
      <p class="muted mono break">{html.escape(local_best_path)}</p>
    </div>
    <div class="card">
      <h3>Current SOTA</h3>
      <div class="metric">{html.escape(external_display)}</div>
      <p class="muted">Top repo leaderboard score</p>
    </div>
    <div class="card">
      <h3>Gap To SOTA</h3>
      <div class="metric">{html.escape(gap_display)}</div>
      <p class="muted">Local best minus current top score</p>
    </div>
  </div>

  <div class="grid three">
    <div class="card">
      <h3>Active Experiment</h3>
      <p class="mono">{html.escape(current_experiment)}</p>
    </div>
    <div class="card">
      <h3>Open Question</h3>
      <p>{html.escape(current_question)}</p>
    </div>
    <div class="card">
      <h3>Recommended Next Step</h3>
      <p>{html.escape(recommended_next)}</p>
    </div>
  </div>

  <div class="grid three">
    <div class="card">
      <h3>Verifier Ready</h3>
      <div class="metric">{html.escape("yes" if ready else "no")}</div>
      <p class="muted">Real iteration readiness from `verifier_env.json`</p>
    </div>
    <div class="card">
      <h3>SP1024 Train Shards</h3>
      <div class="metric">{html.escape(str(train_count))}</div>
      <p class="muted">Downloaded train shard count</p>
    </div>
    <div class="card">
      <h3>Validation / Tokenizer</h3>
      <div class="metric">{html.escape(f"{val_count} / {'ok' if tokenizer_ok else 'missing'}")}</div>
      <p class="muted">Validation shards and tokenizer status</p>
    </div>
  </div>

  <div class="section">
    <h2>Run Batches</h2>
    {render_run_batch_cards(run_batches)}
  </div>

  <div class="section">
    <h2>Latest Run Detail</h2>
    <p class="muted mono break">{html.escape(latest_run.get("run_root", "No run root yet"))}</p>
    {render_phase_cards(phase_meta)}
  </div>

  <div class="section">
    <h2>Progress Curve</h2>
    {progress_curve}
  </div>

  <div class="section">
    <h2>Training Job Curves</h2>
    <p class="muted">Only real training jobs appear here. Export-only experiments reuse an existing checkpoint, so they do not create a new training-loss curve.</p>
    {training_runs_html}
  </div>

  <div class="section">
    <h2>Latest SOTA Snapshot</h2>
    {latest_sota_html}
  </div>

  <div class="section">
    <h2>What Changed</h2>
    <div class="grid three">
      <div class="card">
        <h3>Git Status</h3>
        {html_list(changed_files)}
      </div>
      <div class="card" style="grid-column: span 2;">
        <h3>Diff Stat</h3>
        {html_list(diff_stat)}
      </div>
    </div>
  </div>

  <div class="section">
    <h2>Experiment Highlights</h2>
    {experiment_highlights}
    <details>
      <summary>Full Experiment Ledger</summary>
      {render_table(status.get("experiment_rows", []))}
    </details>
  </div>

  <div class="section">
    <h2>Comparison Highlights</h2>
    {comparison_highlights}
    <details>
      <summary>Full Comparison Summary</summary>
      {render_comparison_summary(status.get("comparison_rows_all", []))}
    </details>
  </div>
  <script>
    (() => {{
      const shells = document.querySelectorAll('.chart-shell');
      let flashedTarget = null;
      const comparisonSummary = document.querySelector('.comparison-summary');
      const comparisonButtons = comparisonSummary ? comparisonSummary.querySelectorAll('[data-comparison-filter]') : [];
      const comparisonRows = comparisonSummary ? comparisonSummary.querySelectorAll('[data-comparison-category]') : [];

      const applyComparisonFilter = (filter) => {{
        for (const button of comparisonButtons) {{
          button.classList.toggle('is-active', button.dataset.comparisonFilter === filter);
        }}
        for (const row of comparisonRows) {{
          row.hidden = !(filter === 'all' || row.dataset.comparisonCategory === filter);
        }}
      }};

      for (const button of comparisonButtons) {{
        button.addEventListener('click', () => applyComparisonFilter(button.dataset.comparisonFilter || 'all'));
      }}
      if (comparisonButtons.length) {{
        applyComparisonFilter('all');
      }}

      for (const shell of shells) {{
        const tooltip = shell.querySelector('.chart-tooltip');
        const points = shell.querySelectorAll('.chart-point');
        if (!tooltip || !points.length) {{
          continue;
        }}

        let activePoint = null;

        const positionTooltip = (event) => {{
          const rect = shell.getBoundingClientRect();
          const tooltipRect = tooltip.getBoundingClientRect();
          const offsetX = event.clientX - rect.left + 14;
          const offsetY = event.clientY - rect.top - tooltipRect.height - 14;
          const maxLeft = Math.max(rect.width - tooltipRect.width - 8, 8);
          const left = Math.min(Math.max(offsetX, 8), maxLeft);
          const top = offsetY < 8 ? Math.min(event.clientY - rect.top + 14, rect.height - tooltipRect.height - 8) : offsetY;
          tooltip.style.left = `${{left}}px`;
          tooltip.style.top = `${{Math.max(top, 8)}}px`;
        }};

        const renderTooltip = (point) => {{
          const lines = [
            point.dataset.tipLine1,
            point.dataset.tipLine2,
            point.dataset.tipLine3,
            point.dataset.tipLine4,
          ].filter(Boolean);
          tooltip.innerHTML =
            `<p class="tooltip-title">${{point.dataset.tipTitle || 'Point'}}</p>` +
            lines
              .map((line, index) => `<p class="${{index === 1 ? 'tooltip-metric' : ''}}">${{line}}</p>`)
              .join('');
        }};

        const showTooltip = (point, event) => {{
          renderTooltip(point);
          tooltip.hidden = false;
          positionTooltip(event);
        }};

        const hideTooltip = () => {{
          if (activePoint) {{
            return;
          }}
          tooltip.hidden = true;
        }};

        const setActivePoint = (point) => {{
          for (const item of points) {{
            item.classList.toggle('is-active', item === point);
          }}
          activePoint = point;
        }};

        const flashTarget = (target) => {{
          if (flashedTarget) {{
            flashedTarget.classList.remove('flash-target');
          }}
          flashedTarget = target;
          target.classList.add('flash-target');
          window.setTimeout(() => {{
            if (flashedTarget === target) {{
              target.classList.remove('flash-target');
              flashedTarget = null;
            }}
          }}, 1800);
        }};

        const revealTarget = (target) => {{
          let parent = target.parentElement;
          while (parent) {{
            if (parent.tagName === 'DETAILS') {{
              parent.open = true;
            }}
            parent = parent.parentElement;
          }}
          if (target.dataset.comparisonCategory) {{
            applyComparisonFilter('all');
          }}
          window.requestAnimationFrame(() => {{
            target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            flashTarget(target);
          }});
        }};

        for (const point of points) {{
          point.addEventListener('mouseenter', (event) => showTooltip(point, event));
          point.addEventListener('mousemove', (event) => showTooltip(point, event));
          point.addEventListener('mouseleave', hideTooltip);
          point.addEventListener('focus', () => {{
            const rect = point.getBoundingClientRect();
            showTooltip(point, {{ clientX: rect.left + rect.width / 2, clientY: rect.top }});
          }});
          point.addEventListener('blur', hideTooltip);
          point.addEventListener('click', (event) => {{
            const isSamePoint = activePoint === point;
            setActivePoint(isSamePoint ? null : point);
            if (isSamePoint) {{
              tooltip.hidden = true;
            }} else {{
              showTooltip(point, event);
            }}
            const targetId = point.dataset.targetId;
            if (targetId) {{
              const target = document.getElementById(targetId);
              if (target) {{
                revealTarget(target);
              }}
            }}
          }});
          point.addEventListener('keydown', (event) => {{
            if (event.key === 'Enter' || event.key === ' ') {{
              event.preventDefault();
              point.click();
            }}
          }});
        }}

        shell.addEventListener('mouseleave', () => {{
          if (!activePoint) {{
            tooltip.hidden = true;
          }}
        }});
      }}
    }})();
  </script>
</body>
</html>
"""


def write_dashboard(project_root: Path, repo_root: Path, output_dir: Path, refresh_seconds: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    status = build_status(project_root, repo_root)
    (output_dir / "status.json").write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / "index.html").write_text(render_dashboard(status, refresh_seconds), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a live-ish HTML dashboard for Parameter Golf research progress.")
    parser.add_argument("--project-root", required=True, help="Path to a research_lab_pg project root.")
    parser.add_argument("--repo-root", required=True, help="Path to the main parameter-golf repo root.")
    parser.add_argument("--output-dir", required=True, help="Directory to write status.json and index.html.")
    parser.add_argument("--refresh-seconds", type=int, default=15, help="HTML auto-refresh cadence.")
    parser.add_argument("--watch-seconds", type=int, default=0, help="If >0, regenerate dashboard every N seconds.")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()

    if args.watch_seconds > 0:
        while True:
            write_dashboard(project_root, repo_root, output_dir, args.refresh_seconds)
            time.sleep(max(args.watch_seconds, 1))
    else:
        write_dashboard(project_root, repo_root, output_dir, args.refresh_seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
