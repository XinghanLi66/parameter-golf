#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
import time
from pathlib import Path
from typing import Any


def write_result(path: str, payload: dict[str, Any]) -> None:
    if path:
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a small CUDA smoke test with PyTorch.")
    parser.add_argument("--output", default="", help="Optional JSON output path.")
    parser.add_argument("--matrix-size", type=int, default=1024, help="Square matrix size for matmul.")
    parser.add_argument("--repeat", type=int, default=2, help="How many matmuls to run per visible GPU.")
    parser.add_argument("--tag", default="gpu_smoke", help="Optional tag stored in the output.")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "tag": args.tag,
        "hostname": socket.gethostname(),
        "python_executable": sys.executable,
        "cuda_visible_devices_env": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "proposal_lab_device": os.environ.get("PROPOSAL_LAB_DEVICE", ""),
    }

    try:
        import torch
    except Exception as exc:
        payload["status"] = "error"
        payload["error"] = f"PyTorch import failed: {exc}"
        write_result(args.output, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    payload["torch_version"] = torch.__version__
    payload["cuda_available"] = bool(torch.cuda.is_available())
    payload["visible_device_count"] = int(torch.cuda.device_count())

    if not torch.cuda.is_available() or torch.cuda.device_count() == 0:
        payload["status"] = "error"
        payload["error"] = "torch.cuda is not available in the current execution environment."
        write_result(args.output, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    torch.manual_seed(0)
    device_reports = []
    for device_index in range(torch.cuda.device_count()):
        device = torch.device(f"cuda:{device_index}")
        torch.cuda.set_device(device)
        name = torch.cuda.get_device_name(device_index)
        samples = []
        checksum = None
        for _ in range(max(args.repeat, 1)):
            a = torch.randn(args.matrix_size, args.matrix_size, device=device)
            b = torch.randn(args.matrix_size, args.matrix_size, device=device)
            torch.cuda.synchronize(device)
            start = time.perf_counter()
            c = a @ b
            torch.cuda.synchronize(device)
            duration_ms = (time.perf_counter() - start) * 1000
            checksum = float(c[0, 0].item())
            samples.append(round(duration_ms, 3))
            del a, b, c
        device_reports.append(
            {
                "visible_device_index": device_index,
                "device_name": name,
                "matmul_samples_ms": samples,
                "last_checksum": checksum,
                "memory_allocated_mib": round(torch.cuda.memory_allocated(device) / 1024 / 1024, 3),
                "memory_reserved_mib": round(torch.cuda.memory_reserved(device) / 1024 / 1024, 3),
            }
        )

    payload["status"] = "ok"
    payload["backend"] = "torch"
    payload["matrix_size"] = args.matrix_size
    payload["repeat"] = args.repeat
    payload["devices"] = device_reports
    write_result(args.output, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
