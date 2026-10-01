from dotenv import load_dotenv

from research_agent import (
    build_research_document,
)

from strategy_agent import (
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


print("RESEARCH COMPLETE.")


print("\nBUILDING READER PROFILE...\n")


reader = build_reader_profile(
    research_document
)


print("READER PROFILE\n")


print("WHO THEY ARE")
print(reader.who_they_are)


print("\nCURRENT SITUATION")
print(reader.current_situation)


print("\nPRIMARY PROBLEM")
print(reader.primary_problem)


print("\nDESIRED OUTCOME")
print(reader.desired_outcome)
