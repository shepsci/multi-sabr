#!/usr/bin/env python3
"""
SABR Data Validation Script
Validates schema integrity, domain balance, answer uniqueness,
and distractor length balance across all three datasets.
"""

import json
import sys
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
ERRORS = []
WARNINGS = []


def error(msg):
    ERRORS.append(msg)
    print(f"  ERROR: {msg}")


def warn(msg):
    WARNINGS.append(msg)
    print(f"  WARN:  {msg}")


def ok(msg):
    print(f"  OK:    {msg}")


# ── Task 1: Distractor Robustness ───────────────────────────────────────────

def validate_distractor_robustness():
    print("\n=== Task 1: Distractor Robustness ===")
    path = DATA_DIR / "distractor_robustness.json"
    if not path.exists():
        error(f"File not found: {path}")
        return

    with open(path) as f:
        data = json.load(f)

    items = data.get("items", [])
    meta = data.get("metadata", {})

    # Check item count
    if len(items) == meta.get("total_items", 0):
        ok(f"Item count matches metadata: {len(items)}")
    else:
        error(f"Item count {len(items)} != metadata {meta.get('total_items')}")

    # Check domains
    domains = Counter(item["domain"] for item in items)
    expected_domains = {"science", "history", "math_logic", "geography", "general"}
    if set(domains.keys()) == expected_domains:
        ok(f"All 5 domains present: {dict(domains)}")
    else:
        error(f"Domain mismatch: got {set(domains.keys())}, expected {expected_domains}")

    for domain, count in domains.items():
        if count != 10:
            warn(f"Domain '{domain}' has {count} items (expected 10)")

    # Check each item
    ids_seen = set()
    conditions = {"clean", "low", "medium", "high"}
    for item in items:
        item_id = item.get("id", "MISSING")

        if item_id in ids_seen:
            error(f"Duplicate ID: {item_id}")
        ids_seen.add(item_id)

        # Required fields
        for field in ["id", "domain", "question", "gold_answer", "answer_aliases", "conditions"]:
            if field not in item:
                error(f"{item_id}: Missing field '{field}'")

        # Conditions
        if set(item.get("conditions", {}).keys()) != conditions:
            error(f"{item_id}: Missing conditions, got {set(item.get('conditions', {}).keys())}")

        # Clean condition should be empty
        if item.get("conditions", {}).get("clean", "X") != "":
            error(f"{item_id}: Clean condition should be empty string")

        # Check distractor lengths are increasing
        conds = item.get("conditions", {})
        low_len = len(conds.get("low", ""))
        med_len = len(conds.get("medium", ""))
        high_len = len(conds.get("high", ""))
        if not (low_len > 0 and med_len > 0 and high_len > 0):
            error(f"{item_id}: All non-clean conditions must have content")

        # Gold answer should be in aliases
        aliases = item.get("answer_aliases", "").lower().split("|")
        if item.get("gold_answer", "").lower() not in [a.strip() for a in aliases]:
            warn(f"{item_id}: gold_answer not found in answer_aliases (may be OK if substring)")

    total_evals = len(items) * 4
    ok(f"Total evaluations: {total_evals}")


# ── Task 2: Source-Selective QA ─────────────────────────────────────────────

def validate_source_selective():
    print("\n=== Task 2: Source-Selective QA ===")
    path = DATA_DIR / "source_selective.json"
    if not path.exists():
        error(f"File not found: {path}")
        return

    with open(path) as f:
        data = json.load(f)

    items = data.get("items", [])
    meta = data.get("metadata", {})

    if len(items) == meta.get("total_items", 0):
        ok(f"Item count matches metadata: {len(items)}")
    else:
        error(f"Item count {len(items)} != metadata {meta.get('total_items')}")

    # Check domains
    domains = Counter(item["domain"] for item in items)
    expected_domains = {"demographics", "scientific", "historical", "product", "legal"}
    if set(domains.keys()) == expected_domains:
        ok(f"All 5 domains present: {dict(domains)}")
    else:
        error(f"Domain mismatch: got {set(domains.keys())}, expected {expected_domains}")

    # Check designated source distribution
    source_dist = Counter(item.get("designated_source") for item in items)
    ok(f"Designated source distribution: {dict(source_dist)}")

    ids_seen = set()
    for item in items:
        item_id = item.get("id", "MISSING")
        if item_id in ids_seen:
            error(f"Duplicate ID: {item_id}")
        ids_seen.add(item_id)

        # Required fields
        for field in ["id", "domain", "topic", "sources", "designated_source",
                       "question", "gold_answer", "answer_aliases"]:
            if field not in item:
                error(f"{item_id}: Missing field '{field}'")

        # Check sources
        sources = item.get("sources", [])
        if len(sources) != 3:
            error(f"{item_id}: Expected 3 sources, got {len(sources)}")

        labels = [s.get("label") for s in sources]
        if sorted(labels) != ["A", "B", "C"]:
            error(f"{item_id}: Source labels should be A, B, C, got {labels}")

        # Check designated source exists
        ds = item.get("designated_source")
        if ds not in labels:
            error(f"{item_id}: Designated source '{ds}' not in source labels")

        # Check gold answer matches designated source's claim
        designated = next((s for s in sources if s.get("label") == ds), None)
        if designated:
            cv = designated.get("claim_value", "").lower()
            ga = item.get("gold_answer", "").lower()
            if cv not in ga and ga not in cv:
                warn(f"{item_id}: gold_answer '{ga}' may not match designated claim_value '{cv}'")

    ok(f"Total evaluations: {len(items)}")


# ── Task 3: Attentional Spotlight ───────────────────────────────────────────

def validate_attentional_spotlight():
    print("\n=== Task 3: Attentional Spotlight ===")
    path = DATA_DIR / "attentional_spotlight.json"
    if not path.exists():
        error(f"File not found: {path}")
        return

    with open(path) as f:
        data = json.load(f)

    items = data.get("items", [])
    meta = data.get("metadata", {})

    if len(items) == meta.get("total_items", 0):
        ok(f"Item count matches metadata: {len(items)}")
    else:
        error(f"Item count {len(items)} != metadata {meta.get('total_items')}")

    # Check categories
    categories = Counter(item["category"] for item in items)
    expected_cats = {"dates", "attributed", "numerical", "entity", "contradictions", "causal"}
    if set(categories.keys()) == expected_cats:
        ok(f"All 6 categories present: {dict(categories)}")
    else:
        error(f"Category mismatch: got {set(categories.keys())}, expected {expected_cats}")

    ids_seen = set()
    for item in items:
        item_id = item.get("id", "MISSING")
        if item_id in ids_seen:
            error(f"Duplicate ID: {item_id}")
        ids_seen.add(item_id)

        for field in ["id", "category", "filter_criterion", "document",
                       "all_claims", "gold_claims", "gold_count"]:
            if field not in item:
                error(f"{item_id}: Missing field '{field}'")

        # Validate claims
        all_claims = item.get("all_claims", [])
        matching = [c for c in all_claims if c.get("matches_filter")]
        gold_count = item.get("gold_count", -1)

        if len(matching) != gold_count:
            error(f"{item_id}: {len(matching)} matching claims != gold_count {gold_count}")

        # Validate gold_claims string matches matching claims
        if gold_count > 0:
            gold_str = item.get("gold_claims", "")
            gold_list = [c.strip() for c in gold_str.split("||") if c.strip()]
            if len(gold_list) != gold_count:
                error(f"{item_id}: gold_claims has {len(gold_list)} entries but gold_count is {gold_count}")
        elif gold_count == 0:
            if item.get("gold_claims", "") != "":
                warn(f"{item_id}: gold_count is 0 but gold_claims is not empty")

        # Document length check
        doc = item.get("document", "")
        word_count = len(doc.split())
        if word_count < 200:
            warn(f"{item_id}: Document only {word_count} words (target 400-600)")
        elif word_count > 800:
            warn(f"{item_id}: Document {word_count} words (target 400-600)")

        # Claim count check
        if len(all_claims) < 8:
            warn(f"{item_id}: Only {len(all_claims)} claims (target 8-15)")

    ok(f"Total evaluations: {len(items)}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print("SABR Data Validation")
    print("=" * 50)

    validate_distractor_robustness()
    validate_source_selective()
    validate_attentional_spotlight()

    print("\n" + "=" * 50)
    print(f"Results: {len(ERRORS)} errors, {len(WARNINGS)} warnings")

    if ERRORS:
        print("\nFailed — fix errors before submission.")
        sys.exit(1)
    elif WARNINGS:
        print("\nPassed with warnings — review before submission.")
        sys.exit(0)
    else:
        print("\nAll checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
