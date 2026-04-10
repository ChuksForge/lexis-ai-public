# LexisAI — Evaluation Methodology

## Why Evals Exist

A research synthesis agent that cannot be evaluated cannot be trusted.
LexisAI's evaluation suite exists to answer one question:

**Does the output actually do what it claims to do?**

This means checking three things independently:
1. Does the report follow the required structure?
2. Are claims correctly annotated with their sources?
3. Is the synthesis genuinely cross-source, or just sequential summaries?

---

## Evaluation Dimensions

LexisAI outputs are scored across four dimensions, each weighted equally:

### 1. Structural Checks (25%)
**Method:** Hardcoded string matching
**What it verifies:** Required sections and elements are present

Checks include:
- `📋 RESEARCH BRIEF` present
- `🔍 DEEP DIVE` header present
- All 7 numbered sections present
- Insight Ranking table present
- Research question stated in brief

This is deterministic — pass/fail per element, no model judgment involved.

### 2. Structure Compliance (25%)
**Method:** LLM-as-judge with explicit rubric
**What it verifies:** Sections are correctly formatted, not just present

Rubric:
- 10: All sections present, correctly formatted
- 7–9: All sections present, minor formatting deviations
- 4–6: Most sections present, some missing or malformed
- 1–3: Major sections missing
- 0: Output does not resemble required format

### 3. Annotation Accuracy (25%)
**Method:** LLM-as-judge with explicit rubric
**What it verifies:** Claims are correctly tagged throughout the report

Rubric criteria:
- Every specific factual claim tagged with source
- `[inferred]` used for claims beyond provided sources
- `[general knowledge]` used for training-based claims
- No source tags used for sources not provided
- No untagged claims present

### 4. Synthesis Quality (25%)
**Method:** LLM-as-judge with 6 sub-criteria
**What it verifies:** The report is genuine synthesis, not sequential summaries

Sub-criteria (equal weight within dimension):

| Criterion | What It Checks |
|---|---|
| Question answered | Does synthesis statement address the research question? |
| Source integration | Are sources synthesized across, not summarized in sequence? |
| Contradiction handling | Are contradictions surfaced and explained? |
| Evidence weighting | Are insights ranked by evidential strength? |
| Uncertainty acknowledgement | Are gaps and limits stated honestly? |
| Actionability | Do next steps follow from the findings? |

---

## Test Cases

The public eval suite includes 5 test cases covering the primary input scenarios:

| ID | Scenario | Primary Assertion |
|---|---|---|
| TC01 | Single high-quality source + clear question | `[S1]` used correctly, no fabricated tags |
| TC02 | Two directly contradicting sources | Contradiction section populated, divergence explained |
| TC03 | Research question only — no sources | All claims `[general knowledge]`, no `[S1]` present |
| TC04 | High-quality source + low-quality blog | Low quality source flagged, claims weighted accordingly |
| TC05 | Three sources — full synthesis | All three annotated, convergence and gaps both identified |

Full test case definitions: [`evals_public/test_cases_public.py`](../evals_public/test_cases_public.py)

---

## Score Interpretation

| Range | Rating | Recommended Action |
|---|---|---|
| 8.0 – 10.0 | Strong | Production-grade output |
| 6.0 – 7.9 | Moderate | Acceptable — investigate lowest-scoring dimension |
| 4.0 – 5.9 | Needs work | Structural or annotation failures present |
| 0.0 – 3.9 | Failing | Significant issues — review prompt or model |

---

## Sample Results

Real eval run results are published in [`examples/eval_runs/`](../examples/eval_runs/).

Each result file contains:
- Per-case scores across all four dimensions
- LLM judge reasoning per dimension
- The full generated report for each test case
- Suite-level summary score

---

## LLM-as-Judge Variance

LLM-as-judge scoring is directionally reliable but not deterministic.
Expect ±0.5 score variation across identical runs due to model temperature.

Recommendations:
- Run the eval suite at least 3 times and average scores before drawing conclusions
- Use trend analysis across multiple runs rather than individual scores
- Treat scores below 6.0 on any dimension as a reliable signal of issues
- Do not make prompt changes based on a single eval run

---

## What the Evals Do Not Measure

- Factual accuracy of the underlying model's general knowledge
- Quality of web search results (external dependency)
- Relevance of suggested next steps to a specific user's goals
- Whether the research question itself was well-formed
- Performance on inputs significantly different from the 5 test cases
