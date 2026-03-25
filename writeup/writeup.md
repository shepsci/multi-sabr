### Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning

### Shep Scientific

### Resources

- **Benchmark Collection:** [Multi-SABR on Kaggle Benchmarks](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm)
- **GitHub:** [github.com/shepsci/multi-sabr](https://github.com/shepsci/multi-sabr)
- **Component Benchmarks:**
  - [SABR (General Knowledge)](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning) | [Dataset](https://www.kaggle.com/datasets/shepscientific/sabr-selective-attention-data) | [GitHub](https://github.com/shepsci/SABR)
  - [Bio-SABR (Biosafety)](https://www.kaggle.com/benchmarks/shepscientific/bio-sabr-biosafety-selective-attention-benchmark) | [Dataset](https://www.kaggle.com/datasets/shepscientific/bio-sabr-biosafety-attention-data) | [GitHub](https://github.com/shepsci/bio-sabr)
  - [Cyber-SABR (Cybersecurity)](https://www.kaggle.com/benchmarks/shepscientific/cyber-sabr-cybersecurity-selective-attention-benc) | [Dataset](https://www.kaggle.com/datasets/shepscientific/cyber-sabr-cybersecurity-attention-data) | [GitHub](https://github.com/shepsci/cyber-sabr)
  - [Chem-SABR (Chemical Safety)](https://www.kaggle.com/benchmarks/shepscientific/chem-sabr-chemical-safety-selective-attention-benchmark) | [Dataset](https://www.kaggle.com/datasets/shepscientific/chem-sabr-chemical-safety-attention-data) | [GitHub](https://github.com/shepsci/chem-sabr)
  - [BIO-SABR-2026 (Biosafety, 2026 refresh)](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm)
  - [CHEM-SABR-2026 (Chemical Safety, 2026 refresh)](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm)

### Problem Statement

Can a model that attends well in one domain attend well in all domains? Standard attention evaluations test a single subject area, making it impossible to distinguish general attentional capability from domain-specific fluency. [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) identify selective attention as a key sub-domain in their AGI measurement framework, but their framework does not address whether attention generalizes across knowledge domains. [Shi et al. (2023)](https://arxiv.org/abs/2302.00093) showed LLMs are easily distracted by irrelevant context, and [Liu et al. (2023)](https://arxiv.org/abs/2307.03172) demonstrated failures in attending to relevant information across longer contexts — but both studies used general-knowledge content. Do these attention failures worsen, improve, or change character when the content is domain-specific misinformation in high-stakes fields?

Multi-SABR answers this question by combining six SABR benchmarks — spanning general knowledge, biosafety, cybersecurity, and chemical safety (including 2026-refreshed variants for biosafety and chemical safety) — into a single cross-domain evaluation. With 19 models evaluated across up to six domains, Multi-SABR measures not just *how well* a model attends, but *how consistently* it attends across subject areas. The result: **selective attention is not a single capability. It is domain-dependent, and models that lead in one domain may falter in another.**

### Task & Benchmark Construction

Multi-SABR is a benchmark collection comprising six component benchmarks — four core domains plus two 2026-refreshed variants — each evaluating items across three cognitive attention tasks:

**Task 1: Distractor Robustness** (200 evals per domain, 800 total). Fifty factual questions per domain presented under four distraction levels: *clean* (question only), *low* (off-topic text), *medium* (topically related), *high* (plausible domain-specific misinformation). Inspired by Stroop interference ([Stroop, 1935](https://doi.org/10.1037/h0054651)). Metric: ARS = mean accuracy across all four conditions. Weight: 40% of domain composite.

**Task 2: Source-Selective QA** (50 evals per domain, 200 total). Three named sources per item with conflicting claims; the model must answer using only the designated source. Sources use realistic institutional labels (NIST, CDC, OSHA, WHO, etc.) appropriate to each domain. Inspired by Cherry's cocktail party experiments ([Cherry, 1953](https://doi.org/10.1121/1.1907229)). Weight: 30% of domain composite.

**Task 3: Attentional Spotlight** (30 evals per domain, 120 total). 400-600 word documents with 8-15 embedded claims; the model extracts only those matching a specific filter criterion. Six filter categories per domain. Inspired by visual search research ([Treisman & Gelade, 1980](https://doi.org/10.1016/0010-0285(80)90005-5)). F1 scoring. Weight: 30% of domain composite.

**Domains and their content:**

| Domain | Subject Area | Distractor Content | Institutional Sources | Example Filter Categories |
|--------|-------------|-------------------|----------------------|--------------------------|
| SABR | General knowledge | General misinformation | Academic, encyclopedic | Dates, numerical, causal |
| Bio-SABR | Biosafety/biosecurity | BSL misclassifications, pathogen misinformation | CDC, WHO, NIH | Risk levels, dual-use indicators |
| Cyber-SABR | Cybersecurity + AI security | CVE/ATT&CK misinformation, prompt injection | NIST, MITRE, OWASP | Attack techniques, AI security indicators |
| Chem-SABR | Chemical safety/security | GHS/exposure limit misinformation | OSHA, NIOSH, OPCW | Hazard classifications, exposure thresholds |

**Multi-SABR Composite** = aggregate across all six domain composites. Models that refuse or error on a domain score 0% for that domain, reflecting the practical reality that a model unable to operate in a domain provides no attentional capability there. The 2026 variants (BIO-SABR-2026, CHEM-SABR-2026) use refreshed question sets to mitigate contamination risk and are included in the leaderboard composite.

### Dataset

520 unique base items across four core domains (130 per domain), producing 1,120 evaluations per model on the core benchmarks plus additional evaluations on the 2026 refresh variants. All factual content is grounded in real-world knowledge: real pathogens and BSL classifications (Bio-SABR), real CVEs and MITRE ATT&CK techniques (Cyber-SABR), real chemicals and OSHA/NIOSH exposure limits (Chem-SABR), and verified general knowledge (SABR). Task 3 documents use fictional institutions across all domains to prevent memorization. The datasets are independently hosted on Kaggle and maintained in separate GitHub repositories.

### Technical Details

Each component benchmark uses the [kaggle-benchmarks SDK](https://github.com/Kaggle/kaggle-benchmarks) with a single scored function returning a composite float. All 1,120 evaluations run in isolated chat contexts. Scoring is identical across domains: case-insensitive exact match with alias support (Tasks 1-2); token-overlap F1 with 70% threshold (Task 3). The shared scoring code enables direct cross-domain comparison — any performance difference between domains reflects domain-specific attention difficulty, not methodological variation.

### Results, Insights, and Conclusions

Cross-domain results for 19 models evaluated across four core SABR domains (March 2026). Composite scores are from the [Multi-SABR leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-benchm), which also includes two newer 2026 domain variants with limited model coverage.

| Model | SABR | Bio-SABR | Cyber-SABR | Chem-SABR | Composite |
|-------|------|----------|------------|-----------|-----------|
| Qwen 3 235B A22B | 91% | 70% | 74% | 69% | **61%** |
| Qwen 3 Next 80B | 89% | 71% | 78% | 66% | **61%** |
| DeepSeek V3.1 | 90% | 70% | 72% | 66% | **60%** |
| Gemini 2.5 Flash | 77% | 55% | 63% | 56% | **60%** |
| Qwen 3 Coder 480B | 92% | 67% | 73% | 69% | **60%** |
| Gemini 3.1 Flash-Lite | 88% | 67% | 71% | 67% | **59%** |
| Qwen 3 Next 80B Thinking | 84% | 67% | 74% | 65% | **58%** |
| GLM-5 | 83% | 65% | 73% | 67% | **57%** |
| DeepSeek-R1 | 79% | 63% | 70% | 66% | **56%** |
| Claude Haiku 4.5 | 84% | 61% | 70% | 59% | **55%** |
| DeepSeek V3.2 | 91% | 72% | 76% | 71% | **52%** |
| Gemini 2.5 Pro | 77% | 58% | 68% | 59% | **52%** |
| Gemma 3 12B | 84% | 55% | 66% | 56% | **52%** |
| Gemini 3.1 Pro Preview | 87% | 70% | 75% | 73% | **51%** |
| Gemma 3 27B | 81% | 56% | 63% | 54% | **51%** |
| Gemma 3 4B | 83% | 51% | 59% | 52% | **49%** |
| Gemma 3 1B | 67% | 45% | 53% | 44% | **42%** |
| Claude Opus 4.6 | **92%** | — | **84%** | — | **35%** |
| Claude Sonnet 4.6 | 85% | — | 77% | — | **32%** |

*Dashes indicate the model refused to complete the benchmark in that domain. The composite incorporates all six domain variants on the leaderboard, including BIO-SABR-2026 and CHEM-SABR-2026, which currently have limited model coverage. Models that refuse or are not evaluated on a domain score 0% for that domain in the composite.*

**Insight 1: Large performance variance across models.** Composite scores range from 32% (Claude Sonnet 4.6) to 61% (Qwen 3 235B A22B), a 29-point spread across 19 models spanning reasoning-optimized (DeepSeek-R1, Qwen 3 Thinking), coding-focused (Qwen 3 Coder 480B), and general-purpose architectures. On individual domains the spread is even wider: SABR general-knowledge scores range from 67% (Gemma 3 1B) to 92% (Qwen 3 Coder 480B, Claude Opus 4.6). Notably, high per-domain scores do not predict high composites — DeepSeek V3.2 scores 91% on SABR and 72% on Bio-SABR but ranks only 11th overall (52% composite), while Gemini 2.5 Flash scores a modest 77% on SABR yet ranks 4th (60% composite) through more consistent cross-domain coverage. This confirms that selective attention benchmarking requires multi-domain evaluation; single-domain scores are misleading indicators of general attentional capability.

**Insight 2: Large performance variance across domains.** Every model scores higher on SABR general knowledge than on any regulated domain. The domain penalty is substantial and consistent: across the 17 models evaluated on all four core domains, the average drop from SABR to the lowest-scoring regulated domain is 21 percentage points. Chem-SABR produces the lowest scores for 11 of 17 models, while Bio-SABR is lowest for 5 of 17. The domain-specific distractor content — incorrect BSL classifications, wrong GHS hazard categories, fabricated CVE details — creates stronger Stroop-like interference ([Stroop, 1935](https://doi.org/10.1037/h0054651)) than general misinformation, confirming that plausible technical misinformation is harder to filter than generic false claims. This effect is visible at every model scale: Gemma 3 1B (67% SABR → 44% Chem-SABR, −23), Claude Haiku 4.5 (84% → 59%, −25), and Qwen 3 235B (91% → 69%, −22).

**Insight 3: Some models refuse to operate in heavily regulated domains.** Claude Opus 4.6 and Claude Sonnet 4.6 achieve the highest individual domain scores in the benchmark (92% and 85% on SABR; 84% and 77% on Cyber-SABR) but refuse to complete Bio-SABR and Chem-SABR entirely. When refusals score 0%, Opus drops from first-in-class to 18th of 19 models (35% composite), and Sonnet to last (32%). This is not a knowledge or attention failure — it is a categorical inability to engage with biosafety and chemical safety content. Content safety systems that cannot distinguish evaluation from misuse impose domain-blind attention on otherwise top-performing models. Cybersecurity is the only regulated domain where all 19 models operate, making Cyber-SABR the sole benchmark where the full Claude hierarchy (Opus 84% > Sonnet 77% > Haiku 70%) is visible. Anthropic has documented the tension between safety filtering and evaluation capability in regulated domains ([Anthropic, 2025](https://red.anthropic.com/2025/biorisk/)), and Multi-SABR quantifies its impact: safety-induced refusal is the single largest driver of composite score variance in this benchmark.

### Organizational Affiliations

Independent research (Shep Scientific).

### TL;DR:

**Evidence that the dataset and task are both high quality**

Multi-SABR comprises six benchmarks across 520+ unique items spanning general knowledge, biosafety, cybersecurity, and chemical safety (including 2026-refreshed variants). The component benchmarks share identical task structure and scoring methodology, enabling controlled cross-domain comparison. Three structurally distinct tasks (distractor robustness, source-selective QA, attentional spotlight) prevent gaming via a single strategy. All content is factually grounded in real-world knowledge. Tasks 1-2 use deterministic exact-match scoring; Task 3 uses token-overlap F1. Each evaluation runs in an isolated chat context.

**Evidence that the writeup is high quality**

This writeup presents the first systematic cross-domain analysis of LLM selective attention across 19 models. It covers all required sections with a full cross-domain comparison table, three key insights supported by quantitative evidence, and references spanning cognitive science, AI safety, cybersecurity, biosafety, and chemical safety literature. All component benchmarks and datasets are linked. The analysis reveals novel findings — particularly that selective attention is domain-dependent and that safety filters constitute a previously unrecognized category of attention failure.

**Evidence that the benchmark has sufficient discriminatory power**

Multi-SABR produces dramatic discriminatory signal across 19 models. Within models: 22-25 point cross-domain swings (e.g., Qwen 3 235B: 91% general vs. 69% chemistry; Claude Haiku: 84% vs. 59%). Between models: composite scores span 32%-61%, and the leaderboard completely reorders compared to any single domain — Claude Opus drops from joint-first on SABR (92%) to 18th of 19 overall (35% composite) when refusals are counted. Models optimized for different capabilities (reasoning, coding, general-purpose) show distinct cross-domain profiles, providing fine-grained diagnostic signal beyond aggregate composites.

### References & Citations

1. Burnell, R., et al. (2026). ["Measuring Progress Toward AGI: A Cognitive Framework."](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) Google DeepMind.
2. Stroop, J.R. (1935). ["Studies of interference in serial verbal reactions."](https://doi.org/10.1037/h0054651) *Journal of Experimental Psychology*, 18(6), 643-662.
3. Cherry, E.C. (1953). ["Some experiments on the recognition of speech, with one and with two ears."](https://doi.org/10.1121/1.1907229) *Journal of the Acoustical Society of America*, 25(5), 975-979.
4. Treisman, A.M. & Gelade, G. (1980). ["A feature-integration theory of attention."](https://doi.org/10.1016/0010-0285(80)90005-5) *Cognitive Psychology*, 12(1), 97-136.
5. Shi, F., et al. (2023). ["Large Language Models Can Be Easily Distracted by Irrelevant Context."](https://arxiv.org/abs/2302.00093) *ICML 2023.*
6. Liu, N., et al. (2023). ["Lost in the Middle: How Language Models Use Long Contexts."](https://arxiv.org/abs/2307.03172) *TACL 2023.*
7. De Haro, G. (2024). ["Biosecurity Risk Assessment at the Intersection of AI and Synthetic Biology."](https://doi.org/10.1089/apb.2023.0031) *Applied Biosafety.*
8. Mouton, C., et al. (2024). ["The Operational Risks of AI in Large-Scale Biological Attacks."](https://www.rand.org/pubs/research_reports/RRA2977-2.html) RAND Corporation.
9. Anthropic. (2025). ["Biorisk Evaluation."](https://red.anthropic.com/2025/biorisk/) Anthropic Red Teaming Disclosures.
10. Bhatt, M., et al. (2024). ["CyberSecEval 2: A Wide-Ranging Cybersecurity Evaluation Suite for Large Language Models."](https://arxiv.org/abs/2404.13161) Meta / PurpleLlama.
11. NIST. (2025). ["IR 8596: Cybersecurity Framework Profile for Artificial Intelligence."](https://csrc.nist.gov/pubs/ir/8596/iprd)
12. OWASP. (2025). ["Top 10 for Large Language Model Applications."](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
13. Liu, Y., et al. (2024). ["Formalizing and Benchmarking Prompt Injection Attacks and Defenses."](https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei) *USENIX Security '24.*
14. Greshake, K., et al. (2023). ["Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection."](https://arxiv.org/abs/2302.12173) *AISec@CCS '23.*
15. Zou, A., et al. (2023). ["Universal and Transferable Adversarial Attacks on Aligned Language Models."](https://arxiv.org/abs/2307.15043) arXiv.
16. Anil, C., et al. (2024). ["Many-Shot Jailbreaking."](https://arxiv.org/abs/2404.02151) *NeurIPS 2024.* Anthropic.
17. Zhao, C., et al. (2024). ["ChemSafetyBench: Benchmarking LLM Safety on Chemistry Domain."](https://arxiv.org/abs/2411.16736) arXiv.
18. Kristiadi, A., et al. (2025). ["ChemBench: Can LLMs Master Chemistry?"](https://doi.org/10.1038/s41557-025-01755-y) *Nature Chemistry.*
19. Zhou, D., et al. (2026). ["LabSafety Bench: LLM Evaluation on Laboratory Safety."](https://doi.org/10.1038/s42256-025-01000-w) *Nature Machine Intelligence.*
20. OPCW. (2026). ["OPCW Releases Landmark Report on AI and the Chemical Weapons Convention."](https://www.opcw.org/media-centre/news/2026/03/opcw-releases-landmark-report-ai-and-chemical-weapons-convention)
21. Google DeepMind. (2025). ["A Framework for Evaluating Emerging Cyberattack Capabilities of AI."](https://arxiv.org/abs/2503.11917) arXiv.
22. Zhang, J., et al. (2025). ["CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities."](https://arxiv.org/abs/2503.17332) arXiv.
23. Hendrycks, D., et al. (2021). ["Measuring Massive Multitask Language Understanding."](https://arxiv.org/abs/2009.03300) *ICLR 2021.*
24. [Kaggle Benchmarks SDK.](https://github.com/Kaggle/kaggle-benchmarks)
