# Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning

Multi-SABR combines four structurally identical SABR benchmarks into a single cross-domain evaluation of LLM selective attention, measuring whether models attend consistently across subject areas or show domain-specific weaknesses.

## Component Benchmarks

| Benchmark | Domain | Evaluations | Kaggle |
|-----------|--------|-------------|--------|
| [SABR](https://github.com/shepsci/SABR) | General knowledge | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning) |
| [Bio-SABR](https://github.com/shepsci/bio-sabr) | Biosafety / Biosecurity | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/bio-sabr-biosafety-selective-attention-benchmark) |
| [Cyber-SABR](https://github.com/shepsci/cyber-sabr) | Cybersecurity / AI Security | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/cyber-sabr-cybersecurity-selective-attention-benc) |
| [Chem-SABR](https://github.com/shepsci/chem-sabr) | Chemical Safety / Security | 280 | [Benchmark](https://www.kaggle.com/benchmarks/shepscientific/chem-sabr-chemical-safety-selective-attention-benchmark) |

**Total: 1,120 evaluations per model across 520 unique items.**

## Scoring

- Each domain produces a composite score: 40% Distractor Robustness (ARS) + 30% Source-Selective QA + 30% Spotlight F1
- Multi-SABR Composite = mean of 4 domain composites (equal weight)
- Models that refuse or error on a domain score 0% for that domain

## Key Finding

Selective attention is domain-dependent. Models show 20-25 point swings across domains using structurally identical tasks. Safety filter interference creates a new category of attention failure, causing frontier models to drop from top-ranked to mid-pack when all domains are considered.

## Resources

- [Multi-SABR Writeup](writeup/writeup.md)
- [Kaggle Benchmark Collection](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm)

## Citation

Shep Scientific (2026). Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning.
