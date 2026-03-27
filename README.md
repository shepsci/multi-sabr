# Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning

Multi-SABR evaluates LLM selective attention across four domain-specific benchmark tasks, measuring whether models attend consistently across subject areas or show domain-specific weaknesses. 19 models evaluated as of March 2026.

## Component Benchmarks

| Benchmark | Domain | Version | Kaggle |
|-----------|--------|---------|--------|
| SABR-2026 | General knowledge | v5 | [Leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench) |
| BIO-SABR-2026 | Biosafety / Biosecurity | v3 | [Leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench) |
| CYBER-SABR-2026 | Cybersecurity / AI Security | v3 | [Leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench) |
| CHEM-SABR-2026 | Chemical Safety / Security | v4 | [Leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench) |

## Scoring

- Each domain produces a composite score: 40% Distractor Robustness (ARS) + 30% Source-Selective QA + 30% Spotlight F1
- Multi-SABR Composite aggregates across all four domain composites
- Models that refuse or error on a domain score 0% for that domain

## Leaderboard (March 2026)

| Rank | Model | Overall | BIO-SABR-2026 | CYBER-SABR-2026 | SABR-2026 | CHEM-SABR-2026 |
|------|-------|---------|---------------|-----------------|-----------|----------------|
| 1 | Claude Opus 4.6 | **0.77** | 0.59 | **0.84** | **0.92** | **0.72** |
| 1 | DeepSeek V3.2 | **0.77** | 0.71 | 0.77 | 0.90 | 0.69 |
| 3 | Gemini 3.1 Pro Preview | 0.76 | 0.71 | 0.75 | 0.88 | 0.71 |
| 3 | Qwen 3 235B A22B Instruct | 0.76 | 0.69 | 0.74 | 0.91 | 0.69 |
| 3 | Qwen 3 Coder 480B | 0.76 | 0.67 | 0.74 | **0.92** | 0.70 |
| 3 | Qwen 3 Next 80B Instruct | 0.76 | **0.72** | 0.78 | 0.90 | 0.65 |
| 7 | DeepSeek V3.1 | 0.75 | 0.69 | 0.73 | 0.91 | 0.67 |
| 8 | Gemini 3.1 Flash-Lite Preview | 0.73 | 0.65 | 0.69 | 0.88 | 0.68 |
| 8 | Qwen 3 Next 80B Thinking | 0.73 | 0.69 | 0.75 | 0.85 | 0.62 |
| 10 | GLM-5 | 0.72 | 0.64 | 0.75 | 0.82 | 0.67 |
| 11 | DeepSeek-R1 | 0.69 | 0.62 | 0.71 | 0.79 | 0.66 |
| 12 | Claude Haiku 4.5 | 0.68 | 0.60 | 0.69 | 0.86 | 0.58 |
| 12 | Claude Sonnet 4.6 | 0.68 | 0.50 | 0.77 | 0.85 | 0.60 |
| 14 | Gemini 2.5 Flash | 0.65 | 0.58 | 0.66 | 0.79 | 0.59 |
| 14 | Gemini 2.5 Pro | 0.65 | 0.56 | 0.67 | 0.77 | 0.59 |
| 14 | Gemma 3 12B | 0.65 | 0.55 | 0.66 | 0.84 | 0.56 |
| 17 | Gemma 3 27B | 0.64 | 0.57 | 0.62 | 0.82 | 0.54 |
| 18 | Gemma 3 4B | 0.61 | 0.51 | 0.60 | 0.83 | 0.52 |
| 19 | Gemma 3 1B | 0.52 | 0.43 | 0.53 | 0.67 | 0.44 |

## Key Findings

Across 19 models, composite scores range from 52% to 77% — a 25-point spread driven by two consistent effects: (1) large variance between models, and (2) large domain penalties for every model (every model scores higher on general knowledge than any regulated domain). Within-model domain gaps can exceed 30 points (Claude Opus 4.6: 92% on SABR-2026, 59% on BIO-SABR-2026).

Claude Opus 4.6 and DeepSeek V3.2 tie for first at 0.77. The Qwen 3 family places four models in the top six. BIO-SABR-2026 and CHEM-SABR-2026 remain the hardest domains across all models.

## Repository Structure

This is a monorepo containing all component SABR benchmarks:

```
multi-sabr/
├── benchmarks/
│   ├── sabr/           # SABR (General Knowledge)
│   ├── bio-sabr/       # Bio-SABR (Biosafety)
│   ├── cyber-sabr/     # Cyber-SABR (Cybersecurity)
│   └── chem-sabr/      # Chem-SABR (Chemical Safety)
├── writeup/            # Multi-SABR cross-domain writeup
├── README.md
└── config.yaml
```

Each `benchmarks/` subdirectory contains a complete, standalone copy of its component benchmark (data, scoring code, Kaggle notebook, and domain-specific writeup).

## Resources

- [Multi-SABR Writeup](writeup/writeup.md)
- [Kaggle Benchmark](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench)

## Citation

Shep Scientific (2026). Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning.
