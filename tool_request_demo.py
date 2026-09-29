import json

from dotenv import load_dotenv
from openai import OpenAI

from agent_tools import APPROVED_CLAIMS_TOOL


load_dotenv()

client = OpenAI()

brand_profile_id = 1

response = client.responses.create(
    model="gpt-6-luna",
    instructions="""
You are a research assistant for KOgenie Copy Studio.

Your job is to retrieve verified brand information using
the tools provided to you.

Do not invent brand claims.
""",
    input=(
        "Retrieve the verified factual claims for "
        f"brand profile ID {brand_profile_id}."
    ),
    tools=[
        APPROVED_CLAIMS_TOOL
    ],
    tool_choice={
        "type": "function",
        "name": "get_approved_brand_claims"
    }
)

for item in response.output:
    if item.type == "function_call":
        print("Tool requested:")
        print(item.name)

        print("\nRaw arguments:")
        print(item.arguments)

        arguments = json.loads(item.arguments)

        print("\nParsed brand profile ID:")
        print(arguments["brand_profile_id"])

        print("\nCall ID:")
        print(item.call_id)
