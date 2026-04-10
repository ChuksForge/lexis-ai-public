# evals_public/run_public_evals.py
# LexisAI Public Eval Runner
#
# Runs the public test cases against the stub research pipeline.
# Validates outputs against schema and scores structural compliance.
#
# Does NOT call any LLM API — uses pre-generated example outputs.
# Does NOT run LLM-as-judge scoring — uses hardcoded structural checks only.
#
# To run: python -m evals_public.run_public_evals

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from evals_public.test_cases_public import TEST_CASES
from stubs.research_stub import research as stub_research
from stubs.source_labeller_stub import label_sources as stub_label_sources
from lexis_ai.utils import validate_report_structure, count_annotation_tags

RESULTS_DIR = Path(__file__).parent / "sample_results"
RESULTS_DIR.mkdir(exist_ok=True)


def run_structural_checks(report: str, expectations: dict) -> dict:
    """Run hardcoded checks against expected strings."""
    must_contain = expectations.get("must_contain", [])
    must_not_contain = expectations.get("must_not_contain", [])

    passed = []
    failed = []

    for item in must_contain:
        if item in report:
            passed.append(f"PASS: Contains '{item}'")
        else:
            failed.append(f"FAIL: Missing '{item}'")

    for item in must_not_contain:
        if item not in report:
            passed.append(f"PASS: Correctly absent '{item}'")
        else:
            failed.append(f"FAIL: Should not contain '{item}'")

    total = len(passed) + len(failed)
    score = round((len(passed) / total) * 10, 1) if total > 0 else 0

    return {
        "score": score,
        "passed": passed,
        "failed": failed,
        "pass_count": len(passed),
        "fail_count": len(failed)
    }


def build_test_input(test_case: dict) -> str:
    """Build combined input string from a test case."""
    tc_input = test_case["input"]
    parts = []

    question = tc_input.get("research_question", "")
    if question:
        parts.append(f"Research question: {question}")

    lens = tc_input.get("lens")
    if lens:
        parts.append(f"Analytical lens: {lens}")

    for source in tc_input.get("sources", []):
        parts.append(
            f"--- SOURCE {source['label']} ---\n"
            f"Type: {source['type']}\n"
            f"{source['description']}"
        )

    return "\n\n".join(parts)


def run_public_eval(test_case: dict, verbose: bool = True) -> dict:
    """Run a single public test case."""
    tc_id = test_case["id"]
    tc_name = test_case["name"]

    if verbose:
        print(f"\n{'='*60}")
        print(f"Running: [{tc_id}] {tc_name}")
        print(f"{'='*60}")

    test_input = build_test_input(test_case)

    # Get stub report
    if verbose:
        print("Getting stub report...")
    report = stub_research(test_input)

    # Run structural checks
    structural = run_structural_checks(report, test_case["expectations"])
    if verbose:
        print(f"Structural checks: {structural['score']}/10")
        for f in structural["failed"]:
            print(f"  {f}")

    # Run schema validation
    validation = validate_report_structure(report)
    schema_score = 10.0 if validation["valid"] else 5.0
    if verbose:
        print(f"Schema validation: {schema_score}/10")

    # Annotation count
    annotations = count_annotation_tags(report)
    annotation_score = min(10.0, annotations["total"] * 0.5)
    if verbose:
        print(f"Annotation count: {annotations['total']} tags")

    overall = round((structural["score"] + schema_score + annotation_score) / 3, 2)
    if verbose:
        print(f"Overall (stub): {overall}/10")

    return {
        "id": tc_id,
        "name": tc_name,
        "description": test_case["description"],
        "timestamp": datetime.now().isoformat(),
        "overall_score": overall,
        "scores": {
            "structural_checks": structural,
            "schema_validation": {
                "score": schema_score,
                "valid": validation["valid"],
                "missing_sections": validation["missing_sections"]
            },
            "annotation_count": {
                "score": annotation_score,
                "counts": annotations
            }
        },
    }


def run_all_public_evals(verbose: bool = True) -> dict:
    """Run all public test cases and save results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = []

    print("\nLexisAI Public Eval Suite")
    print("=" * 60)
    print("Running structural checks against stub outputs.")

    for test_case in TEST_CASES:
        result = run_public_eval(test_case, verbose=verbose)
        results.append(result)

    overall_scores = [r["overall_score"] for r in results]
    suite_score = round(sum(overall_scores) / len(overall_scores), 2)

    summary = {
        "suite_score": suite_score,
        "total_cases": len(results),
        "timestamp": timestamp,
        "eval_type": "public_structural_checks",
        "results": results
    }

    # Save JSON
    json_path = RESULTS_DIR / f"eval_public_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)

    # Save text summary
    txt_path = RESULTS_DIR / f"eval_public_{timestamp}_summary.txt"
    with open(txt_path, "w") as f:
        f.write(f"lexis_ai Public Eval Suite - {timestamp}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Suite Score: {suite_score}/10\n")
        f.write(f"Cases Run:   {len(results)}\n")
        f.write(f"Eval Type:   Structural checks only (no LLM judge)\n\n")
        for r in results:
            f.write(f"[{r['id']}] {r['name']}\n")
            f.write(f"  Overall: {r['overall_score']}/10\n\n")

    if verbose:
        print(f"\n{'='*60}")
        print(f"Public eval complete.")
        print(f"  Suite score: {suite_score}/10")
        print(f"  Results:     {json_path}")
        print(f"  Summary:     {txt_path}")

    return summary


if __name__ == "__main__":
    run_all_public_evals(verbose=True)
