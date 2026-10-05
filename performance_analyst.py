from agents import Agent, Runner

from models import (
    OutcomeEvidenceSnapshot,
    PerformanceAnalysis,
    PerformanceComparison,
    PerformanceContext,
)


from config import (
    get_config,
)


CONFIG = get_config()


performance_analyst_agent = Agent(
    name="Performance Analyst",

    instructions="""
You are the Performance Analyst
for KOgenie Copy Studio.

You receive:

- an OutcomeEvidenceSnapshot
- a PerformanceContext
- a PerformanceComparison

Your job is to explain what the supplied evidence
supports and what it does NOT support.

You are NOT a causal attribution engine.

OBSERVED CHANGES

Report only metric changes directly supported
by PerformanceComparison.

Be numerically precise.

For percentage metrics such as CTR and
conversion rate, distinguish:

- percentage-point change
- relative percentage change

Do not confuse them.

SUPPORTED INTERPRETATIONS

Explain what the observed values mean
descriptively.

Examples:

Higher CTR may support:
"A greater proportion of recorded impressions
resulted in recorded clicks."

Lower CPA may support:
"Recorded spend per recorded conversion was lower."

Do not turn descriptions into causal explanations.

UNSUPPORTED EXPLANATIONS

Explicitly list tempting explanations that the
available evidence does not establish.

Examples include unsupported claims that:

- the creative caused a metric change
- the copy caused a metric change
- the visual caused a metric change
- the angle caused a metric change
- KOgenie caused a performance improvement
- the outcome will reproduce in future campaigns

HYPOTHESES

You MAY propose plausible explanations worth testing.

Label them as hypotheses.

Do not present hypotheses as findings.

Prefer hypotheses that can be tested with
additional evidence.

Possible categories may include:

- creative differences
- audience delivery
- placement mix
- auction conditions
- spend/budget differences
- frequency
- seasonality
- attribution differences

Only include hypotheses relevant to the supplied context.

ADDITIONAL EVIDENCE NEEDED

For important hypotheses, state what evidence
would help test or distinguish them.

Examples:

- creative-level metrics
- audience breakdown
- placement breakdown
- CPM
- frequency
- randomized A/B test
- holdout/control data
- attribution reconciliation

CONFIDENCE

Use exactly:

- low
- medium
- high

Confidence refers to the strength of the
interpretation and explanatory evidence,
not the correctness of deterministic arithmetic.

Respect every interpretation boundary and
comparison boundary supplied in the inputs.

If the data is fictional, manual, estimated,
incomplete, or lacks causal design,
confidence should reflect those limitations.

Do NOT invent benchmarks.

Do NOT invent missing campaign facts.

Do NOT say a campaign was "good", "bad",
"successful", or "unsuccessful" unless a supplied
business objective and valid decision threshold
actually supports that conclusion.

Do NOT write advertising copy.
""",

    model=CONFIG.text_model,

    output_type=PerformanceAnalysis,
)


def analyze_performance(
    snapshot: OutcomeEvidenceSnapshot,
    context: PerformanceContext,
    comparison: PerformanceComparison,
) -> PerformanceAnalysis:

    snapshot_campaign_id = (
        snapshot.raw_outcome.campaign_id
    )

    context_campaign_id = (
        context
        .current_snapshot
        .raw_outcome
        .campaign_id
    )

    if (
        snapshot_campaign_id
        != context_campaign_id
    ):

        raise ValueError(
            "Outcome snapshot and performance "
            "context belong to different campaigns."
        )

    if (
        snapshot.derived_metrics
        != context.current_metrics
    ):

        raise ValueError(
            "Current metrics do not match the "
            "outcome evidence snapshot."
        )

    if not comparison.baseline_available:

        return PerformanceAnalysis(
            observed_changes=[
                (
                    "No valid historical baseline "
                    "is available, so period-over-period "
                    "performance change cannot be stated."
                )
            ],

            supported_interpretations=[
                (
                    "Current-period metrics may be "
                    "reported descriptively using the "
                    "supplied OutcomeEvidenceSnapshot."
                )
            ],

            unsupported_explanations=[
                (
                    "Do not claim that performance "
                    "improved or declined because no "
                    "valid baseline exists."
                ),
                (
                    "Do not attribute current outcomes "
                    "to copy, visual, strategy, or "
                    "another campaign element."
                ),
            ],

            hypotheses=[],

            additional_evidence_needed=[
                (
                    "Collect a historical outcome "
                    "that satisfies the current "
                    "comparability rules."
                )
            ],

            confidence="low",
        )

    result = Runner.run_sync(
        performance_analyst_agent,
        f"""
Here is the OutcomeEvidenceSnapshot:

{snapshot.model_dump_json(indent=2)}


Here is the PerformanceContext:

{context.model_dump_json(indent=2)}


Here is the PerformanceComparison:

{comparison.model_dump_json(indent=2)}


Analyze the measured performance carefully.

Separate:

1. observed numeric changes
2. supported descriptive interpretations
3. explanations that are NOT supported
4. hypotheses worth investigating
5. evidence needed to test those hypotheses

Do not convert correlation into causation.

Do not invent industry benchmarks.

Do not infer that creative, copy, visual,
strategy, or KOgenie caused the observed changes
unless the supplied evidence establishes that.

Respect all evidence and comparison boundaries.
"""
    )

    return result.final_output
