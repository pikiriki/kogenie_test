from pydantic import BaseModel

from agents import Agent, Runner

from brand_voice_reviewer import (
    review_brand_voice,
)

from brand_voice_reviser import (
    revise_brand_voice,
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

from claim_repairer import (
    repair_claim,
)

from claim_reviewer import (
    review_claim_evidence,
)

from copy_critic import (
    critique_sales_message,
)

from copy_reviser import (
    revise_sales_message,
)

from review_aggregator import (
    build_unified_review_report,
)

from models import (
    BrandProfile,
    CampaignPack,
    ClaimEvidenceReport,
    CompleteSalesMessage,
    CopyStrategyCard,
    ResearchDocument,
    RevisionOrchestrationResult,
    RevisionPlan,
)


CORE_SECTIONS = {
    "headline",
    "opening",
    "mechanism_section",
    "proof_section",
    "objection_section",
    "offer_section",
}


class SectionRepairText(BaseModel):
    text: str


claim_section_editor = Agent(
    name="Claim Section Editor",

    instructions="""
You edit ONE section of an existing sales message.

You receive:

- the original section text
- one or more approved ClaimRepairResult objects

Your only job is to apply those claim repairs
inside the supplied section.

Rules:

- Make the minimum textual change needed.
- Preserve all surrounding meaning.
- Preserve all claims not included in the repair list.
- Do not improve style.
- Do not alter brand voice unless necessary
  to make the repaired sentence grammatical.
- Do not add benefits.
- Do not add product capabilities.
- Do not add statistics.
- Do not add performance claims.
- Do not add evidence.
- Do not change the offer.
- Do not change the CTA.

If a repair has:

action_taken = "qualify"

replace the unsupported meaning with
repaired_claim.

If:

action_taken = "remove"

remove that unsupported claim while keeping
the surrounding section coherent.

Return only the resulting section text.
""",

    model="gpt-6-luna",

    output_type=SectionRepairText,
)


def rebuild_full_copy(
    message: CompleteSalesMessage,
) -> CompleteSalesMessage:

    full_copy = "\n\n".join([
        message.headline,
        message.opening,
        message.mechanism_section,
        message.proof_section,
        message.objection_section,
        message.offer_section,
    ])

    return message.model_copy(
        update={
            "full_copy": full_copy,
        }
    )


def to_complete_message(
    revision,
) -> CompleteSalesMessage:

    return CompleteSalesMessage(
        headline=revision.headline,
        opening=revision.opening,
        mechanism_section=(
            revision.mechanism_section
        ),
        proof_section=(
            revision.proof_section
        ),
        objection_section=(
            revision.objection_section
        ),
        offer_section=(
            revision.offer_section
        ),
        full_copy=revision.full_copy,
    )


def apply_claim_repairs(
    message: CompleteSalesMessage,
    claim_report: ClaimEvidenceReport,
    research_document: ResearchDocument,
    strategy_card: CopyStrategyCard,
    verified_claims_json: str,
) -> tuple[CompleteSalesMessage, list[str]]:

    working_message = message.model_copy(
        deep=True
    )

    actions_taken = []

    repairs_by_section = {}

    for claim_review in claim_report.claims:

        action = (
            claim_review
            .required_action
            .strip()
            .lower()
        )

        if action == "keep":
            continue

        if action == "obtain evidence":

            raise RuntimeError(
                "Research-dependent claim reached "
                "claim repair stage."
            )

        if claim_review.section not in CORE_SECTIONS:

            raise ValueError(
                "Unsupported claim section: "
                + claim_review.section
            )

        repair = repair_claim(
            claim_review,
            research_document,
            strategy_card,
            verified_claims_json,
        )

        repairs_by_section.setdefault(
            claim_review.section,
            [],
        ).append(
            repair
        )

    for section, repairs in repairs_by_section.items():

        original_text = getattr(
            working_message,
            section,
        )

        repairs_text = "\n\n".join(
            repair.model_dump_json(indent=2)
            for repair in repairs
        )

        result = Runner.run_sync(
            claim_section_editor,
            f"""
Here is the section name:

{section}

Here is the original section text:

{original_text}

Here are the approved claim repairs:

{repairs_text}

Apply only these repairs.

Do not make unrelated editorial changes.
"""
        )

        setattr(
            working_message,
            section,
            result.final_output.text,
        )

        actions_taken.append(
            f"Applied claim repairs to {section}."
        )

    working_message = rebuild_full_copy(
        working_message
    )

    return (
        working_message,
        actions_taken,
    )


def regenerate_campaign_pack(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    campaign_objective: str,
    search_intent: str,
) -> CampaignPack:

    meta_spec = get_meta_feed_spec(
        campaign_objective
    )

    search_spec = get_google_search_spec(
        campaign_objective
    )

    email_spec = get_email_spec(
        campaign_objective
    )

    landing_spec = get_landing_page_spec(
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
        landing_spec,
    )


    x = write_x_draft(
        complete_message,
        strategy_card,
        x_spec,
    )

    return build_campaign_pack(
        strategy_card,
        meta,
        search,
        email,
        landing_page,
        x,
    )


def run_revision_pass(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    research_document: ResearchDocument,
    brand_profile: BrandProfile,
    campaign_pack: CampaignPack,
    campaign_objective: str,
    search_intent: str,
    verified_claims_json: str,
    revision_plan: RevisionPlan,
) -> RevisionOrchestrationResult:

    current_message = complete_message.model_copy(
        deep=True
    )

    current_strategy_card = strategy_card.model_copy(
        deep=True
    )

    current_pack = campaign_pack.model_copy(
        deep=True
    )

    actions_taken = []

    if revision_plan.research_tasks:

        copy_critique = critique_sales_message(
            current_message,
            current_strategy_card,
        )


        claim_report = review_claim_evidence(
            current_message,
            research_document,
            current_strategy_card,
            verified_claims_json,
        )


        brand_review = review_brand_voice(
            current_message,
            brand_profile,
        )


        channel_report = review_campaign_pack(
            current_pack,
            campaign_objective,
        )

        unified_report = build_unified_review_report(
            copy_critique,
            claim_report,
            brand_review,
            channel_report,
        )

        return RevisionOrchestrationResult(
            status="blocked_by_research",
            actions_taken=[
                (
                    "Stopped before automated revision "
                    "because additional evidence is required."
                )
            ],
            research_blockers=(
                revision_plan.research_tasks
            ),
            complete_message=current_message,
            campaign_pack=current_pack,
            copy_critique=copy_critique,
            claim_report=claim_report,
            brand_review=brand_review,
            channel_report=channel_report,
            unified_report=unified_report,
        )

    claim_report = review_claim_evidence(
        current_message,
        research_document,
        current_strategy_card,
        verified_claims_json,
    )

    claim_repairs_needed = any(
        review.required_action in {
            "qualify",
            "remove",
        }
        for review in claim_report.claims
    )

    core_changed = False


    if claim_repairs_needed:

        (
            current_message,
            claim_actions,
        ) = apply_claim_repairs(
            current_message,
            claim_report,
            research_document,
            current_strategy_card,
            verified_claims_json,
        )

        actions_taken.extend(
            claim_actions
        )

        core_changed = True

        claim_report = review_claim_evidence(
            current_message,
            research_document,
            current_strategy_card,
            verified_claims_json,
        )

        if claim_report.revision_needed:

            copy_critique = critique_sales_message(
                current_message,
                current_strategy_card,
            )

            brand_review = review_brand_voice(
                current_message,
                brand_profile,
            )

            channel_report = review_campaign_pack(
                current_pack,
                campaign_objective,
            )

            unified_report = build_unified_review_report(
                copy_critique,
                claim_report,
                brand_review,
                channel_report,
            )

            return RevisionOrchestrationResult(
                status="core_still_needs_work",
                actions_taken=actions_taken,
                research_blockers=[],
                complete_message=current_message,
                campaign_pack=current_pack,
                copy_critique=copy_critique,
                claim_report=claim_report,
                brand_review=brand_review,
                channel_report=channel_report,
                unified_report=unified_report,
            )

    current_strategy_card = (
        current_strategy_card.model_copy(
            update={
                "final_message": (
                    current_message.full_copy
                )
            }
        )
    )

    brand_review = review_brand_voice(
        current_message,
        brand_profile,
    )

    if brand_review.sections_to_revise:

        brand_revision = revise_brand_voice(
            current_message,
            brand_profile,
            brand_review,
        )

        current_message = to_complete_message(
            brand_revision
        )

        actions_taken.append(
            "Applied targeted brand-voice revision."
        )

        core_changed = True

        brand_review = review_brand_voice(
            current_message,
            brand_profile,
        )


        claim_report = review_claim_evidence(
            current_message,
            research_document,
            current_strategy_card,
            verified_claims_json,
        )

        if (
            brand_review.sections_to_revise
            or claim_report.revision_needed
        ):

            copy_critique = critique_sales_message(
                current_message,
                current_strategy_card,
            )

            channel_report = review_campaign_pack(
                current_pack,
                campaign_objective,
            )

            unified_report = build_unified_review_report(
                copy_critique,
                claim_report,
                brand_review,
                channel_report,
            )

            return RevisionOrchestrationResult(
                status="core_still_needs_work",
                actions_taken=actions_taken,
                research_blockers=[],
                complete_message=current_message,
                campaign_pack=current_pack,
                copy_critique=copy_critique,
                claim_report=claim_report,
                brand_review=brand_review,
                channel_report=channel_report,
                unified_report=unified_report,
            )

    current_strategy_card = (
        current_strategy_card.model_copy(
            update={
                "final_message": (
                    current_message.full_copy
                )
            }
        )
    )

    copy_critique = critique_sales_message(
        current_message,
        current_strategy_card,
    )

    if copy_critique.sections_to_revise:

        copy_revision = revise_sales_message(
            current_message,
            current_strategy_card,
            copy_critique,
        )


        current_message = to_complete_message(
            copy_revision
        )


        actions_taken.append(
            "Applied targeted copy-quality revision."
        )

        core_changed = True

        copy_critique = critique_sales_message(
            current_message,
            current_strategy_card,
        )


        claim_report = review_claim_evidence(
            current_message,
            research_document,
            current_strategy_card,
            verified_claims_json,
        )


        brand_review = review_brand_voice(
            current_message,
            brand_profile,
        )

        if (
            copy_critique.sections_to_revise
            or claim_report.revision_needed
            or brand_review.sections_to_revise
        ):

            channel_report = review_campaign_pack(
                current_pack,
                campaign_objective,
            )

            unified_report = build_unified_review_report(
                copy_critique,
                claim_report,
                brand_review,
                channel_report,
            )

            return RevisionOrchestrationResult(
                status="core_still_needs_work",
                actions_taken=actions_taken,
                research_blockers=[],
                complete_message=current_message,
                campaign_pack=current_pack,
                copy_critique=copy_critique,
                claim_report=claim_report,
                brand_review=brand_review,
                channel_report=channel_report,
                unified_report=unified_report,
            )

    current_strategy_card = (
        current_strategy_card.model_copy(
            update={
                "final_message": (
                    current_message.full_copy
                )
            }
        )
    )

    if core_changed:

        current_pack = regenerate_campaign_pack(
            current_message,
            current_strategy_card,
            campaign_objective,
            search_intent,
        )

        actions_taken.append(
            (
                "Regenerated channel executions from "
                "the revised core message."
            )
        )

    channel_report = review_campaign_pack(
        current_pack,
        campaign_objective,
    )

    if channel_report.revision_needed:

        repair_result = repair_campaign_pack(
            current_pack,
            channel_report,
            campaign_objective,
            search_intent,
        )


        current_pack = (
            repair_result.campaign_pack
        )


        actions_taken.append(
            "Repaired only failing channel executions."
        )

        channel_report = review_campaign_pack(
            current_pack,
            campaign_objective,
        )

        if channel_report.revision_needed:

            unified_report = build_unified_review_report(
                copy_critique,
                claim_report,
                brand_review,
                channel_report,
            )

            return RevisionOrchestrationResult(
                status="channel_still_needs_work",
                actions_taken=actions_taken,
                research_blockers=[],
                complete_message=current_message,
                campaign_pack=current_pack,
                copy_critique=copy_critique,
                claim_report=claim_report,
                brand_review=brand_review,
                channel_report=channel_report,
                unified_report=unified_report,
            )

    copy_critique = critique_sales_message(
        current_message,
        current_strategy_card,
    )


    claim_report = review_claim_evidence(
        current_message,
        research_document,
        current_strategy_card,
        verified_claims_json,
    )


    brand_review = review_brand_voice(
        current_message,
        brand_profile,
    )


    channel_report = review_campaign_pack(
        current_pack,
        campaign_objective,
    )

    unified_report = build_unified_review_report(
        copy_critique,
        claim_report,
        brand_review,
        channel_report,
    )

    if unified_report.ready_for_approval:

        status = "ready_for_human_approval"

    else:

        status = "completed_with_remaining_issues"

    return RevisionOrchestrationResult(
        status=status,
        actions_taken=actions_taken,
        research_blockers=[],
        complete_message=current_message,
        campaign_pack=current_pack,
        copy_critique=copy_critique,
        claim_report=claim_report,
        brand_review=brand_review,
        channel_report=channel_report,
        unified_report=unified_report,
    )
