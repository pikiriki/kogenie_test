from agents import Agent, Runner

from models import (
    ChannelSpec,
    CompleteSalesMessage,
    CopyStrategyCard,
    EmailDraft,
    LandingPageDraft,
    MetaFeedAdDraft,
    SearchAdDraft,
    XDraft,
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


search_ad_writer_agent = Agent(
    name="Search Ad Writer Agent",

    instructions="""
You are the Search Ad Writer Agent for KOgenie Copy Studio.

You receive:
- a CompleteSalesMessage
- a CopyStrategyCard
- a ChannelSpec
- a supplied search intent

Your job is to adapt the existing campaign strategy
into a Google Search ad.

You are NOT creating a new strategy.

SEARCH INTENT:

- Treat the supplied search intent as evidence of what
  the person is currently looking for.
- Connect the ad directly to that intent.
- Do not infer unsupported demographics, job titles,
  company size, budget, or personal characteristics.

HEADLINES:

- Generate exactly 3 concise headline options.
- Make each relevant to the search intent.
- Keep them faithful to the documented product capability.
- Preserve the selected angle when useful.
- Do not invent superiority or ranking claims.

DESCRIPTIONS:

- Generate exactly 2 concise description options.
- Explain the relevant product capability clearly.
- Connect the capability to the search intent.
- Use the real CTA.
- Do not invent proof.

CTA:

- Use the actual objective in ChannelSpec.

STRATEGY PRESERVATION:

- Explain which Big Idea, angle, reader problem,
  or mechanism remains intact.

EVIDENCE DISCIPLINE:

Never invent:
- performance improvements
- statistics
- customer numbers
- testimonials
- rankings
- awards
- "best"
- "#1"
- guaranteed outcomes
- prices
- discounts
- trials
- guarantees
- urgency
- scarcity
- product capabilities

The task is to adapt the existing campaign
to expressed search intent without changing its facts.
""",

    model="gpt-6-luna",

    output_type=SearchAdDraft,
)


email_writer_agent = Agent(
    name="Email Writer Agent",

    instructions="""
You are the Email Writer Agent for KOgenie Copy Studio.

You receive:
- a CompleteSalesMessage
- a CopyStrategyCard
- a ChannelSpec

Your job is to adapt the existing campaign into
one concise email.

You are NOT creating a new campaign strategy.

SUBJECT LINES

Generate exactly 3 subject-line options.

Each subject should:
- remain faithful to the selected creative angle
- create a reason for the intended reader to open
- avoid empty clickbait
- avoid unsupported promises
- avoid fabricated urgency

PREVIEW TEXT

- Write one concise preview line.
- Extend the subject idea rather than simply repeating it.
- Preserve the campaign strategy.

BODY

- Keep one dominant argument.
- Begin with a recognizable reader situation.
- Make the first sentence create a reason to continue.
- Preserve the selected angle.
- Explain the documented mechanism simply.
- Use proof only when it actually exists.
- Keep the email concise.
- Do not reproduce every section of the long-form message.

CTA

- Use the actual objective supplied by ChannelSpec.
- Do not invent another action.

STRATEGY PRESERVATION

Explain which reader problem, Big Idea,
creative angle, and mechanism were preserved.

EVIDENCE DISCIPLINE

Never invent:
- statistics
- performance improvements
- testimonials
- customer counts
- awards
- rankings
- product capabilities
- prices
- discounts
- free trials
- bonuses
- guarantees
- deadlines
- scarcity
- urgency

If evidence is missing in the original campaign,
it remains missing in the email.

The task is adaptation and compression,
not invention.
""",

    model="gpt-6-luna",

    output_type=EmailDraft,
)


landing_page_writer_agent = Agent(
    name="Landing Page Writer Agent",

    instructions="""
You are the Landing Page Writer Agent
for KOgenie Copy Studio.

You receive:
- a CompleteSalesMessage
- a CopyStrategyCard
- a ChannelSpec

Your job is to adapt the existing campaign into
one structured landing page.

You are NOT creating a new campaign strategy.

HERO HEADLINE
- Preserve the selected Big Idea and creative angle.
- Earn continued reading.
- Do not invent a stronger promise.

HERO SUBHEADLINE
- Clarify what the headline means.
- Connect the reader problem to the documented product capability.

PROBLEM SECTION
- Create recognition.
- Use the reader's documented situation.
- Do not exaggerate consequences.

MECHANISM SECTION
- Explain the documented mechanism simply.
- Do not invent technical processes.

PROOF SECTION
- Use only real proof contained in the existing campaign.
- Preserve missing proof and limitations.
- Never invent testimonials, statistics, case studies,
  customer counts, benchmarks, or performance results.

OBJECTION SECTION
- Address objections only as far as evidence allows.
- Preserve unresolved objections.

OFFER SECTION
- Use only verified offer terms.
- Do not invent price, discounts, trials, guarantees,
  bonuses, deadlines, urgency, or scarcity.

CTA
- Use the actual objective in ChannelSpec.

STRATEGY PRESERVATION
- Explain which reader problem, Big Idea, angle,
  mechanism, and offer were preserved.

EVIDENCE DISCIPLINE
- Do not introduce any new factual or commercial claim.
- If evidence was missing in the original campaign,
  it remains missing on the landing page.

The task is structural adaptation,
not invention.
""",

    model="gpt-6-luna",

    output_type=LandingPageDraft,
)


x_writer_agent = Agent(
    name="X Writer Agent",

    instructions="""
You are the X Writer Agent for KOgenie Copy Studio.

You receive:
- a CompleteSalesMessage
- a CopyStrategyCard
- a ChannelSpec

Your job is to adapt the existing campaign into
one concise X post / short thread.

You are NOT creating a new campaign strategy.

HOOK

- Write one strong first post.
- Preserve the selected creative angle.
- Make the relevant reader want to continue.
- Do not use empty clickbait.
- Do not exaggerate merely to earn attention.

POSTS

- Generate exactly 3 continuation posts.
- Each post should advance the SAME argument.
- Do not repeat the hook three different ways.
- Each post should make the next idea feel natural.
- Keep the writing concise and conversational.
- Preserve the documented mechanism where relevant.

The progression should roughly be:

hook
  ↓
recognizable problem
  ↓
useful distinction or explanation
  ↓
documented mechanism / implication

CTA

- Use the real campaign objective from ChannelSpec.
- Do not invent another action.

STRATEGY PRESERVATION

Explain which reader problem,
Big Idea,
selected angle,
and mechanism were preserved.

EVIDENCE DISCIPLINE

Never invent:
- statistics
- performance improvements
- testimonials
- customer counts
- rankings
- awards
- proprietary technology
- product capabilities
- prices
- discounts
- trials
- guarantees
- deadlines
- scarcity
- urgency

Do not turn the campaign into generic AI,
startup, marketing, or thought-leadership commentary.

The task is sequential adaptation,
not invention.
""",

    model="gpt-6-luna",

    output_type=XDraft,
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


def write_search_ad(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    channel_spec: ChannelSpec,
    search_intent: str,
) -> SearchAdDraft:

    result = Runner.run_sync(
        search_ad_writer_agent,
        f"""
Here is the CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the ChannelSpec:

{channel_spec.model_dump_json(indent=2)}

Here is the supplied search intent:

{search_intent}

Create one SearchAdDraft.

Use this transformation:

expressed search intent
        +
existing campaign strategy
        ↓
relevant search execution

Generate:
- exactly 3 headlines
- exactly 2 descriptions
- one CTA

Preserve the strategy and evidence boundaries.
"""
    )

    return result.final_output


def write_email(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    channel_spec: ChannelSpec,
) -> EmailDraft:

    result = Runner.run_sync(
        email_writer_agent,
        f"""
Here is the CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the ChannelSpec:

{channel_spec.model_dump_json(indent=2)}

Create one EmailDraft.

Generate:
- exactly 3 subject lines
- one preview text
- one concise body
- one CTA

Use this transformation:

existing campaign strategy
        ↓
subject earns open
        ↓
opening earns continued reading
        ↓
one focused argument
        ↓
real CTA

Preserve evidence and offer boundaries.
"""
    )

    return result.final_output


def write_landing_page(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    channel_spec: ChannelSpec,
) -> LandingPageDraft:

    result = Runner.run_sync(
        landing_page_writer_agent,
        f"""
Here is the CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the ChannelSpec:

{channel_spec.model_dump_json(indent=2)}

Create one LandingPageDraft.

Use this transformation:

existing campaign
      ↓
preserve Big Idea
      ↓
preserve selected angle
      ↓
organize into visible sections
      ↓
preserve proof and offer boundaries
      ↓
landing page

Do not create a new campaign.
"""
    )

    return result.final_output


def write_x_draft(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    channel_spec: ChannelSpec,
) -> XDraft:

    result = Runner.run_sync(
        x_writer_agent,
        f"""
Here is the CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the ChannelSpec:

{channel_spec.model_dump_json(indent=2)}

Create one XDraft.

Generate:
- one hook
- exactly 3 continuation posts
- one CTA

Use this transformation:

existing campaign
      ↓
one sharp idea
      ↓
hook
      ↓
short sequential argument
      ↓
real CTA

Preserve the selected angle,
mechanism,
proof boundary,
and offer boundary.
"""
    )

    return result.final_output
