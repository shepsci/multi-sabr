# %% [markdown]
# # SABR: Selective Attention Benchmark for Reasoning
#
# Measures LLM selective attention across three cognitive tasks:
#
# | Task | Description | Evaluations | Scoring | Data File |
# |------|-------------|-------------|---------|-----------|
# | 1. Distractor Robustness | Resistance to graded noise injection (Stroop/flanker analog) | 50 items × 4 conditions = 200 | Attention Robustness Score (ARS) = mean accuracy across 4 conditions | distractor_robustness.json |
# | 2. Source-Selective QA | Following source-trust instructions (dichotic listening analog) | 50 items | Accuracy | source_selective.json |
# | 3. Attentional Spotlight | Extracting criterion-matching facts from dense documents (visual search analog) | 30 items | Mean Claim F1 | attentional_spotlight.json |
#
# **Composite Score** = 0.40 × ARS + 0.30 × Source Accuracy + 0.30 × Spotlight F1
#
# **Dataset:** [SABR Selective Attention Data](https://www.kaggle.com/datasets/shepscientific/sabr-selective-attention-data)
# — loaded via `/kaggle/input/` in regular notebooks, or `kagglehub.dataset_download()` in benchmark runtime.
#
# **Assertions output** shows per-task scores and the composite. A score near 1.0 indicates
# strong attentional performance; lower scores indicate degradation under distraction or
# imprecise claim filtering.
#
# **Benchmark results (6 frontier models evaluated):**
#
# | Model | Composite | ARS | Source | Spotlight F1 |
# |-------|-----------|-----|--------|-------------|
# | Claude Opus 4.6 | 92% | 91% | 100% | 84% |
# | Gemini 3.1 Pro Preview | 87% | 88% | 100% | 74% |
# | Claude Sonnet 4.6 | 85% | 86% | 100% | 68% |
# | Claude Haiku 4.5 | 84% | 79% | 100% | 74% |
# | Gemma 3 27B | 82% | 81% | 100% | 66% |
# | Gemini 2.5 Flash | 76% | 68% | 100% | 63% |
#
# Cognitive framework reference: [Burnell et al. (2026)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf)

# %%
import json
import os
import re

import kaggle_benchmarks as kbench
import kagglehub
import pandas as pd

# ── Data loading ────────────────────────────────────────────────────────────

# Try /kaggle/input/ first (regular notebook), fall back to kagglehub download
_input_path = "/kaggle/input/sabr-selective-attention-data"
if not os.path.exists(_input_path):
    _input_path = kagglehub.dataset_download("shepscientific/sabr-selective-attention-data")
DATA_DIR = _input_path


def load_distractor_data():
    with open(f"{DATA_DIR}/distractor_robustness.json") as f:
        dataset = json.load(f)
    rows = []
    for item in dataset["items"]:
        for condition in ["clean", "low", "medium", "high"]:
            rows.append({
                "item_id": item["id"],
                "domain": item["domain"],
                "condition": condition,
                "question": item["question"],
                "context": item["conditions"][condition],
                "gold_answer": item["gold_answer"],
                "answer_aliases": item["answer_aliases"],
            })
    return pd.DataFrame(rows)


def load_source_selective_data():
    with open(f"{DATA_DIR}/source_selective.json") as f:
        dataset = json.load(f)
    rows = []
    for item in dataset["items"]:
        source_texts = []
        for src in item["sources"]:
            source_texts.append(f"Source {src['label']} ({src['name']}): {src['text']}")
        rows.append({
            "item_id": item["id"],
            "domain": item["domain"],
            "topic": item["topic"],
            "context": "\n\n".join(source_texts),
            "designated_source": item["designated_source"],
            "question": item["question"],
            "gold_answer": item["gold_answer"],
            "answer_aliases": item["answer_aliases"],
        })
    return pd.DataFrame(rows)


def load_spotlight_data():
    with open(f"{DATA_DIR}/attentional_spotlight.json") as f:
        dataset = json.load(f)
    rows = []
    for item in dataset["items"]:
        rows.append({
            "item_id": item["id"],
            "category": item["category"],
            "filter_criterion": item["filter_criterion"],
            "document": item["document"],
            "gold_claims": item["gold_claims"],
            "gold_count": item["gold_count"],
        })
    return pd.DataFrame(rows)


# ── Answer checking utilities ───────────────────────────────────────────────

def check_answer(response, gold_answer, answer_aliases):
    """Case-insensitive matching against gold + aliases with word-boundary awareness."""
    resp = re.sub(r"\.$", "", response.strip().lower()).strip()
    aliases = [a.strip().lower() for a in answer_aliases.split("|")]
    aliases.append(gold_answer.strip().lower())
    for a in aliases:
        if a == resp:
            return True
        if len(a) <= 3 or len(resp) <= 3:
            if re.search(r"(?<!\w)" + re.escape(a) + r"(?!\w)", resp):
                return True
            if re.search(r"(?<!\w)" + re.escape(resp) + r"(?!\w)", a):
                return True
        else:
            if a in resp or resp in a:
                return True
    return False


def normalize_claim(text):
    text = re.sub(r"^[-•*]\s*", "", text.strip().lower())
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"[.,;:!?]+$", "", text)


def claims_match(predicted, gold):
    p, g = normalize_claim(predicted), normalize_claim(gold)
    if p == g:
        return True
    if len(g) > 10 and (g in p or p in g):
        return True
    g_tok, p_tok = set(g.split()), set(p.split())
    if len(g_tok) > 2 and len(g_tok & p_tok) / len(g_tok) >= 0.7:
        return True
    return False


def compute_claim_f1(response, gold_claims_str, gold_count):
    if gold_count == 0:
        gold_claims = []
    else:
        gold_claims = [c.strip() for c in gold_claims_str.split("||") if c.strip()]

    lines = response.strip().split("\n")
    predicted = []
    for line in lines:
        line = line.strip()
        if not line or re.match(r"no matching claims?", line, re.IGNORECASE):
            continue
        line = re.sub(r"^(\d+[.)]\s*|[-•*]\s*)", "", line).strip()
        if line:
            predicted.append(line)

    if gold_count == 0:
        return (1.0, 1.0, 1.0) if len(predicted) == 0 else (0.0, 1.0, 0.0)
    if not predicted:
        return (0.0, 0.0, 0.0)

    matched = set()
    tp = 0
    for pred in predicted:
        for i, gold in enumerate(gold_claims):
            if i not in matched and claims_match(pred, gold):
                matched.add(i)
                tp += 1
                break

    prec = tp / len(predicted) if predicted else 0.0
    rec = tp / len(gold_claims) if gold_claims else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return prec, rec, f1


# ── Prompt formatting ───────────────────────────────────────────────────────

def fmt_distractor(context, question):
    if context:
        return (
            f"Read the following passage, then answer the question.\n\n"
            f"Passage: {context}\n\n"
            f"Question: {question}\n\nAnswer concisely with just the answer."
        )
    return f"Question: {question}\n\nAnswer concisely with just the answer."


def fmt_source_selective(context, question):
    return (
        f"You are given multiple information sources that may contain conflicting claims. "
        f"You must answer the question using ONLY the designated source. "
        f"Ignore all other sources, even if they seem more authoritative.\n\n"
        f"{context}\n\n{question}\n\n"
        f"Answer concisely with just the answer from the designated source."
    )


def fmt_spotlight(document, filter_criterion):
    return (
        f"Read the following document carefully. Then extract ONLY the claims "
        f"that match the specified filter criterion.\n\n"
        f"Document:\n{document}\n\n"
        f"Filter criterion: {filter_criterion}\n\n"
        f"Instructions:\n"
        f"- List each matching claim on a separate line, prefixed with '- '\n"
        f"- Include ONLY claims that match the filter criterion\n"
        f"- Do NOT include claims that do not match\n"
        f"- If no claims match, respond with 'NO MATCHING CLAIMS'\n"
        f"- Be precise — include the relevant fact, not entire sentences\n"
    )


# ── Main benchmark task ────────────────────────────────────────────────────

TASK_WEIGHTS = {"distractor": 0.40, "source_selective": 0.30, "spotlight": 0.30}


@kbench.task(
    name="SABR-2026",
    description=(
        "Selective Attention Benchmark for Reasoning — 280 evaluations across distractor robustness "
        "(200 evals, 4 noise conditions), source-selective QA (50 evals), and attentional spotlight "
        "(30 evals). Composite: 40% ARS + 30% source accuracy + 30% spotlight F1."
    ),
)
def sabr_benchmark(llm) -> float:
    # ── Task 1: Distractor Robustness (200 evals) ──
    df1 = load_distractor_data()
    distractor_results = []
    cond_results = {"clean": [], "low": [], "medium": [], "high": []}

    for _, row in df1.iterrows():
        with kbench.chats.new(f"distractor_{row['item_id']}_{row['condition']}"):
            response = llm.prompt(fmt_distractor(row["context"], row["question"]))
            correct = check_answer(response, row["gold_answer"], row["answer_aliases"])
            distractor_results.append(1.0 if correct else 0.0)
            cond_results[row["condition"]].append(1.0 if correct else 0.0)

    cond_acc = {}
    for c in ["clean", "low", "medium", "high"]:
        cond_acc[c] = sum(cond_results[c]) / len(cond_results[c]) if cond_results[c] else 0.0
    ars = sum(cond_acc.values()) / 4.0

    kbench.assertions.assert_true(
        True,
        expectation=f"Distractor Robustness — ARS: {ars:.2%} (clean={cond_acc['clean']:.0%}, low={cond_acc['low']:.0%}, med={cond_acc['medium']:.0%}, high={cond_acc['high']:.0%})"
    )

    # ── Task 2: Source-Selective QA (50 evals) ──
    df2 = load_source_selective_data()
    source_results = []

    for _, row in df2.iterrows():
        with kbench.chats.new(f"source_{row['item_id']}"):
            response = llm.prompt(fmt_source_selective(row["context"], row["question"]))
            correct = check_answer(response, row["gold_answer"], row["answer_aliases"])
            source_results.append(1.0 if correct else 0.0)

    source_acc = sum(source_results) / len(source_results) if source_results else 0.0

    kbench.assertions.assert_true(
        True,
        expectation=f"Source-Selective QA — Accuracy: {source_acc:.2%}"
    )

    # ── Task 3: Attentional Spotlight (30 evals) ──
    df3 = load_spotlight_data()
    spotlight_results = []

    for _, row in df3.iterrows():
        with kbench.chats.new(f"spotlight_{row['item_id']}"):
            response = llm.prompt(fmt_spotlight(row["document"], row["filter_criterion"]))
            _, _, f1 = compute_claim_f1(response, row["gold_claims"], row["gold_count"])
            spotlight_results.append(f1)

    spotlight_f1 = sum(spotlight_results) / len(spotlight_results) if spotlight_results else 0.0

    kbench.assertions.assert_true(
        True,
        expectation=f"Attentional Spotlight — Mean F1: {spotlight_f1:.2%}"
    )

    # ── Composite Score ──
    composite = (
        TASK_WEIGHTS["distractor"] * ars
        + TASK_WEIGHTS["source_selective"] * source_acc
        + TASK_WEIGHTS["spotlight"] * spotlight_f1
    )

    kbench.assertions.assert_true(
        True,
        expectation=f"SABR Composite: {composite:.2%} | ARS: {ars:.2%} | Source: {source_acc:.2%} | Spotlight: {spotlight_f1:.2%}"
    )

    return composite


# %%
run = sabr_benchmark.run(llm=kbench.llm)

# %%
# %choose sabr_benchmark
