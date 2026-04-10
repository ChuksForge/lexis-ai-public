# LexisAI — Synthesis Methodology

## What LexisAI Does

LexisAI synthesizes research sources into structured reports. The output is
not a summary of each source in sequence — it is a cross-source analysis
that identifies what sources agree on, where they contradict each other,
and what questions they leave unanswered.

---

## Core Principles

### 1. Every Claim Is Annotated

Every factual claim in a LexisAI report is tagged at the point of use:

| Tag | Meaning |
|---|---|
| `[S1]`, `[S2]` | Directly traceable to a user-provided source |
| `[WEB-1]`, `[WEB-2]` | Traceable to a web search result |
| `[inferred]` | Logical inference beyond the provided sources |
| `[general knowledge]` | Drawn from model training — not provided material |

No claim is presented as sourced if it is not in the provided material.
This is a hard constraint, not a soft guideline.

### 2. Source Quality Is Assessed and Disclosed

Every source is assigned a quality signal before synthesis begins:

| Signal | Criteria |
|---|---|
| High | Peer-reviewed, established publication, primary source |
| Medium | Reputable outlet, expert blog, industry report |
| Low | Anonymous, undated, anecdotal, unsupported claims |
| Unknown | Cannot be determined from available content |

Low-quality sources are flagged in the Research Brief. Their claims are
treated with proportionally lower confidence in the Insight Ranking.

### 3. Contradiction Is a Primary Finding

When two sources disagree, LexisAI does not average them, weight one over
the other silently, or omit the disagreement.

The Cross-Source Analysis section has a dedicated contradiction subsection.
Every contradiction is:
- Stated explicitly: "[S1] argues X. [S2] argues Y."
- Explained in one sentence: the most likely reason for the divergence
  (methodology, timeframe, population, perspective, funding source)

Unresolved contradictions between credible sources are often the most
important finding in a research synthesis. Hiding them is a failure.

### 4. Uncertainty Is Scoped Explicitly

The Synthesis Statement is written to the level of the evidence:

- Strong evidence → direct conclusion
- Moderate evidence → hedged conclusion ("suggests", "indicates")
- Weak evidence → acknowledged limitation ("insufficient evidence to conclude")
- Contradictory evidence → acknowledged irresolution

The agent is explicitly prohibited from overstating conclusions. Phrases
like "proves", "confirms", and "definitively shows" are not used unless
the evidence actually supports them.

### 5. Insight Ranking Is Evidence-Weighted

The Insight Ranking table orders findings by evidential strength — not by
how interesting or surprising they are. An insight supported by two
high-quality sources that agree ranks above an insight from a single
low-quality source, regardless of the insight's apparent significance.

---

## Report Structure Rationale

Each section of the LexisAI report exists for a specific reason:

| Section | Why It Exists |
|---|---|
| Research Brief | Forces explicit scoping before analysis — prevents scope creep |
| Overview | Frames the problem space — gives context for the findings |
| Key Themes | Organises findings thematically, not source-by-source |
| Cross-Source Analysis | Makes agreement, contradiction, and gaps explicit |
| Insight Ranking | Forces prioritisation — not all findings are equal |
| Open Questions | Surfaces what the sources do NOT answer — often most useful |
| Synthesis Statement | Single defensible answer to the research question |
| Suggested Next Steps | Converts analysis into action |

---

## What LexisAI Does Not Do

- It does not generate citations for sources it has not seen
- It does not smooth over contradictions between sources
- It does not present inferences as facts
- It does not provide a confident conclusion when the evidence is thin
- It does not search the web unless explicitly enabled by the user
- It does not take sides on contested empirical or normative questions

---

## Source Labelling System

Sources are labelled before synthesis begins, in a separate pre-pass:

```
User input
    │
    ▼
Source Labeller (pre-pass)
    │
    ├── Identifies each distinct source
    ├── Assigns label: S1, S2, S3... (user-provided)
    │                  WEB-1, WEB-2... (web search)
    ├── Classifies: type, quality, author, date
    └── Returns structured JSON
    │
    ▼
Main synthesis prompt receives clean, labelled input
```

This separation keeps the main synthesis prompt focused on analysis rather
than extraction. It also makes source labelling independently testable.
