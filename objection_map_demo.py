from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_desire_hypothesis,
    build_mechanism_hypothesis,
    build_objection_map,
    build_reader_profile,
    estimate_awareness,
    estimate_desire_intensity,
)


load_dotenv()


brand_profile_id = 1

competitors = [
    "Jasper",
    "Copy.ai",
    "AdCreative.ai",
]


print("\nBUILDING RESEARCH DOCUMENT...\n")

research_document = build_research_document(
    brand_profile_id,
    competitors
)


print("BUILDING READER PROFILE...\n")

reader_profile = build_reader_profile(
    research_document
)


print("BUILDING DESIRE HYPOTHESIS...\n")

desire_hypothesis = build_desire_hypothesis(
    research_document,
    reader_profile
)


print("ESTIMATING DESIRE INTENSITY...\n")

desire_intensity = estimate_desire_intensity(
    research_document,
    reader_profile,
    desire_hypothesis
)


print("ESTIMATING AWARENESS...\n")

awareness = estimate_awareness(
    research_document,
    reader_profile,
    desire_hypothesis,
    desire_intensity
)


print("BUILDING MECHANISM...\n")

mechanism = build_mechanism_hypothesis(
    research_document,
    reader_profile,
    desire_hypothesis
)


print("BUILDING OBJECTION MAP...\n")

objection_map = build_objection_map(
    research_document,
    reader_profile,
    desire_hypothesis,
    awareness,
    mechanism
)


print("OBJECTION MAP\n")


for index, objection in enumerate(
    objection_map.objections,
    start=1
):
    print(f"OBJECTION {index}")

    print("\nReader concern:")
    print(objection.objection)

    print("\nType:")
    print(objection.objection_type)

    print("\nSupporting evidence:")

    for item in objection.supporting_evidence:
        print(f"- {item}")

    print("\nWhat answer is needed:")
    print(objection.what_answer_is_needed)

    print("\nProof required:")

    for item in objection.proof_required:
        print(f"- {item}")

    print("\nConfidence:")
    print(objection.confidence)

    print("\n" + "-" * 60 + "\n")
