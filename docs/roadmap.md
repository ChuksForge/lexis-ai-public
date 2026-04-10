# LexisAI — Roadmap

## Shipped

| Feature | Description |
|---|---|
| PDF/DOCX/TXT upload | Multi-file upload with per-format text extraction |
| Markdown + PDF export | Sidebar and inline export, timestamped filenames |
| Live web search | Anthropic-native tool, agent-decided trigger |
| Streamlit UI | Replaced Gradio — native session state, no rerun conflicts |
| LLM-as-judge eval suite | 5 test cases, 4 dimensions, Streamlit dashboard |
| Multi-provider support | Anthropic / OpenAI / OpenRouter via `.env` |
| Hybrid model routing | Haiku/Sonnet selected by input complexity and length |

---

## Planned

| Priority | Feature | Description |
|---|---|---|
| High | OCR for scanned PDFs | Tesseract integration — enables scanned document input |
| High | Persistent sessions | Save and resume research sessions across browser closes |
| Medium | Critic agent | Second agent stress-tests Synthesizer output pre-delivery |
| Medium | Tavily web search | Drop-in replacement for Anthropic search on other providers |
| Low | Multi-language support | Source material and output in languages beyond English |
| Low | Citation export | APA/MLA/Chicago formatted citation list from report sources |

---

## Not Planned

The following are out of scope for LexisAI:

- Statistical analysis or quantitative data processing
- Real-time collaboration or shared sessions
- Integration with specific academic databases (JSTOR, PubMed, etc.)
- A mobile application
- A browser extension

---
