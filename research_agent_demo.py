from dotenv import load_dotenv

from agents import Agent, ModelSettings, Runner
from agents.decorators import tool

from agent_tools import (
    get_approved_brand_claims as get_claims_from_database,
)


load_dotenv()


@tool
def get_approved_brand_claims(
    brand_profile_id: int
) -> str:
    """
    Retrieve verified factual claims, evidence notes,
    and source references for a saved brand profile.
    """
    return get_claims_from_database(
        brand_profile_id
    )


research_agent = Agent(
    name="Brand Research Agent",
    instructions="""
You are a research assistant for KOgenie Copy Studio.

Retrieve verified brand information using your tools.

Rules:
- Do not invent brand claims.
- Report only claims supported by tool results.
- Include evidence and source references when available.
- If no verified claims exist, say so clearly.
""",
    tools=[
        get_approved_brand_claims
    ],
    model="gpt-6-luna",
    model_settings=ModelSettings(
        tool_choice="get_approved_brand_claims"
    ),
)


brand_profile_id = 1

result = Runner.run_sync(
    research_agent,
    (
        "What verified factual claims are available "
        f"for brand profile ID {brand_profile_id}?"
    ),
)


print(result.final_output)
