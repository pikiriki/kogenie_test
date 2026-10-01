from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_desire_hypothesis,
    build_reader_profile,
    choose_message_entry_point,
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


print("CHOOSING MESSAGE ENTRY POINT...\n")

entry_point = choose_message_entry_point(
    reader_profile,
    desire_hypothesis,
    desire_intensity,
    awareness
)


print("MESSAGE ENTRY POINT\n")


print("STARTING POINT")
print(entry_point.starting_point)


print("\nWHY THIS START")
print(entry_point.why_this_start)


print("\nINTRODUCE NEXT")

for item in entry_point.information_to_introduce_next:
    print(f"- {item}")


print("\nDO NOT LEAD WITH")

for item in entry_point.information_to_avoid_leading_with:
    print(f"- {item}")
