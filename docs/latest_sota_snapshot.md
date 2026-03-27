# Latest Parameter Golf SOTA Snapshot

- Generated at: `2026-03-27T13:42:09Z`
- Source: `https://raw.githubusercontent.com/openai/parameter-golf/main/README.md`
- Current top leaderboard entry: `LeakyReLU² + Legal Score-First TTT + Parallel Muon` by `abaybektursun` at `1.1194`

## Why this file exists

Use this as the live companion to `docs/sota_review.md`.
The older review explains the broad design space; this file keeps the research loop aligned with the current leaderboard and recent winning motifs.

## Current competition reminders

- Goal: minimize validation `val_bpb` on FineWeb under the 16MB artifact cap.
- Record-track submissions must still train within 10 minutes on 8xH100 and clear the significance bar described in the official repo README.
- Evaluation-side tricks matter. Do not treat train loss alone as sufficient evidence.

## Current top leaderboard entries

- 1. `LeakyReLU² + Legal Score-First TTT + Parallel Muon` | score `1.1194` | abaybektursun | 2026-03-23 | On PR #549: LeakyReLU(0.5)^2 + TTT + Parallel Muon on the PR #414 stack
- 2. `11L EMA + GPTQ-lite + warmdown3500` | score `1.1228` | signalrush | 2026-03-22 | On PR #374: GPTQ-lite clip search + EMA, plus warmdown3500 and QAT@0.15
- 3. `11L Partial RoPE + LN Scale + EMA + XSA4` | score `1.1248` | jfprincz | 2026-03-21 | On PR #287: Partial RoPE (16/64) + layerwise LN scale
- 4. `11L XSA4 + EMA + Int6 MLP3x` | score `1.1271` | jfprincz | 2026-03-20 | On PR #198: XSA on the last 4 layers + EMA replacing SWA
- 5. `11L Efficient Partial XSA` | score `1.1307` | unnir | 2026-03-20 | On PR #198: Efficient Partial XSA on the deepest 3 layers
- 6. `10L Int5-MLP + BigramHash(10240)` | score `1.1428` | thwu1 | 2026-03-20 | 10 layers, mixed int5/int6 quantization, BigramHash(10240), SWA(0.4), WD=0.04
- 7. `Int6 MLP3x + SmearGate + BigramHash` | score `1.1458` | Raahil Shah | 2026-03-20 | 3x MLP + SmearGate + BigramHash + OrthoInit + Muon WD + SWA
- 8. `11L MLP3x + Int6 QAT` | score `1.1502` | aruniyer | 2026-03-20 | 11 layers, 3x MLP, int6 QAT, zstd-22, WD=0.04, sliding eval

## Newly visible runs vs local checkout

- 1. `LeakyReLU² + Legal Score-First TTT + Parallel Muon` | score `1.1194` | abaybektursun | 2026-03-23 | On PR #549: LeakyReLU(0.5)^2 + TTT + Parallel Muon on the PR #414 stack
- 2. `11L EMA + GPTQ-lite + warmdown3500` | score `1.1228` | signalrush | 2026-03-22 | On PR #374: GPTQ-lite clip search + EMA, plus warmdown3500 and QAT@0.15
- 3. `11L Partial RoPE + LN Scale + EMA + XSA4` | score `1.1248` | jfprincz | 2026-03-21 | On PR #287: Partial RoPE (16/64) + layerwise LN scale
- 4. `11L XSA4 + EMA + Int6 MLP3x` | score `1.1271` | jfprincz | 2026-03-20 | On PR #198: XSA on the last 4 layers + EMA replacing SWA
- 5. `11L Efficient Partial XSA` | score `1.1307` | unnir | 2026-03-20 | On PR #198: Efficient Partial XSA on the deepest 3 layers

## Recurring motifs in the current top entries

- `Int6 quantization` appears in 4 of the current top 8 leaderboard entries.
- `EMA` appears in 3 of the current top 8 leaderboard entries.
- `MLP3x` appears in 3 of the current top 8 leaderboard entries.
- `XSA` appears in 3 of the current top 8 leaderboard entries.
- `BigramHash` appears in 2 of the current top 8 leaderboard entries.
- `Muon / WD tuning` appears in 2 of the current top 8 leaderboard entries.
- `QAT / STE` appears in 2 of the current top 8 leaderboard entries.
- `GPTQ-lite` appears in 1 of the current top 8 leaderboard entries.

## How planner/reviewer should use this

- Before proposing a new experiment, identify which top-run motif you are testing, extending, or intentionally excluding.
- Prefer small deltas against the strongest nearby baseline instead of vaguely copying multiple leaderboard ideas at once.
- If the current top runs moved ahead since the older SOTA review, explain whether our next experiment closes that gap on architecture, optimization, evaluation, or export.
- If you are not testing a current leaderboard motif, explicitly justify why the deviation is still scientifically valuable.
