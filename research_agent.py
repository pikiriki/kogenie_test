from agents import Agent, ModelSettings, Runner

from agent_tools import approved_claims_agent_tool


research_agent = Agent(
    name="Brand Research Agent",

    instructions="""
You are the Brand Research Agent for KOgenie Copy Studio.

Your job is to retrieve factual information before copy is written.

Rules:
- Use available tools to retrieve authoritative brand information.
- Do not invent brand claims.
- Distinguish claims from their supporting evidence.
- Include source references when they are available.
- If no verified information is available, say so clearly.
""",

    tools=[
        approved_claims_agent_tool
    ],

    model="gpt-6-luna",

    model_settings=ModelSettings(
        tool_choice="required"
    ),
)


def research_verified_brand_claims(
    brand_profile_id: int
) -> str:
    result = Runner.run_sync(
        research_agent,
        (
            "Retrieve and summarize the verified factual "
            "claims for brand profile ID "
            f"{brand_profile_id}."
        )
    )

    return result.final_output
