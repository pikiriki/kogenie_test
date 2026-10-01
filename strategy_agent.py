from agents import Agent, Runner

from models import (
    DesireHypothesis,
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


desire_strategy_agent = Agent(
    name="Desire Strategy Agent",

    instructions="""
You are the Desire Strategy Agent for KOgenie Copy Studio.

Your job is to connect a documented product capability
to a reader benefit and then to a plausible deeper desire.

You are doing strategy, not new research.

You will receive:
- a ResearchDocument
- a ReaderProfile

Produce one DesireHypothesis.

Rules:

PRODUCT CAPABILITY
- Use only a capability supported by product facts
  or approved claims.
- Do not invent capabilities.

FUNCTIONAL BENEFIT
- Explain what practical change that capability creates
  for this specific reader.
- The benefit must causally follow from the capability.

DEEPER DESIRE
- Infer why that functional benefit may matter to the reader.
- Ground the inference in customer evidence and the ReaderProfile.
- Do not invent dramatic psychological motives.
- Do not claim a desire was directly stated unless the
  customer evidence actually states it.

SUPPORTING EVIDENCE
- Include short evidence statements or customer quotations
  from the supplied ResearchDocument.
- Do not fabricate quotations.

CONFIDENCE
Use exactly one of:
- high
- medium
- low

Use high only when several strong pieces of evidence
directly support the interpretation.

Do not:
- classify awareness
- classify sophistication
- choose the final copy angle
- write advertising copy
""",

    model="gpt-6-luna",

    output_type=DesireHypothesis,
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


def build_desire_hypothesis(
    research_document: ResearchDocument,
    reader_profile: ReaderProfile,
) -> DesireHypothesis:

    result = Runner.run_sync(
        desire_strategy_agent,
        f"""
Here is the ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the chosen ReaderProfile:

{reader_profile.model_dump_json(indent=2)}

Build one DesireHypothesis.

Use this causal chain:

documented product capability
        ↓
functional consequence for this reader
        ↓
why that consequence matters
        ↓
deeper desire hypothesis

Show supporting evidence and give an appropriate
confidence level.
"""
    )

    return result.final_output
