from models import (
    BrandVoiceReview,
    ChannelConsistencyReport,
    ClaimEvidenceReport,
    CopyCritique,
    RevisionPlan,
    UnifiedReviewReport,
)


CLAIM_ACTIONS = {
    "keep",
    "qualify",
    "remove",
    "obtain evidence",
}


def unique_items(
    items: list[str],
) -> list[str]:

    return list(
        dict.fromkeys(items)
    )


def build_revision_plan(
    unified_report: UnifiedReviewReport,
    copy_critique: CopyCritique,
    claim_report: ClaimEvidenceReport,
    brand_review: BrandVoiceReview,
    channel_report: ChannelConsistencyReport,
) -> RevisionPlan:

    if unified_report.ready_for_approval:

        return RevisionPlan(
            research_tasks=[],
            evidence_repairs=[],
            brand_repairs=[],
            copy_repairs=[],
            channel_repairs=[],
            execution_order=[
                (
                    "No automated revision tasks remain. "
                    "Send the campaign for human approval."
                )
            ],
        )

    research_tasks = []
    evidence_repairs = []
    brand_repairs = []
    copy_repairs = []
    channel_repairs = []

    for review in claim_report.claims:

        action = (
            review.required_action
            .strip()
            .lower()
        )

        if action not in CLAIM_ACTIONS:
            raise ValueError(
                "Unknown claim action: "
                + action
            )

        if action == "obtain evidence":

            research_tasks.append(
                (
                    f"Obtain evidence for claim in "
                    f"{review.section}: "
                    f"{review.claim}"
                )
            )

            continue

        if action == "qualify":

            evidence_repairs.append(
                (
                    f"Qualify claim in {review.section}: "
                    f"{review.claim} | "
                    f"Unsupported part: "
                    f"{review.unsupported_part}"
                )
            )

            continue

        if action == "remove":

            evidence_repairs.append(
                (
                    f"Remove unsupported claim from "
                    f"{review.section}: "
                    f"{review.claim}"
                )
            )

            continue

    brand_instructions = " | ".join(
        brand_review.revision_instructions
    )

    for section in brand_review.sections_to_revise:

        task = (
            f"Revise brand voice in {section}"
        )

        if brand_instructions:
            task += (
                f": {brand_instructions}"
            )

        brand_repairs.append(
            task
        )

    copy_instructions = " | ".join(
        copy_critique.revision_instructions
    )

    for section in copy_critique.sections_to_revise:

        task = (
            f"Revise copy quality in {section}"
        )

        if copy_instructions:
            task += (
                f": {copy_instructions}"
            )

        copy_repairs.append(
            task
        )

    for finding in channel_report.channel_findings:

        if not finding.revision_needed:
            continue

        reasons = []

        reasons.extend(
            finding.drift_found
        )

        reasons.extend(
            finding.unsupported_claims
        )

        cta_conflict = (
            finding.cta_conflict
            .strip()
        )

        if (
            cta_conflict
            and cta_conflict.lower()
            not in {
                "none",
                "no conflict",
            }
        ):
            reasons.append(
                cta_conflict
            )

        if reasons:

            channel_repairs.append(
                (
                    f"Repair {finding.channel}: "
                    + " | ".join(reasons)
                )
            )

        else:

            channel_repairs.append(
                (
                    f"Repair {finding.channel}: "
                    "reviewer marked the channel "
                    "for revision."
                )
            )

    research_tasks = unique_items(
        research_tasks
    )

    evidence_repairs = unique_items(
        evidence_repairs
    )

    brand_repairs = unique_items(
        brand_repairs
    )

    copy_repairs = unique_items(
        copy_repairs
    )

    channel_repairs = unique_items(
        channel_repairs
    )

    execution_order = []

    if research_tasks:

        execution_order.append(
            (
                "Complete the missing research tasks first, "
                "update the approved evidence, rebuild the "
                "research context, and rerun claim review."
            )
        )

    if evidence_repairs:

        execution_order.append(
            (
                "Apply claim-level evidence repairs to the "
                "core sales message, then rerun the Claim "
                "Evidence Reviewer."
            )
        )

    if brand_repairs:

        execution_order.append(
            (
                "Apply targeted brand-voice repairs only "
                "after factual meaning is stable, then rerun "
                "the Brand Voice Reviewer and Claim Reviewer."
            )
        )

    if copy_repairs:

        execution_order.append(
            (
                "Apply targeted copy-quality repairs, then "
                "rerun the Copy Critic, Claim Reviewer, "
                "and Brand Voice Reviewer."
            )
        )

    core_message_changes = bool(
        research_tasks
        or evidence_repairs
        or brand_repairs
        or copy_repairs
    )

    if core_message_changes:

        execution_order.append(
            (
                "Regenerate or refresh channel executions "
                "from the stabilized core campaign before "
                "performing final channel-specific repair."
            )
        )

    if channel_repairs:

        execution_order.append(
            (
                "Apply targeted repairs to only the channel "
                "executions that still fail, then rerun the "
                "Cross-Channel Consistency Reviewer."
            )
        )

    execution_order.append(
        (
            "Rebuild the UnifiedReviewReport. "
            "If all automated gates pass, send the "
            "campaign for human approval."
        )
    )

    return RevisionPlan(
        research_tasks=research_tasks,
        evidence_repairs=evidence_repairs,
        brand_repairs=brand_repairs,
        copy_repairs=copy_repairs,
        channel_repairs=channel_repairs,
        execution_order=execution_order,
    )
