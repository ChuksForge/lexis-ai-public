# scripts/run_demo.py
# LexisAI Public Demo Runner
#
# Runs the stub pipeline end to end, demonstrating:
#   1. Input processing
#   2. Source labelling
#   3. Research synthesis (stub — returns pre-generated example)
#   4. Output validation against schema
#
# This does NOT call any LLM API.
# It demonstrates structure and schema compliance using pre-generated outputs.
#
# To run: python scripts/run_demo.py

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from stubs.research_stub import research as stub_research
from stubs.source_labeller_stub import label_sources as stub_label_sources
from lexis_ai.utils import validate_report_structure, count_annotation_tags


def load_sample_input(sample_id: int = 1) -> str:
    """Load a sample input file."""
    path = Path(__file__).parent.parent / "examples" / "inputs" / f"sample_{sample_id}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Research question: What are the cognitive effects of sleep deprivation?"


def print_section(title: str, content: str = "", width: int = 60):
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}")
    if content:
        print(content)


def main():
    print_section("LexisAI Public Demo")
    print("This demo runs the stub pipeline using pre-generated examples.")
    print("No API calls are made. All output comes from examples/outputs/.")

    # ── Step 1: Load input ────────────────────────────────────────────────────
    print_section("Step 1: Loading Sample Input")
    user_input = load_sample_input(sample_id=1)
    print(f"Input length: {len(user_input)} characters")
    print(f"Preview: {user_input[:200]}...")

    # ── Step 2: Source labelling ──────────────────────────────────────────────
    print_section("Step 2: Source Labelling (Stub)")
    source_data = stub_label_sources(user_input)
    print(f"Sources detected: {source_data['source_count']}")
    print(f"Research question stated: {source_data['research_question_stated']}")
    for source in source_data.get("sources", []):
        print(f"  {source['id']}: {source['title_or_description']}")

    # ── Step 3: Research synthesis ────────────────────────────────────────────
    print_section("Step 3: Research Synthesis (Stub)")
    print("Calling stub research() — returns pre-generated example output...")
    conversation_history = []
    report = stub_research(user_input, conversation_history)
    print(f"Report generated: {len(report)} characters")

    # ── Step 4: Schema validation ─────────────────────────────────────────────
    print_section("Step 4: Schema Validation")
    validation = validate_report_structure(report)

    print(f"Valid: {validation['valid']}")
    print(f"Annotation coverage: {validation['annotation_coverage']}")
    print(f"Total annotations: {validation['total_annotations']}")

    print("\nAnnotation tag counts:")
    for tag, count in validation['annotation_counts'].items():
        print(f"  {tag}: {count}")

    if validation['missing_sections']:
        print(f"\nMissing sections: {validation['missing_sections']}")
    else:
        print("\nAll required sections present.")

    if validation['issues']:
        print(f"\nIssues: {validation['issues']}")
    else:
        print("No issues detected.")

    # ── Step 5: Show report preview ───────────────────────────────────────────
    print_section("Step 5: Report Preview (first 800 chars)")
    print(report[:800])
    print("\n... [truncated — full report in examples/outputs/report_1.md]")

    # ── Done ──────────────────────────────────────────────────────────────────
    print_section("Demo Complete")
    print("What you just saw:")
    print("  1. Input loaded from examples/inputs/sample_1.txt")
    print("  2. Source labeller stub classified input sources")
    print("  3. Research stub returned pre-generated example report")
    print("  4. Schema validator confirmed output follows LexisAI contract")
    print("\nTo verify outputs manually:")
    print("  - examples/inputs/sample_1.txt  (input)")
    print("  - examples/outputs/report_1.md  (output)")
    print("  - docs/evaluation.md            (how it is scored)")


if __name__ == "__main__":
    main()
