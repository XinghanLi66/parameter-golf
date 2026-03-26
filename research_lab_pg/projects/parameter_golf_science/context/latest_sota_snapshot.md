# SOTA Snapshot — 2026-03-26 (MAJOR BREAKTHROUGH DAY)

## Current Leaderboard (merged + open PRs)

### Merged (official)
| Rank | BPB | Name |
|------|-----|------|
| 1 | 1.1194 | LeakyReLU_LegalTTT_ParallelMuon (2026-03-23) |
| 2 | 1.1228 | 11L_EMA_GPTQ-lite_warmdown3500_QAT015 (2026-03-22) |
| 3 | 1.1248 | 11L_XSA4_EMA_PartialRoPE_LateQAT (2026-03-21) |

### Open PRs (submitted 2026-03-26, DRAMATIC improvement via n-gram)
| BPB | PR | Key Technique |
|-----|----|---------------|
| **0.295** | #809 | Chunk N-gram (order 9) + TTT (LoRA) + LeakyReLU(0.9)² + GPTQ5 |
| **0.437** | #796 | 15-gram + Distributed Prefill + Order-Adaptive Gating + EBLS |
| **0.442** | #803 | Complementary Training + Backoff N-gram (orders 2-10) + TTT |
| **0.482** | #814 | X-WING 3D Cubric + Complementary Training |
| **0.547** | #798 | Order-Adaptive Entropy Gating + BackoffNgramMixer |
| **0.636** | #808 | Depth Recurrence + Multi-Order N-gram Backoff (orders 2-7) |
| **0.667** | #813 | BackoffNgramMixer baseline (orders 2-10) |
| **0.888** | #795 | order-adaptive 11-gram |

## What Changed: N-gram Backoff Cache

The entire improvement (1.119 → 0.295) comes from **eval-time n-gram backoff cache**:
1. Build a hash table of n-gram frequencies from already-scored tokens (backward-looking = legal)
2. For each token, look up highest-order match (try 9-gram, fall back to 8-gram, ..., 2-gram)
3. Mix neural probability with n-gram probability using entropy-adaptive alpha
4. High model entropy → trust n-gram more (alpha up to 0.6 × order_mult)
5. Per-order multipliers: suppress bigrams (×0.3), boost 5-9grams (×2.0)

**This is not a training change. It's purely eval-time. Adding it to our existing best
model should immediately go from ~1.119 BPB to ~0.67 BPB.**

## Reference Code
- Best (0.295): `/tmp/sota_pr809_train_gpt.py` and `docs/sota_records/sota_code_pr809_0.295bpb_ChunkNgramTTT.py`
- Complementary (0.442): `/tmp/sota_pr803_train_gpt.py` and `docs/sota_records/sota_code_pr803_0.442bpb_ComplementaryTraining.py`
- Baseline n-gram (0.667): `docs/sota_records/sota_code_pr813_0.667bpb_BackoffNgramMixer.py`
- Full context: `context/reference_materials/URGENT_ngram_backoff_breakthrough.md`

## Our Current Best
- best local result: `eval_006` → **1.11935 BPB** (TTT 4 epochs, LR=0.0025)
- active run: `eval_008` (TTT epochs=4 confirmation, seed 42)
- Gap to merged SOTA: ~0.0
- Gap to PR #809: **0.824 BPB** — implementing n-gram is now the ONLY thing that matters
