### SABR: Selective Attention Benchmark for Reasoning

### Shep Scientific

### Resources

- **Benchmark Collection:** [SABR on Kaggle Benchmarks](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning)
- **Benchmark Notebook:** [sabr_notebook on Kaggle](https://www.kaggle.com/code/shepscientific/new-benchmark-task-0adb6)
- **Dataset:** [SABR Selective Attention Data on Kaggle](https://www.kaggle.com/datasets/shepscientific/sabr-selective-attention-data)
- **GitHub:** [github.com/shepsci/SABR](https://github.com/shepsci/SABR)

### Problem Statement

Selective attention — focusing on task-relevant information while filtering distractors — is a core cognitive faculty. [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) identify it as a key sub-domain in their AGI measurement framework, with substantial gaps in existing AI benchmarks. Standard evaluations like [MMLU](https://arxiv.org/abs/2009.03300) test knowledge under clean conditions. But [Shi et al. (2023)](https://arxiv.org/abs/2302.00093) demonstrated that LLMs are easily distracted by irrelevant context, and [Liu et al. (2023)](https://arxiv.org/abs/2307.03172) showed that models fail to reliably attend to relevant information across longer contexts. These are attention failures, not knowledge failures. SABR addresses this gap with a focused question: **When a model fails, is it because it cannot reason, or because it cannot focus?**

### Task & Benchmark Construction

SABR evaluates 280 items across three tasks, each mapped to an established cognitive attention paradigm:

**Task 1: Distractor Robustness** (200 evals). Fifty factual questions presented under four increasing distraction levels: *clean* (question only), *low* (off-topic text added), *medium* (topically related but wrong context), *high* (plausible near-miss answers that could mislead). Inspired by the Stroop interference paradigm ([Stroop, 1935](https://doi.org/10.1037/h0054651)) — the classic "say the ink color, not the word" task. Metric: ARS = mean accuracy across all four conditions. Questions span five domains and are easy at baseline (>95% clean accuracy), so drops reflect distraction, not difficulty.

**Task 2: Source-Selective QA** (50 evals). Each item presents 3–4 named sources giving conflicting answers; the model must answer using only the designated source, ignoring the others — even if another source seems more authoritative. Inspired by [Cherry's (1953)](https://doi.org/10.1121/1.1907229) cocktail party attention experiments. Source position is varied to detect position bias.

**Task 3: Attentional Spotlight** (30 evals). 400–600 word documents containing 8–15 embedded facts; the model must extract only those matching a specific filter (e.g. "dates only" or "causal claims only"). Six filter types. Inspired by visual search research ([Treisman & Gelade, 1980](https://doi.org/10.1016/0010-0285(80)90005-5)). F1 scoring penalizes both missing relevant facts and including irrelevant ones.

Composite: Distractor 40% + Source-Selective 30% + Spotlight 30%.

### Dataset

All 130 base items span five domains. Distractor conditions follow a strict difficulty gradient. Source-conflict items use plausible institutional labels to prevent shortcut reasoning. Spotlight documents have controlled matching/non-matching ratios; two items have zero matching claims, testing false-positive resistance.

Data schema: `item_id`, `domain/category`, `question/document`, `gold_answer/gold_claims`, `answer_aliases`, `condition` (T1), `designated_source` (T2), `filter_criterion`/`gold_count` (T3).

### Technical Details

The [benchmark notebook](https://www.kaggle.com/code/shepscientific/new-benchmark-task-0adb6) uses the [kaggle-benchmarks SDK](https://github.com/Kaggle/kaggle-benchmarks): a single scored function returning a composite float. Each of 280 evaluations runs in its own isolated chat context to prevent earlier answers from influencing later ones. Data loads via `kagglehub.dataset_download()` with `/kaggle/input/` fallback. Scoring: case-insensitive exact match with alias support (Tasks 1–2); token-overlap F1 ≥70% (Task 3). Spotlight items with no correct answers score 1.0 only if the model produces no output.

### Results, Insights, and Conclusions

Results across six frontier models:

| Model | Composite | Distractor (ARS) | Source-Selective | Spotlight (F1) |
|-------|-----------|-------------------|------------------|----------------|
| **Claude Opus 4.6** | **92%** | 91% | 100% | 84% |
| **Gemini 3.1 Pro Preview** | **87%** | 88% | 100% | 74% |
| **Claude Sonnet 4.6** | **85%** | 86% | 100% | 68% |
| **Claude Haiku 4.5** | **84%** | 79% | 100% | 74% |
| **Gemma 3 27B** | **82%** | 81% | 100% | 66% |
| **Gemini 2.5 Flash** | **76%** | 68% | 100% | 63% |

Distractor breakdowns: Gemini 2.5 Flash: clean 100%, low 84%, medium 44%, high 48%. Gemma 3 27B: clean 96%, low 98%, medium 76%, high 54%. Gemini 3.1 Pro Preview: clean 100%, low 100%, medium 86%, high 64%.

**Key insights:**

1. **Attention degrades sharply under distraction.** All models achieve near-perfect accuracy on clean items but drop significantly at medium noise. Gemini 2.5 Flash falls 56 points to 44% at medium distraction — the same questions answered correctly without distractors. SABR isolates this as a pure attentional failure, consistent with [Shi et al. (2023)](https://arxiv.org/abs/2302.00093).

2. **Threshold collapse, not gradual degradation.** The sharp drop from low to medium distraction (when distractors become topically relevant), with minimal further decline to high, reveals a threshold effect invisible to standard QA benchmarks. Gemini 3.1 Pro Preview is a notable exception — maintaining 100% through low distraction before declining more gradually (86% → 64%), suggesting stronger low-level noise filtering.

3. **Explicit attentional instructions are well-followed.** Perfect source-selective accuracy across all models shows top-down attention (explicit "use only Source B") is robustly followed — in contrast to the failures in bottom-up distractor filtering.

4. **Spotlight extraction varies substantially.** F1 ranges from 63% (Gemini 2.5 Flash) to 84% (Claude Opus 4.6). Models over-extract rather than under-extract, suggesting difficulty suppressing partially-relevant claims — echoing [Liu et al. (2023)](https://arxiv.org/abs/2307.03172).

### Organizational Affiliations

Independent research (Shep Scientific).

### TL;DR:

**Evidence that the dataset and task are both high quality**

SABR covers 280 evaluations across 130 unique items; six frontier models have been benchmarked producing 1,680 total model-item evaluations. Three structurally distinct tasks prevent gaming via a single strategy. Task 1's repeated-measures structure (50 items × 4 conditions) isolates attention from knowledge: a question answered correctly without distractors but failed with them is unambiguous evidence of attentional deficit, not a knowledge gap. Tasks 1–2 use deterministic exact-match scoring; Task 3 uses token-overlap F1. Each evaluation runs in an isolated chat context to prevent answers from leaking across items.

**Evidence that the writeup is high quality**

This writeup covers all required sections: problem statement, task construction, dataset provenance, technical details, results with per-model breakdowns, and references. All artifacts are linked: the [benchmark collection](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning), the [notebook](https://www.kaggle.com/code/shepscientific/new-benchmark-task-0adb6), and the [dataset](https://www.kaggle.com/datasets/shepscientific/sabr-selective-attention-data). References span cognitive science, AGI measurement, and ML attention research.

**Evidence that the benchmark has sufficient discriminatory power**

A 16-point composite spread across six models (Claude Opus 4.6 at 92% vs. Gemini 2.5 Flash at 76%). A 56-point intra-model spread within the distractor task (Gemini 2.5 Flash: clean 100%, medium 44%). Model-specific failure profiles emerge: Gemma 3 27B collapses at high distraction (54%) despite near-perfect clean/low performance, while Gemini 2.5 Flash degrades more uniformly. Per-task scores are independently informative, enabling fine-grained comparison beyond a single aggregate.

### References & Citations

1. Burnell, R., et al. (2026). ["Measuring Progress Toward AGI: A Cognitive Framework."](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) Google DeepMind.
2. Stroop, J.R. (1935). ["Studies of interference in serial verbal reactions."](https://doi.org/10.1037/h0054651) *Journal of Experimental Psychology*, 18(6), 643–662.
3. Cherry, E.C. (1953). ["Some experiments on the recognition of speech, with one and with two ears."](https://doi.org/10.1121/1.1907229) *Journal of the Acoustical Society of America*, 25(5), 975–979.
4. Treisman, A.M. & Gelade, G. (1980). ["A feature-integration theory of attention."](https://doi.org/10.1016/0010-0285(80)90005-5) *Cognitive Psychology*, 12(1), 97–136.
5. Hendrycks, D., et al. (2021). ["Measuring Massive Multitask Language Understanding."](https://arxiv.org/abs/2009.03300) *ICLR 2021.*
6. Shi, F., et al. (2023). ["Large Language Models Can Be Easily Distracted by Irrelevant Context."](https://arxiv.org/abs/2302.00093) *ICML 2023.*
7. Liu, N., et al. (2023). ["Lost in the Middle: How Language Models Use Long Contexts."](https://arxiv.org/abs/2307.03172) *TACL 2023.*
8. [Kaggle Benchmarks SDK.](https://github.com/Kaggle/kaggle-benchmarks)
