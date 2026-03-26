# User-Proposed Ideas: Eval-Time Mixing Techniques

These ideas were proposed by the project owner and should be treated as **high-priority** experiment directions.
The agent must actively explore these in upcoming rounds.

---

## Background: What the Current SOTA Is Doing

The current leaderboard #1 (`LeakyReLU²+LegalTTT+ParallelMuon`, BPB=1.1194) uses **Test-Time Training (TTT)**:
- At evaluation time, for each chunk of ~32768 tokens, the model is fine-tuned on those tokens using 3 epochs of SGD before scoring them.
- This is "score-first" TTT: score with sliding window, then adapt on the chunk, then move to the next chunk.
- TTT alone contributes ~-0.002 to -0.003 BPB gain with ~410s of the 10-minute eval budget.
- Key hyperparameters: `TTT_LR=0.002`, `TTT_EPOCHS=3`, `TTT_CHUNK_TOKENS=32768`, `TTT_MOMENTUM=0.9`, all blocks unfrozen.

The TTT mechanism is essentially letting the model "memorize" local patterns in each test chunk, which is analogous to what n-gram models do (capture local statistics). The user's ideas below extend this direction with different mechanisms.

---

## Priority Idea 1: N-gram / Small LM Interpolation at Eval Time

**Core idea**: During evaluation, interpolate the transformer's next-token probabilities with a count-based n-gram language model or a tiny neural LM trained on the same data.

```
p_final(w | context) = (1 - λ) * p_transformer(w | context) + λ * p_ngram(w | context)
```

**Why it might work**:
- N-gram models are near-perfect on repeated local patterns (exact phrase repetitions) that transformers may still miss.
- The interpolation weight λ can be fixed or adaptive (e.g., higher λ when the n-gram model is confident).
- N-gram statistics can be built from the training data (same FineWeb shards) and stored compactly.
- A simple trigram or 4-gram model with Good-Turing or Kneser-Ney smoothing over the validation distribution could fit in a few MB of the artifact budget.

**Variants to explore**:
1. **Count-based n-gram** (trigram/4-gram with KN smoothing) stored as a compact hash table or trie, interpolated with fixed λ=0.1–0.3.
2. **Neural cache** (Grave et al. 2017): at eval time, maintain a cache of recent hidden states and softmax over dot products with current hidden state. Zero training cost.
3. **Pointer network / mixture of softmaxes**: mix the base distribution with a pointer that copies from recent context (good for exact repetitions).

**Practical notes**:
- The n-gram model bytes count toward the 16MB cap, so it must be compact. A pruned 4-gram model with cutoff ≥ 2 counts can be very small.
- Interpolation only changes the eval loop, not training. Zero training cost.
- Can be combined with TTT.

---

## Priority Idea 2: Decoding-Time Temperature Adjustment

**Core idea**: Apply a learned or tuned temperature scaling to the model's logits during evaluation to sharpen or smooth predictions globally or per-position.

```
p_final(w | context) = softmax(logits / T)
```

**Why it might work**:
- Models trained with cross-entropy may produce slightly miscalibrated logits. A temperature T slightly < 1 (e.g., T=0.9–0.95) can sharpen predictions and reduce BPB.
- Temperature can be tuned on a held-out slice of the validation set (but must be done legally — cannot use the full val set for tuning).
- Per-layer or per-head temperature scaling (like in temperature scaling for calibration) could be more powerful.

**Variants to explore**:
1. **Global temperature search**: grid-search T ∈ {0.85, 0.90, 0.95, 1.0, 1.05} on a small held-out slice. Zero model change, zero byte cost.
2. **Per-position temperature**: higher temperature for early positions in context (less certain), lower for later positions (more context).
3. **Logit adjustment**: add a learned bias vector to logits at eval time (cheap calibration).
4. **Combined with TTT**: after TTT adaptation, apply temperature scaling to the adapted model.

**Practical notes**:
- Temperature T is a single scalar — zero byte cost.
- Must be careful not to tune on the official val set (use a held-out train shard instead).
- Expected gain: ~0.001–0.005 BPB if calibration is off.

---

## Priority Idea 3: Small RNN Mixing at Eval Time

**Core idea**: Train a tiny RNN (LSTM or GRU, ~100K–500K parameters) alongside or after the main transformer. At eval time, mix predictions:

```
p_final = (1 - λ) * p_transformer + λ * p_rnn
```

**Why it might work**:
- RNNs and transformers have complementary strengths: RNNs are very good at tracking exact repetitions and long-range repetitive structure.
- A small RNN fits easily within the byte budget (a 2-layer LSTM with hidden_size=256 is ~1MB compressed).
- The mixing weight λ can be learned or tuned.
- This is related to the "mixture of experts at the output distribution" idea.

**Variants to explore**:
1. **Distilled RNN**: train a small LSTM to match the transformer's output distribution (knowledge distillation). At eval, mix the two.
2. **Residual RNN**: train the RNN to predict the transformer's residuals (what the transformer gets wrong). Then: `logits_final = logits_transformer + α * logits_rnn`.
3. **Gating mechanism**: learn a gate g(context) ∈ [0,1] that blends the two distributions based on local context statistics.
4. **Cache-augmented RNN**: the RNN maintains a recurrent state that acts as a neural cache.

**Practical notes**:
- The RNN must be trained (adds training cost) or distilled from the transformer.
- Byte budget: a 2-layer GRU with hidden_dim=128 is ~150K params ≈ ~300KB int8 compressed. Very affordable.
- This can be stacked on top of TTT.

---

## Implementation Priority Order

Given the current local best of ~1.124 BPB and SOTA at 1.119:

1. **First**: Test TTT on the current local best checkpoint (no code change, just eval-time SGD). This is the most direct SOTA technique and has been validated with large gains.
2. **Second**: Temperature scaling search — zero cost, could yield 0.001–0.003 BPB.
3. **Third**: Neural cache / n-gram interpolation — moderate cost, potentially 0.005–0.015 BPB.
4. **Fourth**: Small RNN mixing — requires training, but could be complementary to TTT.

---

## Key Files to Read

Before implementing any of these, read:
- `context/reference_materials/sota_record_01_1.11940_2026-03-23_LeakyReLU_LegalTTT_ParallelMuon.md` — full TTT implementation (lines 1234+)
- The `eval_val_sliding_ttt()` function in that file — exact TTT protocol
- `train_gpt.py` — current local eval loop to understand what to modify

## Success Metric

For all of these: post-export `val_bpb` improvement under the 16MB cap.
Compare against current local best (`repro_005` seed-42 at ~1.12484) as the baseline.
