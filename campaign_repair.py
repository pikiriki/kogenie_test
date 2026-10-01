from agents import Agent, Runner

from models import (
    CampaignPack,
    CampaignRepairResult,
    ChannelConsistencyReport,
    EmailDraft,
    LandingPageDraft,
    MetaFeedAdDraft,
    SearchAdDraft,
    XDraft,
)


CHANNEL_REPAIR_RULES = """
You are repairing ONE failed channel execution
for KOgenie Copy Studio.

You receive:
- the CopyStrategyCard
- the original channel draft
- the reviewer's findings for this channel
- the expected campaign objective
- any channel-specific context

Your job is to fix ONLY the problems identified
by the reviewer.

CRITICAL RULE:

Do not create a new campaign strategy.

Preserve:
- reader
- primary problem
- Big Idea
- selected creative angle
- documented mechanism
- proof boundary
- offer boundary
- campaign objective

Fix:
- strategy drift
- unsupported claims
- CTA conflicts
- other specific issues identified by the reviewer

Do not introduce:
- new product capabilities
- new statistics
- new testimonials
- new performance outcomes
- new customer counts
- new rankings
- new awards
- new prices
- new discounts
- new trials
- new guarantees
- new bonuses
- new urgency
- new scarcity

Make the minimum meaningful revision required.

The goal is REPAIR, not reinvention.
"""


meta_repair_agent = Agent(
    name="Meta Repair Agent",
    instructions=CHANNEL_REPAIR_RULES + """
Return one corrected MetaFeedAdDraft.

Keep the Meta feed format:
- primary_text
- headline
- cta
- strategy_preserved
- evidence_check
""",
    model="gpt-6-luna",
    output_type=MetaFeedAdDraft,
)


search_repair_agent = Agent(
    name="Search Repair Agent",
    instructions=CHANNEL_REPAIR_RULES + """
Return one corrected SearchAdDraft.

Keep the Google Search structure:
- exactly 3 headlines
- exactly 2 descriptions
- cta
- intent_connection
- strategy_preserved
- evidence_check

Preserve relevance to the supplied search intent.
""",
    model="gpt-6-luna",
    output_type=SearchAdDraft,
)


email_repair_agent = Agent(
    name="Email Repair Agent",
    instructions=CHANNEL_REPAIR_RULES + """
Return one corrected EmailDraft.

Keep the email structure:
- exactly 3 subject lines
- preview_text
- body
- cta
- strategy_preserved
- evidence_check
""",
    model="gpt-6-luna",
    output_type=EmailDraft,
)


landing_page_repair_agent = Agent(
    name="Landing Page Repair Agent",
    instructions=CHANNEL_REPAIR_RULES + """
Return one corrected LandingPageDraft.

Preserve the page structure:
- hero_headline
- hero_subheadline
- problem_section
- mechanism_section
- proof_section
- objection_section
- offer_section
- cta
- strategy_preserved
- evidence_check
""",
    model="gpt-6-luna",
    output_type=LandingPageDraft,
)


x_repair_agent = Agent(
    name="X Repair Agent",
    instructions=CHANNEL_REPAIR_RULES + """
Return one corrected XDraft.

Preserve:
- one hook
- exactly 3 continuation posts
- cta
- strategy_preserved
- evidence_check

Keep one sequential campaign argument.
""",
    model="gpt-6-luna",
    output_type=XDraft,
)


def repair_campaign_pack(
    campaign_pack: CampaignPack,
    consistency_report: ChannelConsistencyReport,
    campaign_objective: str,
    search_intent: str,
) -> CampaignRepairResult:

    revised_pack = campaign_pack.model_copy(
        deep=True
    )

    repaired_channels = []
    untouched_channels = []

    for finding in consistency_report.channel_findings:

        if not finding.revision_needed:
            untouched_channels.append(
                finding.channel
            )
            continue

        channel_name = finding.channel.strip().lower()


        if channel_name == "meta":

            result = Runner.run_sync(
                meta_repair_agent,
                f"""
Here is the CopyStrategyCard:

{campaign_pack.strategy_card.model_dump_json(indent=2)}

Here is the original Meta draft:

{campaign_pack.meta.model_dump_json(indent=2)}

Here is the reviewer finding:

{finding.model_dump_json(indent=2)}

Expected campaign objective:

{campaign_objective}

Repair only this Meta execution.
"""
            )

            revised_pack.meta = result.final_output

            repaired_channels.append(
                finding.channel
            )

        elif channel_name in {
            "google search",
            "search",
        }:

            result = Runner.run_sync(
                search_repair_agent,
                f"""
Here is the CopyStrategyCard:

{campaign_pack.strategy_card.model_dump_json(indent=2)}

Here is the original Search draft:

{campaign_pack.search.model_dump_json(indent=2)}

Here is the reviewer finding:

{finding.model_dump_json(indent=2)}

Expected campaign objective:

{campaign_objective}

Search intent:

{search_intent}

Repair only this Search execution.
"""
            )

            revised_pack.search = result.final_output

            repaired_channels.append(
                finding.channel
            )

        elif channel_name == "email":

            result = Runner.run_sync(
                email_repair_agent,
                f"""
Here is the CopyStrategyCard:

{campaign_pack.strategy_card.model_dump_json(indent=2)}

Here is the original Email draft:

{campaign_pack.email.model_dump_json(indent=2)}

Here is the reviewer finding:

{finding.model_dump_json(indent=2)}

Expected campaign objective:

{campaign_objective}

Repair only this Email execution.
"""
            )

            revised_pack.email = result.final_output

            repaired_channels.append(
                finding.channel
            )

        elif channel_name in {
            "landing page",
            "landing_page",
        }:

            result = Runner.run_sync(
                landing_page_repair_agent,
                f"""
Here is the CopyStrategyCard:

{campaign_pack.strategy_card.model_dump_json(indent=2)}

Here is the original Landing Page draft:

{campaign_pack.landing_page.model_dump_json(indent=2)}

Here is the reviewer finding:

{finding.model_dump_json(indent=2)}

Expected campaign objective:

{campaign_objective}

Repair only this Landing Page execution.
"""
            )

            revised_pack.landing_page = (
                result.final_output
            )

            repaired_channels.append(
                finding.channel
            )

        elif channel_name == "x":

            result = Runner.run_sync(
                x_repair_agent,
                f"""
Here is the CopyStrategyCard:

{campaign_pack.strategy_card.model_dump_json(indent=2)}

Here is the original X draft:

{campaign_pack.x.model_dump_json(indent=2)}

Here is the reviewer finding:

{finding.model_dump_json(indent=2)}

Expected campaign objective:

{campaign_objective}

Repair only this X execution.
"""
            )

            revised_pack.x = result.final_output

            repaired_channels.append(
                finding.channel
            )

        else:
            raise ValueError(
                f"Unsupported channel: {finding.channel}"
            )

    return CampaignRepairResult(
        campaign_pack=revised_pack,
        repaired_channels=repaired_channels,
        untouched_channels=untouched_channels,
    )
