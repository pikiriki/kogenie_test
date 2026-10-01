from agents import Agent, Runner

from models import (
    ReaderProfile,
    ResearchDocument,
)


reader_strategy_agent = Agent(
    name="Reader Strategy Agent",

    instructions="""
You are the Reader Strategy Agent for KOgenie Copy Studio.

Your job is to turn an existing ResearchDocument into
one focused ReaderProfile.

You are doing STRATEGY, not new research.

Create exactly one reader profile.

Rules:

- Base the profile only on evidence in the ResearchDocument.
- Do not invent demographics, job titles, company sizes,
  pains, behaviors, or desires that the research does not support.
- Prefer specificity when the evidence supports it.
- If evidence is broad, remain appropriately broad.
- Focus on one coherent reader rather than combining
  several incompatible customer types.
- Choose one primary problem.
- Choose one desired outcome most closely connected
  to that problem.
- Do not create a copy angle yet.
- Do not classify awareness yet.
- Do not classify market sophistication yet.
- Do not write advertising copy.
""",

    model="gpt-6-luna",

    output_type=ReaderProfile,
)


def build_reader_profile(
    research_document: ResearchDocument
) -> ReaderProfile:

    result = Runner.run_sync(
        reader_strategy_agent,
        f"""
Here is the completed copywriting research document:

{research_document.model_dump_json(indent=2)}

Create one ReaderProfile from this evidence.

Remember:

who_they_are
=
the single reader we are imagining

current_situation
=
what is happening for them now

primary_problem
=
the one central problem we will focus on

desired_outcome
=
the change they most want in relation to that problem
"""
    )

    return result.final_output
