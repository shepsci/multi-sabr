"""
SABR Task 1: Distractor Robustness
====================================
Tests perceptual inhibition — can the model maintain accuracy when
irrelevant or misleading context is injected?

Cognitive mapping: Perceptual Inhibition (Burnell et al., 2026)
Analogous to: Stroop interference effect and flanker paradigms

Dataset: data/distractor_robustness.json
  - 50 items × 4 conditions = 200 evaluations
  - Fields per item: id (str), domain (str), question (str),
    gold_answer (str), answer_aliases (pipe-delimited str),
    conditions (dict: clean|low|medium|high → context str)
  - Domains: science, history, math/logic, geography, general_knowledge
  - Conditions:
      clean  — question only (no context)
      low    — off-topic sentences added
      medium — topically related but irrelevant context
      high   — adversarial near-miss context with plausible wrong answers

Scoring: Attention Robustness Score (ARS) = mean(clean, low, medium, high)
  - Answer matching: case-insensitive exact match + word-boundary-aware
    substring matching against gold_answer and pipe-delimited aliases
  - All questions designed for >95% clean accuracy; lower ARS scores
    reflect pure attentional degradation, not knowledge gaps
  - Observed ARS range: 69–79% across frontier models tested

Prompt structure: "Read the following passage, then answer the question."
  (context omitted entirely for clean condition)
"""

import json
import os
import re

import kbench
import pandas as pd


def load_distractor_data(data_path="data/distractor_robustness.json"):
    """Load distractor robustness dataset and flatten into eval rows."""
    with open(data_path) as f:
        dataset = json.load(f)

    rows = []
    for item in dataset["items"]:
        for condition in ["clean", "low", "medium", "high"]:
            context = item["conditions"][condition]
            rows.append({
                "item_id": item["id"],
                "domain": item["domain"],
                "condition": condition,
                "question": item["question"],
                "context": context,
                "gold_answer": item["gold_answer"],
                "answer_aliases": item["answer_aliases"],
            })
    return pd.DataFrame(rows)


def format_distractor_prompt(context, question):
    """Format the prompt for a distractor robustness evaluation."""
    if context:
        return (
            f"Read the following passage, then answer the question.\n\n"
            f"Passage: {context}\n\n"
            f"Question: {question}\n\n"
            f"Answer concisely with just the answer."
        )
    else:
        return (
            f"Question: {question}\n\n"
            f"Answer concisely with just the answer."
        )


def check_answer(response, gold_answer, answer_aliases):
    """Check if model response matches any acceptable answer."""
    response_clean = response.strip().lower()
    response_clean = re.sub(r"\.$", "", response_clean).strip()

    aliases = [a.strip().lower() for a in answer_aliases.split("|")]
    aliases.append(gold_answer.strip().lower())

    for alias in aliases:
        if alias == response_clean:
            return True
        # For short strings (<=3 chars), require word boundary match
        if len(alias) <= 3 or len(response_clean) <= 3:
            if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", response_clean):
                return True
            if re.search(r"(?<!\w)" + re.escape(response_clean) + r"(?!\w)", alias):
                return True
        else:
            if alias in response_clean or response_clean in alias:
                return True
    return False


@kbench.task(name="SABR Distractor Single", store_task=False)
def distractor_single(llm, item_id, domain, condition, question, context,
                       gold_answer, answer_aliases) -> bool:
    prompt = format_distractor_prompt(context, question)
    response = llm.prompt(prompt)
    return check_answer(response, gold_answer, answer_aliases)


@kbench.task(
    name="SABR Distractor Robustness",
    description=(
        "Tests LLM resistance to distractors across 4 graded conditions "
        "(clean, low, medium, high). 50 items × 4 conditions = 200 evals. "
        "Measures perceptual inhibition — a core selective attention ability."
    ),
)
def distractor_robustness_benchmark(llm) -> dict:
    os.environ["RENDER_SUBRUNS"] = "False"
    eval_df = load_distractor_data()

    with kbench.client.enable_cache():
        runs = distractor_single.evaluate(
            llm=[llm],
            evaluation_data=eval_df,
            n_jobs=2,
            timeout=120,
            max_attempts=1,
            remove_run_files=True,
        )

    results_df = runs.as_dataframe()
    valid = results_df[results_df["result"].notna()]

    # Overall accuracy
    overall_acc = float(valid["result"].mean()) if len(valid) > 0 else 0.0

    # Per-condition accuracy
    condition_acc = {}
    for cond in ["clean", "low", "medium", "high"]:
        cond_rows = valid[valid["condition"] == cond]
        condition_acc[cond] = float(cond_rows["result"].mean()) if len(cond_rows) > 0 else 0.0

    # Attention Robustness Score = area under accuracy-vs-distraction curve
    # Normalized: (clean + low + medium + high) / 4
    ars = sum(condition_acc.values()) / 4.0

    # Degradation = clean accuracy - high accuracy
    degradation = condition_acc.get("clean", 0) - condition_acc.get("high", 0)

    summary = (
        f"Overall: {overall_acc:.2%} | "
        f"Clean: {condition_acc.get('clean', 0):.2%} | "
        f"Low: {condition_acc.get('low', 0):.2%} | "
        f"Medium: {condition_acc.get('medium', 0):.2%} | "
        f"High: {condition_acc.get('high', 0):.2%} | "
        f"ARS: {ars:.2%} | Degradation: {degradation:.2%}"
    )

    kbench.assertions.assert_true(
        len(valid) > 0,
        expectation=f"Distractor Robustness — {summary}"
    )

    return {
        "overall_accuracy": overall_acc,
        "condition_accuracy": condition_acc,
        "attention_robustness_score": ars,
        "degradation": degradation,
        "n_evaluated": len(valid),
    }
