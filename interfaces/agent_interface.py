# interfaces/agent_interface.py
# LexisAI Agent Interface — Expected Behavior Contract
#
# This defines the behavioral contract for the LexisAI core agent.
# Any implementation — stub, mock, or production — must satisfy this interface.

from abc import ABC, abstractmethod


class AgentInterface(ABC):
    """
    Abstract interface for the LexisAI research synthesis agent.

    The production implementation of this interface is proprietary.
    The stub implementation in stubs/research_stub.py returns pre-generated
    example outputs.
    """

    @abstractmethod
    def research(
        self,
        user_input: str,
        conversation_history: list[dict]
    ) -> str:
        """
        Synthesize a research report from provided input.

        Args:
            user_input:            Combined input string — sources + question
            conversation_history:  Prior conversation turns for multi-turn support

        Returns:
            Full report as a markdown string conforming to the LexisAI schema.

        Guarantees:
            - Output contains all required sections (see schemas.REQUIRED_SECTIONS)
            - Every factual claim is annotated [S1], [inferred], or [general knowledge]
            - No claim is presented as sourced if not in the provided material
            - Synthesis statement is scoped to the level of the evidence
        """
        ...

    @abstractmethod
    def research_with_search(
        self,
        user_input: str,
        conversation_history: list[dict]
    ) -> tuple[str, list[dict]]:
        """
        Synthesize a research report with optional live web search.

        The agent decides autonomously whether to search based on:
        - Whether sources were provided
        - Quality and sufficiency of provided sources

        Args:
            user_input:            Combined input string — sources + question
            conversation_history:  Prior conversation turns

        Returns:
            Tuple of:
                report:      Full report markdown string
                web_sources: List of {title: str, url: str} dicts found via search
                             Empty list if search was not used.

        Guarantees (in addition to research() guarantees):
            - Web-sourced claims annotated [WEB-1], [WEB-2] etc.
            - User-provided source tags [S1], [S2] never mixed with [WEB-N]
            - Research Brief states whether web search was used
            - If search skipped: scope note confirms "sufficient sources provided"
        """
        ...

    @abstractmethod
    def label_sources(self, user_input: str) -> dict:
        """
        Extract and label sources from raw input.

        Args:
            user_input: Raw combined input string

        Returns:
            JSON-serialisable dict with structure:
            {
                "sources": [
                    {
                        "id": "S1",
                        "type": "article|paper|blog|transcript|notes|unknown",
                        "title_or_description": str,
                        "apparent_author": str | null,
                        "apparent_date": str | null,
                        "quality_signal": "high|medium|low|unknown",
                        "quality_note": str | null
                    }
                ],
                "source_count": int,
                "research_question_stated": bool,
                "analytical_lens_stated": bool
            }
        """
        ...
