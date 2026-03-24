# Parameter Golf SOTA Review

## Scope

This note is based on:

- the current `parameter-golf` repo `README.md` leaderboard and rules,
- recent record folders in `records/track_10min_16mb/`,
- the unlimited-compute non-record baseline in `records/track_non_record_16mb/`,
- the current reference framework in `../research-proposal-lab`, which is a generic planner-worker research loop rather than a Parameter Golf-specific codebase.

I did not make framework changes in this pass.

## 1. Competition Goal And Constraints

- Objective: minimize FineWeb validation compression score under a fixed 16 MB artifact budget, reported as tokenizer-agnostic `val_bpb`.
- Main track constraint: training must complete in under 10 minutes on `8xH100 SXM`.
- Eval constraint: evaluation must also stay under 10 minutes.
- Artifact budget: total counted bytes are `train_gpt.py` code bytes plus compressed model bytes; cap is decimal `16,000,000`.
- Submission bar for new SOTA: beat the current SOTA by at least `0.005` nats with sufficient multi-run significance (`p < 0.01`).
- Practical implication: this is not just a modeling contest. Compression friendliness, evaluation strategy, code-size discipline, and reproducibility all matter directly.

## 2. What Recent SOTA Actually Looks Like

### Current frontier

- `2026-03-20_10L_Int5MLP_MuonWD04_SWA50`: `1.1428`
- `2026-03-20_Int6_MLP3x_SmearGate_BigramHash_MuonWD_SWA`: `1.1458`
- `2026-03-19_MLP3x_QAT_Int6_SlidingWindow`: `1.1502`

### The progression of ideas

1. `Sliding window eval` was the first huge free win.
   - It improved the naive baseline from `1.2244` to `1.1925` with essentially no training change.
   - This is now table stakes, not a differentiator.

2. `Longer context / training optimization` pushed scores toward low `1.20x`.
   - `seq_len=4096`, lower LR, higher Muon momentum, and longer warmdown reached `1.2014`.
   - This showed that context and quantization-aware optimization matter more than raw baseline speed.

3. `Compression-aware training` became central.
   - Stronger warmdown, Muon weight decay, fp16 embeddings, and lower quantization damage were repeatedly beneficial.
   - Several submissions explicitly report that post-quantization loss dominates many architectural gains.

4. `Evaluation + compression + extra capacity` became the dominant recipe.
   - The leaderboard leaders combine sliding eval with aggressive quantization/compression and then spend the saved bytes on more useful capacity: deeper stacks, 3x MLPs, or extra feature pathways.

5. `The current top recipe is a stack, not a single trick`.
   - Mixed `int5/int6`, `BigramHash`, `SmearGate`, `Muon WD=0.04`, `warmdown=3000`, `SWA`, and a 10th layer.

### Relevant tricks from recent strong runs

- `Sliding window eval` with `stride=64`
  - Still one of the largest deltas ever reported.
  - Now a baseline requirement.

- `Aggressive low-bit export`
  - `int6` everywhere important became standard.
  - The current best run goes further: `int5` for MLP weights, `int6` for attention weights.

- `Keep sensitive tensors higher precision`
  - Strong runs often keep tied embeddings in `fp16`.
  - Some also keep late-layer key projections in `fp16`.

- `zstd-22` instead of `zlib`
  - Repeatedly described as critical for fitting deeper/wider models under the byte cap.

- `MLP expansion to 3x`
  - One of the most consistently strong uses of saved bytes.

- `More depth funded by compression`
  - 10-layer and 11-layer models outperform the original 9-layer baseline when paired with quantization/compression improvements.

- `Compression-friendly optimization`
  - Muon with higher momentum warmup and nontrivial decoupled weight decay (`0.02` to `0.04`) is recurrent.
  - Longer warmdown is also recurrent.

- `Orthogonal / muP-style init`
  - Frequently used to get more useful learning inside the short 600s budget.

- `Cheap local inductive bias`
  - `SmearGate` and `BigramHash` are both recurring and directly rewarded at this scale.

- `SWA near the end`
  - Recent top entries report another small but real gain from averaging only late, well-converged checkpoints.

- `QAT / STE`
  - Still competitive, but the very top run currently wins with a more targeted mixed-precision export recipe rather than relying on QAT alone.

- `TTT / LoRA adaptation`
  - Interesting, but currently less important than getting the main recipe stack right.
  - Its reported gain beyond doc-aware/strided eval is comparatively small.

## 3. Recurring Design Patterns Across Strong Submissions

Across the strong submissions, the same meta-pattern shows up:

### A. Treat quantization as a first-class training target

The best runs are not "train a good fp16 model, then compress it." They explicitly shape training so that the exported artifact stays good after quantization and compression.

### B. Use byte savings to buy high-leverage capacity

Saved bytes are mostly reinvested into:

- deeper models,
- wider MLPs,
- small auxiliary feature pathways like `BigramHash`,
- selective high-precision exceptions for sensitive weights.

### C. Separate "free eval gains" from "real model gains"

Top competitors aggressively take evaluation wins such as sliding-window scoring, but they also keep improving the training/export recipe. The frontier is now on both axes simultaneously.

### D. Prefer simple, cheap inductive biases over exotic heavy mechanisms

The winning additions are small and local:

- previous-token blending,
- hashed bigram features,
- skip connections,
- better initialization,
- better schedules.

This is a good sign for fast iteration.

### E. Multi-seed reproducibility is part of the method

Strong submissions are packaged as stable recipes with 3-seed evidence, not as single lucky runs.

## 4. Applicability To The Current Planner-Worker Reference Solution

`../research-proposal-lab` is a generic planner-worker loop:

- planner reads proposal/workspace state and emits round instructions,
- worker executes changes and experiments,
- the loop persists only lightweight state via copied proposal, planning files, previous planner instructions, and previous worker summary.

That structure is reasonable for Parameter Golf, but it currently looks too generic for a rapidly moving leaderboard. The main gap is not the existence of a planner and worker; it is the lack of competition-specific memory, ranking, and search discipline.

Most applicable ideas for this setup:

1. `Make the planner reason in recipe stacks, not isolated tricks.`
   - Current SOTA comes from bundled improvements.
   - The planner should compare candidate stacks like `sliding eval + int6/int5 + fp16 embed + MLP3x + WD + SWA`, not single toggles in isolation.

2. `Track export-time score separately from pre-quant score.`
   - The competition is won on roundtrip/exported `val_bpb`, not raw train loss.
   - The worker should treat quantization gap as a first-class metric in every experiment summary.

3. `Build explicit leaderboard memory inside the loop.`
   - The strongest recent patterns are easy to mine from `records/`.
   - The planner should have a compact rolling summary of best methods, scores, and deltas instead of re-deriving them ad hoc each round.

4. `Bias search toward compression-aware capacity trades.`
   - For a reference solution already around `~1.18` as you stated, generic hyperparameter search is likely too weak.
   - The next wins are more likely to come from targeted byte reallocation and export-aware training.

5. `Exploit the planner-worker split for staged experimentation.`
   - Planner: choose a small number of high-leverage recipe bundles.
   - Worker: run short ablations that isolate whether gains come from eval, training, or export.

## 5. Prioritized Next Optimization Directions

These are the most promising directions for your current setup, in priority order.

### 1. Re-anchor the reference solution around the current standard recipe

If your reference is around `~1.18`, the minimum modern baseline should likely include:

- sliding-window eval,
- `zstd-22`,
- fp16 tied embeddings,
- Muon momentum warmup,
- nontrivial Muon weight decay,
- longer warmdown,
- at least `MLP 3x` or extra depth.

Without this, the planner-worker loop may optimize an already outdated search space.

### 2. Focus search on byte allocation, not just training loss

Highest-value questions now look like:

- where should `int5` vs `int6` be used,
- which tensors should remain `fp16`,
- whether saved bytes should buy a 10th/11th layer, larger MLP, or bigger `BigramHash`,
- whether `SWA` or `QAT` gives the better export-time payoff in your recipe.

### 3. Add cheap local context features early

`SmearGate` and `BigramHash` appear unusually strong relative to their cost. They are among the most plausible upgrades if your current reference solution is still more baseline-like.

### 4. Keep evaluation improvements and training improvements disentangled

The worker should report at least:

- pre-quant metric,
- post-export metric,
- quantization gap,
- artifact bytes,
- eval mode used.

That will prevent the planner from confusing "better model" with "better evaluator."

### 5. Prefer narrow, evidence-producing ablation batches

Useful near-term ablations are likely:

- `MLP 2x vs 3x`,
- `9L vs 10L`,
- `int6-all vs int5-MLP/int6-attn`,
- `no-SWA vs late-SWA`,
- `BigramHash 4096 vs 8192 vs 10240`,
- `WD 0.02 vs 0.04`.

### 6. Treat TTT and more exotic mechanisms as secondary

They are still worth keeping in the idea pool, but the repo evidence suggests they are not the highest-ROI next move until the main stack is competitive.

## Bottom Line

The current Parameter Golf frontier is no longer about finding one clever trick. The winning pattern is:

`better evaluation` + `compression-aware optimization` + `more useful capacity purchased by low-bit export` + `small local inductive biases`.

For your current planner-worker reference solution, the most actionable next step is not a framework rewrite. It is to make the loop competition-aware enough to systematically search that recipe family, with explicit tracking of export-time `val_bpb`, artifact bytes, and leaderboard-derived priors.
