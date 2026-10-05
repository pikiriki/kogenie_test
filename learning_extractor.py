from agents import Agent, Runner

from models import (
    CreativeEvidenceLedger,
    CreativeLearning,
)


from config import (
    get_config,
)


CONFIG = get_config()


def dedupe_strings(
    items: list[str],
) -> list[str]:

    result = []

    seen = set()

    for item in items:

        cleaned = item.strip()

        if not cleaned:
            continue

        if cleaned in seen:
            continue

        seen.add(cleaned)
        result.append(cleaned)

    return result


def build_contradiction_strings(
    ledger: CreativeEvidenceLedger,
) -> list[str]:

    contradictions = []

    for observation in (
        ledger.contradicting_observations
    ):

        if (
            observation.relative_change_pct
            is not None
        ):

            change_text = (
                f"{observation.relative_change_pct:+.2f}% "
                "relative change"
            )

        elif (
            observation.absolute_change
            is not None
        ):

            change_text = (
                f"{observation.absolute_change:+.4f} "
                "absolute change"
            )

        else:

            change_text = (
                "an opposing metric movement"
            )

        contradictions.append(
            (
                f"Campaign {observation.campaign_id}, "
                f"Outcome {observation.outcome_id}: "
                f"{ledger.metric_name} moved against "
                f"the desired '{ledger.desired_direction}' "
                f"direction ({change_text})."
            )
        )

    return contradictions


def build_observation_summary(
    ledger: CreativeEvidenceLedger,
) -> str:

    return (
        f"{ledger.repeated_pattern} "
        f"Evidence strength: "
        f"{ledger.evidence_strength}. "
        f"Evidence cell: channel={ledger.channel}; "
        f"conversion={ledger.conversion_definition}; "
        f"source_quality={ledger.source_quality}."
    )


learning_extractor_agent = Agent(
    name="Creative Learning Extractor",

    instructions="""
You are the Creative Learning Extractor
for KOgenie Copy Studio.

You receive one CreativeEvidenceLedger.

Your job is to convert historical evidence
into the narrowest defensible reusable learning.

You are NOT a causal inference engine.

The ledger contains observational historical
association, not proven creative causality.

REUSABLE LEARNING

Produce a cautious learning that could guide
future TESTING.

Do not state that the creative:
- works
- wins
- causes improvement
- increases the metric
- will perform again

Prefer language such as:
- has repeatedly coincided with
- has shown an emerging association with
- remains worth retesting
- may deserve prioritization as a test candidate

MIXED EVIDENCE

If evidence_strength is "mixed",
do not manufacture a positive rule.

Explain that evidence is inconsistent
and the creative should remain an unresolved hypothesis.

EMERGING EVIDENCE

If evidence_strength is "emerging",
you may say the historical association is promising
within the defined evidence cell.

Do not generalize beyond that cell.

REPEATED ASSOCIATION

If evidence_strength is "repeated_association",
you may say the creative has repeatedly coincided
with the selected metric direction in comparable
historical observations.

This still does NOT establish causality.

CONTRADICTIONS

Contradicting observations matter.

Do not hide, soften away, or explain them
without evidence.

WHERE IT MAY APPLY

Keep applicability narrowly scoped to the ledger's:
- channel
- conversion definition
- attribution context
- source-quality class

You may mention similar conditions,
but do not silently broaden to all advertising.

WHERE IT MAY NOT APPLY

Clearly state contexts not established
by the current ledger.

Do not claim failure in those contexts.
Say evidence is not established there.

NEXT TEST

Suggest one next test that would produce
stronger evidence.

Prefer changing the creative variable of interest
while holding other important conditions as stable
as practical.

CONFIDENCE

Confidence refers to the reusable historical learning,
not deterministic arithmetic.

Observational historical evidence from this ledger
must NEVER receive "high" confidence.

Do not invent:
- benchmarks
- experiments that did not happen
- customer outcomes
- performance thresholds
- deployment facts

Do not write ad copy.
""",

    model=CONFIG.text_model,

    output_type=CreativeLearning,
)


def extract_creative_learning(
    ledger: CreativeEvidenceLedger,
) -> CreativeLearning:

    observation_summary = (
        build_observation_summary(
            ledger
        )
    )

    contradictions = (
        build_contradiction_strings(
            ledger
        )
    )

    if (
        ledger.evidence_strength
        == "insufficient"
    ):

        return CreativeLearning(
            creative_key=(
                ledger.creative_key
            ),

            observation_summary=(
                observation_summary
            ),

            reusable_learning=(
                "No reusable creative-performance "
                "learning is justified yet. "
                "Treat this creative idea as an "
                "untested or weakly observed hypothesis."
            ),

            contradictions=(
                contradictions
            ),

            where_it_may_apply=[
                (
                    "No performance preference "
                    "should currently be inferred "
                    "from this ledger."
                )
            ],

            where_it_may_not_apply=[
                (
                    "Do not generalize this evidence "
                    "to other campaigns, channels, "
                    "conversion definitions, audiences, "
                    "or attribution systems."
                )
            ],

            next_test=(
                "Collect another comparable observation "
                "for this creative key under the same "
                "measurement context before extracting "
                "a reusable historical pattern."
            ),

            confidence="low",
        )

    result = Runner.run_sync(
        learning_extractor_agent,
        f"""
Here is the CreativeEvidenceLedger:

{ledger.model_dump_json(indent=2)}

Extract the narrowest defensible reusable learning.

Important:

The ledger describes historical association,
not causal effect.

Preserve contradictions.

Scope any learning to the evidence cell.

The learning should guide another test,
not become a universal creative rule.
"""
    )

    candidate = result.final_output

    creative_key = (
        ledger.creative_key
    )

    merged_contradictions = (
        dedupe_strings(
            contradictions
            + candidate.contradictions
        )
    )

    required_scope = (
        "Current evidence cell: "
        f"channel={ledger.channel}; "
        f"conversion_definition="
        f"{ledger.conversion_definition}; "
        f"attribution_context="
        f"{ledger.attribution_context}; "
        f"source_quality="
        f"{ledger.source_quality}."
    )

    where_it_may_apply = (
        dedupe_strings(
            [
                required_scope,
            ]
            + candidate.where_it_may_apply
        )
    )

    required_non_applicability = [
        (
            "Evidence is not established for "
            "other channels unless separately "
            "tested there."
        ),
        (
            "Evidence is not established for "
            "different conversion definitions."
        ),
        (
            "Evidence is not established for "
            "different attribution contexts."
        ),
        (
            "Evidence is not established for "
            "materially different campaign conditions "
            "without further testing."
        ),
    ]

    where_it_may_not_apply = (
        dedupe_strings(
            required_non_applicability
            + candidate.where_it_may_not_apply
        )
    )

    max_confidence = {
        "mixed": "low",
        "emerging": "medium",
        "repeated_association": "medium",
    }[
        ledger.evidence_strength
    ]

    confidence_rank = {
        "low": 0,
        "medium": 1,
        "high": 2,
    }

    if (
        confidence_rank[
            candidate.confidence
        ]
        >
        confidence_rank[
            max_confidence
        ]
    ):

        confidence = (
            max_confidence
        )

    else:

        confidence = (
            candidate.confidence
        )

    return CreativeLearning(
        creative_key=creative_key,

        observation_summary=(
            observation_summary
        ),

        reusable_learning=(
            candidate.reusable_learning
        ),

        contradictions=(
            merged_contradictions
        ),

        where_it_may_apply=(
            where_it_may_apply
        ),

        where_it_may_not_apply=(
            where_it_may_not_apply
        ),

        next_test=(
            candidate.next_test
        ),

        confidence=confidence,
    )
