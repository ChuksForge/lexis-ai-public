# stubs/source_labeller_stub.py
# LexisAI Source Labeller Stub

def label_sources(user_input: str) -> dict:
    """
    Stub implementation of label_sources().

    Detects rough source count from input formatting and returns
    a plausible static response. Does not call any API.

    Args:
        user_input: Combined input string

    Returns:
        Static example of the label_sources() output format.
    """
    # Rough heuristic for demo purposes
    source_count = user_input.count("--- UPLOADED FILE") + \
                   user_input.count("--- SOURCE") + \
                   user_input.count("--- PASTED TEXT")

    source_count = max(source_count, 1 if user_input.strip() else 0)

    sources = []
    for i in range(1, source_count + 1):
        sources.append({
            "id": f"S{i}",
            "type": "unknown",
            "title_or_description": f"Source {i} — detected from input",
            "apparent_author": None,
            "apparent_date": None,
            "quality_signal": "unknown",
            "quality_note": "Stub — real labeller classifies quality from content"
        })

    return {
        "sources": sources,
        "source_count": source_count,
        "research_question_stated": "?" in user_input or "what" in user_input.lower(),
        "analytical_lens_stated": "lens" in user_input.lower() or
                                  "perspective" in user_input.lower()
    }
