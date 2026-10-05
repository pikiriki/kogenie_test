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
