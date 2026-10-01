from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_desire_hypothesis,
    build_reader_profile,
    estimate_awareness,
    estimate_desire_intensity,
)


load_dotenv()


brand_profile_id = 1

competitors = [
    "Jasper",
    "Copy.ai",
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


print("AWARENESS HYPOTHESIS\n")


print("LEVEL")
print(awareness.level)


print("\nWHAT THE READER ALREADY KNOWS")

for item in awareness.what_the_reader_knows:
    print(f"- {item}")


print("\nWHAT THE READER DOES NOT YET KNOW")

for item in awareness.what_the_reader_does_not_yet_know:
    print(f"- {item}")


print("\nSUPPORTING EVIDENCE")

for item in awareness.supporting_evidence:
    print(f"- {item}")


print("\nCONFIDENCE")
print(awareness.confidence)
