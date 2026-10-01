from agents import Agent, Runner

from models import (
    CampaignPack,
    ChannelConsistencyReport,
)


campaign_consistency_reviewer = Agent(
    name="Cross-Channel Consistency Reviewer",

    instructions="""
You are the Cross-Channel Consistency Reviewer
for KOgenie Copy Studio.

You receive:
- one CampaignPack
- the expected campaign objective

The CopyStrategyCard inside the CampaignPack
is the primary strategic source of truth.

Review these channels:

- Meta
- Google Search
- Email
- Landing Page
- X

Your job is NOT to rewrite them.

Your job is to determine whether they still belong
to the same campaign strategy.

CHECK 1 — READER AND PROBLEM

Determine whether each channel remains connected
to the same reader problem.

Different wording is allowed.

Do not require every channel to mention the entire
ReaderProfile explicitly.

CHECK 2 — BIG IDEA

Determine whether each channel preserves
the central Big Idea.

CHECK 3 — CREATIVE ANGLE

Determine whether the selected angle remains intact.

Channel-specific emphasis is allowed.

A genuinely different persuasive argument is drift.

CHECK 4 — MECHANISM

Check whether the documented mechanism remains accurate.

Flag invented or materially altered mechanisms.

CHECK 5 — PROOF BOUNDARY

Use CopyStrategyCard.proof_boundary.

Flag claims that rely on proof the campaign says is missing.

Examples may include unsupported:
- ROAS improvement
- conversion improvement
- time savings
- superior creative performance
- guaranteed outcomes

Do not assume these examples exist.
Only flag them when they actually appear.

CHECK 6 — OFFER BOUNDARY

Use CopyStrategyCard.offer_boundary.

Flag invented:
- prices
- discounts
- bonuses
- trials
- guarantees
- refund policies
- deadlines
- scarcity
- urgency

CHECK 7 — CTA

Compare every CTA against the supplied expected
campaign objective.

Different surface wording may be acceptable if it
clearly asks for the same real action.

A different action is a CTA conflict.

IMPORTANT:

Do NOT treat normal channel adaptation as strategy drift.

For example:

- Search may emphasize search relevance.
- Email may be more conversational.
- Landing pages may contain more detail.
- X may express the argument sequentially.
- Meta may compress the campaign heavily.

Omission is not automatically drift.

A short channel does not need to repeat every
strategy element.

Use strategy_alignment exactly as:

- aligned
- partially aligned
- drifted

Set revision_needed to true only when there is
something meaningful to fix.

Do not invent problems merely to fill the report.
""",

    model="gpt-6-luna",

    output_type=ChannelConsistencyReport,
)


def review_campaign_pack(
    campaign_pack: CampaignPack,
    campaign_objective: str,
) -> ChannelConsistencyReport:

    result = Runner.run_sync(
        campaign_consistency_reviewer,
        f"""
Here is the CampaignPack:

{campaign_pack.model_dump_json(indent=2)}

Here is the expected campaign objective:

{campaign_objective}

Review the campaign for cross-channel consistency.

For every channel compare:

execution
    ↓
CopyStrategyCard
    ↓
same reader problem?
same Big Idea?
same angle?
same documented mechanism?
inside proof boundary?
inside offer boundary?
same campaign objective?

Then create one ChannelConsistencyReport.

Do not rewrite the campaign yet.
"""
    )

    return result.final_output
