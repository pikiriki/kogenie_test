from agents import Agent, Runner

from models import (
    AlternativeStrategy,
    AlternativeStrategyEvaluation,
    AlternativeStrategyEvaluationSet,
    AlternativeStrategySet,
    CampaignMemory,
    NoveltyGuidance,
    ResearchDocument,
)


EVALUATION_LEVELS = {
    "strong",
    "mixed",
    "weak",
}


RECOMMENDATIONS = {
    "viable",
    "needs revision",
    "reject",
}


alternative_strategy_evaluator_agent = Agent(
    name="Alternative Strategy Evaluator",

    instructions="""
You are the Alternative Strategy Evaluator
for KOgenie Copy Studio.

You receive ONE AlternativeStrategy at a time,
plus:

- the current ResearchDocument
- NoveltyGuidance
- approved CampaignMemory history
- the campaign objective

Your job is to evaluate whether the candidate
is a viable evidence-grounded strategy hypothesis.

You are NOT selecting between candidates.

You are NOT writing copy.

Evaluate these five dimensions.

1. RESEARCH GROUNDING

Use exactly:
- strong
- mixed
- weak

Ask whether the reader tension, problem interpretation,
and evidence_used are actually supported by the supplied
ResearchDocument.

Do not accept invented:
- psychology
- demographics
- fears
- desires
- customer quotations

2. HISTORICAL DISTINCTNESS

Use exactly:
- strong
- mixed
- weak

Ask whether the candidate is meaningfully different
from previously approved campaign strategies.

Different wording alone is NOT meaningful novelty.

The same truthful product mechanism appearing again
does NOT automatically mean repetition.

3. MECHANISM FIT

Use exactly:
- strong
- mixed
- weak

Ask whether the proposed mechanism emphasis can be
supported by the documented product mechanism and facts.

Do not allow invented capabilities.

4. EVIDENCE SAFETY

Use exactly:
- strong
- mixed
- weak

Check the candidate against its evidence_boundary
and NoveltyGuidance.what_must_stay_fixed.

Flag strategies that imply unsupported:
- performance improvement
- conversion improvement
- ROAS improvement
- quantified time savings
- guaranteed quality
- pricing
- discounts
- trials
- guarantees
- urgency
- scarcity

Only flag these if actually present or implied.

5. READER RELEVANCE

Use exactly:
- strong
- mixed
- weak

Ask whether the chosen reader tension is central enough
to the supplied reader/customer evidence to plausibly
organize a campaign.

A tension can be technically present in research
but still be peripheral.

WEAKNESSES

List concrete weaknesses.

Do not invent weaknesses simply because a list exists.

RECOMMENDATION

Use exactly one:

- viable
- needs revision
- reject

Use "viable" when the strategy is sufficiently grounded,
distinct, mechanism-consistent, evidence-safe,
and relevant.

Use "needs revision" when the strategic direction
has value but one or more fixable issues remain.

Use "reject" when the candidate relies on a fundamentally
unsupported reader tension, invented mechanism,
or other core strategic flaw.

IMPORTANT:

CampaignMemory tells you what was historically approved.

Approval does NOT prove performance.

Do not infer:
- that an old strategy worked
- that an old strategy failed
- that a candidate should be reused because it existed before

Outcome context may only be interpreted literally.

Do not rank the candidate against the other alternatives.
"""
    ,
    model="gpt-6-luna",
    output_type=AlternativeStrategyEvaluation,
)


def evaluate_alternative_strategy(
    strategy_index: int,
    strategy: AlternativeStrategy,
    research_document: ResearchDocument,
    novelty_guidance: NoveltyGuidance,
    memories: list[CampaignMemory],
    campaign_objective: str,
) -> AlternativeStrategyEvaluation:

    if memories:

        memory_context = "\n\n".join(
            memory.model_dump_json(indent=2)
            for memory in memories
        )

    else:

        memory_context = (
            "No approved campaign memories available."
        )

    result = Runner.run_sync(
        alternative_strategy_evaluator_agent,
        f"""
Strategy index:

{strategy_index}

Here is the AlternativeStrategy:

{strategy.model_dump_json(indent=2)}

Here is the current ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the NoveltyGuidance:

{novelty_guidance.model_dump_json(indent=2)}

Here is approved CampaignMemory history:

{memory_context}

Campaign objective:

{campaign_objective}

Evaluate this strategy independently.

Do not compare it with the other alternative
strategies being generated in this run.

Return one AlternativeStrategyEvaluation.
"""
    )

    candidate = result.final_output

    dimensions = [
        candidate.research_grounding,
        candidate.historical_distinctness,
        candidate.mechanism_fit,
        candidate.evidence_safety,
        candidate.reader_relevance,
    ]

    for value in dimensions:

        if value not in EVALUATION_LEVELS:
            raise ValueError(
                f"Unexpected evaluation level: {value}"
            )

    if candidate.recommendation not in RECOMMENDATIONS:

        raise ValueError(
            "Unexpected strategy recommendation: "
            + candidate.recommendation
        )

    return AlternativeStrategyEvaluation(
        strategy_index=strategy_index,
        research_grounding=(
            candidate.research_grounding
        ),
        historical_distinctness=(
            candidate.historical_distinctness
        ),
        mechanism_fit=(
            candidate.mechanism_fit
        ),
        evidence_safety=(
            candidate.evidence_safety
        ),
        reader_relevance=(
            candidate.reader_relevance
        ),
        weaknesses=(
            candidate.weaknesses
        ),
        recommendation=(
            candidate.recommendation
        ),
    )


def evaluate_alternative_strategy_set(
    strategy_set: AlternativeStrategySet,
    research_document: ResearchDocument,
    novelty_guidance: NoveltyGuidance,
    memories: list[CampaignMemory],
    campaign_objective: str,
) -> AlternativeStrategyEvaluationSet:

    if not strategy_set.strategies:

        return AlternativeStrategyEvaluationSet(
            evaluations=[]
        )

    evaluations = []

    for index, strategy in enumerate(
        strategy_set.strategies,
        start=1,
    ):

        evaluation = evaluate_alternative_strategy(
            strategy_index=index,
            strategy=strategy,
            research_document=research_document,
            novelty_guidance=novelty_guidance,
            memories=memories,
            campaign_objective=campaign_objective,
        )

        evaluations.append(
            evaluation
        )

    return AlternativeStrategyEvaluationSet(
        evaluations=evaluations
    )
