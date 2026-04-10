# lexis_ai/client.py
# LexisAI Public SDK — Entry Point

from __future__ import annotations
from lexis_ai.schemas import ResearchReport
from lexis_ai.types import Source


class LexisAIClient:
    """
    Public interface to the LexisAI research synthesis agent.

    Usage:
        from lexis_ai import LexisAIClient

        client = LexisAIClient()
        report = client.synthesize(
            question="What is the impact of sleep deprivation on cognition?",
            sources=["path/to/source1.pdf", "path/to/source2.txt"]
        )
        print(report.synthesis_statement)
    """

    def __init__(self, use_stubs: bool = True):
        """
        Initialise the LexisAI client.

        Args:
            use_stubs: If True (default in public SDK), returns pre-generated
                       example outputs. 
        """
        self.use_stubs = use_stubs

    def synthesize(
        self,
        question: str,
        sources: list[str] | None = None,
        pasted_text: str | None = None,
        lens: str | None = None,
        web_search: bool = False
    ) -> ResearchReport:
        """
        Synthesize a research report from provided sources and question.

        Args:
            question:    The research question to answer
            sources:     List of file paths (PDF, DOCX, TXT)
            pasted_text: Raw text content to include as a source
            lens:        Optional analytical lens (e.g. "economic perspective")
            web_search:  If True, agent may search the web for additional sources

        Returns:
            ResearchReport object with all sections populated

        Raises:
            NotImplementedError: When use_stubs=False and no engine is connected
        """
        if self.use_stubs:
            return self._stub_synthesize(question, sources, pasted_text)
        else:
            raise NotImplementedError(
                "Full synthesis engine is not available in the public SDK. "
            )

    def _stub_synthesize(
        self,
        question: str,
        sources: list[str] | None,
        pasted_text: str | None
    ) -> ResearchReport:
        """Return a pre-generated example report."""
        from stubs.research_stub import get_example_report
        raw = get_example_report()
        return ResearchReport.from_markdown(raw, question=question)

    def get_schema(self) -> dict:
        """Return the output schema definition."""
        return ResearchReport.schema()

    def validate_report(self, report_text: str) -> dict:
        """
        Validate a report string against the LexisAI output schema.

        Returns a dict with:
            valid: bool
            missing_sections: list[str]
            annotation_coverage: float  (0.0 - 1.0)
        """
        from lexis_ai.utils import validate_report_structure
        return validate_report_structure(report_text)
