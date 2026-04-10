# lexis_ai/types.py
# LexisAI Type Definitions

from enum import Enum


class AnnotationTag(str, Enum):
    """Valid annotation tag types in LexisAI reports."""
    SOURCE = "source"           # [S1], [S2] etc.
    WEB = "web"                 # [WEB-1], [WEB-2] etc.
    INFERRED = "inferred"       # [inferred]
    GENERAL = "general_knowledge"  # [general knowledge]


class EvidenceStrength(str, Enum):
    """Evidence strength levels used in Insight Ranking."""
    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"


class SourceType(str, Enum):
    """Source type classifications."""
    ARTICLE = "article"
    PAPER = "paper"
    BLOG = "blog"
    TRANSCRIPT = "transcript"
    NOTES = "notes"
    WEB = "web"
    UNKNOWN = "unknown"


class QualitySignal(str, Enum):
    """Source quality signals."""
    HIGH = "high"       # peer-reviewed, established publication, primary source
    MEDIUM = "medium"   # reputable outlet, expert blog, industry report
    LOW = "low"         # anonymous, undated, anecdotal, unsupported claims
    UNKNOWN = "unknown"


class Source(str, Enum):
    """Source namespace prefixes."""
    USER = "S"      # user-provided sources: S1, S2, S3
    WEB = "WEB"     # web search sources: WEB-1, WEB-2
