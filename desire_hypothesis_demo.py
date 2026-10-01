from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_desire_hypothesis,
    build_reader_profile,
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

desire = build_desire_hypothesis(
    research_document,
    reader_profile
)


print("DESIRE HYPOTHESIS\n")


print("PRODUCT CAPABILITY")
print(desire.product_capability)


print("\nFUNCTIONAL BENEFIT")
print(desire.functional_benefit)


print("\nDEEPER DESIRE")
print(desire.deeper_desire)


print("\nSUPPORTING EVIDENCE")

for evidence in desire.supporting_evidence:
    print(f"- {evidence}")


print("\nCONFIDENCE")
print(desire.confidence)
