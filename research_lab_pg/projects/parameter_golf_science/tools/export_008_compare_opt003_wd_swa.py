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


def build_policy_overrides(policy_name: str, checkpoint_state: dict[str, torch.Tensor]) -> dict[str, int]:
    if policy_name == "uniform_int8":
        return {}
    if policy_name == "mlp_int6_else_int8":
        overrides: dict[str, int] = {}
        for name in checkpoint_state:
            if name.endswith("mlp.fc.weight") or name.endswith("mlp.proj.weight"):
                overrides[name] = 6
        return overrides
    if policy_name == "mlp_int6_plus_attn_proj_int6_else_int8":
        overrides = build_policy_overrides("mlp_int6_else_int8", checkpoint_state)
        for name in checkpoint_state:
            if name.endswith("attn.proj.weight"):
                overrides[name] = 6
        return overrides
    raise ValueError(f"Unsupported export policy: {policy_name}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Controlled opt_003 export comparison with uniform int8, MLP-only int6, and MLP+attn.proj int6."
    )
    parser.add_argument("--train-script", required=True, help="Path to the root train_gpt.py script.")
    parser.add_argument("--checkpoint", required=True, help="Path to the candidate checkpoint (.pt).")
    parser.add_argument("--output-dir", required=True, help="Directory to write experiment artifacts and JSON summary.")
    parser.add_argument("--baseline-summary", required=True, help="Path to arch_003 summary.json for baseline comparison.")
    parser.add_argument("--tokenizer-path", default="", help="SentencePiece model path.")
    parser.add_argument("--val-files", default="", help="Validation shard glob.")
    parser.add_argument("--eval-mode", default="sliding_window", choices=["non_overlapping", "sliding_window", "both"])
    parser.add_argument("--eval-stride", type=int, default=64)
    parser.add_argument("--zstd-level", type=int, default=22)
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
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    device = torch.device("cuda", local_rank)
    torch.cuda.set_device(device)
    distributed, rank, world_size, local_rank = maybe_init_distributed(device)
    grad_accum_steps = 8 // world_size

    root = load_module(train_script_path)
    args = build_eval_args(root, cli)
    code_bytes = len(train_script_path.read_bytes())
    baseline_summary = json.loads(baseline_summary_path.read_text(encoding="utf-8"))

    log0("experiment_id:opt_003_arch_003_muon_wd004_plus_late_swa", rank)
    log0(f"checkpoint:{checkpoint_path}", rank)
    log0(f"baseline_summary:{baseline_summary_path}", rank)
    log0(f"eval_config:mode={args.eval_mode} stride={args.eval_stride}", rank)
    log0(f"compression_config:zstd-{cli.zstd_level}", rank)
    log0(
        f"feature_config:bigram_hash_buckets={args.bigram_hash_buckets} "
        f"bigram_hash_dim={args.bigram_hash_dim} use_smeargate={args.use_smeargate}",
        rank,
    )
    log0("precision_config:uniform_int8 vs mlp_int6_else_int8 vs mlp_int6_plus_attn_proj_int6_else_int8", rank)
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

    policies = [
        ("uniform_int8", 8),
        ("mlp_int6_else_int8", 8),
        ("mlp_int6_plus_attn_proj_int6_else_int8", 8),
    ]
    results: dict[str, Any] = {
        "experiment_id": "opt_003_arch_003_muon_wd004_plus_late_swa",
        "checkpoint": str(checkpoint_path),
        "train_script": str(train_script_path),
        "baseline_summary": str(baseline_summary_path),
        "code_bytes": code_bytes,
        "eval_mode": args.eval_mode,
        "eval_stride": args.eval_stride,
        "compression_label": f"zstd-{cli.zstd_level}",
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
        "artifacts": {},
    }

    for policy_name, default_bits in policies:
        bit_overrides = build_policy_overrides(policy_name, checkpoint_state)
        quant_obj, quant_stats = root.quantize_state_dict_mixed_precision(
            checkpoint_state,
            default_num_bits=default_bits,
            bit_overrides=bit_overrides,
        )
        quant_buf = io.BytesIO()
        torch.save(quant_obj, quant_buf)
        quant_raw = quant_buf.getvalue()
        quant_raw_bytes = len(quant_raw)

        export_start = time.perf_counter()
        blob, compression_label = root.compress_export_bytes(quant_raw, backend="zstd", level=cli.zstd_level)
        export_time_ms = 1000.0 * (time.perf_counter() - export_start)

        artifact_path = output_dir / f"final_model.{policy_name}.zstd.ptz"
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
        result = {
            "policy_name": policy_name,
            "default_num_bits": default_bits,
            "overrides": bit_overrides,
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
        }
        results["artifacts"][policy_name] = result
        log0(
            f"artifact:{policy_name} bytes:{artifact_bytes} total:{total_submission_bytes} "
            f"val_bpb:{val_bpb:.8f} quant_gap:{quantization_gap_bpb:+.8f} "
            f"roundtrip_exact:{roundtrip_exact}",
            rank,
        )

    if rank == 0:
        uniform = results["artifacts"]["uniform_int8"]
        mlp = results["artifacts"]["mlp_int6_else_int8"]
        candidate = results["artifacts"]["mlp_int6_plus_attn_proj_int6_else_int8"]
        baseline_uniform = baseline_summary["artifacts"]["uniform_int8"]
        baseline_mlp = baseline_summary["artifacts"]["mlp_int6_else_int8"]
        baseline_candidate = baseline_summary["artifacts"]["mlp_int6_plus_attn_proj_int6_else_int8"]
        results["comparison"] = {
            "vs_current_baseline_uniform_int8": {
                "artifact_bytes_delta": uniform["artifact_bytes"] - baseline_uniform["artifact_bytes"],
                "total_submission_bytes_delta": uniform["total_submission_bytes"] - baseline_uniform["total_submission_bytes"],
                "val_bpb_delta": uniform["val_bpb"] - baseline_uniform["val_bpb"],
                "quantization_gap_bpb_delta": uniform["quantization_gap_bpb"] - baseline_uniform["quantization_gap_bpb"],
            },
            "vs_current_baseline_mlp_int6": {
                "artifact_bytes_delta": mlp["artifact_bytes"] - baseline_mlp["artifact_bytes"],
                "total_submission_bytes_delta": mlp["total_submission_bytes"] - baseline_mlp["total_submission_bytes"],
                "val_bpb_delta": mlp["val_bpb"] - baseline_mlp["val_bpb"],
                "quantization_gap_bpb_delta": mlp["quantization_gap_bpb"] - baseline_mlp["quantization_gap_bpb"],
            },
            "vs_current_baseline_locked_best": {
                "artifact_bytes_delta": candidate["artifact_bytes"] - baseline_candidate["artifact_bytes"],
                "total_submission_bytes_delta": candidate["total_submission_bytes"] - baseline_candidate["total_submission_bytes"],
                "val_bpb_delta": candidate["val_bpb"] - baseline_candidate["val_bpb"],
                "quantization_gap_bpb_delta": candidate["quantization_gap_bpb"] - baseline_candidate["quantization_gap_bpb"],
            },
            "candidate_vs_uniform_int8_this_checkpoint": {
                "artifact_bytes_delta": candidate["artifact_bytes"] - uniform["artifact_bytes"],
                "total_submission_bytes_delta": candidate["total_submission_bytes"] - uniform["total_submission_bytes"],
                "val_bpb_delta": candidate["val_bpb"] - uniform["val_bpb"],
                "quantization_gap_bpb_delta": candidate["quantization_gap_bpb"] - uniform["quantization_gap_bpb"],
            },
            "candidate_vs_mlp_int6_this_checkpoint": {
                "artifact_bytes_delta": candidate["artifact_bytes"] - mlp["artifact_bytes"],
                "total_submission_bytes_delta": candidate["total_submission_bytes"] - mlp["total_submission_bytes"],
                "val_bpb_delta": candidate["val_bpb"] - mlp["val_bpb"],
                "quantization_gap_bpb_delta": candidate["quantization_gap_bpb"] - mlp["quantization_gap_bpb"],
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
