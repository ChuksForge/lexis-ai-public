# lexis_ai/schemas.py
# LexisAI Output Schema Definitions

from __future__ import annotations
from dataclasses import dataclass, field
import re


REQUIRED_SECTIONS = [
    "RESEARCH BRIEF",
    "DEEP DIVE",
    "OVERVIEW",
    "KEY THEMES",
    "CROSS-SOURCE ANALYSIS",
    "Points of Agreement",
    "Points of Contradiction",
    "Gaps in the Evidence",
    "INSIGHT RANKING",
    "OPEN QUESTIONS",
    "SYNTHESIS STATEMENT",
    "SUGGESTED NEXT STEPS"
]

ANNOTATION_TAGS = [
    r"\[S\d+\]",          # [S1], [S2], [S3]...
    r"\[WEB-\d+\]",       # [WEB-1], [WEB-2]...
    r"\[inferred\]",
    r"\[general knowledge\]"
]


@dataclass
class SourceEntry:
    """A single source as identified in the Research Brief."""
    id: str                    # e.g. "S1", "WEB-2"
    source_type: str           # article, paper, blog, transcript, notes, web
    description: str           # title or description
    quality_signal: str        # high, medium, low, unknown
    is_web_source: bool = False


@dataclass
class InsightRankingEntry:
    """A single row in the Insight Ranking table."""
    rank: int
    insight: str
    evidence_strength: str     # Strong, Moderate, Weak
    sources: list[str]         # list of source IDs


@dataclass
class CrossSourceAnalysis:
    """The cross-source analysis section."""
    points_of_agreement: list[str] = field(default_factory=list)
    points_of_contradiction: list[str] = field(default_factory=list)
    gaps_in_evidence: list[str] = field(default_factory=list)


@dataclass
class ResearchBrief:
    """The Research Brief section."""
    question: str
    sources: list[SourceEntry] = field(default_factory=list)
    lens: str = "Balanced multi-perspective"
    scope_note: str = ""


@dataclass
class ResearchReport:
    """
    A complete LexisAI research report.

    This is the top-level output object. All synthesis engine outputs —
    stub and full — must be expressible as a ResearchReport instance.
    """
    question: str
    brief: ResearchBrief | None = None
    overview: str = ""
    themes: list[dict] = field(default_factory=list)
    cross_source: CrossSourceAnalysis | None = None
    insight_ranking: list[InsightRankingEntry] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    synthesis_statement: str = ""
    suggested_next_steps: list[str] = field(default_factory=list)
    raw_markdown: str = ""

    @classmethod
    def from_markdown(cls, markdown: str, question: str = "") -> "ResearchReport":
        """
        Parse a markdown report string into a ResearchReport object.
        This is a best-effort parser for the fixed LexisAI output schema.
        """
        return cls(
            question=question,
            raw_markdown=markdown,
            synthesis_statement=cls._extract_section(
                markdown, "SYNTHESIS STATEMENT"
            ),
            overview=cls._extract_section(markdown, "OVERVIEW"),
        )

    @staticmethod
    def _extract_section(text: str, section_name: str) -> str:
        """Extract content following a section header."""
        pattern = rf"###?\s+\d*\.?\s*{re.escape(section_name)}\s*\n(.*?)(?=###|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    @staticmethod
    def schema() -> dict:
        """Return the output schema as a dictionary."""
        return {
            "version": "1.0.0",
            "required_sections": REQUIRED_SECTIONS,
            "annotation_tags": [t.replace("\\", "") for t in ANNOTATION_TAGS],
            "source_namespaces": {
                "user_provided": "[S1], [S2], [S3]...",
                "web_search": "[WEB-1], [WEB-2]...",
                "inferred": "[inferred]",
                "general_knowledge": "[general knowledge]"
            },
            "insight_ranking": {
                "columns": ["Rank", "Insight", "Evidence Strength", "Source(s)"],
                "evidence_strength_values": ["Strong", "Moderate", "Weak"]
            },
            "cross_source_analysis": {
                "required_subsections": [
                    "Points of Agreement",
                    "Points of Contradiction",
                    "Gaps in the Evidence"
                ]
            }
        }
