# URGENT: N-gram Backoff Cache — MASSIVE BPB Breakthrough (2026-03-26)

## STATUS: CRITICAL — Implement This NOW

The leaderboard has been transformed TODAY (2026-03-26). **The target SOTA is PR #803 at 0.4416 BPB**
(PR #809 at 0.295 is excluded pending legality review). The entire improvement comes from
eval-time n-gram backoff cache + complementary training.
Our current best is ~1.119 BPB. Implementing n-gram backoff alone will take us to ~0.67 BPB.
With complementary training it goes to ~0.44 BPB (matching PR #803 target).

This is not a small optimization. This is a paradigm shift. DROP everything else and implement this.

---

## Current Leaderboard (2026-03-26, all open PRs, not yet merged)

| BPB   | PR   | Name |
|-------|------|------|
| 0.295 | #809 | ChunkNgram_TTT + LeakyReLU(0.9)² + GPTQ5 |
| 0.437 | #796 | Distributed Prefill + Order-Adaptive 15-Gram + EBLS |
| 0.442 | #803 | Complementary Training + Backoff N-gram Mixer |
| 0.482 | #814 | X-WING 3D Cubric + Complementary Training |
| 0.547 | #798 | Order-Adaptive Entropy Gating + BackoffNgramMixer |
| 0.564 | #800 | X-WING — Shared N-gram Tables + Cubric |
| 0.636 | #808 | Depth Recurrence + Multi-Order N-gram Backoff |
| 0.667 | #813 | BackoffNgramMixer (baseline n-gram) |
| 0.888 | #795 | 11L + order-adaptive 11-gram |

The accepted SOTA in the main branch is still 1.1194, but these PRs have been submitted today.

---

## Technique 1: N-gram Backoff Cache (THE KEY TECHNIQUE)

### What it is
At eval time, maintain a hash-based frequency table of n-gram occurrences. For each scored token,
look up the highest-order n-gram match (orders 2-9) in the already-scored tokens (backward-looking,
legal). Mix neural model probability with n-gram probability.

### Why it works so well
The validation data has strong local repetition patterns. High-order n-grams (7-9) are extremely
precise predictors when they match. The neural model's uncertainty (entropy) guides when to trust
n-gram vs neural.

### Full implementation (from PR #809, 0.295 BPB)

```python
# Hash function for context keys (orders 2-9)
_NGRAM_PRIMES = np.array([36313, 27191, 51647, 81929, 131071, 174763, 233017, 283721, 347237], dtype=np.uint64)

def _batch_hash_ctx(tokens_np, positions, n, bucket_mask):
    h = np.zeros(len(positions), dtype=np.uint64)
    for k in range(n - 1):
        idx = positions - (n - 1 - k)
        h ^= tokens_np[idx].astype(np.uint64) * _NGRAM_PRIMES[k]
    return h & bucket_mask

def _batch_hash_full(tokens_np, positions, targets, n, bucket_mask):
    h = np.zeros(len(positions), dtype=np.uint64)
    for k in range(n - 1):
        idx = positions - (n - 1 - k)
        h ^= tokens_np[idx].astype(np.uint64) * _NGRAM_PRIMES[k]
    h ^= targets.astype(np.uint64) * _NGRAM_PRIMES[min(n - 1, len(_NGRAM_PRIMES) - 1)]
    return h & bucket_mask

class NgramEvalCache:
    def __init__(self, max_order=9, min_order=2, num_buckets=4194304, min_count=2):
        # num_buckets MUST be a power of 2
        self.max_order = max_order
        self.min_order = min_order
        self.num_buckets = num_buckets
        self.bucket_mask = num_buckets - 1
        self.min_count = min_count
        # Two tables per order: context counts and full (context+target) counts
        self.ctx_tables = [np.zeros(num_buckets, dtype=np.int32) for _ in range(max_order + 1)]
        self.full_tables = [np.zeros(num_buckets, dtype=np.int32) for _ in range(max_order + 1)]

    def batch_lookup(self, tokens_np, positions, targets):
        """Backoff lookup: try highest order first, fall back if no match."""
        n_pos = len(positions)
        ngram_p = np.zeros(n_pos, dtype=np.float64)
        matched = np.zeros(n_pos, dtype=bool)
        matched_orders = np.zeros(n_pos, dtype=np.int32)

        for n in range(self.max_order, self.min_order - 1, -1):
            eligible = (~matched) & (positions >= n - 1)
            if not eligible.any():
                continue
            elig_pos = positions[eligible]
            elig_tgt = targets[eligible]
            ctx_keys = _batch_hash_ctx(tokens_np, elig_pos, n, self.bucket_mask).astype(np.int64)
            ctx_counts = self.ctx_tables[n][ctx_keys]
            has_data = ctx_counts >= self.min_count
            if not has_data.any():
                continue
            full_keys = _batch_hash_full(tokens_np, elig_pos[has_data], elig_tgt[has_data], n, self.bucket_mask).astype(np.int64)
            full_counts = self.full_tables[n][full_keys]
            capped_full = np.minimum(full_counts, ctx_counts[has_data])
            probs = capped_full.astype(np.float64) / np.maximum(ctx_counts[has_data].astype(np.float64), 1.0)
            elig_indices = np.where(eligible)[0]
            data_indices = elig_indices[has_data]
            ngram_p[data_indices] = probs
            matched[data_indices] = True
            matched_orders[data_indices] = n

        return ngram_p, matched, matched_orders

    def update_batch(self, tokens_np, start_pos, end_pos):
        """Update cache with tokens[start_pos:end_pos]. Called AFTER scoring (score-first)."""
        if end_pos <= start_pos:
            return
        positions = np.arange(start_pos, end_pos, dtype=np.int64)
        targets = tokens_np[positions].astype(np.int64)
        for n in range(self.min_order, self.max_order + 1):
            valid = positions >= n - 1
            if not valid.any():
                continue
            v_pos = positions[valid]
            v_tgt = targets[valid]
            ctx_keys = _batch_hash_ctx(tokens_np, v_pos, n, self.bucket_mask).astype(np.int64)
            full_keys = _batch_hash_full(tokens_np, v_pos, v_tgt, n, self.bucket_mask).astype(np.int64)
            self.ctx_tables[n] += np.bincount(ctx_keys, minlength=self.num_buckets).astype(np.int32)
            self.full_tables[n] += np.bincount(full_keys, minlength=self.num_buckets).astype(np.int32)
```

### Entropy-adaptive alpha mixing

```python
# For each scored position with an n-gram match:
# 1. Compute model entropy: H = -sum(p * log(p))
# 2. Center shifts per order: higher orders trusted even at low entropy
# 3. Sigmoid blending: high entropy → high alpha (trust n-gram more)

# Per-order multipliers from PR #809 (best 0.295 BPB):
ORDER_MULTS = np.array([0.3, 0.3, 0.97, 2.0, 2.0, 2.0, 2.0, 2.0])  # orders 2-9

alpha_min = 0.05
alpha_max = 0.60
entropy_center = 3.0  # shift by -0.25*(order - min_order)
entropy_scale = 2.0

# In eval loop, for each batch segment:
if ng_matched.any():
    matched_ords = ng_orders[ng_matched].astype(np.float64)
    centers = entropy_center - 0.25 * (matched_ords - min_order)
    sig = 1.0 / (1.0 + np.exp(-entropy_scale * (seg_entropy[ng_matched] - centers)))
    alpha = alpha_min + (alpha_max - alpha_min) * sig
    # Per-order multipliers
    mult_indices = ng_orders[ng_matched] - min_order
    mult_indices = np.clip(mult_indices, 0, len(ORDER_MULTS) - 1)
    alpha = alpha * ORDER_MULTS[mult_indices]
    alpha = np.clip(alpha, 0.0, 0.95)
    # Final mix
    final_p[ng_matched] = (1.0 - alpha) * p_neural[ng_matched] + alpha * ngram_p[ng_matched]
    final_p = np.maximum(final_p, 1e-10)
```

### Chunk-based processing for multi-GPU

Process in 1M-token chunks. Within each chunk, score all positions first, THEN update cache.
This ensures all 8 GPU ranks see the same cache state (since distributed eval assigns different
segments to different ranks, but the cache update covers the full chunk for all ranks).

```python
chunk_tokens = 1_000_000  # must be multiple of stride and aligned with segments

for chunk_start in range(1, total_tokens + 1, chunk_tokens):
    chunk_end = min(chunk_start + chunk_tokens, total_tokens + 1)
    # Score all segments in this chunk (distributed across ranks)
    rank_segments = chunk_segments[rank::world_size]
    for seg in rank_segments:
        # ... score and compute final_p with current cache state ...
    # After ALL scoring in chunk: update cache
    cache.update_batch(tokens_np, chunk_start, chunk_end)
```

---

## Technique 2: Complementary Training (PR #803, boosts n-gram further)

During training, weight the loss inversely to bigram predictability. The model specializes
on tokens that n-gram CANNOT predict, which enables higher alpha at eval time.

```python
class TrainNgramTracker:
    def __init__(self, vocab_size, device, complement_alpha=0.5):
        self.V = vocab_size
        self.alpha = complement_alpha
        self.bi_counts = torch.zeros(vocab_size, vocab_size, device=device, dtype=torch.float32)
        self.bi_totals = torch.zeros(vocab_size, device=device, dtype=torch.float32)

    @torch.no_grad()
    def update(self, x, y):
        xf, yf = x.reshape(-1), y.reshape(-1)
        ones = torch.ones(xf.numel(), device=xf.device, dtype=torch.float32)
        self.bi_counts.reshape(-1).scatter_add_(0, xf * self.V + yf, ones)
        self.bi_totals.scatter_add_(0, xf, ones)

    def get_weights(self, x, y):
        xf, yf = x.reshape(-1), y.reshape(-1)
        total = self.bi_totals[xf]
        count = self.bi_counts.reshape(-1)[xf * self.V + yf]
        ngram_prob = count / (total + 1)
        return (1.0 - self.alpha * ngram_prob).clamp(min=0.1)

# In training loop:
# complement_alpha = 0.5 (env var COMPLEMENT_ALPHA)
# tracker.update(x_batch, y_batch)  # update bigram stats
# weights = tracker.get_weights(x_batch, y_batch)  # shape: (B*T,)
# loss = (ce_loss_per_token * weights).mean()  # weighted loss
```

Ablation from PR #803:
- Base model only: 1.139 BPB
- + Standard backoff (alpha=0.05): 0.700 BPB  (-0.44!)
- + Complementary training + alpha=0.20: 0.442 BPB  (-0.26 more!)

---

## Implementation Priority for Our System

### Priority 1 (IMPLEMENT IMMEDIATELY): Basic N-gram Backoff Eval Cache

This alone will take us from ~1.119 to ~0.67 BPB. Add to existing `train_gpt.py`:

1. Add env vars: `NGRAM_EVAL_ENABLED`, `NGRAM_EVAL_MAX_ORDER` (start with 9), `NGRAM_EVAL_BUCKETS` (4194304)
2. Add `NgramEvalCache` class (copy from above)
3. Add `eval_ngram()` function that wraps the existing eval loop
4. When `NGRAM_EVAL_ENABLED=1`, use `eval_ngram()` instead of `eval_standard()`
5. Set `ngram_eval_enabled=True` by default in profile `full_8gpu_600s`

Key parameters:
- `NGRAM_EVAL_MAX_ORDER=9` (try 7, 9, 11, 15 — higher is better but slower)
- `NGRAM_EVAL_BUCKETS=4194304` (4M, must be power of 2)
- `NGRAM_EVAL_CHUNK_TOKENS=1000000` (1M token chunks)
- `NGRAM_EVAL_ALPHA_MIN=0.05`, `NGRAM_EVAL_ALPHA_MAX=0.60`
- `NGRAM_EVAL_ENTROPY_CENTER=3.0`, `NGRAM_EVAL_ENTROPY_SCALE=2.0`

### Priority 2: Tune N-gram Parameters

After getting basic n-gram working:
- Try `NGRAM_EVAL_MAX_ORDER` in {9, 11, 15}
- Tune `ORDER_MULTS` array
- Tune alpha range
- Try `NGRAM_EVAL_CHUNK_TOKENS=1000000` vs smaller chunks

### Priority 3: Complementary Training

Add `COMPLEMENT_ALPHA=0.5` to training. This takes ~same training time but enables
higher eval-time n-gram weight. PR #803 shows this gives ~-0.26 BPB additional gain.

### Priority 4: TTT + N-gram Combined

PR #809 (0.295 BPB) uses both TTT (LoRA rank 8) AND n-gram. TTT first, then n-gram.
The combination is multiplicative in benefit.

---

## Eval Time Budget

Current concern: n-gram eval is slower than standard eval. PR timings:
- PR #809 (0.295 BPB): TTT 53s + N-gram 287s = 340s eval total (within 600s budget)
- PR #803 (0.4416 BPB): 458s eval total
- PR #796 (0.4374 BPB): ~330s eval total

Our current TTT takes ~465s. If we add n-gram, we need to be careful about budget.
Start with n-gram alone (without TTT) first to verify it fits in 600s.

---

## Files to Read

Before implementing, study:
- `/tmp/sota_pr809_train_gpt.py` — full 0.295 BPB implementation (chunk n-gram + TTT)
- `/tmp/sota_pr803_train_gpt.py` — complementary training + backoff n-gram
- Current `train_gpt.py` in the latest run directory — our base to modify

## Immediate Action

1. Copy our current best `train_gpt.py` (from `arch_010` lineage)
2. Add the `NgramEvalCache` class
3. Add `eval_ngram()` function
4. Wire it up with env var `NGRAM_EVAL_ENABLED=1`
5. Run a quick eval-only test on our best existing checkpoint
6. This should immediately go from ~1.119 to ~0.67 BPB
