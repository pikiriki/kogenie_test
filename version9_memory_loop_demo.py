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

from database import (
    get_campaign_memories,
    initialize_database,
)

from agent_tools import (
    get_approved_brand_claims,
)

from campaign_refresh import (
    refresh_campaign_channels,
)

from database import (
    create_approval_request,
    decide_approval,
    get_approval_record,
    get_campaign_memories,
    save_campaign_memory,
)

from campaign_memory import (
    build_campaign_memory,
)

from strategy_regenerator import (
    regenerate_core_message,
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

from strategy_application import (
    apply_selected_strategy,
)

from strategy_selection import (
    create_strategy_selection,
    get_viable_candidate_indices,
)

from alternative_strategy_evaluator import (
    evaluate_alternative_strategy_set,
)

from alternative_strategy_generator import (
    generate_alternative_strategies,
)

from novelty_guard import (
    build_novelty_guidance,
)

from repetition_reviewer import (
    review_strategic_repetition,
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


# Make sure every table exists (including campaign_memories)
# before spending API calls on the pipeline below.
initialize_database()


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


print("\nLOADING CAMPAIGN MEMORY...\n")


memories = get_campaign_memories()


print(
    f"Approved campaign memories found: {len(memories)}"
)


print("\nREVIEWING STRATEGIC REPETITION...\n")


repetition_report = review_strategic_repetition(
    strategy_card,
    memories,
)


print("=" * 70)
print("STRATEGIC REPETITION REPORT")
print("=" * 70)


print("\nPROPOSED BIG IDEA")
print(
    repetition_report.proposed_big_idea
)


print("\nPROPOSED ANGLE")
print(
    repetition_report.proposed_angle
)


print("\nSIMILAR CAMPAIGNS")


if repetition_report.similar_campaigns:

    for match in (
        repetition_report.similar_campaigns
    ):

        print("\n" + "-" * 60)

        print(
            f"Campaign {match.campaign_id}"
        )

        print("\nOverlap level:")
        print(
            match.overlap_level
        )

        print("\nWhy similar:")
        print(
            match.similarity_reason
        )

        print("\nShared elements:")

        for item in match.shared_elements:
            print(f"- {item}")

        print("\nMeaningful differences:")

        if match.meaningful_differences:

            for item in (
                match.meaningful_differences
            ):
                print(f"- {item}")

        else:
            print("- None")

else:

    print("- None")


print("\nREPEATED PATTERNS")

if repetition_report.repeated_patterns:

    for item in (
        repetition_report.repeated_patterns
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nNOVELTY GAPS")

if repetition_report.novelty_gaps:

    for item in (
        repetition_report.novelty_gaps
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nREVISION NEEDED")
print(
    repetition_report.revision_needed
)


print("\nBUILDING NOVELTY GUIDANCE...\n")


guidance = build_novelty_guidance(
    research_document,
    strategy_card,
    repetition_report,
    memories,
    campaign_objective,
)


print("=" * 70)
print("NOVELTY GUIDANCE")
print("=" * 70)


print("\nWHAT MUST STAY FIXED")

for item in guidance.what_must_stay_fixed:
    print(f"- {item}")


print("\nOVERUSED PATTERNS")

if guidance.overused_patterns:

    for item in guidance.overused_patterns:
        print(f"- {item}")

else:

    print("- None")


print("\nUNEXPLORED READER TENSIONS")

if guidance.unexplored_reader_tensions:

    for item in (
        guidance.unexplored_reader_tensions
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nUNEXPLORED MECHANISM EMPHASES")

if guidance.unexplored_mechanism_emphases:

    for item in (
        guidance.unexplored_mechanism_emphases
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nFORBIDDEN SHORTCUTS")

for item in guidance.forbidden_shortcuts:
    print(f"- {item}")


print("\nSTRATEGY GUIDANCE")

for index, item in enumerate(
    guidance.strategy_guidance,
    start=1,
):
    print(f"{index}. {item}")


print("\nGENERATING ALTERNATIVE STRATEGIES...\n")


strategy_set = generate_alternative_strategies(
    research_document,
    strategy_card,
    repetition_report,
    guidance,
    memories,
    campaign_objective,
)


if not strategy_set.strategies:

    print(
        "\nNo alternative strategy generation "
        "is currently required."
    )

    print(
        "\nReason:"
        "\nThe current strategy was not flagged "
        "for material historical repetition."
    )

    raise SystemExit


print("=" * 70)
print("ALTERNATIVE STRATEGY SET")
print("=" * 70)


for index, strategy in enumerate(
    strategy_set.strategies,
    start=1,
):

    print("\n" + "=" * 70)
    print(f"STRATEGY {index}")
    print("=" * 70)

    print("\nREADER TENSION")
    print(strategy.reader_tension)


    print("\nMECHANISM EMPHASIS")
    print(strategy.mechanism_emphasis)


    print("\nPROPOSED BIG IDEA")
    print(strategy.proposed_big_idea)


    print("\nPROPOSED ANGLE")
    print(strategy.proposed_angle)

    print("\nEVIDENCE USED")

    if strategy.evidence_used:
        for item in strategy.evidence_used:
            print(f"- {item}")
    else:
        print("- None")

    print("\nEVIDENCE BOUNDARY")

    if strategy.evidence_boundary:
        for item in strategy.evidence_boundary:
            print(f"- {item}")
    else:
        print("- None")

    print("\nHISTORICAL DIFFERENCE")
    print(
        strategy.historical_difference
    )


print(
    "\nEVALUATING ALTERNATIVE STRATEGIES...\n"
)


evaluation_set = (
    evaluate_alternative_strategy_set(
        strategy_set,
        research_document,
        guidance,
        memories,
        campaign_objective,
    )
)


if not evaluation_set.evaluations:

    print(
        "\nNo alternative strategies "
        "currently require evaluation."
    )

    print(
        "\nThe production strategy was not "
        "flagged for historical repetition."
    )

    raise SystemExit


print("=" * 70)
print("ALTERNATIVE STRATEGY EVALUATIONS")
print("=" * 70)


for evaluation in evaluation_set.evaluations:

    print("\n" + "=" * 70)

    print(
        f"STRATEGY {evaluation.strategy_index}"
    )

    print("=" * 70)

    print("\nRESEARCH GROUNDING")
    print(
        evaluation.research_grounding
    )


    print("\nHISTORICAL DISTINCTNESS")
    print(
        evaluation.historical_distinctness
    )


    print("\nMECHANISM FIT")
    print(
        evaluation.mechanism_fit
    )


    print("\nEVIDENCE SAFETY")
    print(
        evaluation.evidence_safety
    )


    print("\nREADER RELEVANCE")
    print(
        evaluation.reader_relevance
    )

    print("\nWEAKNESSES")

    if evaluation.weaknesses:

        for weakness in evaluation.weaknesses:
            print(f"- {weakness}")

    else:

        print("- None")

    print("\nRECOMMENDATION")
    print(
        evaluation.recommendation
    )


if not strategy_set.strategies:

    print(
        "\nNo alternative strategies are "
        "currently available for selection."
    )

    print(
        "\nThe current production strategy "
        "was not flagged for historical repetition."
    )

    raise SystemExit


viable_indices = (
    get_viable_candidate_indices(
        evaluation_set
    )
)


print("\nVIABLE STRATEGIES")


if viable_indices:

    for index in viable_indices:
        print(f"- Strategy {index}")

else:

    print("- None")


if not viable_indices:

    print(
        "\nNo strategy candidate currently "
        "qualifies for human selection."
    )

    print(
        "\nRevise or regenerate alternatives first."
    )

    raise SystemExit


for index in viable_indices:

    strategy = strategy_set.strategies[
        index - 1
    ]

    evaluation = (
        evaluation_set.evaluations[
            index - 1
        ]
    )

    print("\n" + "=" * 70)

    print(
        f"STRATEGY {index} — VIABLE"
    )

    print("=" * 70)


    print("\nREADER TENSION")
    print(strategy.reader_tension)


    print("\nMECHANISM EMPHASIS")
    print(strategy.mechanism_emphasis)


    print("\nBIG IDEA")
    print(strategy.proposed_big_idea)


    print("\nANGLE")
    print(strategy.proposed_angle)


    print("\nWEAKNESSES")

    if evaluation.weaknesses:

        for weakness in evaluation.weaknesses:
            print(f"- {weakness}")

    else:

        print("- None")


print(
    "\nEnter the strategy number you want "
    "to select."
)

print(
    "Or type NONE to decline all candidates."
)


choice = input(
    "\nSelection: "
).strip()


if choice.lower() == "none":

    reason = input(
        "\nWhy are you declining "
        "all candidates? "
    ).strip()

    selection = create_strategy_selection(
        strategy_set=strategy_set,
        evaluation_set=evaluation_set,
        candidate_index=None,
        human_reason=reason,
    )

else:

    try:

        candidate_index = int(
            choice
        )

    except ValueError:

        raise ValueError(
            "Selection must be a strategy "
            "number or NONE."
        )

    reason = input(
        "\nWhy are you selecting "
        f"Strategy {candidate_index}? "
    ).strip()

    selection = create_strategy_selection(
        strategy_set=strategy_set,
        evaluation_set=evaluation_set,
        candidate_index=candidate_index,
        human_reason=reason,
    )


print("\n" + "=" * 70)
print("STRATEGY SELECTION")
print("=" * 70)


print("\nSTATUS")
print(
    selection.selection_status
)


print("\nCANDIDATE INDEX")
print(
    selection.candidate_index
    if selection.candidate_index is not None
    else "None"
)


print("\nEVALUATION SUMMARY")
print(
    selection.evaluation_summary
)


print("\nHUMAN REASON")
print(
    selection.human_reason
)


print("\nSELECTED AT")
print(
    selection.selected_at
)


if selection.selection_status != "selected":

    print(
        "\nNo alternative strategy was selected."
    )

    print(
        "The current active strategy remains unchanged."
    )

    raise SystemExit


print("\n" + "=" * 70)
print("OLD ACTIVE STRATEGY")
print("=" * 70)


print("\nACTIVE READER TENSION")
print(
    strategy_card.active_reader_tension
)


print("\nMECHANISM EMPHASIS")
print(
    strategy_card.mechanism_emphasis
)


print("\nBIG IDEA")
print(
    strategy_card.big_idea
)


print("\nANGLE")
print(
    strategy_card.selected_angle
)


print("\nOLD FINAL MESSAGE LENGTH")

print(
    len(strategy_card.final_message)
)


print("\nAPPLYING SELECTED STRATEGY...\n")


application = apply_selected_strategy(
    current_strategy=strategy_card,
    strategy_set=strategy_set,
    evaluation_set=evaluation_set,
    selection=selection,
    campaign_objective=campaign_objective,
)


updated_strategy = (
    application.updated_strategy_card
)


print("=" * 70)
print("NEW ACTIVE STRATEGY")
print("=" * 70)


print("\nACTIVE READER TENSION")
print(
    updated_strategy.active_reader_tension
)


print("\nMECHANISM EMPHASIS")
print(
    updated_strategy.mechanism_emphasis
)


print("\nBIG IDEA")
print(
    updated_strategy.big_idea
)


print("\nANGLE")
print(
    updated_strategy.selected_angle
)


print("\nNEW FINAL MESSAGE LENGTH")

print(
    len(updated_strategy.final_message)
)


print("\nAPPLIED CHANGES")

for item in application.applied_changes:
    print(f"- {item}")


print("\nPRESERVED CONSTRAINTS")

for item in application.preserved_constraints:
    print(f"- {item}")


print("\nHUMAN SELECTION REASON")
print(
    application.human_reason
)


# The Lessons 83-88 demo chain never loaded the brand profile,
# so load it here (same pattern as Lesson 75).
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


verified_claims_json = get_approved_brand_claims(
    brand_profile_id
)


print("\nREGENERATING CORE MESSAGE...\n")


regeneration = regenerate_core_message(
    application=application,
    research_document=research_document,
    verified_claims_json=(
        verified_claims_json
    ),
    offer_strategy=offer,
    brand_profile=brand_profile,
    campaign_objective=(
        campaign_objective
    ),
)


new_message = regeneration.complete_message

new_strategy_card = (
    regeneration.updated_strategy_card
)


print("=" * 70)
print("STRATEGY-DRIVEN REGENERATION")
print("=" * 70)


print("\nREGENERATION REASON")
print(
    regeneration.regeneration_reason
)


print("\nACTIVE READER TENSION")
print(
    new_strategy_card.active_reader_tension
)


print("\nMECHANISM EMPHASIS")
print(
    new_strategy_card.mechanism_emphasis
)


print("\nBIG IDEA")
print(
    new_strategy_card.big_idea
)


print("\nANGLE")
print(
    new_strategy_card.selected_angle
)


print("\n" + "=" * 70)
print("REGENERATED SALES MESSAGE")
print("=" * 70)


print(new_message.full_copy)


print("\n" + "=" * 70)
print("INVALIDATED DOWNSTREAM ARTIFACTS")
print("=" * 70)


for item in regeneration.invalidated_artifacts:
    print(f"- {item}")


print("\nRUNNING COPY CRITIC...\n")


copy_critique = critique_sales_message(
    new_message,
    new_strategy_card,
)


print("RUNNING CLAIM REVIEW...\n")


claim_report = review_claim_evidence(
    new_message,
    research_document,
    new_strategy_card,
    verified_claims_json,
)


print("RUNNING BRAND VOICE REVIEW...\n")


brand_review = review_brand_voice(
    new_message,
    brand_profile,
)


core_ready = (
    not copy_critique.sections_to_revise
    and not claim_report.revision_needed
    and not brand_review.sections_to_revise
)


print("\n" + "=" * 70)
print("CORE REGENERATION REVIEW")
print("=" * 70)


print("\nCOPY SECTIONS NEEDING WORK")

if copy_critique.sections_to_revise:

    for section in (
        copy_critique.sections_to_revise
    ):
        print(f"- {section}")

else:

    print("- None")


print("\nCLAIM REVISION NEEDED")
print(
    claim_report.revision_needed
)


print("\nBRAND SECTIONS NEEDING WORK")

if brand_review.sections_to_revise:

    for section in (
        brand_review.sections_to_revise
    ):
        print(f"- {section}")

else:

    print("- None")


print("\nCORE READY FOR NEXT STAGE")
print(core_ready)


# The Lessons 83-89 demo chain never set these,
# so define them here (same values as earlier lessons).
search_intent = "AI ad idea generator"

campaign_id = 1


print(
    "\nREGENERATING CHANNELS "
    "FROM NEW STRATEGY...\n"
)


refresh = refresh_campaign_channels(
    regeneration=regeneration,
    research_document=research_document,
    brand_profile=brand_profile,
    verified_claims_json=(
        verified_claims_json
    ),
    campaign_objective=(
        campaign_objective
    ),
    search_intent=search_intent,
)


print("=" * 70)
print("CAMPAIGN REFRESH RESULT")
print("=" * 70)


print("\nSTATUS")
print(refresh.status)


print("\nREPAIRED CHANNELS")

if refresh.repaired_channels:

    for channel in refresh.repaired_channels:
        print(f"- {channel}")

else:

    print("- None")


if refresh.status == "core_not_ready":

    print(
        "\nThe regenerated core message "
        "still has unresolved review issues."
    )

    print(
        "Do not regenerate or approve "
        "the campaign yet."
    )

    raise SystemExit


if (
    refresh.status
    == "channel_still_needs_work"
):

    print(
        "\nOne bounded channel repair pass "
        "was completed, but issues remain."
    )

    print(
        "Human inspection is required "
        "before another repair pass."
    )

    raise SystemExit


campaign_pack = refresh.campaign_pack


print("\n" + "=" * 70)
print("META")
print("=" * 70)

print(
    campaign_pack.meta.primary_text
)

print("\nHeadline:")
print(
    campaign_pack.meta.headline
)


print("\n" + "=" * 70)
print("SEARCH")
print("=" * 70)


for headline in (
    campaign_pack.search.headlines
):
    print(f"- {headline}")


print("\n" + "=" * 70)
print("EMAIL")
print("=" * 70)

print(
    campaign_pack.email.body
)


print("\n" + "=" * 70)
print("LANDING PAGE")
print("=" * 70)

print(
    campaign_pack
    .landing_page
    .hero_headline
)

print()

print(
    campaign_pack
    .landing_page
    .hero_subheadline
)


print("\n" + "=" * 70)
print("X")
print("=" * 70)

print(
    campaign_pack.x.hook
)

for post in campaign_pack.x.posts:
    print("\n" + post)


choice = input(
    "\nCreate human approval request "
    "for this regenerated campaign? "
    "(yes/no): "
).strip().lower()


if choice != "yes":

    print(
        "\nNo approval request created."
    )

    print(
        "The regenerated campaign remains "
        "unapproved."
    )

    raise SystemExit


approval_id = create_approval_request(
    campaign_id,
    regeneration.complete_message,
)


print(
    f"\nApproval request created: "
    f"{approval_id}"
)


print("\n" + "=" * 70)
print("CORE MESSAGE REQUIRING APPROVAL")
print("=" * 70)


print(
    regeneration
    .complete_message
    .full_copy
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
    "\nReview note: "
).strip()


decide_approval(
    approval_id=approval_id,
    decision=final_decision,
    reviewer=reviewer,
    note=note,
)


approval_record = get_approval_record(
    approval_id
)


if approval_record.status == "rejected":

    print(
        "\nCampaign rejected."
    )

    print(
        "Campaign memory will NOT be updated."
    )

    raise SystemExit


if approval_record.status != "approved":

    raise RuntimeError(
        "Unexpected approval state."
    )


new_memory = build_campaign_memory(
    strategy_card=(
        regeneration
        .updated_strategy_card
    ),
    approval_record=approval_record,
    outcome_context=(
        "No campaign outcome data recorded."
    ),
)


save_campaign_memory(
    new_memory
)


print(
    "\nNew approved campaign memory saved."
)


memories = get_campaign_memories()


print("\n" + "=" * 70)
print("UPDATED CAMPAIGN MEMORY LIBRARY")
print("=" * 70)


print(
    f"\nMemories stored: {len(memories)}"
)


for memory in memories:

    print(
        f"\nCampaign {memory.campaign_id}"
    )

    print(
        f"Big Idea: "
        f"{memory.approved_big_idea}"
    )

    print(
        f"Angle: "
        f"{memory.approved_angle}"
    )

    print(
        f"Outcome: "
        f"{memory.outcome_context}"
    )
