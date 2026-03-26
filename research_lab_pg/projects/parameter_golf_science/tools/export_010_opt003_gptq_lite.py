#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import time
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

import sentencepiece as spm
import torch
import torch.distributed as dist
from torch import nn
from torch.nn.parallel import DistributedDataParallel as DDP


def load_module(module_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("root_train_gpt", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def maybe_init_distributed(device: torch.device) -> tuple[bool, int, int, int]:
    distributed = "RANK" in os.environ and "WORLD_SIZE" in os.environ
    rank = int(os.environ.get("RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    if distributed:
        dist.init_process_group(backend="nccl", device_id=device)
        dist.barrier()
    return distributed, rank, world_size, local_rank


def log0(message: str, rank: int) -> None:
    if rank == 0:
        print(message, flush=True)


def build_eval_args(root: ModuleType, cli: argparse.Namespace) -> Any:
    defaults = root.Hyperparameters
    return SimpleNamespace(
        val_batch_size=cli.val_batch_size if cli.val_batch_size is not None else defaults.val_batch_size,
        eval_mode=cli.eval_mode,
        eval_stride=cli.eval_stride,
        train_seq_len=cli.train_seq_len if cli.train_seq_len is not None else defaults.train_seq_len,
        val_files=cli.val_files if cli.val_files else defaults.val_files,
        tokenizer_path=cli.tokenizer_path if cli.tokenizer_path else defaults.tokenizer_path,
        vocab_size=cli.vocab_size if cli.vocab_size is not None else defaults.vocab_size,
        num_layers=cli.num_layers if cli.num_layers is not None else defaults.num_layers,
        model_dim=cli.model_dim if cli.model_dim is not None else defaults.model_dim,
        num_heads=cli.num_heads if cli.num_heads is not None else defaults.num_heads,
        num_kv_heads=cli.num_kv_heads if cli.num_kv_heads is not None else defaults.num_kv_heads,
        mlp_mult=cli.mlp_mult if cli.mlp_mult is not None else defaults.mlp_mult,
        tie_embeddings=bool(cli.tie_embeddings) if cli.tie_embeddings is not None else defaults.tie_embeddings,
        tied_embed_init_std=cli.tied_embed_init_std if cli.tied_embed_init_std is not None else defaults.tied_embed_init_std,
        logit_softcap=cli.logit_softcap if cli.logit_softcap is not None else defaults.logit_softcap,
        rope_base=cli.rope_base if cli.rope_base is not None else defaults.rope_base,
        qk_gain_init=cli.qk_gain_init if cli.qk_gain_init is not None else defaults.qk_gain_init,
        bigram_hash_buckets=cli.bigram_hash_buckets if cli.bigram_hash_buckets is not None else defaults.bigram_hash_buckets,
        bigram_hash_dim=cli.bigram_hash_dim if cli.bigram_hash_dim is not None else defaults.bigram_hash_dim,
        use_smeargate=bool(cli.use_smeargate) if cli.use_smeargate is not None else defaults.use_smeargate,
    )


def build_model(root: ModuleType, args: Any, device: torch.device, distributed: bool, local_rank: int) -> tuple[nn.Module, nn.Module]:
    base_model = root.GPT(
        vocab_size=args.vocab_size,
        num_layers=args.num_layers,
        model_dim=args.model_dim,
        num_heads=args.num_heads,
        num_kv_heads=args.num_kv_heads,
        mlp_mult=args.mlp_mult,
        tie_embeddings=args.tie_embeddings,
        tied_embed_init_std=args.tied_embed_init_std,
        logit_softcap=args.logit_softcap,
        rope_base=args.rope_base,
        qk_gain_init=args.qk_gain_init,
        bigram_hash_buckets=args.bigram_hash_buckets,
        bigram_hash_dim=args.bigram_hash_dim,
        use_smeargate=args.use_smeargate,
    ).to(device).bfloat16()
    for module in base_model.modules():
        if isinstance(module, root.CastedLinear):
            module.float()
    root.restore_low_dim_params_to_fp32(base_model)
    model: nn.Module = DDP(base_model, device_ids=[local_rank], broadcast_buffers=False) if distributed else base_model
    return base_model, model


def compare_objects(expected: Any, actual: Any, prefix: str = "") -> list[str]:
    mismatches: list[str] = []
    if isinstance(expected, torch.Tensor):
        if not isinstance(actual, torch.Tensor):
            return [f"{prefix}: expected tensor, got {type(actual).__name__}"]
        if expected.dtype != actual.dtype:
            mismatches.append(f"{prefix}: dtype {expected.dtype} != {actual.dtype}")
        if tuple(expected.shape) != tuple(actual.shape):
            mismatches.append(f"{prefix}: shape {tuple(expected.shape)} != {tuple(actual.shape)}")
        if not torch.equal(expected.cpu(), actual.cpu()):
            mismatches.append(f"{prefix}: tensor values differ")
        return mismatches
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return [f"{prefix}: expected dict, got {type(actual).__name__}"]
        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())
        if expected_keys != actual_keys:
            mismatches.append(f"{prefix}: keys {sorted(expected_keys)} != {sorted(actual_keys)}")
        for key in sorted(expected_keys & actual_keys):
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            mismatches.extend(compare_objects(expected[key], actual[key], child_prefix))
        return mismatches
    if expected != actual:
        return [f"{prefix}: value {expected!r} != {actual!r}"]
    return mismatches


def evaluate_loaded_state(
    root: ModuleType,
    args: Any,
    base_model: nn.Module,
    model: nn.Module,
    checkpoint_state: dict[str, torch.Tensor],
    loaded_state: dict[str, torch.Tensor],
    rank: int,
    world_size: int,
    device: torch.device,
    grad_accum_steps: int,
    val_tokens: torch.Tensor,
    base_bytes_lut: torch.Tensor,
    has_leading_space_lut: torch.Tensor,
    is_boundary_token_lut: torch.Tensor,
) -> tuple[float, float, float]:
    base_model.load_state_dict(checkpoint_state, strict=True)
    base_model.load_state_dict(loaded_state, strict=True)
    eval_result = root.evaluate_modes(
        args,
        model,
        rank,
        world_size,
        device,
        grad_accum_steps,
        val_tokens,
        base_bytes_lut,
        has_leading_space_lut,
        is_boundary_token_lut,
    )
    return eval_result[args.eval_mode]


def parse_clip_percentiles(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("At least one clip percentile is required")
    for value in values:
        if value <= 0.0 or value > 1.0:
            raise ValueError(f"Clip percentile must be in (0, 1], got {value}")
    return values


def quantize_float_tensor_gptq_lite(
    root: ModuleType,
    tensor: torch.Tensor,
    clip_percentiles: list[float],
) -> tuple[torch.Tensor, torch.Tensor, dict[str, Any]]:
    qmin, qmax = root._signed_quant_bounds(8)
    denom = float(qmax)
    t32 = tensor.float()
    if t32.ndim != 2:
        q, s = root.quantize_float_tensor(tensor, num_bits=8)
        return q, s, {
            "search_applied": False,
            "selected_clip_percentile": float(root.INT8_CLIP_Q),
            "search_metric": "baseline_uniform_int8",
        }

    best_q: torch.Tensor | None = None
    best_s: torch.Tensor | None = None
    best_pct: float | None = None
    best_err = float("inf")
    for pct in clip_percentiles:
        if pct < 1.0:
            row_clip = torch.quantile(t32.abs(), pct, dim=1)
        else:
            row_clip = t32.abs().amax(dim=1)
        scale = (row_clip / denom).clamp_min(1.0 / denom).to(dtype=root.INT8_PER_ROW_SCALE_DTYPE).contiguous()
        q = torch.clamp(torch.round(t32 / scale.float()[:, None]), qmin, qmax).to(torch.int8).contiguous()
        recon = q.float() * scale.float()[:, None]
        err = float((t32 - recon).pow(2).mean().item())
        if err < best_err:
            best_q = q
            best_s = scale
            best_pct = pct
            best_err = err
    if best_q is None or best_s is None or best_pct is None:
        raise RuntimeError("GPTQ-lite clip search failed to produce a quantized tensor")
    return best_q, best_s, {
        "search_applied": True,
        "selected_clip_percentile": best_pct,
        "search_metric": "weight_reconstruction_mse",
        "selected_reconstruction_mse": best_err,
    }


def quantize_state_dict_uniform_int8_gptq_lite(
    root: ModuleType,
    state_dict: dict[str, torch.Tensor],
    clip_percentiles: list[float],
) -> tuple[dict[str, object], dict[str, Any], dict[str, Any]]:
    quantized: dict[str, torch.Tensor] = {}
    scales: dict[str, torch.Tensor] = {}
    dtypes: dict[str, str] = {}
    passthrough: dict[str, torch.Tensor] = {}
    passthrough_orig_dtypes: dict[str, str] = {}
    qmeta: dict[str, dict[str, object]] = {}
    stats = dict.fromkeys(
        ("param_count", "num_tensors", "num_float_tensors", "num_nonfloat_tensors", "baseline_tensor_bytes", "quant_payload_bytes"),
        0,
    )
    search_summary: dict[str, Any] = {
        "clip_percentiles_considered": clip_percentiles,
        "search_scope": "2d_float_tensors_only",
        "search_metric": "weight_reconstruction_mse",
        "activation_calibration": "none",
        "searched_tensor_count": 0,
        "selected_percentile_counts": {f"{pct:.8f}": 0 for pct in clip_percentiles},
        "per_tensor_selected_percentile": {},
    }

    for name, tensor in state_dict.items():
        t = tensor.detach().to("cpu").contiguous()
        stats["param_count"] += int(t.numel())
        stats["num_tensors"] += 1
        stats["baseline_tensor_bytes"] += root.tensor_nbytes(t)

        if not t.is_floating_point():
            stats["num_nonfloat_tensors"] += 1
            passthrough[name] = t
            stats["quant_payload_bytes"] += root.tensor_nbytes(t)
            continue

        if t.numel() <= root.INT8_KEEP_FLOAT_MAX_NUMEL:
            kept = root.keep_float_tensor(name, t, passthrough_orig_dtypes)
            passthrough[name] = kept
            stats["quant_payload_bytes"] += root.tensor_nbytes(kept)
            continue

        stats["num_float_tensors"] += 1
        q, s, search_meta = quantize_float_tensor_gptq_lite(root, t, clip_percentiles)
        if search_meta["search_applied"]:
            selected_pct = float(search_meta["selected_clip_percentile"])
            selected_key = f"{selected_pct:.8f}"
            search_summary["searched_tensor_count"] += 1
            search_summary["selected_percentile_counts"][selected_key] += 1
            search_summary["per_tensor_selected_percentile"][name] = selected_pct
        q_packed = root._pack_signed_tensor(q, num_bits=8)
        meta: dict[str, object] = {"bits": 8, **search_meta}
        if s.ndim > 0:
            meta["scheme"] = "per_row"
            meta["axis"] = 0
        qmeta[name] = meta
        quantized[name] = q_packed
        scales[name] = s
        dtypes[name] = str(t.dtype).removeprefix("torch.")
        stats["quant_payload_bytes"] += root.tensor_nbytes(q_packed) + root.tensor_nbytes(s)

    obj: dict[str, object] = {
        "__quant_format__": "uniform_int8_gptq_lite_per_row_v1",
        "quantized": quantized,
        "scales": scales,
        "dtypes": dtypes,
        "passthrough": passthrough,
        "qmeta": qmeta,
        "gptq_lite_config": {
            "clip_percentiles": clip_percentiles,
            "search_scope": "2d_float_tensors_only",
            "search_metric": "weight_reconstruction_mse",
            "activation_calibration": "none",
        },
    }
    if passthrough_orig_dtypes:
        obj["passthrough_orig_dtypes"] = passthrough_orig_dtypes
    stats["int8_payload_bytes"] = stats["quant_payload_bytes"]
    return obj, stats, search_summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Controlled opt_003 GPTQ-lite clip-search export comparison against the locked uniform-int8 baseline."
    )
    parser.add_argument("--train-script", required=True, help="Path to the root train_gpt.py script.")
    parser.add_argument("--checkpoint", required=True, help="Path to the fixed checkpoint (.pt).")
    parser.add_argument("--output-dir", required=True, help="Directory to write experiment artifacts and JSON summary.")
    parser.add_argument("--baseline-summary", required=True, help="Path to the locked opt_003 summary.json baseline.")
    parser.add_argument("--tokenizer-path", default="", help="SentencePiece model path.")
    parser.add_argument("--val-files", default="", help="Validation shard glob.")
    parser.add_argument("--eval-mode", default="sliding_window", choices=["non_overlapping", "sliding_window", "both"])
    parser.add_argument("--eval-stride", type=int, default=64)
    parser.add_argument("--zstd-level", type=int, default=22)
    parser.add_argument(
        "--clip-percentiles",
        default="0.999,0.9995,0.9999,0.99999,1.0",
        help="Comma-separated GPTQ-lite clip percentiles to search for large 2D float tensors.",
    )
    parser.add_argument("--val-batch-size", type=int, default=None)
    parser.add_argument("--train-seq-len", type=int, default=None)
    parser.add_argument("--vocab-size", type=int, default=None)
    parser.add_argument("--num-layers", type=int, default=None)
    parser.add_argument("--model-dim", type=int, default=None)
    parser.add_argument("--num-heads", type=int, default=None)
    parser.add_argument("--num-kv-heads", type=int, default=None)
    parser.add_argument("--mlp-mult", type=int, default=None)
    parser.add_argument("--tie-embeddings", type=int, choices=[0, 1], default=None)
    parser.add_argument("--tied-embed-init-std", type=float, default=None)
    parser.add_argument("--logit-softcap", type=float, default=None)
    parser.add_argument("--rope-base", type=float, default=None)
    parser.add_argument("--qk-gain-init", type=float, default=None)
    parser.add_argument("--bigram-hash-buckets", type=int, default=None)
    parser.add_argument("--bigram-hash-dim", type=int, default=None)
    parser.add_argument("--use-smeargate", type=int, choices=[0, 1], default=None)
    cli = parser.parse_args()

    train_script_path = Path(cli.train_script).resolve()
    checkpoint_path = Path(cli.checkpoint).resolve()
    output_dir = Path(cli.output_dir).resolve()
    baseline_summary_path = Path(cli.baseline_summary).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this comparison runner")
    clip_percentiles = parse_clip_percentiles(cli.clip_percentiles)
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    device = torch.device("cuda", local_rank)
    torch.cuda.set_device(device)
    distributed, rank, world_size, local_rank = maybe_init_distributed(device)
    grad_accum_steps = 8 // world_size

    root = load_module(train_script_path)
    args = build_eval_args(root, cli)
    code_bytes = len(train_script_path.read_bytes())
    baseline_summary = json.loads(baseline_summary_path.read_text(encoding="utf-8"))

    log0("experiment_id:export_010_opt003_gptq_lite_clip_search_on_uniform_int8", rank)
    log0(f"checkpoint:{checkpoint_path}", rank)
    log0(f"baseline_summary:{baseline_summary_path}", rank)
    log0(f"eval_config:mode={args.eval_mode} stride={args.eval_stride}", rank)
    log0(f"compression_config:zstd-{cli.zstd_level}", rank)
    log0(
        f"feature_config:bigram_hash_buckets={args.bigram_hash_buckets} "
        f"bigram_hash_dim={args.bigram_hash_dim} use_smeargate={args.use_smeargate}",
        rank,
    )
    log0(
        "gptq_lite_config:"
        f"clip_percentiles={','.join(f'{pct:.8f}' for pct in clip_percentiles)} "
        "scope=2d_float_tensors_only metric=weight_reconstruction_mse activation_calibration=none",
        rank,
    )
    log0(f"world_size:{world_size} grad_accum_steps:{grad_accum_steps}", rank)

    sp = spm.SentencePieceProcessor(model_file=args.tokenizer_path)
    if int(sp.vocab_size()) != args.vocab_size:
        raise ValueError(f"Vocab mismatch: args.vocab_size={args.vocab_size} tokenizer={int(sp.vocab_size())}")
    val_tokens = root.load_validation_tokens(args.val_files, args.train_seq_len)
    base_bytes_lut, has_leading_space_lut, is_boundary_token_lut = root.build_sentencepiece_luts(sp, args.vocab_size, device)

    checkpoint_state = torch.load(checkpoint_path, map_location="cpu")
    base_model, model = build_model(root, args, device, distributed, local_rank)
    base_model.load_state_dict(checkpoint_state, strict=True)

    checkpoint_eval = root.evaluate_modes(
        args,
        model,
        rank,
        world_size,
        device,
        grad_accum_steps,
        val_tokens,
        base_bytes_lut,
        has_leading_space_lut,
        is_boundary_token_lut,
    )
    if args.eval_mode == "both":
        raise ValueError("This controlled export comparison should use one fixed evaluation mode")
    checkpoint_val_loss, checkpoint_val_bpb, checkpoint_eval_time_ms = checkpoint_eval[args.eval_mode]
    log0(
        f"checkpoint_eval mode:{args.eval_mode} stride:{args.eval_stride} "
        f"val_loss:{checkpoint_val_loss:.8f} val_bpb:{checkpoint_val_bpb:.8f} eval_time:{checkpoint_eval_time_ms:.0f}ms",
        rank,
    )

    quant_obj, quant_stats, search_summary = quantize_state_dict_uniform_int8_gptq_lite(
        root,
        checkpoint_state,
        clip_percentiles,
    )
    quant_buf = io.BytesIO()
    torch.save(quant_obj, quant_buf)
    quant_raw = quant_buf.getvalue()
    quant_raw_bytes = len(quant_raw)

    export_start = time.perf_counter()
    blob, compression_label = root.compress_export_bytes(quant_raw, backend="zstd", level=cli.zstd_level)
    export_time_ms = 1000.0 * (time.perf_counter() - export_start)

    artifact_path = output_dir / "final_model.uniform_int8_gptq_lite.zstd.ptz"
    if rank == 0:
        artifact_path.write_bytes(blob)
    if distributed:
        dist.barrier()

    load_start = time.perf_counter()
    blob_disk = artifact_path.read_bytes()
    decompressed = root.decompress_export_bytes(blob_disk, backend="zstd")
    quant_state = torch.load(io.BytesIO(decompressed), map_location="cpu")
    dequantized_state = root.dequantize_state_dict_uniform(quant_state)
    load_time_ms = 1000.0 * (time.perf_counter() - load_start)

    raw_bytes_equal = decompressed == quant_raw
    tensor_mismatches = compare_objects(quant_obj, quant_state)
    roundtrip_exact = raw_bytes_equal and not tensor_mismatches
    dequantized_reference = root.dequantize_state_dict_uniform(quant_obj)
    dequantized_mismatches = compare_objects(dequantized_reference, dequantized_state)

    val_loss, val_bpb, eval_time_ms = evaluate_loaded_state(
        root,
        args,
        base_model,
        model,
        checkpoint_state,
        dequantized_state,
        rank,
        world_size,
        device,
        grad_accum_steps,
        val_tokens,
        base_bytes_lut,
        has_leading_space_lut,
        is_boundary_token_lut,
    )

    artifact_bytes = len(blob)
    total_submission_bytes = artifact_bytes + code_bytes
    quantization_gap_bpb = val_bpb - checkpoint_val_bpb
    baseline_uniform = baseline_summary["artifacts"]["uniform_int8"]
    candidate_result = {
        "policy_name": "uniform_int8_gptq_lite",
        "default_num_bits": 8,
        "compression_label": compression_label,
        "artifact_path": str(artifact_path),
        "artifact_bytes": artifact_bytes,
        "total_submission_bytes": total_submission_bytes,
        "export_time_ms": export_time_ms,
        "load_time_ms": load_time_ms,
        "raw_torch_bytes": quant_raw_bytes,
        "payload_bytes": quant_stats["quant_payload_bytes"],
        "baseline_tensor_bytes": quant_stats["baseline_tensor_bytes"],
        "roundtrip_raw_bytes_equal": raw_bytes_equal,
        "roundtrip_quantized_tensor_equal": not tensor_mismatches,
        "roundtrip_exact": roundtrip_exact,
        "tensor_mismatches": tensor_mismatches,
        "roundtrip_dequantized_state_equal": not dequantized_mismatches,
        "dequantized_state_mismatches": dequantized_mismatches,
        "val_loss": val_loss,
        "val_bpb": val_bpb,
        "eval_time_ms": eval_time_ms,
        "quantization_gap_bpb": quantization_gap_bpb,
        "gptq_lite_search": search_summary,
    }
    log0(
        f"artifact:uniform_int8_gptq_lite bytes:{artifact_bytes} total:{total_submission_bytes} "
        f"val_bpb:{val_bpb:.8f} quant_gap:{quantization_gap_bpb:+.8f} "
        f"roundtrip_exact:{roundtrip_exact}",
        rank,
    )

    results: dict[str, Any] = {
        "experiment_id": "export_010_opt003_gptq_lite_clip_search_on_uniform_int8",
        "checkpoint": str(checkpoint_path),
        "train_script": str(train_script_path),
        "baseline_summary": str(baseline_summary_path),
        "code_bytes": code_bytes,
        "eval_mode": args.eval_mode,
        "eval_stride": args.eval_stride,
        "compression_label": f"zstd-{cli.zstd_level}",
        "gptq_lite_config": {
            "clip_percentiles": clip_percentiles,
            "search_scope": "2d_float_tensors_only",
            "search_metric": "weight_reconstruction_mse",
            "activation_calibration": "none",
        },
        "feature_config": {
            "bigram_hash_buckets": args.bigram_hash_buckets,
            "bigram_hash_dim": args.bigram_hash_dim,
            "use_smeargate": args.use_smeargate,
            "smeargate_init_logit": 3.0 if args.use_smeargate else None,
        },
        "checkpoint_eval": {
            "val_loss": checkpoint_val_loss,
            "val_bpb": checkpoint_val_bpb,
            "eval_time_ms": checkpoint_eval_time_ms,
        },
        "artifacts": {
            "uniform_int8_gptq_lite": candidate_result,
        },
    }

    if rank == 0:
        results["comparison"] = {
            "vs_locked_baseline_uniform_int8": {
                "baseline_checkpoint_val_bpb": baseline_summary["checkpoint_eval"]["val_bpb"],
                "baseline_post_export_val_bpb": baseline_uniform["val_bpb"],
                "candidate_post_export_val_bpb": candidate_result["val_bpb"],
                "artifact_bytes_delta": candidate_result["artifact_bytes"] - baseline_uniform["artifact_bytes"],
                "total_submission_bytes_delta": candidate_result["total_submission_bytes"] - baseline_uniform["total_submission_bytes"],
                "val_bpb_delta": candidate_result["val_bpb"] - baseline_uniform["val_bpb"],
                "quantization_gap_bpb_delta": candidate_result["quantization_gap_bpb"] - baseline_uniform["quantization_gap_bpb"],
            },
            "budget": {
                "byte_cap": 16_000_000,
                "candidate_under_cap": candidate_result["total_submission_bytes"] < 16_000_000,
            },
        }
        summary_path = output_dir / "summary.json"
        summary_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        log0(f"summary:{summary_path}", rank)

    if distributed:
        dist.barrier()
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
