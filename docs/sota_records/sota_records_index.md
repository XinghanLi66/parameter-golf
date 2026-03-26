# SOTA Records Index

Top 15 submissions from `openai/parameter-golf` sorted by post-export val_bpb (lower is better).

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

6. **2026-03-20_Int6_MLP3x_SmearGate_BigramHash_MuonWD_SWA** | bpb=`1.14581692` | Raahil Shah
   > Per-row int6 quantization on MLP/attention weights with zstd-22 compression, enabling 3x MLP expansion (hidden=1536). Sm...

7. **2026-03-19_MLP3x_QAT_Int6_SlidingWindow** | bpb=`1.15015359` | aruniyer

8. **2026-03-19_smeargate_orthoinit_muonwd** | bpb=`1.1556` | ?

9. **2026-03-19_WarmdownQuantization** | bpb=`1.1574404` | samuellarson
   > Int6 post-training quantization enables 3x MLP expansion (21.8M params in 16MB). Combined with train@2048 + sliding wind...

10. **2026-03-19_Seq2048_FP16Emb_TunedLR** | bpb=`1.15861696` | yahya010
   > 10-layer 512dim SP-1024, STE int6 QAT (zero quant gap), full int6 [-31,31] + zstd-22, MLP hidden=1344, fp16 tied embeddi...

11. **2026-03-19_MixedQuant_Int6Int8_SlidingWindow** | bpb=`1.16301431` | aquariouseworkman
   > 3x MLP expansion with mixed-precision quantization: int6 per-row (31 levels) on STE-protected block weights, int8 per-ro...

12. **2026-03-19_SlidingWindowEval** | bpb=`1.19250007` | Matthew Li
   > Baseline 9x512 SP-1024 architecture with sliding window evaluation at stride=64. Each token is scored with 960+ tokens o...

13. **2026-03-17_LoRA_TTT** | bpb=`1.1929` | sam
   > Naive baseline + per-document LoRA test-time training at eval. Rank-8 LoRA on lm_head/Q/V with Adam lr=0.01, overlapping...

14. **2026-03-19_TrainingOptSeq4096** | bpb=`1.20143417` | Spokane Way
   > SP-1024 9x512 KV4 run at TRAIN_SEQ_LEN=4096 with aggressively tuned Muon optimizer: momentum 0.99, lower LR (0.020/0.020...

15. **2026-03-18_LongContextSeq2048** | bpb=`1.20576485` | Spokane Way
   > SP-1024 9x512 KV4 run at TRAIN_SEQ_LEN=2048 with tuned seq2048 learning rates (0.040/0.032/0.032). This standalone recor...

