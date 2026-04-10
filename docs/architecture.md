# LexisAI — System Architecture

## Overview

LexisAI is a research synthesis agent built on a two-prompt architecture.
Input processing, source labelling, synthesis, and export are separated into
distinct components — each independently testable and replaceable.

---

## High-Level Flow

```
User Input (files + text + research question)
        │
        ▼
Input Processing Layer
  PDF  ──► text extraction (PyMuPDF)
  DOCX ──► text extraction (python-docx)
  TXT  ──► direct read (pathlib)
  Paste──► direct pass
  All sources merged → single structured input string
        │
        ▼
Pre-Pass: Source Labeller
  Lightweight API call → structured JSON
  Assigns: S1, S2, S3...
  Classifies: type | quality signal | author | date
        │
        ├─────────────────────────────────┐
        │                                 │
        ▼                                 ▼
  research()                   research_with_search()
  Standard mode                Web search mode
  Provided sources only        Agent decides whether to search
        │                                 │
        └──────────────┬──────────────────┘
                       │
                       ▼
               Main Agent: LexisAI

               Phase 1 — Scoping
                 Identify research question
                 Label sources [S1][S2] or [WEB-1][WEB-2]
                 Identify analytical lens
                 Output: Research Brief

               Phase 2 — Report
                 Overview
                 Key Themes & Findings (annotated)
                 Cross-Source Analysis
                 Insight Ranking
                 Open Questions
                 Synthesis Statement
                 Suggested Next Steps

               Phase 3 — Drill-Down
                 Multi-turn conversation on the report
                 New sources integrated and re-labelled
                       │
               ┌───────┴───────┐
               │               │
               ▼               ▼
         Export System    Evaluation System
         Markdown + PDF   5 test cases
         On-demand        4 scoring dimensions
         Cached bytes     JSON + dashboard
```

---

## Two-Prompt Design

LexisAI uses two distinct prompts rather than one monolithic system prompt.

**Source Labeller** — runs first as a cheap pre-pass. Returns structured JSON:
source IDs, types, quality signals, author, date. This happens before the main
prompt touches the material.

**Main Agent** — receives the labelled, structured input and runs the full
synthesis pipeline. It never needs to do source extraction — that work is
already done.

This separation means:
- Each component is independently testable
- The Source Labeller can be swapped without touching agent logic
- The main prompt receives clean, structured input every time
- Failures in one step are isolated from the other

---

## Mode Separation

`research()` and `research_with_search()` are distinct functions with distinct
system prompts. Web search is not a flag on the base function — it is a
separate execution path with its own prompt addendum, tool configuration,
and response parsing logic.

When web search is used, the agent applies this decision logic:

```
No sources provided      → search for 5–10 relevant sources
Sources thin/low quality → supplement with web search
Sources sufficient       → synthesize directly, skip search
```

Web sources are labelled `[WEB-1]`, `[WEB-2]` — always distinct from
user-provided `[S1]`, `[S2]`. The two namespaces never mix.

---

## State Management

The Streamlit UI follows a state-before-render pattern. All input processing
and API calls complete and write to `session_state` before the chat render
loop runs. This avoids the rerun conflicts that cause blank pages and frozen
inputs in Streamlit chat applications.

Export bytes are generated on-demand and cached in `session_state` after
first generation. WeasyPrint (PDF) is never called during a render pass —
only when the user explicitly clicks "Prepare PDF".

---

## Component Responsibilities

| Component | File | Responsibility |
|---|---|---|
| Core agent | `lexis_ai.py` (private) | Prompts, orchestration, API calls |
| LLM client | `llm_client.py` (private) | Provider abstraction |
| UI | `ui.py` (private) | Streamlit interface, session state |
| Exporter | `exporter.py` (private) | Markdown + PDF generation |
| Eval runner | `evals/runner.py` (private) | Test execution, result saving |
| Eval judges | `evals/judges.py` (private) | LLM-as-judge scoring prompts |
| Public SDK | `lexisai/client.py` (public) | Clean interface for external use |
| Interfaces | `interfaces/` (public) | Behavioral contracts |
| Stubs | `stubs/` (public) | Runnable placeholders |

---

## Provider Abstraction

LexisAI supports three LLM providers via a unified client layer.
Provider selection requires only `.env` changes — no code modifications.

```
.env: LLM_PROVIDER=anthropic|openai|openrouter
         │
         ▼
llm_client.py → chat()
         │
         ├── _chat_anthropic()     Anthropic SDK
         └── _chat_openai_compat() OpenAI SDK (also covers OpenRouter)
```

Web search uses Anthropic's native tool. On other providers, a
third-party search API (Tavily) is required as a replacement.
