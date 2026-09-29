from dotenv import load_dotenv

from research_agent import (
    extract_customer_evidence,
)


load_dotenv()


report = extract_customer_evidence(
    "What problems do customers experience when "
    "trying to produce fresh advertising ideas?"
)

print("\nRAW STRUCTURED REPORT\n")

print(
    report.model_dump_json(
        indent=2
    )
)

print("\nVOICE OF CUSTOMER EVIDENCE\n")


for index, item in enumerate(
    report.evidence,
    start=1
):
    print(f"Evidence {index}")

    print("Exact quote:")
    print(item.exact_quote)

    print("\nSource:")
    print(item.source)

    print("\nProblem:")
    print(item.problem)

    print("\nDesired outcome:")
    print(item.desired_outcome)

    print("\nInterpretation:")
    print(item.interpretation)

    print("\n" + "-" * 50 + "\n")
