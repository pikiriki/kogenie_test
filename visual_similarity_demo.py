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

from channel_specs import get_meta_feed_spec

from channel_writer import write_meta_feed_ad

from database import get_brand_profiles

from models import BrandProfile

from visual_reviewer import (
    review_generated_visual,
)

from visual_generator import (
    generate_visual,
)

from visual_generation_spec import (
    build_visual_generation_spec,
)

from visual_style import (
    build_visual_style_spec,
)

from visual_strategy import (
    build_meta_visual_brief,
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


print("\nBUILDING META FEED SPEC...\n")


channel_spec = get_meta_feed_spec(
    campaign_objective
)


print("WRITING META FEED AD...\n")


meta_ad = write_meta_feed_ad(
    complete_message,
    strategy_card,
    channel_spec,
)


print("=" * 70)
print("META FEED AD")
print("=" * 70)


print("\nPRIMARY TEXT")
print(meta_ad.primary_text)


print("\nHEADLINE")
print(meta_ad.headline)


print("\nCTA")
print(meta_ad.cta)


print("\nSTRATEGY PRESERVED")
print(meta_ad.strategy_preserved)


print("\nEVIDENCE CHECK")
print(meta_ad.evidence_check)


# meta_feed_ad_demo.py never loaded the brand profile,
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


print("\nBUILDING VISUAL CREATIVE BRIEF...\n")


visual_brief = build_meta_visual_brief(
    strategy_card=strategy_card,
    meta_draft=meta_ad,
    # The Meta spec built above is named channel_spec in this demo.
    channel_spec=channel_spec,
    brand_profile=brand_profile,
)


print("=" * 70)
print("VISUAL CREATIVE BRIEF")
print("=" * 70)


print("\nVISUAL JOB")
print(
    visual_brief.visual_job
)


print("\nSUBJECT")
print(
    visual_brief.subject
)


print("\nSCENE")
print(
    visual_brief.scene
)


print("\nCOMPOSITION")
print(
    visual_brief.composition
)


print("\nTEXT HIERARCHY")

for item in visual_brief.text_hierarchy:
    print(f"- {item}")


print("\nPRODUCT ROLE")
print(
    visual_brief.product_role
)


print("\nVISUAL PROOF")
print(
    visual_brief.visual_proof
)


print("\nAVOID")

for item in visual_brief.avoid:
    print(f"- {item}")


print("\nCOPY CONNECTION")
print(
    visual_brief.copy_connection
)


print("\nBUILDING VISUAL STYLE SPEC...\n")


style_spec = build_visual_style_spec(
    visual_brief,
    brand_profile,
)


print("=" * 70)
print("VISUAL STYLE SPEC")
print("=" * 70)


print("\nAESTHETIC DIRECTION")
print(
    style_spec.aesthetic_direction
)


print("\nPALETTE DIRECTION")
print(
    style_spec.palette_direction
)


print("\nTYPOGRAPHY DIRECTION")
print(
    style_spec.typography_direction
)


print("\nIMAGERY STYLE")
print(
    style_spec.imagery_style
)


print("\nSPACING DENSITY")
print(
    style_spec.spacing_density
)


print("\nSHAPE LANGUAGE")
print(
    style_spec.shape_language
)


print("\nBRAND CONSISTENCY RULES")

for rule in (
    style_spec.brand_consistency_rules
):
    print(f"- {rule}")


print("\nPROHIBITED STYLES")

for item in (
    style_spec.prohibited_styles
):
    print(f"- {item}")


width = 1024
height = 1024

# This demo chain never defined a campaign; use the real
# existing campaign 1 rather than creating a new one.
campaign_id = 1


print("\nBUILDING VISUAL GENERATION SPEC...\n")


generation_spec = (
    build_visual_generation_spec(
        strategy_card=strategy_card,
        visual_brief=visual_brief,
        style_spec=style_spec,
        meta_draft=meta_ad,
        # The Meta spec is named channel_spec in this demo chain.
        channel_spec=channel_spec,
        width=width,
        height=height,
    )
)


print("=" * 70)
print("VISUAL GENERATION SPEC")
print("=" * 70)


print("\nCANVAS")
print(
    generation_spec.canvas
)


print("\nOBJECTIVE")
print(
    generation_spec.objective
)


print("\nREQUIRED ELEMENTS")

for item in (
    generation_spec.required_elements
):
    print(f"- {item}")


print("\nTEXT TO RENDER")

for item in (
    generation_spec.text_to_render
):
    print(f"- {item}")


print("\nEVIDENCE CONSTRAINTS")

for item in (
    generation_spec.evidence_constraints
):
    print(f"- {item}")


print("\nNEGATIVE CONSTRAINTS")

for item in (
    generation_spec.negative_constraints
):
    print(f"- {item}")


print("\n" + "=" * 70)
print("GENERATION INSTRUCTION")
print("=" * 70)


print(
    generation_spec.generation_instruction
)


print("\nGENERATING FIRST REAL VISUAL...\n")


generated_visual = generate_visual(
    campaign_id=campaign_id,
    channel="Meta",
    generation_spec=generation_spec,
)


print("=" * 70)
print("GENERATED VISUAL")
print("=" * 70)


print("\nCAMPAIGN")
print(
    generated_visual.campaign_id
)


print("\nCHANNEL")
print(
    generated_visual.channel
)


print("\nMODEL")
print(
    generated_visual.model
)


print("\nIMAGE PATH")
print(
    generated_visual.image_path
)


print("\nMETADATA PATH")
print(
    generated_visual.metadata_path
)


print("\nAPPROVAL STATUS")
print(
    generated_visual.approval_status
)


print("\nREVIEWING GENERATED VISUAL...\n")


visual_review = review_generated_visual(
    generated_visual=generated_visual,
    generation_spec=generation_spec,
    visual_brief=visual_brief,
    style_spec=style_spec,
)


print("=" * 70)
print("VISUAL REVIEW REPORT")
print("=" * 70)


print("\nOBJECTIVE ALIGNMENT")
print(
    visual_review.objective_alignment
)


print("\nREQUIRED ELEMENTS PRESENT")

if visual_review.required_elements_present:

    for item in (
        visual_review
        .required_elements_present
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nMISSING ELEMENTS")

if visual_review.missing_elements:

    for item in (
        visual_review.missing_elements
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nTEXT ACCURACY")
print(
    visual_review.text_accuracy
)


print("\nCOMPOSITION ALIGNMENT")
print(
    visual_review.composition_alignment
)


print("\nSTYLE ALIGNMENT")
print(
    visual_review.style_alignment
)


print("\nEVIDENCE VIOLATIONS")

if visual_review.evidence_violations:

    for item in (
        visual_review.evidence_violations
    ):
        print(f"- {item}")

else:

    print("- None")


print(
    "\nNEGATIVE CONSTRAINT VIOLATIONS"
)

if (
    visual_review
    .negative_constraint_violations
):

    for item in (
        visual_review
        .negative_constraint_violations
    ):
        print(f"- {item}")

else:

    print("- None")


print("\nREVISION NEEDED")
print(
    visual_review.revision_needed
)


from database import (
    get_visual_assets,
)

from visual_similarity import (
    review_visual_repetition,
)


# The copied review demo names these generated_visual and
# visual_review; alias them to the names Lesson 99 uses.
candidate_visual = generated_visual
candidate_review = visual_review


if candidate_review.revision_needed:

    print(
        "\nCandidate visual still has "
        "unresolved visual-review issues."
    )

    print(
        "Fix those before evaluating "
        "historical repetition."
    )

    raise SystemExit


historical_assets = (
    get_visual_assets()
)


print(
    "\nApproved historical visual assets:",
    len(historical_assets),
)


print(
    "\nREVIEWING VISUAL REPETITION...\n"
)


similarity_report = (
    review_visual_repetition(
        candidate_visual=(
            candidate_visual
        ),

        current_strategy=(
            strategy_card
        ),

        current_visual_brief=(
            visual_brief
        ),

        historical_assets=(
            historical_assets
        ),
    )
)


print("=" * 70)
print("VISUAL SIMILARITY REPORT")
print("=" * 70)


print("\nHISTORY AVAILABLE")
print(
    similarity_report.history_available
)


print("\nHISTORY NOTE")
print(
    similarity_report.history_note
)


print("\nEXACT DUPLICATE ASSET IDS")


if (
    similarity_report
    .exact_duplicate_asset_ids
):

    for asset_id in (
        similarity_report
        .exact_duplicate_asset_ids
    ):

        print(
            f"- Visual Asset {asset_id}"
        )

else:

    print("- None")


print("\nSIMILAR HISTORICAL ASSETS")


if similarity_report.similar_assets:

    for match in (
        similarity_report.similar_assets
    ):

        print("\n" + "-" * 60)

        print(
            f"Visual Asset {match.asset_id}"
        )

        print(
            "Overlap:",
            match.overlap_level,
        )

        print(
            "Same visual territory:",
            match.same_visual_territory,
        )

        print("\nWhy similar:")
        print(
            match.similarity_reason
        )

        print("\nShared visual patterns:")

        for pattern in (
            match.shared_visual_patterns
        ):

            print(
                f"- {pattern}"
            )

        print("\nMeaningful differences:")

        if match.meaningful_differences:

            for difference in (
                match.meaningful_differences
            ):

                print(
                    f"- {difference}"
                )

        else:

            print("- None")

        print("\nNovelty gaps:")

        if match.novelty_gaps:

            for gap in match.novelty_gaps:

                print(
                    f"- {gap}"
                )

        else:

            print("- None")

else:

    print("- None")


print(
    "\nREPEATED VISUAL PATTERNS"
)


if (
    similarity_report
    .repeated_visual_patterns
):

    for pattern in (
        similarity_report
        .repeated_visual_patterns
    ):

        print(f"- {pattern}")

else:

    print("- None")


print("\nNOVELTY GAPS")


if similarity_report.novelty_gaps:

    for gap in (
        similarity_report.novelty_gaps
    ):

        print(f"- {gap}")

else:

    print("- None")


print(
    "\nDIFFERENTIATION REVIEW NEEDED"
)

print(
    similarity_report.revision_needed
)
