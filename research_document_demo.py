from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)


load_dotenv()


brand_profile_id = 1

competitors = [
    "Jasper",
    "Copy.ai",
]


document = build_research_document(
    brand_profile_id,
    competitors
)


print("\nCOPYWRITING RESEARCH DOCUMENT\n")


print("PRODUCT FACTS\n")

for item in document.product_facts:
    print(f"- {item}")


print("\nAPPROVED CLAIMS\n")

for item in document.approved_claims:
    print(f"- {item}")


print("\nCUSTOMER EVIDENCE\n")

for evidence in document.customer_evidence:
    print(f'Quote: "{evidence.exact_quote}"')
    print(f"Source: {evidence.source}")
    print(f"Problem: {evidence.problem}")
    print(
        f"Desired outcome: "
        f"{evidence.desired_outcome}"
    )
    print(
        f"Interpretation: "
        f"{evidence.interpretation}"
    )
    print()


print("\nSYNTHESIZED PROBLEMS\n")

for item in document.problems:
    print(f"- {item}")


print("\nDESIRED OUTCOMES\n")

for item in document.desired_outcomes:
    print(f"- {item}")


print("\nCOMPETITOR MESSAGE MAP\n")

for message in document.competitor_messages:
    print(f"Competitor: {message.competitor}")
    print(
        f"Observed claim: "
        f"{message.observed_claim}"
    )
    print(f"Mechanism: {message.mechanism}")
    print(f"Audience: {message.audience}")
    print(
        f"Offer / CTA: "
        f"{message.offer_or_cta}"
    )
    print(f"Source: {message.source}")
    print()


print("\nEVIDENCE GAPS\n")

for item in document.evidence_gaps:
    print(f"- {item}")


print("\nUNANSWERED QUESTIONS\n")

for item in document.unanswered_questions:
    print(f"- {item}")
