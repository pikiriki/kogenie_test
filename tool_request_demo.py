import json

from dotenv import load_dotenv
from openai import OpenAI

from agent_tools import (
    APPROVED_CLAIMS_TOOL,
    get_approved_brand_claims,
)


load_dotenv()

client = OpenAI()

brand_profile_id = 1

instructions = """
You are a research assistant for KOgenie Copy Studio.

Your job is to retrieve verified brand information using
the tools provided to you.

Do not invent brand claims.

After receiving tool results:
- Report only information supported by the tool result.
- Clearly say when no verified claims are available.
- Mention the evidence and source when they are provided.
"""


response = client.responses.create(
    model="gpt-6-luna",
    instructions=instructions,
    input=(
        "What verified factual claims are available for "
        f"brand profile ID {brand_profile_id}?"
    ),
    tools=[
        APPROVED_CLAIMS_TOOL
    ],
    tool_choice={
        "type": "function",
        "name": "get_approved_brand_claims"
    }
)


function_call = None

for item in response.output:
    if item.type == "function_call":
        function_call = item
        break


if function_call is None:
    raise RuntimeError(
        "The model did not request the expected tool."
    )


print("1. Model requested tool:")
print(function_call.name)

print("\n2. Model supplied arguments:")
print(function_call.arguments)


if function_call.name != "get_approved_brand_claims":
    raise ValueError(
        f"Unexpected tool requested: {function_call.name}"
    )


arguments = json.loads(
    function_call.arguments
)

brand_id = arguments[
    "brand_profile_id"
]


print("\n3. Python is executing the real tool...")

tool_result = get_approved_brand_claims(
    brand_id
)

print("\n4. Tool returned:")
print(tool_result)


final_response = client.responses.create(
    model="gpt-6-luna",
    instructions=instructions,
    previous_response_id=response.id,
    tools=[
        APPROVED_CLAIMS_TOOL
    ],
    tool_choice="none",
    input=[
        {
            "type": "function_call_output",
            "call_id": function_call.call_id,
            "output": tool_result,
        }
    ],
)


print("\n5. Agent final answer:")
print(final_response.output_text)
