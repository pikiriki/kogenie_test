from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_desire_hypothesis,
    build_mechanism_hypothesis,
    build_reader_profile,
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


print("BUILDING MECHANISM HYPOTHESIS...\n")

mechanism = build_mechanism_hypothesis(
    research_document,
    reader_profile,
    desire_hypothesis
)


print("MECHANISM HYPOTHESIS\n")


print("DESIRED OUTCOME")
print(mechanism.desired_outcome)


print("\nPRODUCT CAPABILITY")
print(mechanism.product_capability)


print("\nCAUSAL EXPLANATION")
print(mechanism.causal_explanation)


print("\nSUPPORTING EVIDENCE")

for item in mechanism.supporting_evidence:
    print(f"- {item}")


print("\nUNSUPPORTED LEAPS")

for item in mechanism.unsupported_leaps:
    print(f"- {item}")


print("\nCONFIDENCE")
print(mechanism.confidence)
