from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
    build_big_idea,
    build_desire_hypothesis,
    build_mechanism_hypothesis,
    build_objection_map,
    build_reader_profile,
    choose_message_entry_point,
    estimate_awareness,
    estimate_desire_intensity,
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


print("ESTIMATING MARKET SOPHISTICATION...\n")

sophistication = estimate_market_sophistication(
    research_document
)


print("BUILDING MECHANISM...\n")

mechanism = build_mechanism_hypothesis(
    research_document,
    reader_profile,
    desire_hypothesis
)


print("BUILDING OBJECTION MAP...\n")

objections = build_objection_map(
    research_document,
    reader_profile,
    desire_hypothesis,
    awareness,
    mechanism
)


print("BUILDING BIG IDEA...\n")

big_idea = build_big_idea(
    reader_profile,
    desire_hypothesis,
    mechanism,
    entry_point,
    sophistication,
    objections
)


print("BIG IDEA\n")


print("READER PROBLEM")
print(big_idea.reader_problem)


print("\nDEEPER DESIRE")
print(big_idea.deeper_desire)


print("\nMECHANISM")
print(big_idea.mechanism)


print("\nCENTRAL THOUGHT")
print(big_idea.central_thought)


print("\nPROMISE BOUNDARY")
print(big_idea.promise_boundary)


print("\nSUPPORTING EVIDENCE")

for item in big_idea.supporting_evidence:
    print(f"- {item}")


print("\nCONFIDENCE")
print(big_idea.confidence)
