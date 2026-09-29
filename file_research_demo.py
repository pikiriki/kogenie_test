from dotenv import load_dotenv

from research_agent import (
    research_uploaded_documents,
)


load_dotenv()


result = research_uploaded_documents(
    "What documented capabilities and limitations "
    "does KOgenie currently have?"
)


print("DOCUMENT RESEARCH\n")
print(result.final_output)
