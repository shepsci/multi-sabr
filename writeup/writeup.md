### Multi-SABR: Cross-Domain Selective Attention Benchmark for Reasoning

### Shep Scientific

### Resources

- **Benchmark:** [Multi-SABR on Kaggle Benchmarks](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench)
- **GitHub:** [github.com/shepsci/multi-sabr](https://github.com/shepsci/multi-sabr)
- **Tasks and Datasets:**
  - SABR-2026 (General Knowledge, v5) | [Dataset](https://www.kaggle.com/datasets/shepscientific/sabr-selective-attention-data) | [Code](https://github.com/shepsci/multi-sabr/tree/main/benchmarks/sabr)
  - BIO-SABR-2026 (Biosafety, v3) | [Dataset](https://www.kaggle.com/datasets/shepscientific/bio-sabr-biosafety-attention-data) | [Code](https://github.com/shepsci/multi-sabr/tree/main/benchmarks/bio-sabr)
  - CYBER-SABR-2026 (Cybersecurity, v3) | [Dataset](https://www.kaggle.com/datasets/shepscientific/cyber-sabr-cybersecurity-attention-data) | [Code](https://github.com/shepsci/multi-sabr/tree/main/benchmarks/cyber-sabr)
  - CHEM-SABR-2026 (Chemical Safety, v4) | [Dataset](https://www.kaggle.com/datasets/shepscientific/chem-sabr-chemical-safety-attention-data) | [Code](https://github.com/shepsci/multi-sabr/tree/main/benchmarks/chem-sabr)

### Problem Statement

Can a model that attends well in one domain attend well in all domains? Standard attention evaluations test a single subject area, making it impossible to distinguish general attentional capability from domain-specific fluency. [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) identify selective attention as a key sub-domain in their AGI measurement framework but do not address whether it generalizes across knowledge domains. [Shi et al. (2023)](https://arxiv.org/abs/2302.00093) showed LLMs are easily distracted by irrelevant context, and [Liu et al. (2023)](https://arxiv.org/abs/2307.03172) demonstrated long-context attention failures — but both used general-knowledge content. Do these failures worsen when content is domain-specific misinformation in high-stakes fields?

Multi-SABR answers this by combining four benchmark tasks — general knowledge (SABR-2026), biosafety (BIO-SABR-2026), cybersecurity (CYBER-SABR-2026), and chemical safety (CHEM-SABR-2026) — into a single cross-domain evaluation. 19 models were evaluated across all four domains, totaling 1,120 evaluations per model (520 unique items across 4 domains × 280 per domain). The result: **selective attention is not a single capability. It is domain-dependent, and models that lead in one domain may falter in another.**

### Task & Benchmark Construction

Each domain is evaluated across three cognitive attention sub-tasks (280 evaluations per domain, 1,120 per model total across the four domains):

**Task 1: Distractor Robustness** (50 questions × 4 conditions = 200 evals/domain, 800 total). Factual questions presented under four distraction levels: *clean* (question only), *low* (off-topic text), *medium* (topically related), *high* (plausible domain-specific misinformation). Inspired by Stroop interference ([Stroop, 1935](https://doi.org/10.1037/h0054651)). Metric: ARS = mean accuracy across all four conditions. Weight: 40%.

**Task 2: Source-Selective QA** (50 evals/domain, 200 total). Three named sources per item with conflicting claims; the model must answer using only the designated source. Institutional labels (NIST, CDC, OSHA, WHO, etc.) vary by domain. Inspired by Cherry's cocktail party experiments ([Cherry, 1953](https://doi.org/10.1121/1.1907229)). Weight: 30%.

**Task 3: Attentional Spotlight** (30 evals/domain, 120 total). 400–600 word documents with 8–15 embedded claims; the model extracts only those matching a specific filter criterion (six filter categories per domain). Inspired by visual search research ([Treisman & Gelade, 1980](https://doi.org/10.1016/0010-0285(80)90005-5)). F1 scoring. Weight: 30%.

**Domain content:**

| Domain | Subject Area | Distractor Content | Sources | Filter Categories |
|--------|-------------|-------------------|---------|------------------|
| SABR-2026 | General knowledge | General misinformation | Academic, encyclopedic | Dates, numerical, causal |
| BIO-SABR-2026 | Biosafety/biosecurity | BSL misclassifications, pathogen misinformation | CDC, WHO, NIH | Risk levels, dual-use indicators |
| CYBER-SABR-2026 | Cybersecurity + AI security | CVE/ATT&CK misinformation, prompt injection | NIST, MITRE, OWASP | Attack techniques, AI security indicators |
| CHEM-SABR-2026 | Chemical safety/security | GHS/exposure limit misinformation | OSHA, NIOSH, OPCW | Hazard classifications, exposure thresholds |

**Multi-SABR Composite** = mean across all four domain composites. Models that refuse or error on a domain score 0% for it. All tasks use 2026-refreshed question sets to mitigate contamination risk.

### Dataset

520 unique items (130 per domain) grounded in real-world knowledge: real pathogens and BSL classifications (BIO-SABR-2026, [De Haro, 2024](https://doi.org/10.1089/apb.2023.0031); [Mouton et al., 2024](https://www.rand.org/pubs/research_reports/RRA2977-2.html); [Anthropic, 2025](https://red.anthropic.com/2025/biorisk/); [Zhou et al., 2026](https://doi.org/10.1038/s42256-025-01152-1)); real CVEs, ATT&CK techniques, and prompt injection scenarios (CYBER-SABR-2026, [Bhatt et al., 2024](https://arxiv.org/abs/2404.13161); [NIST, 2025](https://csrc.nist.gov/pubs/ir/8596/iprd); [OWASP, 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/); [Greshake et al., 2023](https://arxiv.org/abs/2302.12173); [Liu et al., 2024](https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei); [Zou et al., 2023](https://arxiv.org/abs/2307.15043); [Anil et al., 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ea456e232efb72d261715e33ce25f208-Abstract-Conference.html); [Google DeepMind, 2025](https://arxiv.org/abs/2503.11917); [Zhu et al., 2025](https://arxiv.org/abs/2503.17332)); real chemicals and OSHA/NIOSH/GHS hazard data (CHEM-SABR-2026, [Zhao et al., 2024](https://arxiv.org/abs/2411.16736); [Mirza et al., 2025](https://doi.org/10.1038/s41557-025-01815-x); [OPCW, 2026](https://www.opcw.org/media-centre/news/2026/03/opcw-releases-landmark-report-ai-and-chemical-weapons-convention)); and verified general knowledge (SABR-2026, [Hendrycks et al., 2021](https://arxiv.org/abs/2009.03300)). Task 3 documents use fictional institutions to prevent memorization. Datasets are hosted on Kaggle (see Resources above) and source code is maintained in the [multi-sabr monorepo](https://github.com/shepsci/multi-sabr).

### Technical Details

Each task uses the [kaggle-benchmarks SDK](https://github.com/Kaggle/kaggle-benchmarks) with a single scored function returning a composite float. All evaluations run in isolated chat contexts. Scoring is identical across domains: case-insensitive exact match with alias support (Tasks 1–2); token-overlap F1 with 70% threshold (Task 3). Shared scoring code ensures any performance difference between domains reflects domain-specific attention difficulty, not methodological variation.

### Results, Insights, and Conclusions

19 models × 1,120 evaluations each = 21,280 total evaluations across all four SABR-2026 tasks (March 2026). Composite scores from the [Multi-SABR leaderboard](https://www.kaggle.com/benchmarks/shepscientific/multi-sabr-cross-domain-selective-attention-bench).

| Model | SABR-2026 | BIO-SABR-2026 | CYBER-SABR-2026 | CHEM-SABR-2026 | Composite |
|-------|-----------|---------------|-----------------|----------------|-----------|
| Claude Opus 4.6 | **92%** | 59% | **84%** | **72%** | **77%** |
| DeepSeek V3.2 | 90% | 71% | 77% | 69% | **77%** |
| Gemini 3.1 Pro Preview | 88% | 71% | 75% | 71% | **76%** |
| Qwen 3 235B A22B Instruct | 91% | 69% | 74% | 69% | **76%** |
| Qwen 3 Coder 480B | **92%** | 67% | 74% | 70% | **76%** |
| Qwen 3 Next 80B Instruct | 90% | **72%** | 78% | 65% | **76%** |
| DeepSeek V3.1 | 91% | 69% | 73% | 67% | **75%** |
| Gemini 3.1 Flash-Lite Preview | 88% | 65% | 69% | 68% | **73%** |
| Qwen 3 Next 80B Thinking | 85% | 69% | 75% | 62% | **73%** |
| GLM-5 | 82% | 64% | 75% | 67% | **72%** |
| DeepSeek-R1 | 79% | 62% | 71% | 66% | **69%** |
| Claude Haiku 4.5 | 86% | 60% | 69% | 58% | **68%** |
| Claude Sonnet 4.6 | 85% | 50% | 77% | 60% | **68%** |
| Gemini 2.5 Flash | 79% | 58% | 66% | 59% | **65%** |
| Gemini 2.5 Pro | 77% | 56% | 67% | 59% | **65%** |
| Gemma 3 12B | 84% | 55% | 66% | 56% | **65%** |
| Gemma 3 27B | 82% | 57% | 62% | 54% | **64%** |
| Gemma 3 4B | 83% | 51% | 60% | 52% | **61%** |
| Gemma 3 1B | 67% | 43% | 53% | 44% | **52%** |

**Insight 1: Single-domain scores do not predict cross-domain rank.** Composite scores span 52%–77% (25 points) across 19 models. The Qwen 3 family places four models in the top six (all at 76%). Per-domain spreads are wider: SABR-2026 ranges from 67% to 92%, BIO-SABR-2026 from 43% to 72%. Yet domain leadership does not translate to composite leadership — Qwen 3 Next 80B Instruct leads BIO-SABR-2026 (72%) but ties third overall, while Claude Opus 4.6 leads SABR-2026 and CYBER-SABR-2026 but scores only 59% on BIO-SABR-2026. Multi-domain evaluation is required; single-domain scores are misleading indicators of attentional capability.

**Insight 2: Every model takes a substantial domain penalty on regulated content.** The average drop from SABR-2026 to each model's lowest regulated domain score is approximately 24 percentage points (range: 17–35 pp). BIO-SABR-2026 and CHEM-SABR-2026 are the hardest domains for roughly equal numbers of models, suggesting biosafety and chemical safety misinformation create comparable interference. Domain-specific distractors — incorrect BSL classifications, fabricated GHS hazard categories, false CVE details — produce stronger Stroop-like interference ([Stroop, 1935](https://doi.org/10.1037/h0054651)) than general misinformation: the penalty is visible at every scale, from Gemma 3 1B (−23 pp) to Claude Opus 4.6 (−33 pp).

**Insight 3: In this dataset, a thinking model underperforms its instruction-tuned counterpart on all four domains.** Qwen 3 Next 80B Thinking (73%) scores below Qwen 3 Next 80B Instruct (76%) across every domain: BIO (69% vs. 72%), CHEM (62% vs. 65%), SABR (85% vs. 90%), CYBER (75% vs. 78%). This is consistent with work showing that chain-of-thought provides strong gains on math and symbolic tasks but negligible or negative gains on retrieval-style tasks ([Sprague et al., 2025](https://arxiv.org/abs/2409.12183); [Stechly et al., 2024](https://arxiv.org/abs/2410.21333)). Selective attention under interference — filtering distractors, following source attribution, extracting matching claims — may be more analogous to retrieval than multi-step inference. However, this finding rests on a single model pair and should be treated as a hypothesis to test across additional families.

### Organizational Affiliations

Independent research (Shep Scientific).

### TL;DR

**Scale.** Four benchmark tasks, 520 unique items (130/domain), 1,120 evaluations per model (280/domain), 19 models, 21,280 total evaluations. Datasets hosted on Kaggle; identical task structure and deterministic scoring across all domains.

**Models.** 19 models from seven families (Claude, Gemini, Gemma, Qwen, DeepSeek, GLM, DeepSeek-R1), spanning reasoning-optimized, coding-focused, and general-purpose architectures, 1B–480B parameters.

**Findings.** Composite scores range from 52% to 77% (25-point spread). Every model takes an average ~24 pp penalty moving from general knowledge to its worst regulated domain. Cross-domain rank diverges substantially from single-domain rank. In the one available thinking/instruct pair, the thinking model underperforms on all four domains.

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
11. NIST. (2025). ["IR 8596: Cybersecurity Framework Profile for Artificial Intelligence (preliminary draft)."](https://csrc.nist.gov/pubs/ir/8596/iprd)
12. OWASP. (2025). ["Top 10 for Large Language Model Applications."](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
13. Liu, Y., et al. (2024). ["Formalizing and Benchmarking Prompt Injection Attacks and Defenses."](https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei) *USENIX Security '24.*
14. Greshake, K., et al. (2023). ["Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection."](https://arxiv.org/abs/2302.12173) *AISec@CCS '23.*
15. Zou, A., et al. (2023). ["Universal and Transferable Adversarial Attacks on Aligned Language Models."](https://arxiv.org/abs/2307.15043) arXiv.
16. Anil, C., et al. (2024). ["Many-Shot Jailbreaking."](https://proceedings.neurips.cc/paper_files/paper/2024/hash/ea456e232efb72d261715e33ce25f208-Abstract-Conference.html) *NeurIPS 2024.* Anthropic.
17. Zhao, H., et al. (2024). ["ChemSafetyBench: Benchmarking LLM Safety on Chemistry Domain."](https://arxiv.org/abs/2411.16736) arXiv.
18. Mirza, A., et al. (2025). ["A framework for evaluating the chemical knowledge and reasoning abilities of large language models against the expertise of chemists."](https://doi.org/10.1038/s41557-025-01815-x) *Nature Chemistry*, 17, 1027-1034.
19. Zhou, Y., et al. (2026). ["Benchmarking large language models on safety risks in scientific laboratories."](https://doi.org/10.1038/s42256-025-01152-1) *Nature Machine Intelligence*, 8, 20-31.
20. OPCW. (2026). ["OPCW Releases Landmark Report on AI and the Chemical Weapons Convention."](https://www.opcw.org/media-centre/news/2026/03/opcw-releases-landmark-report-ai-and-chemical-weapons-convention)
21. Google DeepMind. (2025). ["A Framework for Evaluating Emerging Cyberattack Capabilities of AI."](https://arxiv.org/abs/2503.11917) arXiv.
22. Zhu, Y., et al. (2025). ["CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities."](https://arxiv.org/abs/2503.17332) arXiv.
23. Hendrycks, D., et al. (2021). ["Measuring Massive Multitask Language Understanding."](https://arxiv.org/abs/2009.03300) *ICLR 2021.*
24. [Kaggle Benchmarks SDK.](https://github.com/Kaggle/kaggle-benchmarks)
25. Sprague, Z., et al. (2025). ["To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning."](https://arxiv.org/abs/2409.12183) *ICLR 2025.*
26. Stechly, M., et al. (2024). ["Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse."](https://arxiv.org/abs/2410.21333) arXiv.
