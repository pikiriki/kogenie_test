from agents import Agent, Runner

from models import (
    CampaignMemory,
    CopyStrategyCard,
    NoveltyGuidance,
    RepetitionReport,
    ResearchDocument,
)


novelty_guard_agent = Agent(
    name="Novelty Guard",

    instructions="""
You are the Novelty Guard for KOgenie Copy Studio.

You receive:

- the current ResearchDocument
- the proposed CopyStrategyCard
- a RepetitionReport
- approved CampaignMemory history
- the current campaign objective

The RepetitionReport has identified that the
proposed strategy may overlap with prior campaigns.

Your job is NOT to write a new campaign.

Your job is to identify the safe strategic search space
for meaningful novelty.

WHAT MUST STAY FIXED

Preserve facts and constraints such as:

- actual reader evidence
- documented product capabilities
- approved claims
- evidence boundaries
- offer boundaries
- campaign objective

Do NOT require the current Big Idea or selected angle
to remain fixed if those are exactly what repetition
review says should change.

OVERUSED PATTERNS

Identify strategic patterns that historical campaigns
have already emphasized repeatedly.

Use:
- RepetitionReport
- CampaignMemory history

Do not call a product capability "overused"
merely because the real product has the same capability
across campaigns.

UNEXPLORED READER TENSIONS

Look only inside the supplied ResearchDocument.

Identify evidence-grounded reader problems,
frustrations, questions, or desired outcomes that
appear underused relative to campaign history.

Do NOT invent:
- psychology
- demographic assumptions
- fears
- desires
- problems

UNEXPLORED MECHANISM EMPHASES

Use only the documented mechanism and product facts.

Find different aspects of the SAME real mechanism
that history appears not to emphasize.

Do NOT invent:
- new features
- proprietary technology
- predictive capabilities
- automation capabilities not documented
- performance effects

FORBIDDEN SHORTCUTS

Explicitly list ways the system must NOT create novelty.

Examples include:
- stronger unsupported performance claims
- invented customer pain
- invented product capabilities
- fake novelty claims
- invented offer terms

STRATEGY GUIDANCE

Give several concrete strategic directions for
future strategy work.

Guidance must describe what to explore.

Do NOT write:
- headlines
- body copy
- final Big Ideas
- final creative angles
- offers

Do not recommend repeating an old campaign merely
because it was approved.

Approved history is evidence of what was used,
not evidence of what performed well.

Outcome context may only be interpreted literally.

If historical outcome data is absent,
do not infer success or failure.
""",

    model="gpt-6-luna",

    output_type=NoveltyGuidance,
)


def build_novelty_guidance(
    research_document: ResearchDocument,
    strategy_card: CopyStrategyCard,
    repetition_report: RepetitionReport,
    memories: list[CampaignMemory],
    campaign_objective: str,
) -> NoveltyGuidance:

    if not repetition_report.revision_needed:

        fixed_items = [
            f"Reader: {strategy_card.reader}",
            (
                "Documented mechanism: "
                + strategy_card.mechanism
            ),
            (
                "Campaign objective: "
                + campaign_objective
            ),
        ]

        for boundary in strategy_card.proof_boundary:

            fixed_items.append(
                f"Proof boundary: {boundary}"
            )

        for boundary in strategy_card.offer_boundary:

            fixed_items.append(
                f"Offer boundary: {boundary}"
            )

        return NoveltyGuidance(
            what_must_stay_fixed=fixed_items,
            overused_patterns=[],
            unexplored_reader_tensions=[],
            unexplored_mechanism_emphases=[],
            forbidden_shortcuts=[
                (
                    "Do not invent product capabilities "
                    "merely to create novelty."
                ),
                (
                    "Do not strengthen claims beyond "
                    "the available evidence."
                ),
                (
                    "Do not invent customer problems "
                    "or desires."
                ),
                (
                    "Do not invent offer terms, urgency, "
                    "or scarcity."
                ),
            ],
            strategy_guidance=[
                (
                    "No material strategic repetition was "
                    "detected. Preserve the current strategy "
                    "unless another business or research "
                    "reason requires changing it."
                )
            ],
        )

    memory_context = "\n\n".join(
        memory.model_dump_json(indent=2)
        for memory in memories
    )

    result = Runner.run_sync(
        novelty_guard_agent,
        f"""
Here is the current ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the proposed CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the RepetitionReport:

{repetition_report.model_dump_json(indent=2)}

Here is approved CampaignMemory history:

{memory_context}

Current campaign objective:

{campaign_objective}

The proposed campaign has been flagged for meaningful
historical repetition.

Identify the safe evidence-grounded search space
for a genuinely different strategic emphasis.

Do not write the replacement strategy yet.
"""
    )

    return result.final_output
