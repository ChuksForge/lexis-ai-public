# lexis_ai/utils.py
# LexisAI Utility Functions — Report Validation and Parsing

import re
from lexis_ai.schemas import REQUIRED_SECTIONS, ANNOTATION_TAGS


def validate_report_structure(report_text: str) -> dict:
    """
    Validate a report string against the LexisAI output schema.

    Args:
        report_text: The full markdown report string

    Returns:
        {
            "valid": bool,
            "missing_sections": list[str],
            "annotation_coverage": float,
            "annotation_counts": dict,
            "issues": list[str]
        }
    """
    missing = []
    issues = []

    # Check required sections
    for section in REQUIRED_SECTIONS:
        if section not in report_text:
            missing.append(section)

    # Count annotation tags
    annotation_counts = {}
    total_annotations = 0
    for pattern in ANNOTATION_TAGS:
        matches = re.findall(pattern, report_text)
        tag_name = pattern.replace(r"\[", "[").replace(r"\]", "]") \
                          .replace(r"\d+", "N")
        annotation_counts[tag_name] = len(matches)
        total_annotations += len(matches)

    # Estimate annotation coverage
    # Heuristic: count sentences in body, compare to annotation count
    sentences = len(re.findall(r"[.!?]+", report_text))
    coverage = min(1.0, total_annotations / max(sentences, 1))

    if total_annotations == 0:
        issues.append("No annotation tags found — claims are not sourced")

    if missing:
        issues.append(f"Missing {len(missing)} required section(s)")

    return {
        "valid": len(missing) == 0 and total_annotations > 0,
        "missing_sections": missing,
        "annotation_coverage": round(coverage, 2),
        "annotation_counts": annotation_counts,
        "total_annotations": total_annotations,
        "issues": issues
    }


def extract_sources_from_brief(report_text: str) -> list[dict]:
    """
    Extract source list from the Research Brief section.

    Returns a list of dicts: {id, description}
    """
    brief_match = re.search(
        r"RESEARCH BRIEF.*?\*\*Sources:\*\*\s*(.+?)(?=\*\*Lens|\Z)",
        report_text,
        re.DOTALL | re.IGNORECASE
    )
    if not brief_match:
        return []

    sources_text = brief_match.group(1).strip()
    sources = []
    for part in sources_text.split(","):
        part = part.strip()
        id_match = re.match(r"(S\d+|WEB-\d+):\s*(.+)", part)
        if id_match:
            sources.append({
                "id": id_match.group(1),
                "description": id_match.group(2).strip()
            })

    return sources


def count_annotation_tags(report_text: str) -> dict:
    """Count all annotation tags in a report."""
    counts = {
        "source_tags": len(re.findall(r"\[S\d+\]", report_text)),
        "web_tags": len(re.findall(r"\[WEB-\d+\]", report_text)),
        "inferred_tags": len(re.findall(r"\[inferred\]", report_text)),
        "general_knowledge_tags": len(
            re.findall(r"\[general knowledge\]", report_text)
        )
    }
    counts["total"] = sum(counts.values())
    return counts
