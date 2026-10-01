from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_big_idea,
    build_desire_hypothesis,
    build_mechanism_hypothesis,
    build_objection_map,
    build_reader_profile,
    choose_message_entry_point,
    estimate_awareness,
    estimate_desire_intensity,
    estimate_market_sophistication,
    generate_creative_angles,
)

from writer_agent import (
    generate_headline_candidates,
    write_mechanism_section,
    write_opening,
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
