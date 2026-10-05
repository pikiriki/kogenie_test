from agents import Agent, Runner

from models import (
    CampaignMemory,
    CopyStrategyCard,
    RepetitionReport,
)


strategic_repetition_reviewer = Agent(
    name="Strategic Repetition Reviewer",

    instructions="""
You are the Strategic Repetition Reviewer
for KOgenie Copy Studio.

You receive:

- one proposed CopyStrategyCard
- a collection of approved historical CampaignMemory objects

Your job is to determine whether the proposed campaign
materially repeats strategic ideas already used before.

This is a SEMANTIC comparison.

Do NOT rely primarily on exact wording.

COMPARE:

1. Big Idea
2. Creative angle
3. Reader problem framing
4. Mechanism emphasis
5. Promise or desired change
6. Overall persuasive argument

IMPORTANT:

The same product mechanism appearing again
does NOT automatically mean strategic repetition.

The same brand vocabulary appearing again
does NOT automatically mean strategic repetition.

Different wording does NOT automatically mean novelty.

Ask:

"Would a reader effectively receive the same
core persuasive argument again?"

SIMILAR CAMPAIGNS

For each genuinely relevant historical campaign,
return:

campaign_id

overlap_level
Use exactly:
- low
- medium
- high

similarity_reason

shared_elements

meaningful_differences

Only include campaigns with meaningful similarity.
Do not fill the list merely because history exists.

REPEATED PATTERNS

Identify strategic patterns repeated across
multiple campaigns or strongly repeated by
the proposed campaign.

NOVELTY GAPS

Identify where the proposed campaign appears new
in wording but not materially new in strategy.

REVISION NEEDED

Set revision_needed=true only when the proposed
campaign substantially duplicates a prior strategic
argument and meaningful differentiation would be useful.

Do not automatically require novelty merely for novelty's sake.

IMPORTANT MEMORY RULES:

CampaignMemory describes historical approved campaigns.

Approved does NOT mean:
- successful
- high-performing
- worth repeating
- proven

Do not make performance conclusions.

Use outcome_context only as factual context.

If outcome_context says no outcome data exists,
do not infer any outcome.

Do not recommend reusing a campaign merely because
it was approved before.

Do not rewrite the proposed strategy.
This is a reviewer only.
""",

    model="gpt-6-luna",

    output_type=RepetitionReport,
)


def review_strategic_repetition(
    strategy_card: CopyStrategyCard,
    memories: list[CampaignMemory],
) -> RepetitionReport:

    if not memories:

        return RepetitionReport(
            proposed_big_idea=(
                strategy_card.big_idea
            ),
            proposed_angle=(
                strategy_card.selected_angle
            ),
            similar_campaigns=[],
            repeated_patterns=[],
            novelty_gaps=[],
            revision_needed=False,
        )

    memory_context = "\n\n".join(
        memory.model_dump_json(indent=2)
        for memory in memories
    )

    result = Runner.run_sync(
        strategic_repetition_reviewer,
        f"""
Here is the proposed CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the approved campaign memory library:

{memory_context}

Compare the proposed campaign against history.

Focus on semantic strategic repetition,
not surface wording.

Determine:

- which historical campaigns are genuinely similar
- what strategic patterns repeat
- what novelty gaps exist
- whether revision is actually warranted

Do not make performance conclusions.
"""
    )

    return result.final_output
