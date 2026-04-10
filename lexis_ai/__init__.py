# lexis_ai/__init__.py
# LexisAI Public SDK

from lexis_ai.client import LexisAIClient
from lexis_ai.schemas import ResearchReport, ResearchBrief, SourceEntry as SourceAnnotation
from lexis_ai.types import Source, AnnotationTag, EvidenceStrength

__version__ = "1.0.0"
__all__ = [
    "LexisAIClient",
    "ResearchReport",
    "ResearchBrief",
    "SourceAnnotation",
    "Source",
    "AnnotationTag",
    "EvidenceStrength"
]
