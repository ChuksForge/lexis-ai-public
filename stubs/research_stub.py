# stubs/research_stub.py
# LexisAI Research Stub

import os
from pathlib import Path

EXAMPLES_DIR = Path(__file__).parent.parent / "examples" / "outputs"


def get_example_report(example_id: int = 1) -> str:
    """
    Return a pre-generated example report.

    Args:
        example_id: Which example to return (1, 2, or 3)

    Returns:
        Report content as a string.
    """
    filename = f"report_{example_id}.md"
    filepath = EXAMPLES_DIR / filename

    if filepath.exists():
        return filepath.read_text(encoding="utf-8")

    # Fallback minimal example if file not found
    return _minimal_example()


def research(input_text: str, conversation_history: list | None = None) -> str:
    """
    Stub implementation of research().

    Args:
        input_text:            Combined input (sources + question)
        conversation_history:  Ignored in stub — real engine uses this for
                               multi-turn conversation support

    Returns:
        Pre-generated example report as a markdown string.
    """
    print("[LexisAI Stub] research() called")
    print("[LexisAI Stub] Returning pre-generated example output.")
    return get_example_report(example_id=1)


def research_with_search(
    input_text: str,
    conversation_history: list | None = None
) -> tuple[str, list[dict]]:
    """
    Stub implementation of research_with_search().

    Returns a pre-generated example report with example web sources.
    The real implementation searches the web and synthesizes live results.
    """
    print("[LexisAI Stub] research_with_search() called")
    print("[LexisAI Stub] Returning pre-generated example output.")

    report = get_example_report(example_id=2)
    example_sources = [
        {
            "title": "Example Source — Nature (2023)",
            "url": "https://www.nature.com/example"
        },
        {
            "title": "Example Source — NEJM (2022)",
            "url": "https://www.nejm.org/example"
        }
    ]
    return report, example_sources


def _minimal_example() -> str:
    return """## 📋 RESEARCH BRIEF
**Question:** What is the impact of sleep deprivation on cognitive performance?
**Sources:** None provided
**Lens:** Balanced multi-perspective
**Scope note:** This is a stub example. All claims are flagged [general knowledge].

---

## 🔍 DEEP DIVE: Impact of Sleep Deprivation on Cognitive Performance

### 1. OVERVIEW
Sleep deprivation is one of the most studied environmental factors affecting
human cognition [general knowledge]. The field distinguishes between acute
total sleep deprivation and chronic partial restriction [general knowledge].

### 2. KEY THEMES & FINDINGS

#### Theme 1: Attention and Vigilance
Sustained attention is the cognitive domain most consistently impaired by
sleep deprivation [general knowledge]. Even moderate restriction produces
measurable performance decrements [general knowledge].

### 3. CROSS-SOURCE ANALYSIS

#### Points of Agreement
- Sleep deprivation impairs attention — [general knowledge]

#### Points of Contradiction
- No contradictions identified in this example.

#### Gaps in the Evidence
- This is a stub with no real sources. Provide sources for real synthesis.

### 4. INSIGHT RANKING

| Rank | Insight | Evidence Strength | Source(s) |
|------|---------|-------------------|-----------|
| 1 | Attention is most immediately affected | Strong | [general knowledge] |

### 5. OPEN QUESTIONS
- What is the minimum sleep duration before cognitive deficits appear?

### 6. SYNTHESIS STATEMENT
This is a stub output demonstrating the LexisAI report structure. The real
synthesis engine produces fully sourced, cross-source analysis from provided
material. [general knowledge]

### 7. SUGGESTED NEXT STEPS
- Provide source material to generate a real synthesis report
"""
