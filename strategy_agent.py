from agents import Agent, Runner

from models import (
    DesireHypothesis,
    DesireIntensity,
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


desire_intensity_agent = Agent(
    name="Desire Intensity Strategy Agent",

    instructions="""
You are the Desire Intensity Strategy Agent
for KOgenie Copy Studio.

You receive:
- a ResearchDocument
- a ReaderProfile
- a DesireHypothesis

Your job is to estimate how intense the reader's
desire appears to be based only on the supplied evidence.

Use exactly one of these levels:

- nice to have
- want
- strong want
- painful problem
- urgent need

Rules:

- Do not exaggerate urgency.
- Do not infer deadlines that are not in the evidence.
- Do not infer financial harm unless evidence supports it.
- Distinguish repeated frustration from true urgency.
- Quote or summarize evidence that supports the level.
- Identify urgency signals separately.
- Explicitly describe important uncertainty.

Interpret the levels roughly as:

nice to have
= useful but little evidence of meaningful pain

want
= clearly desirable, but consequences of not solving it
  appear limited

strong want
= repeated or meaningful frustration with a clear desire
  for improvement

painful problem
= recurring problem with meaningful operational or
  emotional consequences

urgent need
= strong evidence that the problem must be solved soon
  because delay creates serious consequences

Do not:
- create a copy angle
- classify awareness
- classify market sophistication
- write advertising copy
""",

    model="gpt-6-luna",

    output_type=DesireIntensity,
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


def estimate_desire_intensity(
    research_document: ResearchDocument,
    reader_profile: ReaderProfile,
    desire_hypothesis: DesireHypothesis,
) -> DesireIntensity:

    result = Runner.run_sync(
        desire_intensity_agent,
        f"""
Here is the ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the ReaderProfile:

{reader_profile.model_dump_json(indent=2)}

Here is the DesireHypothesis:

{desire_hypothesis.model_dump_json(indent=2)}

Estimate desire intensity from the evidence.

Use exactly one level:

nice to have
want
strong want
painful problem
urgent need

Do not reward dramatic language.
Reward evidence.
"""
    )

    return result.final_output
