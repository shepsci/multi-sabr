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

### Problem Statement

Can a model that attends well in one domain attend well in all domains? Standard attention evaluations test a single subject area, making it impossible to distinguish general attentional capability from domain-specific fluency. [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) identify selective attention as a key sub-domain in their AGI measurement framework, but their framework does not address whether attention generalizes across knowledge domains. [Shi et al. (2023)](https://arxiv.org/abs/2302.00093) showed LLMs are easily distracted by irrelevant context, and [Liu et al. (2023)](https://arxiv.org/abs/2307.03172) demonstrated failures in attending to relevant information across longer contexts — but both studies used general-knowledge content. Do these attention failures worsen, improve, or change character when the content is domain-specific misinformation in high-stakes fields?

Multi-SABR answers this question by combining four structurally identical SABR benchmarks — spanning general knowledge, biosafety, cybersecurity, and chemical safety — into a single cross-domain evaluation. With 1,120 total evaluations per model across four domains, Multi-SABR measures not just *how well* a model attends, but *how consistently* it attends across subject areas. The result: **selective attention is not a single capability. It is domain-dependent, and models that lead in one domain may falter in another.**

### Task & Benchmark Construction

Multi-SABR is a benchmark collection comprising four structurally identical component benchmarks, each evaluating 280 items across three cognitive attention tasks:

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

**Multi-SABR Composite** = mean of four domain composites, each weighted 25%. Models that refuse or error on a domain score 0% for that domain, reflecting the practical reality that a model unable to operate in a domain provides no attentional capability there.

### Dataset

520 unique base items across four domains (130 per domain), producing 1,120 evaluations per model. All factual content is grounded in real-world knowledge: real pathogens and BSL classifications (Bio-SABR), real CVEs and MITRE ATT&CK techniques (Cyber-SABR), real chemicals and OSHA/NIOSH exposure limits (Chem-SABR), and verified general knowledge (SABR). Task 3 documents use fictional institutions across all domains to prevent memorization. The four datasets are independently hosted on Kaggle and maintained in separate GitHub repositories.

### Technical Details

Each component benchmark uses the [kaggle-benchmarks SDK](https://github.com/Kaggle/kaggle-benchmarks) with a single scored function returning a composite float. All 1,120 evaluations run in isolated chat contexts. Scoring is identical across domains: case-insensitive exact match with alias support (Tasks 1-2); token-overlap F1 with 70% threshold (Task 3). The shared scoring code enables direct cross-domain comparison — any performance difference between domains reflects domain-specific attention difficulty, not methodological variation.

### Results, Insights, and Conclusions

Cross-domain results for models with data across multiple SABR variants:

| Model | SABR (General) | Bio-SABR (Biosafety) | Cyber-SABR (Cybersecurity) | Chem-SABR (Chemistry) | Multi-SABR Composite |
|-------|---------------|---------------------|---------------------------|----------------------|---------------------|
| **Claude Opus 4.6** | **92%** | 0% (refused) | **84%** | 0% (refused) | **44%** |
| **Claude Sonnet 4.6** | 85% | — | 77% | 0% (refused) | — |
| **Claude Haiku 4.5** | 84% | 61% | 70% | 59% | **69%** |
| **Gemini 3.1 Pro Preview** | 87% | — | 75% | — | — |
| **Gemini 3.1 Flash-Lite Preview** | — | 67% | 71% | 67% | — |
| **Gemini 2.5 Flash** | 76% | 55% | 63% | 56% | **63%** |
| **Gemma 3 27B** | 82% | 56% | — | — | — |
| **Gemini 2.5 Pro** | — | — | — | 59% | — |
| **Gemma 3 12B** | — | 55% | — | — | — |
| **Gemma 3 4B** | — | 51% | — | — | — |
| **Gemma 3 1B** | — | 45% | — | — | — |

*Multi-SABR composite shown only for models with results across all four domains. Dashes indicate the model has not been evaluated on that domain.*

**Key Insight 1: Selective attention is domain-dependent, not general.** Claude Haiku 4.5 scores 84% on general knowledge but drops to 59% on chemical safety — a 25-point swing using structurally identical tasks with identical scoring. Gemini 2.5 Flash shows a similar pattern: 76% general, 55% biosafety (21-point drop). These gaps cannot be attributed to task difficulty alone because the tasks are methodologically identical — the only variable is domain content. Models attend differently depending on what they are attending to.

**Key Insight 2: Safety filters create a new category of attention failure.** Claude Opus 4.6 achieves the highest score on any single SABR variant (92% general, 84% cyber) but refuses to complete Bio-SABR and Chem-SABR entirely. When refusals are scored as 0%, Opus drops from first place to a 44% Multi-SABR composite — below Claude Haiku 4.5 (69%) and Gemini 2.5 Flash (63%). This is not a knowledge failure or an attention failure in the traditional sense — it is a categorical inability to engage with certain domains. Content safety systems that cannot distinguish evaluation from misuse effectively impose domain-blind attention on otherwise capable models.

**Key Insight 3: Domain-specific misinformation is harder to resist.** Across all models, Bio-SABR and Chem-SABR scores are 15-25 points lower than SABR general-knowledge scores. The distractor robustness task shows the sharpest effect: domain-specific misinformation (e.g., incorrect BSL classifications, wrong GHS hazard categories) creates stronger interference than general misinformation. This confirms that the Stroop-like interference effect scales with the domain specificity of distractors — plausible-sounding technical misinformation is harder to filter than generic false claims.

**Key Insight 4: Task-level patterns are consistent across domains.** Source-selective QA is the easiest task across all four domains (near-perfect accuracy), confirming that explicit top-down attention instructions ("use only Source B") are robustly followed regardless of domain. Distractor robustness is universally the hardest, with sharp non-linear degradation from clean to medium distraction. Spotlight F1 varies substantially across models (63-84% in SABR, comparable ranges in domain variants). This consistency suggests these three tasks capture genuinely different attentional mechanisms that generalize across content areas.

**Key Insight 5: No single model dominates across all domains.** Gemini 3.1 Flash-Lite Preview shows the most consistent cross-domain performance (67-71% across Bio/Cyber/Chem), while Claude models show the widest variance (0-92%). For applications requiring reliable attention across diverse domains, cross-domain consistency may be more valuable than peak single-domain performance. The Multi-SABR composite rewards this consistency by design.

**Key Insight 6: The cybersecurity domain is uniquely evaluable.** Cyber-SABR produces the broadest model comparison across all SABR variants because cybersecurity content does not trigger content moderation refusals from any tested model. This makes it the only domain where the full Claude model hierarchy (Opus 84% > Sonnet 77% > Haiku 70%) is visible. The monotonic scaling with model capability suggests attention improves with scale when safety filters do not interfere.

### Organizational Affiliations

Independent research (Shep Scientific).

### TL;DR:

**Evidence that the dataset and task are both high quality**

Multi-SABR comprises 1,120 evaluations across 520 unique items spanning four domains: general knowledge, biosafety, cybersecurity, and chemical safety. The four component benchmarks share identical task structure and scoring methodology, enabling controlled cross-domain comparison. Three structurally distinct tasks (distractor robustness, source-selective QA, attentional spotlight) prevent gaming via a single strategy. All content is factually grounded in real-world knowledge. Tasks 1-2 use deterministic exact-match scoring; Task 3 uses token-overlap F1. Each evaluation runs in an isolated chat context.

**Evidence that the writeup is high quality**

This writeup presents the first systematic cross-domain analysis of LLM selective attention. It covers all required sections with cross-domain comparison tables, six key insights supported by quantitative evidence, and references spanning cognitive science, AI safety, cybersecurity, biosafety, and chemical safety literature. All component benchmarks and datasets are linked. The analysis reveals novel findings — particularly that selective attention is domain-dependent and that safety filters constitute a previously unrecognized category of attention failure.

**Evidence that the benchmark has sufficient discriminatory power**

Multi-SABR produces dramatic discriminatory signal. Within models: 25-point cross-domain swings (Claude Haiku: 84% general vs. 59% chemistry). Between models: the Multi-SABR composite completely reorders the leaderboard compared to any single domain — Claude Opus drops from #1 (92% general) to below Haiku and Gemini Flash when refusals are counted. The 0% refusal scoring reveals that peak performance in accessible domains does not predict cross-domain reliability. Per-domain and per-task breakdowns provide fine-grained diagnostic signal beyond the aggregate composite.

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
