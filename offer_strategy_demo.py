from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_offer_strategy,
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


supplied_offer_terms = """
The business has supplied no pricing information yet.

No bonus has been defined.

No guarantee or refund policy has been supplied.

No deadline, limited availability, or other urgency
has been supplied.

The only confirmed commercial element for this test
is access to the documented KOgenie product capability.
"""


print("BUILDING OFFER STRATEGY...\n")

offer = build_offer_strategy(
    research_document,
    supplied_offer_terms
)


print("OFFER STRATEGY\n")


print("CORE PRODUCT")
print(offer.core_product)


print("\nPRICE")
print(offer.price)


print("\nBONUSES")

if offer.bonuses:
    for item in offer.bonuses:
        print(f"- {item}")
else:
    print("- None supplied")


print("\nGUARANTEE")
print(offer.guarantee)


print("\nTERMS")

if offer.terms:
    for item in offer.terms:
        print(f"- {item}")
else:
    print("- None supplied")


print("\nURGENCY")
print(offer.urgency)


print("\nVERIFIED ELEMENTS")

for item in offer.verified_elements:
    print(f"- {item}")


print("\nMISSING ELEMENTS")

for item in offer.missing_elements:
    print(f"- {item}")
