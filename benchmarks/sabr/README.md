# SABR: Selective Attention Benchmark for Reasoning

A novel benchmark measuring LLMs' ability to selectively attend to relevant information while filtering noise and distractors — targeting the **Attention** track of the [Measuring Progress Toward AGI](https://www.kaggle.com/competitions/kaggle-measuring-agi) hackathon.

## Overview

SABR evaluates three facets of selective attention:

1. **Distractor Robustness** (200 evals) — Can the model maintain accuracy when irrelevant or misleading context is injected?
2. **Source-Selective QA** (50 evals) — Can the model follow instructions to trust one source while ignoring conflicting alternatives?
3. **Attentional Spotlight** (30 evals) — Can the model extract only criterion-matching facts from information-dense documents?

## Quick Start

```bash
pip install -r requirements.txt

# Validate dataset integrity
python scripts/validate_data.py

# Run on Kaggle: upload sabr_notebook.py as a Kaggle Benchmark task
```

## Project Structure

```
SABR/
├── benchmark/           # Benchmark task implementations
├── data/                # Evaluation datasets (JSON)
├── scripts/             # Validation and analysis tools
├── writeup/             # Hackathon writeup
├── results/             # Evaluation results
├── config.yaml          # Benchmark configuration
└── requirements.txt     # Dependencies
```

## Cognitive Science Grounding

Each task maps to established attention paradigms:
- **Distractor Robustness** → Stroop effect / flanker tasks (interference resistance)
- **Source-Selective QA** → Dichotic listening (voluntary attention control)
- **Attentional Spotlight** → Visual search (targeted information extraction)
