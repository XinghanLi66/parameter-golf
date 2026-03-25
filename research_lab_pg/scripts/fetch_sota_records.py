#!/usr/bin/env python3
"""
Fetch the top SOTA training scripts from openai/parameter-golf and save them
as self-contained markdown reference files for the research loop agents.

Each top submission is saved as:
  {output_dir}/sota_record_{rank:02d}_{bpb:.5f}_{name}.md

containing the full submission.json, README.md, and train_gpt.py so agents
can read and learn from the actual winning code.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen, Request

GITHUB_API_BASE = "https://api.github.com/repos/openai/parameter-golf"
RAW_BASE = "https://raw.githubusercontent.com/openai/parameter-golf/main"
RECORDS_PATH = "records/track_10min_16mb"
DEFAULT_TOP_N = 5


def safe_url(url: str) -> str:
    """Percent-encode only the path component, preserving the scheme and host."""
    # Split off scheme+host from path
    if "://" in url:
        scheme_host, _, path = url.partition("://")
        host, _, rest = path.partition("/")
        return f"{scheme_host}://{host}/{quote(rest, safe='/?=&:@')}"
    return quote(url, safe='/:?=&@')


def fetch_url(url: str, timeout: int = 20) -> str | None:
    try:
        req = Request(safe_url(url), headers={"User-Agent": "parameter-golf-research-loop/1.0"})
        with urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except (URLError, TimeoutError, OSError) as exc:
        print(f"  [fetch] Warning: could not fetch {url}: {exc}")
        return None


def fetch_json(url: str, timeout: int = 20) -> list | dict | None:
    text = fetch_url(url, timeout)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"  [fetch] Warning: JSON parse error for {url}: {exc}")
        return None


def list_remote_submissions(timeout: int = 20) -> list[str]:
    """Return directory names in records/track_10min_16mb via GitHub API."""
    url = f"{GITHUB_API_BASE}/contents/{RECORDS_PATH}"
    data = fetch_json(url, timeout)
    if not isinstance(data, list):
        return []
    return [item["name"] for item in data if item.get("type") == "dir"]


def list_local_submissions(repo_root: Path) -> list[str]:
    records_dir = repo_root / RECORDS_PATH
    if not records_dir.is_dir():
        return []
    return [p.name for p in records_dir.iterdir() if p.is_dir()]


def fetch_remote_submission(name: str, timeout: int = 20) -> dict[str, str]:
    """Fetch submission.json, README.md, train_gpt.py for one submission from GitHub."""
    files = {}
    for filename in ("submission.json", "README.md", "train_gpt.py"):
        url = f"{RAW_BASE}/{RECORDS_PATH}/{name}/{filename}"
        content = fetch_url(url, timeout)
        if content is not None:
            files[filename] = content
        time.sleep(0.1)  # be polite to GitHub
    return files


def read_local_submission(name: str, repo_root: Path) -> dict[str, str]:
    base = repo_root / RECORDS_PATH / name
    files = {}
    for filename in ("submission.json", "README.md", "train_gpt.py"):
        path = base / filename
        if path.exists():
            files[filename] = path.read_text(encoding="utf-8", errors="replace")
    return files


def parse_bpb(files: dict[str, str]) -> float:
    """Extract val_bpb from submission.json, fallback to large value."""
    raw = files.get("submission.json", "")
    if not raw:
        return 9999.0
    try:
        data = json.loads(raw)
        return float(data.get("val_bpb", 9999.0))
    except (json.JSONDecodeError, TypeError, ValueError):
        return 9999.0


def parse_meta(files: dict[str, str]) -> dict:
    raw = files.get("submission.json", "")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}


def sanitize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", name)[:80]


def build_markdown(name: str, files: dict[str, str], rank: int) -> str:
    meta = parse_meta(files)
    bpb = meta.get("val_bpb", "?")
    author = meta.get("author", "?")
    date = meta.get("date", "?")
    blurb = meta.get("blurb", "")
    bytes_total = meta.get("bytes_total", "?")
    pre_bpb = meta.get("pre_quant_val_bpb", "?")

    parts = [
        f"# SOTA Record #{rank}: {name}",
        "",
        f"- **Rank**: #{rank} (by val_bpb, lower is better)",
        f"- **val_bpb (post-export)**: `{bpb}`",
        f"- **val_bpb (pre-quant)**: `{pre_bpb}`",
        f"- **Artifact bytes**: `{bytes_total}` / 16,000,000",
        f"- **Author**: {author}",
        f"- **Date**: {date}",
        "",
    ]

    if blurb:
        parts += ["## Technique summary", "", blurb, ""]

    if "submission.json" in files:
        parts += ["## submission.json", "", "```json", files["submission.json"].strip(), "```", ""]

    if "README.md" in files:
        readme = files["README.md"].strip()
        if readme:
            parts += ["## README.md", "", readme, ""]

    if "train_gpt.py" in files:
        parts += [
            "## train_gpt.py",
            "",
            "This is the complete training script for this submission. Study it carefully to understand the exact implementation of the techniques described above.",
            "",
            "```python",
            files["train_gpt.py"].strip(),
            "```",
            "",
        ]

    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch top SOTA training scripts from openai/parameter-golf."
    )
    parser.add_argument("--repo-root", required=True, help="Local parameter-golf repo root.")
    parser.add_argument("--output-dir", required=True, help="Directory to write markdown files.")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N, help="Number of top records to fetch.")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Discover submissions: merge remote and local lists
    print("[fetch_sota_records] Listing remote submissions from GitHub API...")
    remote_names = list_remote_submissions(args.timeout)
    local_names = list_local_submissions(repo_root)
    all_names = list(dict.fromkeys(remote_names + local_names))  # remote-first, deduped
    print(f"[fetch_sota_records] Found {len(remote_names)} remote, {len(local_names)} local → {len(all_names)} total.")

    if not all_names:
        print("[fetch_sota_records] No submissions found. Exiting.")
        return 1

    # Fetch content for each (try remote first, fall back to local)
    print(f"[fetch_sota_records] Fetching content for {len(all_names)} submissions...")
    all_submissions: list[tuple[str, dict[str, str]]] = []
    for name in all_names:
        print(f"  Fetching {name}...")
        files = fetch_remote_submission(name, args.timeout)
        if not files.get("train_gpt.py"):
            # Fall back to local
            local_files = read_local_submission(name, repo_root)
            for key, val in local_files.items():
                if key not in files:
                    files[key] = val
        if files.get("train_gpt.py") or files.get("submission.json"):
            all_submissions.append((name, files))

    # Sort by val_bpb ascending (best first)
    all_submissions.sort(key=lambda x: parse_bpb(x[1]))

    # Clear old files in output dir
    for old in output_dir.glob("sota_record_*.md"):
        old.unlink()

    # Write top N
    top_n = min(args.top_n, len(all_submissions))
    written: list[Path] = []
    for rank, (name, files) in enumerate(all_submissions[:top_n], start=1):
        bpb = parse_bpb(files)
        safe_name = sanitize_name(name)
        out_name = f"sota_record_{rank:02d}_{bpb:.5f}_{safe_name}.md"
        out_path = output_dir / out_name
        out_path.write_text(build_markdown(name, files, rank), encoding="utf-8")
        print(f"  [{rank}/{top_n}] {out_name}  (bpb={bpb})")
        written.append(out_path)

    # Write an index file
    index_lines = [
        "# SOTA Records Index",
        "",
        f"Top {top_n} submissions from `openai/parameter-golf` sorted by post-export val_bpb (lower is better).",
        "",
    ]
    for rank, (name, files) in enumerate(all_submissions[:top_n], start=1):
        meta = parse_meta(files)
        bpb = meta.get("val_bpb", "?")
        author = meta.get("author", "?")
        blurb = meta.get("blurb", "")[:120]
        index_lines.append(f"{rank}. **{name}** | bpb=`{bpb}` | {author}")
        if blurb:
            index_lines.append(f"   > {blurb}...")
        index_lines.append("")

    index_path = output_dir / "sota_records_index.md"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"[fetch_sota_records] Wrote index: {index_path}")
    print(f"[fetch_sota_records] Done. {top_n} records saved to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
