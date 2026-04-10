# scripts/reproduce_example.py
# LexisAI Output Reproduction Script
#
# This script:
#   1. Loads a saved input from examples/inputs/
#   2. Loads the corresponding saved output from examples/outputs/
#   3. Validates both against the LexisAI schema
#   4. Compares annotation coverage and structure compliance
#   5. Prints a side-by-side verification report
#
#
# To run: python scripts/reproduce_example.py [example_id]
# Example: python scripts/reproduce_example.py 1

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lexis_ai.utils import (
    validate_report_structure,
    count_annotation_tags,
    extract_sources_from_brief
)
from lexis_ai.schemas import REQUIRED_SECTIONS


EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def load_input(example_id: int) -> str:
    path = EXAMPLES_DIR / "inputs" / f"sample_{example_id}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def load_output(example_id: int) -> str:
    path = EXAMPLES_DIR / "outputs" / f"report_{example_id}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def print_divider(char: str = "-", width: int = 60):
    print(char * width)


def verify_example(example_id: int):
    print(f"\n{'='*60}")
    print(f"  LexisAI Output Verification — Example {example_id}")
    print(f"{'='*60}\n")

    # Load files
    input_text = load_input(example_id)
    output_text = load_output(example_id)

    if not input_text:
        print(f"ERROR: examples/inputs/sample_{example_id}.txt not found")
        return
    if not output_text:
        print(f"ERROR: examples/outputs/report_{example_id}.md not found")
        return

    print(f"Input file:  examples/inputs/sample_{example_id}.txt")
    print(f"Output file: examples/outputs/report_{example_id}.md")
    print(f"Input length:  {len(input_text)} characters")
    print(f"Output length: {len(output_text)} characters\n")

    # ── Section check ─────────────────────────────────────────────────────────
    print_divider()
    print("REQUIRED SECTIONS CHECK")
    print_divider()

    all_present = True
    for section in REQUIRED_SECTIONS:
        present = section in output_text
        status = "PASS" if present else "FAIL"
        print(f"  [{status}] {section}")
        if not present:
            all_present = False

    print()
    print(f"Result: {'All sections present' if all_present else 'MISSING SECTIONS DETECTED'}")

    # ── Annotation check ──────────────────────────────────────────────────────
    print_divider()
    print("ANNOTATION TAG CHECK")
    print_divider()

    counts = count_annotation_tags(output_text)
    for tag, count in counts.items():
        if tag != "total":
            print(f"  {tag}: {count}")
    print(f"  {'─'*30}")
    print(f"  total: {counts['total']}")

    if counts["total"] == 0:
        print("\nFAIL: No annotation tags found — output is not compliant.")
    else:
        print("\nPASS: Annotation tags present.")

    # ── Source verification ───────────────────────────────────────────────────
    print_divider()
    print("SOURCE ATTRIBUTION CHECK")
    print_divider()

    sources_in_brief = extract_sources_from_brief(output_text)
    if sources_in_brief:
        print(f"  Sources declared in Research Brief: {len(sources_in_brief)}")
        for s in sources_in_brief:
            tag_count = output_text.count(f"[{s['id']}]")
            print(f"    [{s['id']}]: used {tag_count} time(s) — {s['description'][:50]}")
    else:
        print("  No sources declared in Research Brief.")
        gk_count = output_text.count("[general knowledge]")
        print(f"  [general knowledge] used {gk_count} time(s)")

    # ── Full validation ───────────────────────────────────────────────────────
    print_divider()
    print("FULL SCHEMA VALIDATION")
    print_divider()

    result = validate_report_structure(output_text)
    print(f"  Valid:                {result['valid']}")
    print(f"  Annotation coverage:  {result['annotation_coverage']}")
    print(f"  Total annotations:    {result['total_annotations']}")

    if result['issues']:
        print(f"\n  Issues:")
        for issue in result['issues']:
            print(f"    - {issue}")
    else:
        print("\n  No issues detected.")

    # ── Summary ───────────────────────────────────────────────────────────────
    print_divider("=")
    print("VERIFICATION SUMMARY")
    print_divider("=")
    passed = all_present and counts["total"] > 0 and result["valid"]
    print(f"\n  Sections:    {'PASS' if all_present else 'FAIL'}")
    print(f"  Annotations: {'PASS' if counts['total'] > 0 else 'FAIL'}")
    print(f"  Schema:      {'PASS' if result['valid'] else 'FAIL'}")
    print(f"\n  Overall: {'VERIFIED — output conforms to LexisAI schema' if passed else 'ISSUES DETECTED'}")
    print()


def main():
    example_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    if example_id == 0:
        # Run all examples
        for i in range(1, 3):
            verify_example(i)
    else:
        verify_example(example_id)

    print("To verify all examples: python scripts/reproduce_example.py 0")


if __name__ == "__main__":
    main()
