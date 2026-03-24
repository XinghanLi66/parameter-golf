#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen


REMOTE_README_URL = "https://raw.githubusercontent.com/openai/parameter-golf/main/README.md"

KEYWORD_PATTERNS = [
    ("ema", "EMA"),
    ("gptq-lite", "GPTQ-lite"),
    ("partial rope", "Partial RoPE"),
    ("xsa", "XSA"),
    ("mlp3x", "MLP3x"),
    ("int6", "Int6 quantization"),
    ("int5", "Int5 quantization"),
    ("qat", "QAT / STE"),
    ("sliding", "Sliding-window eval"),
    ("bigramhash", "BigramHash"),
    ("smeargate", "SmearGate"),
    ("muon", "Muon / WD tuning"),
    ("warmdown", "Warmdown tuning"),
    ("zstd", "zstd export"),
    ("seq2048", "Longer context"),
    ("seq4096", "Longer context"),
    ("lora", "LoRA / TTT"),
]


def now_utc() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_remote_readme(timeout_seconds: int) -> tuple[str | None, str]:
    try:
        with urlopen(REMOTE_README_URL, timeout=timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace"), REMOTE_README_URL
    except (URLError, TimeoutError, OSError):
        return None, REMOTE_README_URL


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def parse_leaderboard_rows(readme_text: str) -> list[dict[str, str]]:
    lines = readme_text.splitlines()
    in_leaderboard = False
    collecting = False
    table_lines: list[str] = []
    for line in lines:
        if line.startswith("## Leaderboard"):
            in_leaderboard = True
            continue
        if not in_leaderboard:
            continue
        if line.startswith("## ") or line.startswith("#### "):
            break
        if line.lstrip().startswith("|"):
            collecting = True
            table_lines.append(line)
            continue
        if collecting:
            break

    if len(table_lines) < 3:
        return []

    headers = [cell.strip() for cell in table_lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def strip_markdown_links(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def normalize_name(text: str) -> str:
    return re.sub(r"\s+", " ", strip_markdown_links(text)).strip().lower()


def summarize_patterns(rows: list[dict[str, str]], top_n: int = 8) -> list[str]:
    counts: dict[str, int] = {}
    for row in rows[:top_n]:
        haystack = f"{row.get('Run', '')} {row.get('Summary', '')}".lower()
        for needle, label in KEYWORD_PATTERNS:
            if needle in haystack:
                counts[label] = counts.get(label, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [f"`{label}` appears in {count} of the current top {top_n} leaderboard entries." for label, count in ranked[:8]]


def format_rows(rows: list[dict[str, str]], limit: int) -> list[str]:
    formatted: list[str] = []
    for index, row in enumerate(rows[:limit], start=1):
        run_name = strip_markdown_links(row.get("Run", ""))
        score = row.get("Score", "")
        author = row.get("Author", "")
        summary = strip_markdown_links(row.get("Summary", ""))
        date = row.get("Date", "")
        formatted.append(f"{index}. `{run_name}` | score `{score}` | {author} | {date} | {summary}")
    return formatted


def build_snapshot(
    remote_rows: list[dict[str, str]],
    local_rows: list[dict[str, str]],
    source_label: str,
) -> str:
    top_rows = remote_rows or local_rows
    if not top_rows:
        top_rows = []
    local_names = {normalize_name(row.get("Run", "")) for row in local_rows}
    remote_only = [row for row in remote_rows if normalize_name(row.get("Run", "")) not in local_names]
    top_score = top_rows[0].get("Score", "unknown") if top_rows else "unknown"
    top_run = strip_markdown_links(top_rows[0].get("Run", "unknown")) if top_rows else "unknown"
    top_author = top_rows[0].get("Author", "unknown") if top_rows else "unknown"
    pattern_lines = summarize_patterns(top_rows)
    latest_lines = format_rows(top_rows, limit=8)
    new_since_local = format_rows(remote_only, limit=5)

    parts = [
        "# Latest Parameter Golf SOTA Snapshot",
        "",
        f"- Generated at: `{now_utc()}`",
        f"- Source: `{source_label}`",
        f"- Current top leaderboard entry: `{top_run}` by `{top_author}` at `{top_score}`",
        "",
        "## Why this file exists",
        "",
        "Use this as the live companion to `docs/sota_review.md`.",
        "The older review explains the broad design space; this file keeps the research loop aligned with the current leaderboard and recent winning motifs.",
        "",
        "## Current competition reminders",
        "",
        "- Goal: minimize validation `val_bpb` on FineWeb under the 16MB artifact cap.",
        "- Record-track submissions must still train within 10 minutes on 8xH100 and clear the significance bar described in the official repo README.",
        "- Evaluation-side tricks matter. Do not treat train loss alone as sufficient evidence.",
        "",
        "## Current top leaderboard entries",
        "",
    ]
    parts.extend([f"- {line}" for line in latest_lines] if latest_lines else ["- No leaderboard rows parsed."])
    parts.extend(
        [
            "",
            "## Newly visible runs vs local checkout",
            "",
        ]
    )
    parts.extend(
        [f"- {line}" for line in new_since_local]
        if new_since_local
        else ["- No remote-only rows detected relative to the local README snapshot."]
    )
    parts.extend(
        [
            "",
            "## Recurring motifs in the current top entries",
            "",
        ]
    )
    parts.extend(
        [f"- {line}" for line in pattern_lines]
        if pattern_lines
        else ["- No recurring motif summary available yet."]
    )
    parts.extend(
        [
            "",
        "## How planner/reviewer should use this",
        "",
        "- Before proposing a new experiment, identify which top-run motif you are testing, extending, or intentionally excluding.",
        "- Prefer small deltas against the strongest nearby baseline instead of vaguely copying multiple leaderboard ideas at once.",
        "- If the current top runs moved ahead since the older SOTA review, explain whether our next experiment closes that gap on architecture, optimization, evaluation, or export.",
        "- If you are not testing a current leaderboard motif, explicitly justify why the deviation is still scientifically valuable.",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh a live Parameter Golf SOTA snapshot for the research loop.")
    parser.add_argument("--repo-root", required=True, help="Path to the local parameter-golf repo.")
    parser.add_argument("--output", action="append", required=True, help="Output markdown file path. May be passed multiple times.")
    parser.add_argument("--timeout-seconds", type=int, default=15, help="HTTP timeout for the remote README fetch.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    local_readme = read_text(repo_root / "README.md")
    remote_readme, remote_source = fetch_remote_readme(args.timeout_seconds)

    local_rows = parse_leaderboard_rows(local_readme)
    remote_rows = parse_leaderboard_rows(remote_readme or "")
    source_label = remote_source if remote_rows else str(repo_root / "README.md")
    snapshot = build_snapshot(remote_rows, local_rows, source_label)

    for output_name in args.output:
        output_path = Path(output_name).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(snapshot, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
