from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    estimate_market_sophistication,
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


print("ESTIMATING MARKET SOPHISTICATION...\n")

sophistication = estimate_market_sophistication(
    research_document
)


print("MARKET SOPHISTICATION\n")


print("STAGE")
print(sophistication.stage)


print("\nCOMMON MARKET CLAIMS")

for item in sophistication.common_market_claims:
    print(f"- {item}")


print("\nSIGNS OF SATURATION")

for item in sophistication.signs_of_saturation:
    print(f"- {item}")


print("\nMECHANISM PRESENCE")

for item in sophistication.mechanism_presence:
    print(f"- {item}")


print("\nSUPPORTING EVIDENCE")

for item in sophistication.supporting_evidence:
    print(f"- {item}")


print("\nCONFIDENCE")
print(sophistication.confidence)
