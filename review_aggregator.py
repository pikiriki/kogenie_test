from models import (
    BrandVoiceReview,
    ChannelConsistencyReport,
    ClaimEvidenceReport,
    CopyCritique,
    UnifiedReviewReport,
)


CORE_SECTIONS = {
    "headline",
    "opening",
    "mechanism_section",
    "proof_section",
    "objection_section",
    "offer_section",
}


def unique_items(
    items: list[str],
) -> list[str]:

    return list(
        dict.fromkeys(items)
    )


def build_unified_review_report(
    copy_critique: CopyCritique,
    claim_report: ClaimEvidenceReport,
    brand_review: BrandVoiceReview,
    channel_report: ChannelConsistencyReport,
) -> UnifiedReviewReport:

    copy_issues = []

    for issue in copy_critique.clarity_issues:
        copy_issues.append(
            f"[Clarity] {issue}"
        )

    for issue in copy_critique.specificity_issues:
        copy_issues.append(
            f"[Specificity] {issue}"
        )

    for issue in copy_critique.credibility_issues:
        copy_issues.append(
            f"[Credibility] {issue}"
        )

    for issue in copy_critique.flow_issues:
        copy_issues.append(
            f"[Flow] {issue}"
        )

    for issue in copy_critique.repetition_issues:
        copy_issues.append(
            f"[Repetition] {issue}"
        )

    claim_issues = []

    for review in claim_report.claims:

        if review.support_status == "supported":
            continue

        if review.support_status == "partially supported":

            claim_issues.append(
                "[Partially supported] "
                + review.claim
                + " | Unsupported part: "
                + review.unsupported_part
            )

        elif review.support_status == "unsupported":

            claim_issues.append(
                "[Unsupported] "
                + review.claim
                + " | Action: "
                + review.required_action
            )

    brand_voice_issues = []

    for issue in brand_review.avoided_language_violations:

        brand_voice_issues.append(
            f"[Avoided language] {issue}"
        )

    for issue in brand_review.voice_drift:

        brand_voice_issues.append(
            f"[Voice drift] {issue}"
        )

    channel_issues = []

    for finding in channel_report.channel_findings:

        if not finding.revision_needed:
            continue

        for issue in finding.drift_found:

            channel_issues.append(
                f"[{finding.channel} — Drift] {issue}"
            )

        for issue in finding.unsupported_claims:

            channel_issues.append(
                f"[{finding.channel} — Claim] {issue}"
            )

        if (
            finding.cta_conflict
            and finding.cta_conflict.strip().lower()
            not in {"none", "no conflict"}
        ):

            channel_issues.append(
                f"[{finding.channel} — CTA] "
                + finding.cta_conflict
            )

    sections_requiring_work = []

    sections_requiring_work.extend(
        copy_critique.sections_to_revise
    )

    sections_requiring_work.extend(
        brand_review.sections_to_revise
    )

    for review in claim_report.claims:

        if (
            review.required_action != "keep"
            and review.section in CORE_SECTIONS
        ):
            sections_requiring_work.append(
                review.section
            )

    sections_requiring_work = unique_items(
        sections_requiring_work
    )

    research_needed = []

    for review in claim_report.claims:

        if review.required_action == "obtain evidence":

            research_needed.append(
                "Obtain evidence for: "
                + review.claim
            )

    research_needed = unique_items(
        research_needed
    )

    ready_for_approval = (
        not sections_requiring_work
        and not research_needed
        and not channel_report.revision_needed
        and not claim_report.revision_needed
        and not brand_review.sections_to_revise
        and not copy_critique.sections_to_revise
    )

    return UnifiedReviewReport(
        copy_issues=unique_items(
            copy_issues
        ),
        claim_issues=unique_items(
            claim_issues
        ),
        brand_voice_issues=unique_items(
            brand_voice_issues
        ),
        channel_issues=unique_items(
            channel_issues
        ),
        sections_requiring_work=(
            sections_requiring_work
        ),
        research_needed=research_needed,
        ready_for_approval=ready_for_approval,
    )
