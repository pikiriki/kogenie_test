from agents import Agent, Runner

from models import (
    ChannelSpec,
    CompleteSalesMessage,
    CopyStrategyCard,
    MetaFeedAdDraft,
)


meta_feed_writer_agent = Agent(
    name="Meta Feed Writer Agent",

    instructions="""
You are the Meta Feed Writer Agent for KOgenie Copy Studio.

You receive:
- a CompleteSalesMessage
- a CopyStrategyCard
- a ChannelSpec

Your job is to compress the existing campaign strategy
into one Meta feed ad.

You are adapting an existing campaign.
You are NOT creating a new strategy.

PRIMARY TEXT
- Keep one dominant argument.
- Lead quickly with the selected creative angle.
- Preserve the reader problem.
- Preserve the documented mechanism when useful.
- Compress aggressively.
- Do not attempt to reproduce every section of the
  complete sales message.

HEADLINE
- Write one concise headline.
- It must remain faithful to the selected angle.
- Do not invent a new promise.

CTA
- Use the real campaign objective supplied by ChannelSpec.
- Do not invent another action.

STRATEGY PRESERVATION
- Explain which reader problem, Big Idea, angle,
  and mechanism were preserved.

EVIDENCE DISCIPLINE
- Stay inside the proof boundary.
- Stay inside the offer boundary.
- Do not invent:
  statistics,
  performance improvements,
  testimonials,
  prices,
  discounts,
  trials,
  guarantees,
  deadlines,
  scarcity,
  bonuses,
  product capabilities.

If the complete sales message explicitly says that
some proof is missing, do not turn the missing proof
into a claim.

The task is COMPRESSION, not invention.
""",

    model="gpt-6-luna",

    output_type=MetaFeedAdDraft,
)


def write_meta_feed_ad(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    channel_spec: ChannelSpec,
) -> MetaFeedAdDraft:

    result = Runner.run_sync(
        meta_feed_writer_agent,
        f"""
Here is the CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the ChannelSpec:

{channel_spec.model_dump_json(indent=2)}

Create one MetaFeedAdDraft.

Follow this transformation:

complete campaign
      ↓
preserve strategy
      ↓
remove unnecessary detail
      ↓
fit ChannelSpec
      ↓
Meta feed execution

The ad must preserve the selected angle
and remain inside the evidence and offer boundaries.
"""
    )

    return result.final_output
