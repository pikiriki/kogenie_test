from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_desire_hypothesis,
    build_reader_profile,
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

intensity = estimate_desire_intensity(
    research_document,
    reader_profile,
    desire_hypothesis
)


print("DESIRE INTENSITY\n")


print("LEVEL")
print(intensity.level)


print("\nSUPPORTING EVIDENCE")

for item in intensity.evidence:
    print(f"- {item}")


print("\nURGENCY SIGNALS")

for item in intensity.urgency_signals:
    print(f"- {item}")


print("\nUNCERTAINTY")
print(intensity.uncertainty)
