"""
Bio-SABR Task 3: Attentional Spotlight (Biosafety/Biosecurity)
================================================================
Tests sustained attention + attention shifting -- can the model extract
ONLY criterion-matching facts from information-dense biosafety documents?

Cognitive mapping: Sustained Attention + Attention Shifting (Burnell et al., 2026)
Analogous to: Visual search paradigms (Treisman & Gelade, 1980)

Dataset: data/attentional_spotlight.json
  - 30 items = 30 evaluations
  - Fields per item: id (str), category (str), filter_criterion (str),
    document (str, 400-600 words), all_claims (list of str),
    gold_claims (str, claims delimited by "||"), gold_count (int)
  - Filter categories: risk_levels, regulatory_requirements,
    dual_use_indicators, containment_specifications, temporal_claims,
    attribution
  - Each document contains 8-15 embedded factual claims about biosafety
    topics; typically 3-5 match the filter criterion
  - 2 items have gold_count=0 (zero matching claims), testing
    false-positive resistance

Scoring: Precision/Recall/F1 at the claim level per item; mean F1 reported
  - Claim matching: three-tier fuzzy match:
      1. Exact string match (after normalization)
      2. Substring containment (if gold claim len > 10 chars)
      3. Token overlap >= 70% of gold tokens
  - Zero-gold-count items: score 1.0 if model returns nothing, 0.0 otherwise

Prompt structure: Models are given the full document and a filter criterion,
  instructed to list matching claims one per line prefixed with "- ".
"""

import json
import os
import re

import kbench
import pandas as pd


def load_spotlight_data(data_path="data/attentional_spotlight.json"):
    """Load attentional spotlight dataset and build eval rows."""
    with open(data_path) as f:
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


def format_spotlight_prompt(document, filter_criterion):
    """Format the prompt for attentional spotlight evaluation."""
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
        f"- Be precise -- include the relevant fact, not entire sentences\n"
    )


def normalize_claim(text):
    """Normalize a claim for fuzzy matching."""
    text = text.strip().lower()
    text = re.sub(r"^[-\u2022*]\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[.,;:!?]+$", "", text)
    return text


def claims_match(predicted, gold):
    """Check if a predicted claim matches a gold claim (fuzzy)."""
    p = normalize_claim(predicted)
    g = normalize_claim(gold)

    if p == g:
        return True

    if len(g) > 10 and (g in p or p in g):
        return True

    g_tokens = set(g.split())
    p_tokens = set(p.split())
    if len(g_tokens) > 2:
        overlap = len(g_tokens & p_tokens) / len(g_tokens)
        if overlap >= 0.7:
            return True

    return False


def compute_claim_f1(response, gold_claims_str, gold_count):
    """Compute precision, recall, F1 for claim-level matching."""
    if gold_count == 0:
        gold_claims = []
    else:
        gold_claims = [c.strip() for c in gold_claims_str.split("||") if c.strip()]

    lines = response.strip().split("\n")
    predicted_claims = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"no matching claims?", line, re.IGNORECASE):
            continue
        line = re.sub(r"^(\d+[.)]\s*|[-\u2022*]\s*)", "", line).strip()
        if line:
            predicted_claims.append(line)

    if gold_count == 0:
        if len(predicted_claims) == 0:
            return 1.0, 1.0, 1.0
        else:
            return 0.0, 1.0, 0.0

    if len(predicted_claims) == 0:
        return 0.0, 0.0, 0.0

    matched_gold = set()
    true_positives = 0
    for pred in predicted_claims:
        for i, gold in enumerate(gold_claims):
            if i not in matched_gold and claims_match(pred, gold):
                matched_gold.add(i)
                true_positives += 1
                break

    precision = true_positives / len(predicted_claims) if predicted_claims else 0.0
    recall = true_positives / len(gold_claims) if gold_claims else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


@kbench.task(name="Bio-SABR Spotlight Single", store_task=False)
def spotlight_single(llm, item_id, category, filter_criterion, document,
                      gold_claims, gold_count) -> float:
    prompt = format_spotlight_prompt(document, filter_criterion)
    response = llm.prompt(prompt)
    _, _, f1 = compute_claim_f1(response, gold_claims, gold_count)
    return f1


@kbench.task(
    name="Bio-SABR Attentional Spotlight",
    description=(
        "Tests sustained attention and attention shifting in biosafety contexts: "
        "can the model extract ONLY criterion-matching facts from dense biosafety "
        "documents? 30 items, scored by precision/recall/F1 at the claim level."
    ),
)
def spotlight_benchmark(llm) -> dict:
    os.environ["RENDER_SUBRUNS"] = "False"
    eval_df = load_spotlight_data()

    with kbench.client.enable_cache():
        runs = spotlight_single.evaluate(
            llm=[llm],
            evaluation_data=eval_df,
            n_jobs=2,
            timeout=180,
            max_attempts=1,
            remove_run_files=True,
        )

    results_df = runs.as_dataframe()
    valid = results_df[results_df["result"].notna()]

    mean_f1 = float(valid["result"].mean()) if len(valid) > 0 else 0.0

    category_f1 = {}
    for cat in ["risk_levels", "regulatory_requirements", "dual_use_indicators",
                "containment_specifications", "temporal_claims", "attribution"]:
        cat_rows = valid[valid["category"] == cat]
        category_f1[cat] = float(cat_rows["result"].mean()) if len(cat_rows) > 0 else 0.0

    summary = (
        f"Mean F1: {mean_f1:.2%} | "
        + " | ".join(f"{k}: {v:.2%}" for k, v in category_f1.items())
    )

    kbench.assertions.assert_true(
        len(valid) > 0,
        expectation=f"Bio-SABR Attentional Spotlight -- {summary}"
    )

    return {
        "mean_f1": mean_f1,
        "category_f1": category_f1,
        "n_evaluated": len(valid),
    }
