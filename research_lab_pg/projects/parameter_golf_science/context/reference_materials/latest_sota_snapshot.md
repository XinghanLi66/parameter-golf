# Latest Parameter Golf SOTA Snapshot

- Generated at: `2026-03-26T08:30:00Z`
- Source: `https://github.com/openai/parameter-golf/pulls`
- Current top leaderboard entry: `Complementary Training + Backoff N-gram + TTT` by `community` at `0.4416`

## !! PARADIGM SHIFT — 2026-03-26 !!

On 2026-03-26 the leaderboard was TRANSFORMED by eval-time n-gram backoff caching.
**Target SOTA: PR #803 at 0.4416 BPB** (PR #809 at 0.295 is under legality review and excluded for now).

N-gram backoff cache is PURELY EVAL-TIME — no retraining needed. Add it to our best
existing checkpoint and immediately jump from ~1.119 to ~0.67 BPB.
Full implementation guide: `context/reference_materials/URGENT_ngram_backoff_breakthrough.md`
Code references: `docs/sota_records/sota_code_pr803_0.442bpb_ComplementaryTraining.py`

## Why this file exists

Use this as the live companion to `docs/sota_review.md`.
The older review explains the broad design space; this file keeps the research loop aligned with the current leaderboard and recent winning motifs.

## Current competition reminders

- Goal: minimize validation `val_bpb` on FineWeb under the 16MB artifact cap.
- Record-track submissions must still train within 10 minutes on 8xH100 and clear the significance bar described in the official repo README.
- Evaluation-side tricks matter critically. The n-gram backoff cache is now the #1 technique.

## Current top leaderboard entries

- 1. `Complementary Training + Backoff N-gram + TTT` | score `0.4416` | community | 2026-03-26 | PR #803: CURRENT TARGET — train loss weighted by bigram-predictability, backoff n-gram orders 2-10 at eval, AdamW TTT (LR=5e-4, 4 epochs/chunk, Polyak EMA 0.998, freeze 9/11 blocks)
- 2. `X-WING 3D Cubric + Complementary Training` | score `0.4820` | community | 2026-03-26 | PR #814: cubric architecture + complementary training
- 3. `Order-Adaptive Entropy Gating + BackoffNgramMixer` | score `0.5466` | community | 2026-03-26 | PR #798: per-order entropy thresholds + drift-free TTT
- 4. `BackoffNgramMixer baseline` | score `0.6671` | community | 2026-03-26 | PR #813: simplest n-gram backoff, orders 2-10, entropy-adaptive alpha — good first target
- 5. `LeakyReLU² + Legal Score-First TTT + Parallel Muon` | score `1.1194` | abaybektursun | 2026-03-23 | LAST MERGED SOTA: PR #549
- NOTE: PR #809 (0.2952) is excluded from target — under legality review.

## Newly visible runs vs local checkout

- 1. `Complementary Training + Backoff N-gram + TTT` | score `0.4416` | community | 2026-03-26 | PR #803 — TARGET
- 2. `BackoffNgramMixer baseline` | score `0.6671` | community | 2026-03-26 | PR #813 — first milestone
- 3. `LeakyReLU² + Legal TTT + Parallel Muon` | score `1.1194` | abaybektursun | 2026-03-23 | Merged

## Recurring motifs in the current top entries

- `N-gram backoff cache (eval-time)` is the single biggest technique in ALL top 2026-03-26 entries.
- `Entropy-adaptive alpha mixing` appears in all n-gram entries: mix more when model is uncertain.
- `Score-first legality`: all n-gram caches are backward-looking (updated after scoring, not before).
- `TTT (Test-Time Training)` still adds value but is now secondary to n-gram cache.
- `Order multipliers`: boost high-order (5-9gram) matches x2.0, suppress bigrams x0.3.

## How planner/reviewer should use this

- READ `context/reference_materials/URGENT_ngram_backoff_breakthrough.md` FIRST before planning.
- The ONLY priority right now is implementing n-gram backoff eval cache in our `train_gpt.py`.
- This is an eval-time change only. Run it against our best existing checkpoint first.
- Expected outcome: ~1.119 BPB → ~0.67 BPB from n-gram alone; ~0.44 with complementary training.
- Before proposing a new experiment, identify which top-run motif you are testing, extending, or intentionally excluding.
- If you are not testing n-gram backoff, you MUST explicitly justify why this deviation is warranted.
