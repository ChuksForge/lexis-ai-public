# interfaces/exporter_interface.py
# LexisAI Exporter Interface — Export Abstraction
#
# Defines the contract for report export implementations.
# The production system supports Markdown and PDF via WeasyPrint.
# Additional formats (DOCX, HTML) can be added by implementing this interface.

from abc import ABC, abstractmethod


class ExporterInterface(ABC):
    """
    Abstract interface for LexisAI report exporters.

    Implementations:
        - MarkdownExporter  (production, private) — outputs .md files
        - PDFExporter       (production, private) — outputs .pdf via WeasyPrint
        - StubExporter      (stubs/)              — returns static example bytes
    """

    @abstractmethod
    def export(
        self,
        messages: list[dict],
        include_followups: bool = False
    ) -> tuple[bytes, str]:
        """
        Export a research session to bytes.

        Args:
            messages:          Chat display messages in format:
                               [{"role": "user"|"assistant", "content": str}]
            include_followups: Whether to include follow-up Q&A after the
                               main report (default False)

        Returns:
            Tuple of:
                bytes:    Export content as bytes
                filename: Suggested filename with extension
                          Format: lexis_ai_{slug}_{timestamp}.{ext}

        Guarantees:
            - Always returns valid bytes (never raises on content issues)
            - Filename is filesystem-safe (no special characters)
            - Timestamp in filename is UTC ISO format: YYYYMMDD_HHMMSS
            - Slug derived from research question in the report
        """
        ...

    @abstractmethod
    def get_mime_type(self) -> str:
        """
        Return the MIME type for this export format.

        Examples:
            "text/markdown"
            "application/pdf"
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        """
        ...

    @abstractmethod
    def get_extension(self) -> str:
        """
        Return the file extension for this export format (without dot).

        Examples: "md", "pdf", "docx"
        """
        ...


class StubExporter(ExporterInterface):
    """
    Stub exporter — returns the content of a pre-generated example report.
    Used in the public SDK for demonstration purposes.
    """

    def __init__(self, fmt: str = "md"):
        self.fmt = fmt

    def export(
        self,
        messages: list[dict],
        include_followups: bool = False
    ) -> tuple[bytes, str]:
        example_path = f"examples/outputs/report_1.{self.fmt}"
        try:
            with open(example_path, "rb") as f:
                content = f.read()
        except FileNotFoundError:
            content = b"# LexisAI Example Report\n\nExample content."
        return content, f"lexis_ai_example_report.{self.fmt}"

    def get_mime_type(self) -> str:
        return "text/markdown" if self.fmt == "md" else "application/pdf"

    def get_extension(self) -> str:
        return self.fmt
