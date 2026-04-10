# evals_public/test_cases_public.py
# LexisAI Public Evaluation Test Cases
#
# These are the 5 test cases used to evaluate LexisAI output quality.
# Each case defines:
#   - Input: research question and/or sources
#   - Expectations: what a correct output must contain

TEST_CASES = [
    {
        "id": "TC01",
        "name": "Single source — clear research question",
        "description": (
            "Agent receives one high-quality peer-reviewed source and a "
            "clearly stated research question. Tests correct [S1] usage, "
            "absence of fabricated source tags, and basic schema compliance."
        ),
        "input": {
            "research_question": (
                "What are the cognitive effects of chronic sleep deprivation?"
            ),
            "sources": [
                {
                    "label": "S1",
                    "type": "academic paper",
                    "description": "Van Dongen et al. (2003) — Sleep journal. "
                                   "Controlled study of cognitive deficits from "
                                   "chronic sleep restriction."
                }
            ],
            "lens": None
        },
        "expectations": {
            "must_contain": [
                "📋 RESEARCH BRIEF",
                "🔍 DEEP DIVE",
                "OVERVIEW",
                "KEY THEMES",
                "CROSS-SOURCE ANALYSIS",
                "INSIGHT RANKING",
                "OPEN QUESTIONS",
                "SYNTHESIS STATEMENT",
                "SUGGESTED NEXT STEPS",
                "[S1]"
            ],
            "must_not_contain": ["[S2]", "[S3]"],
            "annotation_rules": {
                "expected_source_tags": ["S1"],
                "general_knowledge_expected": True,
                "fabricated_sources_forbidden": True
            }
        }
    },

    {
        "id": "TC02",
        "name": "Two contradicting sources",
        "description": (
            "Two sources that directly contradict each other on the same "
            "research question. Tests whether the contradiction section is "
            "populated and both sources are annotated correctly."
        ),
        "input": {
            "research_question": (
                "Does intermittent fasting outperform continuous caloric "
                "restriction for weight loss?"
            ),
            "sources": [
                {
                    "label": "S1",
                    "type": "academic paper",
                    "description": "Study reporting 13% productivity gain "
                                   "with time-restricted eating (Cell Metabolism)"
                },
                {
                    "label": "S2",
                    "type": "academic paper",
                    "description": "RCT finding no significant difference "
                                   "between IF and standard dieting (NEJM Evidence)"
                }
            ],
            "lens": "Focus on RCT evidence quality"
        },
        "expectations": {
            "must_contain": [
                "📋 RESEARCH BRIEF",
                "Points of Contradiction",
                "[S1]",
                "[S2]",
                "INSIGHT RANKING",
                "SYNTHESIS STATEMENT"
            ],
            "must_not_contain": ["[S3]"],
            "annotation_rules": {
                "expected_source_tags": ["S1", "S2"],
                "contradiction_section_required": True
            }
        }
    },

    {
        "id": "TC03",
        "name": "No sources — topic only",
        "description": (
            "Agent receives only a research question with no sources provided. "
            "Tests that all claims are flagged [general knowledge] and no "
            "source tags like [S1] appear in the output."
        ),
        "input": {
            "research_question": (
                "What is the impact of microplastics on human health?"
            ),
            "sources": [],
            "lens": None
        },
        "expectations": {
            "must_contain": [
                "📋 RESEARCH BRIEF",
                "[general knowledge]",
                "SYNTHESIS STATEMENT",
                "SUGGESTED NEXT STEPS"
            ],
            "must_not_contain": ["[S1]", "[S2]"],
            "annotation_rules": {
                "expected_source_tags": [],
                "general_knowledge_required": True,
                "source_tags_forbidden": True
            }
        }
    },

    {
        "id": "TC04",
        "name": "High-quality + low-quality source",
        "description": (
            "One peer-reviewed source and one anonymous blog post. "
            "Tests whether the low-quality source is flagged in the "
            "Research Brief and claims are weighted accordingly."
        ),
        "input": {
            "research_question": (
                "Is cold water immersion effective for muscle recovery?"
            ),
            "sources": [
                {
                    "label": "S1",
                    "type": "systematic review",
                    "description": (
                        "Bleakley et al. (2012) — Cochrane Systematic Review. "
                        "Meta-analysis of 17 trials on cold water immersion."
                    )
                },
                {
                    "label": "S2",
                    "type": "blog post",
                    "description": (
                        "FitnessBlog.net — anonymous author, no date. "
                        "Anecdotal claims about ice baths, no citations."
                    )
                }
            ],
            "lens": None
        },
        "expectations": {
            "must_contain": [
                "📋 RESEARCH BRIEF",
                "[S1]",
                "[S2]",
                "INSIGHT RANKING",
                "SYNTHESIS STATEMENT"
            ],
            "must_not_contain": [],
            "annotation_rules": {
                "expected_source_tags": ["S1", "S2"],
                "low_quality_flag_required": True,
                "low_quality_source_id": "S2"
            }
        }
    },

    {
        "id": "TC05",
        "name": "Three sources — full synthesis",
        "description": (
            "Three sources covering different angles of the same topic. "
            "Tests full cross-source synthesis: all three annotated, "
            "convergence identified, gaps surfaced."
        ),
        "input": {
            "research_question": (
                "What drives employee burnout in knowledge work environments?"
            ),
            "sources": [
                {
                    "label": "S1",
                    "type": "academic paper",
                    "description": (
                        "Maslach & Leiter (2016) — job demands-resources model, "
                        "six workplace mismatch antecedents of burnout."
                    )
                },
                {
                    "label": "S2",
                    "type": "industry report",
                    "description": (
                        "Microsoft Work Trend Index (2022) — survey of 31,000 "
                        "workers, always-on culture and autonomy as primary drivers."
                    )
                },
                {
                    "label": "S3",
                    "type": "industry report",
                    "description": (
                        "Gallup State of the Global Workplace (2023) — "
                        "manager quality accounts for 70% of engagement variance."
                    )
                }
            ],
            "lens": "Organisational and managerial perspective"
        },
        "expectations": {
            "must_contain": [
                "📋 RESEARCH BRIEF",
                "[S1]",
                "[S2]",
                "[S3]",
                "Points of Agreement",
                "Points of Contradiction",
                "Gaps in the Evidence",
                "INSIGHT RANKING",
                "SYNTHESIS STATEMENT",
                "SUGGESTED NEXT STEPS"
            ],
            "must_not_contain": [],
            "annotation_rules": {
                "expected_source_tags": ["S1", "S2", "S3"],
                "convergence_expected": True,
                "all_sections_required": True
            }
        }
    }
]
