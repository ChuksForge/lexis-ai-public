# LexisAI — Known Limitations

This document describes known constraints and tradeoffs in LexisAI's current
implementation. It is written to be accurate and complete, not reassuring.

---

## Input Constraints

**PDF extraction quality varies.**
PyMuPDF extracts embedded text from PDFs page by page. Scanned PDFs — those
produced by photographing a physical document — contain images rather than
embedded text. Extraction from scanned PDFs produces empty or garbled output.
OCR is not currently implemented. Text-layer PDFs from most academic publishers,
government sources, and modern office software extract cleanly.

**Context window limits apply.**
Very long documents may be truncated by the model's context window. The exact
limit depends on the model in use. As a practical guideline, documents over
100 pages should be split before uploading. The agent does not warn when
truncation occurs — this is a known gap.

**No persistent file storage.**
Uploaded files and conversation history exist only for the duration of a
Streamlit session. Closing the browser tab or refreshing the page resets all
state. There is no database persistence between sessions.

---

## Synthesis Constraints

**Quality depends on source quality.**
LexisAI synthesizes what it is given. If the input sources are low quality,
the synthesis will be low quality regardless of how well the agent performs.
The quality signal system flags low-quality sources but cannot compensate for
them. Garbage in, garbage out — this is not a limitation of the agent, it is
a constraint of the problem.

**General knowledge claims are unverifiable.**
When the agent draws on `[general knowledge]` rather than provided sources,
those claims come from the underlying model's training data. That training data
has a cutoff date and contains errors. Claims flagged `[general knowledge]`
should be independently verified before being cited or acted on.

**Annotation is a best-effort guarantee.**
The annotation system (`[S1]`, `[inferred]`, etc.) is enforced by prompt
instruction, not by deterministic code. In rare cases — particularly with
very long or complex multi-source inputs — the agent may miss an annotation
or apply one incorrectly. The eval suite measures annotation accuracy; current
scores reflect the realistic error rate.

---

## Web Search Constraints

**Web search is Anthropic-native.**
The `web_search_20250305` tool is specific to the Anthropic API. When using
OpenAI or OpenRouter as the LLM provider, web search is not available without
integrating a third-party search API (Tavily recommended).
The agent falls back to standard research mode automatically.

**Web source quality is not guaranteed.**
The agent applies quality signals to web sources found during search, but has
no control over what the search tool returns. Authoritative and low-quality
sources may both appear in results. The quality assessment is a best-effort
classification, not a verified ranking.

**Search capping at 4 calls.**
The `max_uses: 4` cap on search calls limits the agent to approximately 5–10
web sources per session turn. For research questions requiring broader coverage,
the user should provide sources directly rather than relying solely on search.

---

## Evaluation Constraints

**LLM-as-judge scores have variance.**
Scores are directionally reliable but not deterministic. Expect ±0.5 variation
across identical runs. Use trend analysis across multiple runs rather than
individual scores for prompt decisions.

**5 test cases is a narrow baseline.**
The public eval suite covers the primary input scenarios but does not cover
all edge cases. Unusual inputs — very long sources, highly technical material,
sources in non-English languages — are not represented in the test suite.
Performance on out-of-distribution inputs is not guaranteed.

**Self-evaluation risk.**
LLM-as-judge uses the same model family for both generation and evaluation.
This introduces a potential blind spot — systematic errors in the generation
model may not be caught by the evaluation model. This is a known limitation
of the approach at this scale.

---

## Export Constraints

**PDF export requires GTK on Windows.**
WeasyPrint depends on the GTK3 runtime, which is not bundled with Python on
Windows. Installation is a manual prerequisite step. Without it, PDF export
fails with an error; Markdown export is unaffected.

**PDF rendering varies by platform.**
The WeasyPrint stylesheet is developed and tested on Ubuntu. Minor rendering
differences (font rendering, spacing) may appear on macOS and Windows due to
differences in the GTK and font rendering stack.

---

## What LexisAI Does Not Do

- It does not access proprietary databases, paywalled journals, or internal
  knowledge bases
- It does not perform statistical analysis on quantitative data
- It does not generate or interpret data visualizations
- It does not produce academic citations in standard formats (APA, MLA, etc.)
- It does not verify claims against external fact-checking sources
- It does not support real-time collaboration or shared sessions
