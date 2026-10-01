from models import (
    CampaignPack,
    CopyStrategyCard,
    EmailDraft,
    LandingPageDraft,
    MetaFeedAdDraft,
    SearchAdDraft,
    XDraft,
)


def build_campaign_pack(
    strategy_card: CopyStrategyCard,
    meta: MetaFeedAdDraft,
    search: SearchAdDraft,
    email: EmailDraft,
    landing_page: LandingPageDraft,
    x: XDraft,
) -> CampaignPack:

    return CampaignPack(
        strategy_card=strategy_card,
        meta=meta,
        search=search,
        email=email,
        landing_page=landing_page,
        x=x,
    )
