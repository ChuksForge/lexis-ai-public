# LexisAI — Evaluation Scoring Rubric

This rubric defines the criteria applied to every LexisAI output in the
evaluation suite. All scores are 0–10.

---

## Dimension 1: Structural Checks

**Method:** Hardcoded string matching — deterministic, no model judgment.

**Required elements** (each checked as present/absent):

| Element | Check |
|---|---|
| `📋 RESEARCH BRIEF` header | Present |
| `**Question:**` field in brief | Present |
| `**Sources:**` field in brief | Present |
| `**Lens:**` field in brief | Present |
| `**Scope :**` field in brief | Present |
| `🔍 DEEP DIVE` header | Present |
| `### 1. OVERVIEW` section | Present |
| `### 2. KEY THEMES` section | Present |
| `### 3. CROSS-SOURCE ANALYSIS` section | Present |
| `Points of Agreement` subsection | Present |
| `Points of Contradiction` subsection | Present |
| `Gaps in the Evidence` subsection | Present |
| `### 4. INSIGHT RANKING` section | Present |
| `### 5. OPEN QUESTIONS` section | Present |
| `### 6. SYNTHESIS STATEMENT` section | Present |
| `### 7. SUGGESTED NEXT STEPS` section | Present |

**Scoring:** (elements present / total elements) × 10

---

## Dimension 2: Structure Compliance

**Method:** LLM judge

**Criteria:**
- All required sections are present
- Sections appear in the correct order
- Tables are correctly formatted (Insight Ranking)
- Research Brief fields are all populated
- No sections are truncated or malformed

**Rubric:**

| Score | Meaning |
|---|---|
| 10 | All sections present, correctly ordered, correctly formatted |
| 7–9 | All sections present, minor formatting deviations |
| 4–6 | Most sections present, one or more missing or malformed |
| 1–3 | Multiple major sections missing |
| 0 | Output does not resemble the required format |

---

## Dimension 3: Annotation Accuracy

**Method:** LLM judge

**Criteria:**
- Every specific factual claim is tagged with its source
- Correct tags used: `[S1]` for provided sources, `[WEB-N]` for web sources
- `[inferred]` used for logical inferences beyond sources
- `[general knowledge]` used for training-based claims
- No source tags applied to sources not provided in the input
- No claims left untagged

**Rubric:**

| Score | Meaning |
|---|---|
| 10 | All claims correctly annotated, no unsourced claims, tags precise |
| 7–9 | Most claims annotated, minor inconsistencies (1–3 gaps) |
| 4–6 | Partial annotation — some claims untagged or incorrectly sourced |
| 1–3 | Poor annotation — many untagged claims or wrong source references |
| 0 | No annotation present |

**Special rules:**
- If no sources were provided, ALL claims must be `[general knowledge]` or `[inferred]`
- If `[S1]` appears in a report where no sources were provided: automatic 0
- Each unique untagged factual claim counts as one annotation gap

---

## Dimension 4: Synthesis Quality

**Method:** LLM judge — 6 sub-criteria, equal weight

### Sub-criterion 1: Question Answered

Does the Synthesis Statement directly address the stated research question?

| Score | Meaning |
|---|---|
| 10 | Synthesis Statement directly and completely answers the question |
| 7–9 | Answers the question with minor gaps |
| 4–6 | Partially addresses the question |
| 1–3 | Does not address the question |

### Sub-criterion 2: Source Integration

Are sources synthesized across (compared, contrasted, connected) or merely
summarized in sequence?

| Score | Meaning |
|---|---|
| 10 | Sources genuinely synthesized — findings compared across sources |
| 7–9 | Mostly synthesized, minor sequential sections |
| 4–6 | Sources summarized more than integrated |
| 1–3 | Pure sequential summaries — no cross-source analysis |

### Sub-criterion 3: Contradiction Handling

Are contradictions between sources surfaced, explained, and included in the
Contradiction section?

| Score | Meaning |
|---|---|
| 10 | All contradictions identified, explained with one-sentence rationale |
| 7–9 | Most contradictions identified, minor gaps in explanation |
| 4–6 | Some contradictions identified, others missed or unexplained |
| 1–3 | Contradictions present but not surfaced |
| N/A | No contradictions in input — scores default to 8 |

### Sub-criterion 4: Evidence Weighting

Are insights in the Insight Ranking ordered by evidential strength, with
high-quality sources weighted above low-quality sources?

| Score | Meaning |
|---|---|
| 10 | Rankings clearly reflect evidence quality — peer-reviewed above anecdotal |
| 7–9 | Generally correct ordering, minor misjudgements |
| 4–6 | Partial evidence-weighting — some rankings not justified |
| 1–3 | Insights ordered by apparent importance, not evidence quality |

### Sub-criterion 5: Uncertainty Acknowledgement

Does the report acknowledge limitations, gaps, and areas of genuine uncertainty?

| Score | Meaning |
|---|---|
| 10 | Uncertainty explicitly scoped — hedged language used where appropriate |
| 7–9 | Most uncertainty acknowledged, minor overstatements |
| 4–6 | Some uncertainty acknowledged, others smoothed over |
| 1–3 | Conclusions overstated — evidence presented as stronger than it is |

### Sub-criterion 6: Actionability

Do the Suggested Next Steps follow logically from the findings and gaps
identified in the report?

| Score | Meaning |
|---|---|
| 10 | Next steps are specific, follow directly from findings, actionable |
| 7–9 | Mostly specific and relevant, minor vagueness |
| 4–6 | Some specific steps, others generic ("do more research") |
| 1–3 | Generic steps with no connection to the specific report findings |

---

## Overall Score Calculation

```
Structural Checks    × 0.25
Structure Compliance × 0.25
Annotation Accuracy  × 0.25
Synthesis Quality    × 0.25
─────────────────────────────
Overall Score (0–10)
```

## Score Interpretation

| Range | Rating | Recommended Action |
|---|---|---|
| 8.0 – 10.0 | Strong | Production-grade |
| 6.0 – 7.9 | Moderate | Investigate lowest dimension |
| 4.0 – 5.9 | Needs work | Prompt revision required |
| 0.0 – 3.9 | Failing | Significant regression |
