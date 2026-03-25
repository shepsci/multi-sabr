### Bio-SABR: Biosafety Selective Attention Benchmark for Reasoning

### Shep Scientific

### Resources

- **Benchmark Notebook:** [Bio-SABR Benchmark on Kaggle](https://www.kaggle.com/code/shepscientific/new-benchmark-task-13123)
- **Dataset:** [Bio-SABR Biosafety Attention Data on Kaggle](https://www.kaggle.com/datasets/shepscientific/bio-sabr-biosafety-attention-data)
- **GitHub:** [github.com/shepsci/bio-sabr](https://github.com/shepsci/bio-sabr)
- **Related benchmark:** [SABR: Selective Attention Benchmark for Reasoning](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning)

### Problem Statement

Attention failures in biosafety and biosecurity contexts carry disproportionate consequences. A model that confuses BSL-2 with BSL-3 containment requirements due to distracting text, extracts the wrong regulatory threshold from a dense biosafety manual, or follows the wrong source when institutional guidance conflicts could contribute to real-world harm. [De Haro (2024)](https://doi.org/10.1089/apb.2023.0031) highlights that AI systems interacting with synthetic biology and biosafety workflows must maintain rigorous attention to safety-critical details. [Mouton et al. (2024)](https://www.rand.org/pubs/research_reports/RRA2977-2.html) demonstrated that LLMs possess substantial biological knowledge but vary in reliability — and [Anthropic's biorisk evaluations (2025)](https://red.anthropic.com/2025/biorisk/) show that even frontier models can produce harmful biosecurity outputs when attention lapses.

Bio-SABR addresses this by adapting the [SABR attention testing framework](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning) to biosafety/biosecurity domains. Where SABR tests general selective attention, Bio-SABR asks: **Do attention failures worsen when the stakes are higher and the distractors are domain-specific misinformation?** [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) identify selective attention as a key sub-domain in their AGI measurement framework — Bio-SABR stress-tests it in a domain where failures matter most.

### Task & Benchmark Construction

Bio-SABR evaluates 280 items across three tasks, each mapped to an established cognitive attention paradigm. All content spans five biosecurity domains: pathogen biology, biosafety protocols, dual-use research, biosecurity policy, and synthetic biology.

**Task 1: Distractor Robustness** (200 evals). Fifty biosafety questions presented under four distraction levels: *clean* (question only), *low* (off-topic sentences), *medium* (related biosafety text), *high* (near-miss biosecurity misinformation designed to mislead). For example: "What BSL is required for Mycobacterium tuberculosis?" (answer: BSL-3) with a high distractor claiming BSL-2 enhanced is sufficient. Inspired by Stroop interference ([Stroop, 1935](https://doi.org/10.1037/h0054651)). Metric: ARS = mean accuracy across all four conditions.

**Task 2: Source-Selective QA** (50 evals). Three named institutional sources (e.g., CDC, WHO, university biosafety office) present conflicting biosafety claims; the model must answer using only the designated source. For example: conflicting BSL classifications from different agencies — the model must follow the one it is told to trust, not the one that seems most authoritative. Inspired by Cherry's cocktail party experiments ([Cherry, 1953](https://doi.org/10.1121/1.1907229)). Designated source position is counterbalanced (A=17, B=17, C=16) to prevent position bias.

**Task 3: Attentional Spotlight** (30 evals). 400–600 word biosafety documents (facility incident reports, select agent reviews, gain-of-function policy analyses, synthesis screening procedures) containing 8–15 embedded claims. The model must extract only claims matching a specific filter criterion across six categories: risk levels, regulatory requirements, dual-use indicators, containment specifications, temporal claims, and attribution. Two items have zero matching claims, testing false-positive resistance. Documents use fictional institutions and scenarios to prevent memorization while maintaining realistic biosafety language. Inspired by visual search research ([Treisman & Gelade, 1980](https://doi.org/10.1016/0010-0285(80)90005-5)). F1 scoring penalizes both omissions and over-extraction.

Composite: Distractor 40% + Source-Selective 30% + Spotlight 30%.

### Dataset

130 base items across five biosafety domains (10 per domain for Tasks 1–2, 5 per category for Task 3). All biosafety facts in Tasks 1–2 are grounded in real-world data — real pathogens, real BSL classifications, real treaties and regulations — ensuring factual accuracy. Task 3 uses fictional institutions and scenarios to prevent memorization while maintaining domain realism.

Distractor conditions follow a strict difficulty gradient: low distractors are off-topic, medium distractors are topically related, and high distractors contain plausible biosafety misinformation that directly contradicts the correct answer. Source-conflict items use realistic institutional labels (CDC, WHO, NIH, university biosafety offices) with genuinely conflicting claims to prevent shortcut reasoning.

Data schema: `item_id`, `domain/category`, `question/document`, `gold_answer/gold_claims`, `answer_aliases`, `conditions` (T1), `designated_source` + `sources` (T2), `filter_criterion` + `gold_count` (T3).

### Technical Details

The [benchmark notebook](https://www.kaggle.com/code/shepscientific/bio-sabr-benchmark-k7m2x9) uses the [kaggle-benchmarks SDK](https://github.com/Kaggle/kaggle-benchmarks): a single scored function returning a composite float. Each of 280 evaluations runs in its own isolated chat context. Data loads via `kagglehub.dataset_download()` with `/kaggle/input/` fallback. Scoring: case-insensitive exact match with alias support (Tasks 1–2); token-overlap F1 with 70% threshold (Task 3). Spotlight items with zero correct answers score 1.0 only if the model produces no output.

The benchmark shares SABR's scoring code and task structure, enabling direct cross-benchmark comparison: does a model's attention profile change when general-knowledge distractors are replaced with biosafety-specific misinformation?

### Results, Insights, and Conclusions

| Model | Composite |
|-------|-----------|
| Gemini 3.1 Flash-Lite Preview | 67% |
| Claude Haiku 4.5 | 61% |
| Gemma 3 27B | 56% |
| Gemma 3 12B | 55% |
| Gemini 2.5 Flash | 55% |
| Gemma 3 4B | 51% |
| Gemma 3 1B | 45% |

Results across seven models reveal a 22-point spread (45–67% composite), confirming that Bio-SABR provides meaningful discriminatory power. Gemini 3.1 Flash-Lite Preview leads at 67%, followed by Claude Haiku 4.5 at 61% — notably, the strongest performers are not the largest models, suggesting that biosafety attention may depend more on training methodology than raw scale. The Gemma family shows a clear scaling pattern (1B: 45% → 4B: 51% → 12B: 55% → 27B: 56%), though gains diminish sharply above 12B parameters.

**Distractor robustness remains the hardest task across all models.** The distractor degradation curve is sharply non-linear: models that answer correctly under clean conditions collapse when presented with domain-specific biosafety misinformation. This steep decline — far steeper than SABR's general-knowledge distractor curves — confirms that biosafety-specific misinformation creates uniquely powerful interference. A model that knows the correct BSL classification in isolation can still be misled by plausible-sounding but incorrect biosafety text.

**Key insights:** (1) Bio-SABR composite scores (45–67%) are substantially lower than SABR general-knowledge scores for comparable models, confirming that biosafety-domain attention is harder than general attention. (2) Source-selective QA is the strongest sub-task across models, suggesting models can follow designated institutional sources when explicitly instructed — an encouraging finding for biosafety applications. (3) Spotlight F1 reveals moderate claim extraction ability, with room for improvement in distinguishing target claims from near-miss distractors in dense biosafety documents. (4) The gap between the top and bottom model (22 points) is substantial, indicating that model selection matters for biosafety-critical applications.

### Organizational Affiliations

Independent research (Shep Scientific).

### TL;DR:

**Evidence that the dataset and task are both high quality**

Bio-SABR covers 280 evaluations across 130 unique items in five biosafety/biosecurity domains. Three structurally distinct tasks prevent gaming via a single strategy. Task 1's repeated-measures design (50 items x 4 conditions) isolates attention from knowledge: a biosafety question answered correctly without distractors but failed with domain-specific misinformation is unambiguous evidence of attentional deficit. All biosafety content is factually grounded (real pathogens, real regulations, real institutional sources). Tasks 1–2 use deterministic exact-match scoring; Task 3 uses token-overlap F1. Each evaluation runs in an isolated chat context.

**Evidence that the writeup is high quality**

This writeup covers all required sections: problem statement with domain-specific motivation, task construction, dataset provenance, technical details, and references. All artifacts are linked. The benchmark is grounded in both cognitive science attention paradigms and biosafety/biosecurity literature. It extends SABR to a high-stakes domain, enabling cross-benchmark comparison of attention profiles.

**Evidence that the benchmark has sufficient discriminatory power**

Bio-SABR produces strong discriminatory signal across seven models: composite scores range from 45% (Gemma 3 1B) to 67% (Gemini 3.1 Flash-Lite Preview), a 22-point spread. The Gemma scaling series (1B→4B→12B→27B) shows monotonic improvement (45→51→55→56%), confirming the benchmark tracks meaningful capability differences. Scores are substantially lower than SABR general-knowledge equivalents for comparable models, confirming domain-specific attention weakness. The three sub-tasks (distractor robustness, source-selective QA, spotlight F1) each contribute distinct diagnostic signal, preventing any single-strategy gaming.

### References & Citations

1. Burnell, R., et al. (2026). ["Measuring Progress Toward AGI: A Cognitive Framework."](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) Google DeepMind.
2. De Haro, G. (2024). ["Biosecurity Risk Assessment at the Intersection of AI and Synthetic Biology."](https://doi.org/10.1089/apb.2023.0031) *Applied Biosafety.*
3. Mouton, C., et al. (2024). ["The Operational Risks of AI in Large-Scale Biological Attacks: Results of a Red-Team Study."](https://www.rand.org/pubs/research_reports/RRA2977-2.html) RAND Corporation.
4. Anthropic. (2025). ["Biorisk Evaluation."](https://red.anthropic.com/2025/biorisk/) Anthropic Red Teaming Disclosures.
5. Stroop, J.R. (1935). ["Studies of interference in serial verbal reactions."](https://doi.org/10.1037/h0054651) *Journal of Experimental Psychology*, 18(6), 643–662.
6. Cherry, E.C. (1953). ["Some experiments on the recognition of speech, with one and with two ears."](https://doi.org/10.1121/1.1907229) *Journal of the Acoustical Society of America*, 25(5), 975–979.
7. Treisman, A.M. & Gelade, G. (1980). ["A feature-integration theory of attention."](https://doi.org/10.1016/0010-0285(80)90005-5) *Cognitive Psychology*, 12(1), 97–136.
8. Shi, F., et al. (2023). ["Large Language Models Can Be Easily Distracted by Irrelevant Context."](https://arxiv.org/abs/2302.00093) *ICML 2023.*
9. Liu, N., et al. (2023). ["Lost in the Middle: How Language Models Use Long Contexts."](https://arxiv.org/abs/2307.03172) *TACL 2023.*
10. [Kaggle Benchmarks SDK.](https://github.com/Kaggle/kaggle-benchmarks)
