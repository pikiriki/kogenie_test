from brand_voice_reviewer import (
    review_brand_voice,
)

from campaign_pack import (
    build_campaign_pack,
)

from campaign_repair import (
    repair_campaign_pack,
)

from campaign_reviewer import (
    review_campaign_pack,
)

from channel_specs import (
    get_email_spec,
    get_google_search_spec,
    get_landing_page_spec,
    get_meta_feed_spec,
    get_x_spec,
)

from channel_writer import (
    write_email,
    write_landing_page,
    write_meta_feed_ad,
    write_search_ad,
    write_x_draft,
)

from claim_reviewer import (
    review_claim_evidence,
)

from copy_critic import (
    critique_sales_message,
)

from models import (
    BrandProfile,
    CampaignRefreshResult,
    ResearchDocument,
    StrategyRegenerationResult,
)


def refresh_campaign_channels(
    regeneration: StrategyRegenerationResult,
    research_document: ResearchDocument,
    brand_profile: BrandProfile,
    verified_claims_json: str,
    campaign_objective: str,
    search_intent: str,
) -> CampaignRefreshResult:

    complete_message = (
        regeneration.complete_message
    )

    strategy_card = (
        regeneration.updated_strategy_card
    )

    copy_critique = critique_sales_message(
        complete_message,
        strategy_card,
    )

    claim_report = review_claim_evidence(
        complete_message,
        research_document,
        strategy_card,
        verified_claims_json,
    )

    brand_review = review_brand_voice(
        complete_message,
        brand_profile,
    )

    core_ready = (
        not copy_critique.sections_to_revise
        and not claim_report.revision_needed
        and not brand_review.sections_to_revise
    )

    if not core_ready:

        return CampaignRefreshResult(
            status="core_not_ready",
            campaign_pack=None,
            channel_report=None,
            repaired_channels=[],
        )

    meta_spec = get_meta_feed_spec(
        campaign_objective
    )


    search_spec = get_google_search_spec(
        campaign_objective
    )


    email_spec = get_email_spec(
        campaign_objective
    )


    landing_page_spec = get_landing_page_spec(
        campaign_objective
    )


    x_spec = get_x_spec(
        campaign_objective
    )

    meta = write_meta_feed_ad(
        complete_message,
        strategy_card,
        meta_spec,
    )

    search = write_search_ad(
        complete_message,
        strategy_card,
        search_spec,
        search_intent,
    )

    email = write_email(
        complete_message,
        strategy_card,
        email_spec,
    )

    landing_page = write_landing_page(
        complete_message,
        strategy_card,
        landing_page_spec,
    )

    x = write_x_draft(
        complete_message,
        strategy_card,
        x_spec,
    )

    campaign_pack = build_campaign_pack(
        strategy_card,
        meta,
        search,
        email,
        landing_page,
        x,
    )

    channel_report = review_campaign_pack(
        campaign_pack,
        campaign_objective,
    )

    repaired_channels = []

    if not channel_report.revision_needed:

        return CampaignRefreshResult(
            status="ready_for_human_approval",
            campaign_pack=campaign_pack,
            channel_report=channel_report,
            repaired_channels=[],
        )

    repair_result = repair_campaign_pack(
        campaign_pack,
        channel_report,
        campaign_objective,
        search_intent,
    )

    campaign_pack = (
        repair_result.campaign_pack
    )

    repaired_channels = (
        repair_result.repaired_channels
    )

    channel_report = review_campaign_pack(
        campaign_pack,
        campaign_objective,
    )

    if channel_report.revision_needed:

        return CampaignRefreshResult(
            status="channel_still_needs_work",
            campaign_pack=campaign_pack,
            channel_report=channel_report,
            repaired_channels=(
                repaired_channels
            ),
        )

    return CampaignRefreshResult(
        status="ready_for_human_approval",
        campaign_pack=campaign_pack,
        channel_report=channel_report,
        repaired_channels=repaired_channels,
    )
