from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_big_idea,
    build_desire_hypothesis,
    build_mechanism_hypothesis,
    build_objection_map,
    build_offer_strategy,
    build_reader_profile,
    choose_message_entry_point,
    estimate_awareness,
    estimate_desire_intensity,
    estimate_market_sophistication,
    generate_creative_angles,
)

from campaign_pack import build_campaign_pack

from campaign_reviewer import review_campaign_pack

from agent_tools import (
    get_approved_brand_claims,
)

from brand_voice_reviewer import (
    review_brand_voice,
)

from claim_reviewer import (
    review_claim_evidence,
)

from copy_critic import (
    critique_sales_message,
)

from database import get_brand_profiles

from models import BrandProfile

from database import (
    create_approval_request,
    decide_approval,
    get_approval_record,
)

from revision_orchestrator import (
    run_revision_pass,
)

from revision_planner import (
    build_revision_plan,
)

from review_aggregator import (
    build_unified_review_report,
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

from strategy_card import build_copy_strategy_card

from writer_agent import (
    assemble_sales_message,
    generate_headline_candidates,
    write_mechanism_section,
    write_objection_section,
    write_offer_section,
    write_opening,
    write_proof_section,
)


load_dotenv()


brand_profile_id = 1

competitors = [
    "Jasper",
    "Copy.ai",
    "AdCreative.ai",
]


print("\nBUILDING RESEARCH...\n")

research_document = build_research_document(
    brand_profile_id,
    competitors
)


reader = build_reader_profile(
    research_document
)


desire = build_desire_hypothesis(
    research_document,
    reader
)


intensity = estimate_desire_intensity(
    research_document,
    reader,
    desire
)


awareness = estimate_awareness(
    research_document,
    reader,
    desire,
    intensity
)


entry_point = choose_message_entry_point(
    reader,
    desire,
    intensity,
    awareness
)


sophistication = estimate_market_sophistication(
    research_document
)


mechanism = build_mechanism_hypothesis(
    research_document,
    reader,
    desire
)


objections = build_objection_map(
    research_document,
    reader,
    desire,
    awareness,
    mechanism
)


big_idea = build_big_idea(
    reader,
    desire,
    mechanism,
    entry_point,
    sophistication,
    objections
)


angle_set = generate_creative_angles(
    big_idea,
    reader,
    desire,
    entry_point,
    mechanism,
    sophistication,
    objections
)


selected_angle = angle_set.angles[0]


print("\nSELECTED ANGLE\n")
print(selected_angle.angle_name)

print("\nCENTRAL ARGUMENT\n")
print(selected_angle.central_argument)


print("\nGENERATING HEADLINES...\n")


headline_set = generate_headline_candidates(
    reader,
    big_idea,
    selected_angle,
    entry_point
)


print("HEADLINE CANDIDATES\n")


for index, candidate in enumerate(
    headline_set.headlines,
    start=1
):
    print(f"HEADLINE {index}")

    print("\nHeadline:")
    print(candidate.headline)

    print("\nAttention principle:")
    print(candidate.attention_principle)

    print("\nAngle connection:")
    print(candidate.angle_connection)

    print("\nEvidence check:")
    print(candidate.evidence_check)

    print("\nRisk:")
    print(candidate.risk)

    print("\n" + "-" * 60 + "\n")


selected_headline = headline_set.headlines[0]


print("\nSELECTED HEADLINE\n")
print(selected_headline.headline)


print("\nWRITING OPENING...\n")


opening = write_opening(
    reader,
    big_idea,
    selected_angle,
    entry_point,
    selected_headline
)


print("OPENING DRAFT\n")


print("OPENING")
print(opening.opening)


print("\nRECOGNITION TRIGGER")
print(opening.recognition_trigger)


print("\nTRANSITION TO PROBLEM")
print(opening.transition_to_problem)


print("\nANGLE CONNECTION")
print(opening.angle_connection)


print("\nEVIDENCE CHECK")
print(opening.evidence_check)


print("\nWRITING MECHANISM SECTION...\n")


mechanism_section = write_mechanism_section(
    reader,
    big_idea,
    selected_angle,
    opening,
    mechanism,
    objections
)


print("MECHANISM SECTION\n")


print("PROBLEM EXPLANATION")
print(mechanism_section.problem_explanation)


print("\nMECHANISM EXPLANATION")
print(mechanism_section.mechanism_explanation)


print("\nREASON WHY")
print(mechanism_section.reason_why)


print("\nBRIDGE TO PRODUCT")
print(mechanism_section.bridge_to_product)


print("\nEVIDENCE CHECK")
print(mechanism_section.evidence_check)


print("\nWRITING PROOF SECTION...\n")


proof_section = write_proof_section(
    research_document,
    mechanism,
    objections,
    mechanism_section
)


print("PROOF SECTION\n")


print("PROOF POINTS")

for item in proof_section.proof_points:
    print(f"- {item}")


print("\nDEMONSTRATION PLAN")

for item in proof_section.demonstration_plan:
    print(f"- {item}")


print("\nVERIFIED CLAIMS USED")

for item in proof_section.verified_claims_used:
    print(f"- {item}")


print("\nMISSING PROOF")

for item in proof_section.missing_proof:
    print(f"- {item}")


print("\nPROOF COPY")
print(proof_section.proof_copy)


supplied_offer_terms = """
No pricing information has been supplied.

No free trial has been supplied.

No bonus has been supplied.

No guarantee or refund policy has been supplied.

No deadline or scarcity has been supplied.

The only confirmed next action for this test is:
join the waitlist.
"""


print("\nBUILDING OFFER STRATEGY...\n")


offer = build_offer_strategy(
    research_document,
    supplied_offer_terms
)


print("WRITING OBJECTION SECTION...\n")


objection_section = write_objection_section(
    objections,
    proof_section,
    offer,
    mechanism
)


print("OBJECTION SECTION\n")


for index, response in enumerate(
    objection_section.objection_responses,
    start=1
):
    print(f"OBJECTION RESPONSE {index}")

    print("\nObjection:")
    print(response.objection)

    print("\nAnswer:")
    print(response.answer)

    print("\nProof used:")

    if response.proof_used:
        for item in response.proof_used:
            print(f"- {item}")
    else:
        print("- None")

    print("\nStatus:")
    print(response.status)

    print("\n" + "-" * 50 + "\n")


print("UNRESOLVED OBJECTIONS")

if objection_section.unresolved_objections:
    for item in objection_section.unresolved_objections:
        print(f"- {item}")
else:
    print("- None")


print("\nRISK REVERSAL AVAILABLE")
print(
    objection_section.risk_reversal_available
)


print("\nOBJECTION COPY")
print(
    objection_section.objection_copy
)


campaign_objective = "Join the waitlist"


print("\nWRITING OFFER + CTA...\n")


offer_section = write_offer_section(
    offer,
    campaign_objective,
    objection_section
)


print("OFFER + CTA\n")


print("OFFER COPY")
print(offer_section.offer_copy)


print("\nTERMS STATED")

if offer_section.terms_stated:
    for item in offer_section.terms_stated:
        print(f"- {item}")
else:
    print("- None")


print("\nURGENCY USED")
print(offer_section.urgency_used)


print("\nCTA")
print(offer_section.cta)


print("\nEVIDENCE CHECK")
print(offer_section.evidence_check)


print("\nASSEMBLING COMPLETE SALES MESSAGE...\n")


complete_message = assemble_sales_message(
    selected_headline,
    opening,
    mechanism_section,
    proof_section,
    objection_section,
    offer_section,
)


print("COMPLETE SALES MESSAGE\n")


print("=" * 70)
print("HEADLINE")
print("=" * 70)

print(complete_message.headline)


print("\n" + "=" * 70)
print("OPENING")
print("=" * 70)

print(complete_message.opening)


print("\n" + "=" * 70)
print("MECHANISM")
print("=" * 70)

print(complete_message.mechanism_section)


print("\n" + "=" * 70)
print("PROOF")
print("=" * 70)

print(complete_message.proof_section)


print("\n" + "=" * 70)
print("OBJECTIONS")
print("=" * 70)

print(complete_message.objection_section)


print("\n" + "=" * 70)
print("OFFER")
print("=" * 70)

print(complete_message.offer_section)


print("\n" + "=" * 70)
print("FULL COPY")
print("=" * 70)

print(complete_message.full_copy)


print("\nBUILDING COPY STRATEGY CARD...\n")


strategy_card = build_copy_strategy_card(
    reader,
    desire,
    awareness,
    sophistication,
    entry_point,
    mechanism,
    big_idea,
    selected_angle,
    objections,
    proof_section,
    offer,
    complete_message,
)


print("=" * 70)
print("COPY STRATEGY CARD")
print("=" * 70)


print("\nREADER")
print(strategy_card.reader)


print("\nPRIMARY PROBLEM")
print(strategy_card.primary_problem)


print("\nDEEPER DESIRE")
print(strategy_card.deeper_desire)


print("\nAWARENESS")
print(strategy_card.awareness)


print("\nMARKET SOPHISTICATION")
print(strategy_card.sophistication)


print("\nMESSAGE ENTRY")
print(strategy_card.message_entry)


print("\nMECHANISM")
print(strategy_card.mechanism)


print("\nBIG IDEA")
print(strategy_card.big_idea)


print("\nSELECTED ANGLE")
print(strategy_card.selected_angle)


print("\nMAJOR OBJECTIONS")

for item in strategy_card.major_objections:
    print(f"- {item}")


print("\nPROOF BOUNDARY")

if strategy_card.proof_boundary:
    for item in strategy_card.proof_boundary:
        print(f"- {item}")
else:
    print("- No major missing proof recorded")


print("\nOFFER BOUNDARY")

if strategy_card.offer_boundary:
    for item in strategy_card.offer_boundary:
        print(f"- {item}")
else:
    print("- No major missing offer elements recorded")


print("\n" + "=" * 70)
print("FINAL SALES MESSAGE")
print("=" * 70)

print(strategy_card.final_message)


campaign_objective = "Join the waitlist"

search_intent = "AI ad idea generator"


print("\nBUILDING CHANNEL SPECS...\n")


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


print("WRITING META AD...\n")


meta_ad = write_meta_feed_ad(
    complete_message,
    strategy_card,
    meta_spec,
)


print("WRITING SEARCH AD...\n")


search_ad = write_search_ad(
    complete_message,
    strategy_card,
    search_spec,
    search_intent,
)


print("WRITING EMAIL...\n")


email = write_email(
    complete_message,
    strategy_card,
    email_spec,
)


print("WRITING LANDING PAGE...\n")


landing_page = write_landing_page(
    complete_message,
    strategy_card,
    landing_page_spec,
)


print("WRITING X DRAFT...\n")


x_draft = write_x_draft(
    complete_message,
    strategy_card,
    x_spec,
)


print("BUILDING CAMPAIGN PACK...\n")


campaign_pack = build_campaign_pack(
    strategy_card,
    meta_ad,
    search_ad,
    email,
    landing_page,
    x_draft,
)


print("=" * 70)
print("CROSS-CHANNEL CAMPAIGN PACK")
print("=" * 70)


print("\nBIG IDEA")
print(
    campaign_pack.strategy_card.big_idea
)


print("\nSELECTED ANGLE")
print(
    campaign_pack.strategy_card.selected_angle
)


print("\n" + "=" * 70)
print("META FEED")
print("=" * 70)

print("\nPrimary text:")
print(campaign_pack.meta.primary_text)

print("\nHeadline:")
print(campaign_pack.meta.headline)

print("\nCTA:")
print(campaign_pack.meta.cta)


print("\n" + "=" * 70)
print("GOOGLE SEARCH")
print("=" * 70)


print("\nHeadlines:")

for headline in campaign_pack.search.headlines:
    print(f"- {headline}")


print("\nDescriptions:")

for description in campaign_pack.search.descriptions:
    print(f"- {description}")


print("\nCTA:")
print(campaign_pack.search.cta)


print("\n" + "=" * 70)
print("EMAIL")
print("=" * 70)


print("\nSubject lines:")

for subject in campaign_pack.email.subject_lines:
    print(f"- {subject}")


print("\nPreview:")
print(campaign_pack.email.preview_text)


print("\nBody:")
print(campaign_pack.email.body)


print("\nCTA:")
print(campaign_pack.email.cta)


print("\n" + "=" * 70)
print("LANDING PAGE")
print("=" * 70)


print("\nHero:")
print(
    campaign_pack.landing_page.hero_headline
)


print("\nSubheadline:")
print(
    campaign_pack.landing_page.hero_subheadline
)


print("\nProblem:")
print(
    campaign_pack.landing_page.problem_section
)


print("\nMechanism:")
print(
    campaign_pack.landing_page.mechanism_section
)


print("\nCTA:")
print(
    campaign_pack.landing_page.cta
)


print("\n" + "=" * 70)
print("X")
print("=" * 70)


print("\nPost 1:")
print(campaign_pack.x.hook)


for index, post in enumerate(
    campaign_pack.x.posts,
    start=2
):
    print(f"\nPost {index}:")
    print(post)


print("\nCTA:")
print(campaign_pack.x.cta)


print("\nREVIEWING CROSS-CHANNEL CONSISTENCY...\n")


consistency_report = review_campaign_pack(
    campaign_pack,
    campaign_objective,
)


print("=" * 70)
print("CROSS-CHANNEL CONSISTENCY REPORT")
print("=" * 70)


print("\nSHARED STRATEGY")
print(consistency_report.shared_strategy)


for finding in consistency_report.channel_findings:

    print("\n" + "=" * 70)
    print(finding.channel.upper())
    print("=" * 70)

    print("\nSTRATEGY ALIGNMENT")
    print(finding.strategy_alignment)

    print("\nDRIFT FOUND")

    if finding.drift_found:
        for item in finding.drift_found:
            print(f"- {item}")
    else:
        print("- None")

    print("\nUNSUPPORTED CLAIMS")

    if finding.unsupported_claims:
        for item in finding.unsupported_claims:
            print(f"- {item}")
    else:
        print("- None")

    print("\nCTA CONFLICT")
    print(finding.cta_conflict)

    print("\nREVISION NEEDED")
    print(finding.revision_needed)


print("\n" + "=" * 70)
print("CAMPAIGN-LEVEL FINDINGS")
print("=" * 70)


print("\nSTRATEGY DRIFT")

if consistency_report.strategy_drift:
    for item in consistency_report.strategy_drift:
        print(f"- {item}")
else:
    print("- None")


print("\nUNSUPPORTED CLAIMS")

if consistency_report.unsupported_claims:
    for item in consistency_report.unsupported_claims:
        print(f"- {item}")
else:
    print("- None")


print("\nCTA CONFLICTS")

if consistency_report.cta_conflicts:
    for item in consistency_report.cta_conflicts:
        print(f"- {item}")
else:
    print("- None")


print("\nREVISION NEEDED")
print(consistency_report.revision_needed)


profiles = get_brand_profiles()


saved_profile = next(
    (
        profile
        for profile in profiles
        if profile["id"] == brand_profile_id
    ),
    None,
)


if saved_profile is None:
    raise RuntimeError(
        f"Brand profile {brand_profile_id} was not found."
    )


brand_profile = BrandProfile(
    name=saved_profile["name"],
    tone=saved_profile["tone"],
    preferred_words=saved_profile["preferred_words"],
    avoided_words=saved_profile["avoided_words"],
)


print("\nRUNNING COPY CRITIC...\n")


copy_critique = critique_sales_message(
    complete_message,
    strategy_card,
)


verified_claims_json = get_approved_brand_claims(
    brand_profile_id
)


print("RUNNING CLAIM REVIEW...\n")


claim_report = review_claim_evidence(
    complete_message,
    research_document,
    strategy_card,
    verified_claims_json,
)


print("RUNNING BRAND VOICE REVIEW...\n")


brand_review = review_brand_voice(
    complete_message,
    brand_profile,
)


print("RUNNING CHANNEL REVIEW...\n")


# Reuse the consistency review already run above, so the
# printed channel report and the unified report always agree.
channel_report = consistency_report


print("BUILDING UNIFIED REVIEW REPORT...\n")


unified_report = build_unified_review_report(
    copy_critique,
    claim_report,
    brand_review,
    channel_report,
)


print("=" * 70)
print("UNIFIED REVIEW REPORT")
print("=" * 70)


print("\nCOPY ISSUES")

if unified_report.copy_issues:
    for item in unified_report.copy_issues:
        print(f"- {item}")
else:
    print("- None")


print("\nCLAIM ISSUES")

if unified_report.claim_issues:
    for item in unified_report.claim_issues:
        print(f"- {item}")
else:
    print("- None")


print("\nBRAND VOICE ISSUES")

if unified_report.brand_voice_issues:
    for item in unified_report.brand_voice_issues:
        print(f"- {item}")
else:
    print("- None")


print("\nCHANNEL ISSUES")

if unified_report.channel_issues:
    for item in unified_report.channel_issues:
        print(f"- {item}")
else:
    print("- None")


print("\nSECTIONS REQUIRING WORK")

if unified_report.sections_requiring_work:
    for item in unified_report.sections_requiring_work:
        print(f"- {item}")
else:
    print("- None")


print("\nRESEARCH NEEDED")

if unified_report.research_needed:
    for item in unified_report.research_needed:
        print(f"- {item}")
else:
    print("- None")


print("\n" + "=" * 70)
print("READY FOR APPROVAL")
print("=" * 70)


print(
    unified_report.ready_for_approval
)


print("\nBUILDING REVISION PLAN...\n")


revision_plan = build_revision_plan(
    unified_report,
    copy_critique,
    claim_report,
    brand_review,
    channel_report,
)


print("=" * 70)
print("REVISION PLAN")
print("=" * 70)


print("\nRESEARCH TASKS")

if revision_plan.research_tasks:
    for item in revision_plan.research_tasks:
        print(f"- {item}")
else:
    print("- None")


print("\nEVIDENCE REPAIRS")

if revision_plan.evidence_repairs:
    for item in revision_plan.evidence_repairs:
        print(f"- {item}")
else:
    print("- None")


print("\nBRAND REPAIRS")

if revision_plan.brand_repairs:
    for item in revision_plan.brand_repairs:
        print(f"- {item}")
else:
    print("- None")


print("\nCOPY REPAIRS")

if revision_plan.copy_repairs:
    for item in revision_plan.copy_repairs:
        print(f"- {item}")
else:
    print("- None")


print("\nCHANNEL REPAIRS")

if revision_plan.channel_repairs:
    for item in revision_plan.channel_repairs:
        print(f"- {item}")
else:
    print("- None")


print("\n" + "=" * 70)
print("EXECUTION ORDER")
print("=" * 70)


for index, step in enumerate(
    revision_plan.execution_order,
    start=1,
):
    print(f"{index}. {step}")


print("\nRUNNING BOUNDED REVISION PASS...\n")


result = run_revision_pass(
    complete_message=complete_message,
    strategy_card=strategy_card,
    research_document=research_document,
    brand_profile=brand_profile,
    campaign_pack=campaign_pack,
    campaign_objective=campaign_objective,
    search_intent=search_intent,
    verified_claims_json=verified_claims_json,
    revision_plan=revision_plan,
)


print("=" * 70)
print("REVISION ORCHESTRATION RESULT")
print("=" * 70)


print("\nSTATUS")
print(result.status)


print("\nACTIONS TAKEN")

if result.actions_taken:
    for index, action in enumerate(
        result.actions_taken,
        start=1,
    ):
        print(f"{index}. {action}")
else:
    print("- No automated changes were required")


print("\nRESEARCH BLOCKERS")

if result.research_blockers:
    for item in result.research_blockers:
        print(f"- {item}")
else:
    print("- None")


print("\nREADY FOR APPROVAL")

print(
    result.unified_report.ready_for_approval
)


print("\nSECTIONS STILL REQUIRING WORK")

if result.unified_report.sections_requiring_work:
    for section in (
        result.unified_report
        .sections_requiring_work
    ):
        print(f"- {section}")
else:
    print("- None")


print("\n" + "=" * 70)
print("FINAL CORE MESSAGE")
print("=" * 70)


print(
    result.complete_message.full_copy
)


print("\n" + "=" * 70)
print("HUMAN APPROVAL GATE")
print("=" * 70)


if (
    result.status
    != "ready_for_human_approval"
):

    print(
        "\nCampaign cannot enter human approval yet."
    )

    print(
        f"\nCurrent status: {result.status}"
    )

    raise SystemExit


campaign_id = 1


approval_id = create_approval_request(
    campaign_id,
    result.complete_message,
)


print(
    f"\nApproval request created: {approval_id}"
)


print("\n" + "=" * 70)
print("MESSAGE REQUIRING HUMAN APPROVAL")
print("=" * 70)


print(
    result.complete_message.full_copy
)


reviewer = input(
    "\nReviewer name: "
).strip()


if not reviewer:
    raise ValueError(
        "Reviewer name cannot be empty."
    )


decision = input(
    "\nType APPROVE or REJECT: "
).strip().lower()


if decision == "approve":

    final_decision = "approved"

elif decision == "reject":

    final_decision = "rejected"

else:

    raise ValueError(
        "Please type APPROVE or REJECT."
    )


note = input(
    "\nReview note (optional): "
).strip()


decide_approval(
    approval_id,
    final_decision,
    reviewer,
    note,
)


approval = get_approval_record(
    approval_id
)


print("\n" + "=" * 70)
print("APPROVAL RECORD")
print("=" * 70)


print("\nID")
print(approval.id)


print("\nCAMPAIGN ID")
print(approval.campaign_id)


print("\nSTATUS")
print(approval.status)


print("\nREVIEWER")
print(approval.reviewer)


print("\nNOTE")
print(
    approval.note
    or "No note supplied"
)


print("\nAPPROVED AT")
print(
    approval.approved_at
    or "Not approved"
)
