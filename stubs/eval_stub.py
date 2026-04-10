# stubs/eval_stub.py
# LexisAI Eval Stub

import json
from pathlib import Path

SAMPLE_RESULTS_DIR = Path(__file__).parent.parent / "examples" / "eval_runs"


def run_eval(test_case_id: str = "TC01") -> dict:
    """
    Stub implementation of the eval runner.

    Returns pre-computed scores from saved example results.
    The real eval runner generates reports and scores them via LLM judges.

    Args:
        test_case_id: Which test case to return results for (TC01–TC05)

    Returns:
        Example eval result dict matching the production result schema.
    """
    sample_path = SAMPLE_RESULTS_DIR / "eval_sample.json"

    if sample_path.exists():
        with open(sample_path) as f:
            data = json.load(f)
            results = data.get("results", [])
            for r in results:
                if r.get("id") == test_case_id:
                    return r

    return _static_example_result(test_case_id)


def run_all_evals() -> dict:
    """
    Stub implementation of run_all_evals().

    Returns the full pre-computed sample eval run.
    """
    sample_path = SAMPLE_RESULTS_DIR / "eval_sample.json"

    if sample_path.exists():
        with open(sample_path) as f:
            return json.load(f)

    return {
        "suite_score": 8.2,
        "total_cases": 5,
        "timestamp": "20250408_120000",
        "results": [_static_example_result(f"TC0{i}") for i in range(1, 6)],
    }


def _static_example_result(test_case_id: str) -> dict:
    return {
        "id": test_case_id,
        "name": f"Example Test Case {test_case_id}",
        "description": "Stub result — real scores from production eval run.",
        "overall_score": 8.2,
        "scores": {
            "structural_checks": {"score": 9.0, "passed": [], "failed": []},
            "structure_compliance": {"score": 8.5, "reasoning": "Stub result."},
            "annotation_accuracy": {"score": 8.0, "reasoning": "Stub result."},
            "synthesis_quality": {
                "score": 7.5,
                "reasoning": "Stub result.",
                "criteria_scores": {
                    "question_answered": 8,
                    "source_integration": 7,
                    "contradiction_handling": 8,
                    "evidence_weighting": 7,
                    "uncertainty_acknowledgement": 8,
                    "actionability": 7
                }
            }
        },
        "report": "See examples/outputs/report_1.md for a real report.",
    }
