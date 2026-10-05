from agents import Agent, Runner

from models import (
    AlternativeStrategySet,
    CampaignMemory,
    CopyStrategyCard,
    NoveltyGuidance,
    RepetitionReport,
    ResearchDocument,
)


from config import (
    get_config,
)


CONFIG = get_config()


alternative_strategy_agent = Agent(
    name="Alternative Strategy Generator",

    instructions="""
You are the Alternative Strategy Generator
for KOgenie Copy Studio.

You receive:

- a ResearchDocument
- the current CopyStrategyCard
- a RepetitionReport
- NoveltyGuidance
- approved CampaignMemory history
- the campaign objective

Your job is to generate exactly 3 alternative
strategy hypotheses.

You are NOT writing advertising copy.

The alternatives must remain inside the same
evidence and business reality.

EVERY ALTERNATIVE MUST INCLUDE:

reader_tension
- Use a reader tension supported by current research.
- Do not invent psychology, demographics, fears,
  motivations, or problems.

mechanism_emphasis
- Use only the documented product mechanism.
- You may emphasize a different part of that mechanism.
- Do not invent new capabilities.

proposed_big_idea
- Create one organizing strategic thought.
- It should connect an evidence-grounded problem/desire
  with the documented mechanism.
- Stay inside the available promise boundary.

proposed_angle
- Give a distinct strategic argument.
- It must not merely rename an historically repeated angle.

evidence_used
- List the supplied evidence that justifies this strategy.
- Never invent customer quotations.

evidence_boundary
- Preserve relevant proof and offer limitations.
- State what the strategy must NOT claim.

historical_difference
- Explain how this strategy differs materially from
  the repeated historical campaign patterns.
- Different wording alone does not count.

CRITICAL RULES:

All 3 alternatives must be meaningfully different
from each other.

Prefer differences in:
- reader tension
- problem interpretation
- mechanism emphasis

Do NOT manufacture novelty through:
- stronger unsupported claims
- invented product capabilities
- invented customer pain
- fake performance claims
- invented pricing
- invented guarantees
- invented urgency
- invented scarcity

CampaignMemory tells you what was used before.

It does NOT tell you what performed well.

Do not infer performance from approval history.

Do not write:
- headlines
- body copy
- CTAs
- complete advertisements

Return exactly 3 AlternativeStrategy objects.
""",

    model=CONFIG.text_model,

    output_type=AlternativeStrategySet,
)


def generate_alternative_strategies(
    research_document: ResearchDocument,
    strategy_card: CopyStrategyCard,
    repetition_report: RepetitionReport,
    novelty_guidance: NoveltyGuidance,
    memories: list[CampaignMemory],
    campaign_objective: str,
) -> AlternativeStrategySet:

    if not repetition_report.revision_needed:

        return AlternativeStrategySet(
            strategies=[]
        )

    memory_context = "\n\n".join(
        memory.model_dump_json(indent=2)
        for memory in memories
    )

    result = Runner.run_sync(
        alternative_strategy_agent,
        f"""
Here is the current ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the current CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the RepetitionReport:

{repetition_report.model_dump_json(indent=2)}

Here is the NoveltyGuidance:

{novelty_guidance.model_dump_json(indent=2)}

Here is the approved CampaignMemory history:

{memory_context}

Campaign objective:

{campaign_objective}

Generate exactly 3 alternative strategy hypotheses.

Each must remain grounded in current research,
the real product mechanism,
and current evidence boundaries.

Each must differ meaningfully from:
1. the historically repeated strategy
2. the other alternatives

Do not write advertising copy.
"""
    )

    strategy_set = result.final_output

    if len(strategy_set.strategies) != 3:

        raise RuntimeError(
            "Expected exactly 3 alternative strategies."
        )

    return strategy_set
