from dotenv import load_dotenv

from research_agent import (
    research_competitor_messages,
)


load_dotenv()


competitors = [
    "Jasper",
    "Copy.ai",
    "AdCreative.ai",
]


message_map = research_competitor_messages(
    competitors
)


print("\nCOMPETITOR MESSAGE MAP\n")


for index, message in enumerate(
    message_map.messages,
    start=1
):
    print(f"Observation {index}")

    print("\nCompetitor:")
    print(message.competitor)

    print("\nObserved claim:")
    print(message.observed_claim)

    print("\nMechanism:")
    print(message.mechanism)

    print("\nAudience:")
    print(message.audience)

    print("\nOffer / CTA:")
    print(message.offer_or_cta)

    print("\nSource:")
    print(message.source)

    print("\n" + "-" * 50 + "\n")
