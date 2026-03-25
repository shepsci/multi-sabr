# Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning

Multi-SABR combines six SABR benchmarks into a single cross-domain evaluation of LLM selective attention, measuring whether models attend consistently across subject areas or show domain-specific weaknesses. 19 models evaluated as of March 2026.

## Component Benchmarks

| Benchmark | Domain | Evaluations | Kaggle |
|-----------|--------|-------------|--------|
| [SABR](https://github.com/shepsci/SABR) | General knowledge | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning) |
| [Bio-SABR](https://github.com/shepsci/bio-sabr) | Biosafety / Biosecurity | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/bio-sabr-biosafety-selective-attention-benchmark) |
| [Cyber-SABR](https://github.com/shepsci/cyber-sabr) | Cybersecurity / AI Security | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/cyber-sabr-cybersecurity-selective-attention-benc) |
| [Chem-SABR](https://github.com/shepsci/chem-sabr) | Chemical Safety / Security | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/chem-sabr-chemical-safety-selective-attention-benchmark) |
| BIO-SABR-2026 | Biosafety (2026 refresh) | — | [Leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm) |
| CHEM-SABR-2026 | Chemical Safety (2026 refresh) | — | [Leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm) |

**Core benchmarks: 1,120 evaluations per model across 520 unique items.**

## Scoring

- Each domain produces a composite score: 40% Distractor Robustness (ARS) + 30% Source-Selective QA + 30% Spotlight F1
- Multi-SABR Composite aggregates across all six domain composites
- Models that refuse or error on a domain score 0% for that domain

## Key Findings

Across 19 models, composite scores range from 32% to 61% — driven by three effects: (1) large variance between models, (2) large variance between domains (every model scores higher on general knowledge than any regulated domain), and (3) some frontier models refuse to operate in biosafety and chemical safety domains entirely, dropping from first-in-class to near-last when refusals are scored as 0%.

## Resources

- [Multi-SABR Writeup](writeup/writeup.md)
- [Kaggle Benchmark Collection](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm)

## Citation

Shep Scientific (2026). Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning.
