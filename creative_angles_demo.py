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


print("GENERATING CREATIVE ANGLES...\n")


angle_set = generate_creative_angles(
    big_idea,
    reader,
    desire,
    entry_point,
    mechanism,
    sophistication,
    objections
)


print("CREATIVE ANGLES\n")


for index, angle in enumerate(
    angle_set.angles,
    start=1
):
    print(f"ANGLE {index}")

    print("\nName:")
    print(angle.angle_name)

    print("\nCentral argument:")
    print(angle.central_argument)

    print("\nReader hook:")
    print(angle.reader_hook)

    print("\nMechanism emphasis:")
    print(angle.mechanism_emphasis)

    print("\nSupporting evidence:")

    for evidence in angle.supporting_evidence:
        print(f"- {evidence}")

    print("\nRisk of repetition:")
    print(angle.risk_of_repetition)

    print("\n" + "-" * 60 + "\n")
