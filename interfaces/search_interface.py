# interfaces/search_interface.py
# LexisAI Search Interface — Web Search Abstraction
#
# This defines the contract for any web search implementation.
# The production system uses Anthropic's native web_search_20250305 tool.
# Non-Anthropic providers can implement this interface using Tavily or
# another search API.

from abc import ABC, abstractmethod


class SearchInterface(ABC):
    """
    Abstract interface for web search capability in LexisAI.

    Implementations:
        - AnthropicSearch  (production, private) — uses web_search_20250305
        - TavilySearch     (optional)            — for non-Anthropic providers
        - StubSearch       (stubs/)              — returns static example results
    """

    @abstractmethod
    def search(self, query: str, max_results: int = 8) -> list[dict]:
        """
        Execute a web search query.

        Args:
            query:       Search query string
            max_results: Maximum number of results to return (default 8)

        Returns:
            List of result dicts, each containing:
            {
                "title":   str,   # Page title
                "url":     str,   # Full URL
                "snippet": str,   # Short text excerpt
                "content": str    # Longer extracted content (if available)
            }

        Guarantees:
            - Returns an empty list on failure (never raises)
            - Results ordered by relevance
            - Each result contains at minimum: title and url
        """
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check whether the search backend is available and configured.

        Returns:
            True if search can be performed, False otherwise.
            Used to decide whether to fall back to standard research().
        """
        ...


class StubSearch(SearchInterface):
    """
    Stub search implementation — returns static example results.
    Used in the public SDK for demonstration purposes.
    """

    def search(self, query: str, max_results: int = 8) -> list[dict]:
        return [
            {
                "title": "Example Search Result — Nature (2023)",
                "url": "https://www.nature.com/example",
                "snippet": "This is an example search result for demonstration purposes.",
                "content": "Full content would appear here in a real search result."
            },
            {
                "title": "Example Research Paper — NEJM (2022)",
                "url": "https://www.nejm.org/example",
                "snippet": "Another example result demonstrating the search interface.",
                "content": "Full content would appear here in a real search result."
            }
        ][:max_results]

    def is_available(self) -> bool:
        return True
