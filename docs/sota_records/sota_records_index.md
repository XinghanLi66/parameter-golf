# SOTA Records Index

Top 5 submissions from `openai/parameter-golf` sorted by post-export val_bpb (lower is better).

1. **2026-03-23_LeakyReLU_LegalTTT_ParallelMuon** | bpb=`1.1194` | abaybektursun
   > LeakyReLU(0.5)² activation (-0.003 BPB vs relu²) + legal score-first TTT (PR #461 recipe, 3ep SGD, all blocks unfrozen) ...

2. **2026-03-22_11L_EMA_GPTQ-lite_warmdown3500_QAT015_1.1233** | bpb=`1.12278022` | Tianhao Wu
   > EMA(0.997) weight averaging + GPTQ-lite optimal clip percentile search + warmdown=3500 + Late QAT threshold=0.15, built ...

3. **2026-03-21_11L_XSA4_EMA_PartialRoPE_LateQAT_1.1248** | bpb=`1.12484502` | Jack Princz
   > 11 layers with Partial RoPE (16 of 64 dims), LN Scale (1/sqrt(l+1)), EMA weight averaging (decay=0.997), Exclusive Self ...

4. **2026-03-20_11L_XSA4_EMA_Int6_MLP3x_WD04_1.1271** | bpb=`1.12707468` | Jack Princz
   > 11 layers with Exclusive Self Attention (XSA) on last 4 layers, EMA weight averaging (decay=0.997), int6 per-row on all ...

5. **2026-03-20_11L_EfficientPartialXSA_FA3_SWA120** | bpb=`1.13071416` | vadim borisov (tabularis.ai)
   > 11 layers, int6 quant, zstd-22. Novel contribution: Efficient Partial Exclusive Self Attention (XSA, arXiv:2603.09078) a...

