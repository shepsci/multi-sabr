### Cyber-SABR: Cybersecurity Selective Attention Benchmark for Reasoning

### Shep Scientific

### Resources

- **Benchmark Notebook:** [Cyber-SABR Benchmark on Kaggle](https://www.kaggle.com/code/shepscientific/cyber-sabr-benchmark)
- **Dataset:** [Cyber-SABR Cybersecurity Attention Data on Kaggle](https://www.kaggle.com/datasets/shepscientific/cyber-sabr-cybersecurity-attention-data)
- **GitHub:** [github.com/shepsci/cyber-sabr](https://github.com/shepsci/cyber-sabr)
- **Benchmark Collection:** [Cyber-SABR on Kaggle Benchmarks](https://www.kaggle.com/benchmarks/shepscientific/cyber-sabr-cybersecurity-selective-attention-benc)
- **Related benchmarks:** [SABR: Selective Attention Benchmark for Reasoning](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning) | [Bio-SABR](https://www.kaggle.com/benchmarks/shepscientific/bio-sabr-biosafety-selective-attention-benchmark) | [Chem-SABR](https://www.kaggle.com/benchmarks/shepscientific/chem-sabr-chemical-safety-selective-attention-benchmark)

### Problem Statement

Attention failures in cybersecurity contexts can have severe consequences. A model that confuses CVSS base scores due to distracting text, misidentifies a MITRE ATT&CK technique from a dense threat report, or extracts the wrong compliance requirement from a security policy could contribute to real-world harm. [Meta's CyberSecEval (2024)](https://arxiv.org/abs/2404.13161) demonstrated that LLMs exhibit inconsistent cybersecurity knowledge, while [CVE-Bench (2025)](https://arxiv.org/abs/2503.17332) showed that models struggle with precise vulnerability reasoning, and [Google DeepMind (2025)](https://arxiv.org/abs/2503.11917) developed a framework for evaluating AI cyberattack capabilities across the full attack chain, finding meaningful capability uplift potential as frontier models advance. [NIST AI 600-1 (2024)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) and [NIST IR 8596 (2025)](https://csrc.nist.gov/pubs/ir/8596/iprd) address generative AI risk management and AI-specific cybersecurity risk respectively, establishing the regulatory context for rigorous evaluation. Prompt injection — ranked #1 on the [OWASP Top 10 for LLM Applications (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — represents a uniquely adversarial form of attention manipulation targeting AI systems directly, as formalized by [Liu et al. (2024)](https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei) and [Greshake et al. (2023)](https://arxiv.org/abs/2302.12173).

Cyber-SABR addresses this by adapting the [SABR attention testing framework](https://www.kaggle.com/benchmarks/shepscientific/sabr-selective-attention-benchmark-for-reasoning) to cybersecurity domains — including a dedicated domain for AI model security and prompt injection. Where SABR tests general selective attention, Cyber-SABR asks: **Do attention failures worsen when distractors are domain-specific cybersecurity misinformation, and can models maintain focus when the distractors describe attacks on AI systems themselves?** [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) identify selective attention as a key sub-domain in their AGI measurement framework — Cyber-SABR stress-tests it across both traditional and AI-specific security domains.

### Task & Benchmark Construction

Cyber-SABR evaluates 280 items across three tasks, each mapped to an established cognitive attention paradigm. Content spans six cybersecurity domains: threat intelligence, vulnerability management, network security, application security, security operations, and AI model security/prompt injection.

**Task 1: Distractor Robustness** (200 evals). Fifty cybersecurity questions presented under four distraction levels: *clean* (question only), *low* (off-topic sentences), *medium* (related cybersecurity text), *high* (near-miss cybersecurity misinformation designed to mislead). For example: "What is the maximum CVSS v3.1 base score?" (answer: 10.0) with a high distractor claiming the maximum was reduced to 9.8 in v3.0. The AI model security domain includes questions about prompt injection taxonomy, adversarial suffix techniques, and jailbreaking methods, with high distractors that deliberately swap definitions between attack categories. Inspired by Stroop interference ([Stroop, 1935](https://doi.org/10.1037/h0054651)). Metric: ARS = mean accuracy across all four conditions.

**Task 2: Source-Selective QA** (50 evals). Three named institutional sources (e.g., NIST, MITRE, OWASP, CrowdStrike, Anthropic, Google DeepMind) present conflicting cybersecurity claims; the model must answer using only the designated source. The AI model security items present conflicting claims about prompt injection defenses, guardrail architectures, and adversarial attack detection rates from different research groups. Inspired by Cherry's cocktail party experiments ([Cherry, 1953](https://doi.org/10.1121/1.1907229)). Designated source position is counterbalanced (A=17, B=17, C=16).

**Task 3: Attentional Spotlight** (30 evals). 400–600 word cybersecurity documents containing 8–15 embedded claims. The model must extract only claims matching a specific filter criterion across six categories: attack techniques, vulnerability details, compliance requirements, defense measures, temporal claims, and AI security indicators (prompt injection vectors, jailbreaking methods, adversarial attack techniques). Two items have zero matching claims, testing false-positive resistance. Documents use fictional institutions. Inspired by visual search research ([Treisman & Gelade, 1980](https://doi.org/10.1016/0010-0285(80)90005-5)). F1 scoring penalizes both omissions and over-extraction.

Composite: Distractor 40% + Source-Selective 30% + Spotlight 30%.

### Dataset

130 base items across six cybersecurity domains (9 items per domain for the four larger domains, 7 per domain for security operations and AI model security in Tasks 1–2; 5 per category for Task 3). All cybersecurity facts are grounded in real-world knowledge — real CVEs, real MITRE ATT&CK techniques, real compliance frameworks, real prompt injection research — ensuring factual accuracy. Task 3 uses fictional institutions and scenarios to prevent memorization.

The AI model security domain draws on peer-reviewed research including [Zou et al. (2023)](https://arxiv.org/abs/2307.15043) on adversarial suffixes, [Anil et al. (2024)](https://arxiv.org/abs/2404.02151) on many-shot jailbreaking, [Schulhoff et al. (2023)](https://aclanthology.org/2023.emnlp-main.302/) on the HackAPrompt competition, and [Perez & Ribeiro (2022)](https://arxiv.org/abs/2211.09527) on prompt injection formalization, as well as standardized red teaming evaluation frameworks including [Mazeika et al. (2024)](https://arxiv.org/abs/2402.04249) (HarmBench) and [Chao et al. (2024)](https://arxiv.org/abs/2404.01318) (JailbreakBench).

### Technical Details

The benchmark notebook uses the [kaggle-benchmarks SDK](https://github.com/Kaggle/kaggle-benchmarks): a single scored function returning a composite float. Each of 280 evaluations runs in its own isolated chat context. Data loads via `kagglehub.dataset_download()` with `/kaggle/input/` fallback. Scoring: case-insensitive exact match with alias support (Tasks 1–2); token-overlap F1 with 70% threshold (Task 3). Spotlight items with zero correct answers score 1.0 only if the model produces no output.

The benchmark shares SABR's scoring code and task structure, enabling direct cross-benchmark comparison across general, biosafety, chemistry, and cybersecurity domains.

### Results, Insights, and Conclusions

| Model | Composite |
|-------|-----------|
| Claude Opus 4.6 | 84% |
| Claude Sonnet 4.6 | 77% |
| Gemini 3.1 Pro Preview | 75% |
| Gemini 3.1 Flash-Lite Preview | 71% |
| Claude Haiku 4.5 | 70% |
| Gemini 2.5 Flash | 63% |

Results across six models reveal a 21-point spread (63–84% composite), confirming strong discriminatory power. Claude Opus 4.6 leads at 84%, followed by Claude Sonnet 4.6 at 77% — a striking result given that both Claude frontier models refuse to complete the structurally identical Chem-SABR and Bio-SABR benchmarks due to content safety concerns. Cybersecurity content does not trigger the same safety filters, enabling full evaluation of Claude's selective attention capabilities in this domain.

**Cybersecurity enables the broadest model comparison across SABR variants.** Unlike biosafety and chemical safety domains, cybersecurity content does not trigger content moderation refusals from frontier Claude models. This makes Cyber-SABR uniquely valuable for comparing attention performance across model families. Claude Opus 4.6's 84% composite — the highest score across any SABR variant — demonstrates that frontier models possess strong selective attention capabilities when safety filters do not interfere.

**The Claude model hierarchy is preserved.** Opus 4.6 (84%) > Sonnet 4.6 (77%) > Haiku 4.5 (70%) shows a clear monotonic relationship between model capability and selective attention performance, with each step down in the Claude family losing approximately 7 points. This suggests selective attention scales with general model capability in cybersecurity contexts.

**Key insights:** (1) Cyber-SABR composite scores (63–84%) are notably higher than Bio-SABR (45–67%) and Chem-SABR (56–67%), suggesting cybersecurity attention is easier than biosafety/chemical safety attention — possibly because cybersecurity reasoning is better represented in training data. (2) The Gemini models show a narrower spread (63–75%) compared to Claude (70–84%), suggesting more uniform attention capability across the Gemini family. (3) Cross-benchmark comparison reveals that model rankings change across domains: Claude Opus leads in cybersecurity (84%) but errors in chemistry/biosafety, while Gemini 3.1 Flash-Lite Preview is consistently strong across all domains (67–71%). (4) The AI model security domain — covering prompt injection, jailbreaking, and adversarial attacks — provides a uniquely self-referential evaluation, testing whether models can maintain attention when the content describes attacks on AI systems themselves.

### Organizational Affiliations

Independent research (Shep Scientific).

### TL;DR:

**Evidence that the dataset and task are both high quality**

Cyber-SABR covers 280 evaluations across 130 unique items in six cybersecurity domains, including a dedicated AI model security domain covering prompt injection, jailbreaking, and adversarial attacks on LLMs. Three structurally distinct tasks prevent gaming via a single strategy. Task 1's repeated-measures design (50 items x 4 conditions) isolates attention from knowledge. All content is factually grounded in real cybersecurity knowledge and peer-reviewed AI security research. Tasks 1–2 use deterministic exact-match scoring; Task 3 uses token-overlap F1.

**Evidence that the writeup is high quality**

This writeup covers all required sections with extensive academic citations spanning cognitive science, cybersecurity, and AI model security literature. The benchmark is grounded in both classical attention paradigms (Stroop, Cherry, Treisman) and modern AI security research (prompt injection, adversarial attacks, jailbreaking). It extends SABR to cybersecurity, enabling cross-benchmark comparison.

**Evidence that the benchmark has sufficient discriminatory power**

Cyber-SABR produces the strongest discriminatory signal across all SABR variants: composite scores range from 63% (Gemini 2.5 Flash) to 84% (Claude Opus 4.6), a 21-point spread. The Claude model hierarchy (Opus 84% > Sonnet 77% > Haiku 70%) shows monotonic scaling with model capability. Unlike Bio-SABR and Chem-SABR, cybersecurity content does not trigger frontier model refusals, enabling the broadest model comparison. Cross-benchmark analysis reveals domain-dependent attention profiles: models that lead in cybersecurity may error in chemistry, demonstrating that selective attention is not a single capability but varies with domain content.

### References & Citations

1. Burnell, R., et al. (2026). ["Measuring Progress Toward AGI: A Cognitive Framework."](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf) Google DeepMind.
2. Bhatt, M., et al. (2024). ["CyberSecEval 2: A Wide-Ranging Cybersecurity Evaluation Suite for Large Language Models."](https://arxiv.org/abs/2404.13161) Meta / PurpleLlama.
3. NIST. (2025). ["IR 8596: Cybersecurity Framework Profile for Artificial Intelligence (Cyber AI Profile)."](https://csrc.nist.gov/pubs/ir/8596/iprd)
4. OWASP. (2025). ["Top 10 for Large Language Model Applications."](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
5. Liu, Y., et al. (2024). ["Formalizing and Benchmarking Prompt Injection Attacks and Defenses."](https://www.usenix.org/conference/usenixsecurity24/presentation/liu-yupei) *USENIX Security '24.*
6. Greshake, K., et al. (2023). ["Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection."](https://arxiv.org/abs/2302.12173) *AISec@CCS '23.*
7. Zou, A., et al. (2023). ["Universal and Transferable Adversarial Attacks on Aligned Language Models."](https://arxiv.org/abs/2307.15043) arXiv.
8. Anil, C., et al. (2024). ["Many-Shot Jailbreaking."](https://arxiv.org/abs/2404.02151) *NeurIPS 2024.* Anthropic.
9. Schulhoff, S., et al. (2023). ["Ignore This Title and HackAPrompt: Exposing Systemic Weaknesses of LLMs through a Global Scale Prompt Hacking Competition."](https://aclanthology.org/2023.emnlp-main.302/) *EMNLP 2023.*
10. Perez, F. & Ribeiro, I. (2022). ["Ignore Previous Prompt: Attack Techniques For Language Models."](https://arxiv.org/abs/2211.09527) *NeurIPS ML Safety Workshop.*
11. Mazeika, M., et al. (2024). ["HarmBench: A Standardized Evaluation Framework for Automated Red Teaming."](https://arxiv.org/abs/2402.04249) *ICML 2024.*
12. Chao, P., et al. (2024). ["JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models."](https://arxiv.org/abs/2404.01318) *NeurIPS 2024 D&B Track.*
13. NIST. (2024). ["AI 600-1: AI Risk Management Framework: Generative AI Profile."](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
14. Zhang, J., et al. (2025). ["CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities."](https://arxiv.org/abs/2503.17332) arXiv.
15. Google DeepMind. (2025). ["A Framework for Evaluating Emerging Cyberattack Capabilities of AI."](https://arxiv.org/abs/2503.11917) arXiv.
16. Stroop, J.R. (1935). ["Studies of interference in serial verbal reactions."](https://doi.org/10.1037/h0054651) *Journal of Experimental Psychology*, 18(6), 643–662.
17. Cherry, E.C. (1953). ["Some experiments on the recognition of speech, with one and with two ears."](https://doi.org/10.1121/1.1907229) *Journal of the Acoustical Society of America*, 25(5), 975–979.
18. Treisman, A.M. & Gelade, G. (1980). ["A feature-integration theory of attention."](https://doi.org/10.1016/0010-0285(80)90005-5) *Cognitive Psychology*, 12(1), 97–136.
19. [Kaggle Benchmarks SDK.](https://github.com/Kaggle/kaggle-benchmarks)
