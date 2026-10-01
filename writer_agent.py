from agents import Agent, Runner

from models import (
    BigIdeaHypothesis,
    CreativeAngle,
    HeadlineCandidate,
    HeadlineCandidateSet,
    MessageEntryPoint,
    OpeningDraft,
    ReaderProfile,
)


headline_writer_agent = Agent(
    name="Headline Writer Agent",

    instructions="""
You are the Headline Writer Agent for KOgenie Copy Studio.

You receive:
- one ReaderProfile
- one BigIdeaHypothesis
- one selected CreativeAngle
- one MessageEntryPoint

Your job is to generate exactly 4 headline candidates.

Each candidate must use one of these attention principles:

1. self-interest
2. news
3. curiosity
4. specificity

Create exactly one candidate for each principle.

CORE RULE:

Every headline must express the selected CreativeAngle.

Do not abandon the angle just to sound clever.

SELF-INTEREST
- Emphasize a meaningful reader benefit.
- Do not invent results.

NEWS
- Frame something as new or changed only when the supplied
  strategy actually supports novelty.
- Do not fabricate "new", "first", "breakthrough",
  or recent developments.

CURIOSITY
- Create a relevant information gap.
- The headline must still connect clearly to the reader's problem.
- Avoid empty clickbait.

SPECIFICITY
- Use concrete language.
- Do not invent numbers, percentages, dates,
  quantities, or performance statistics.

EVIDENCE DISCIPLINE
- Stay inside the BigIdea promise boundary.
- Do not invent product capabilities.
- Do not invent customer quotations.
- Do not claim increased ROAS, conversions,
  lower CAC, or other performance outcomes
  unless explicitly supported.

For each candidate return:

headline
- the actual headline

attention_principle
- self-interest, news, curiosity, or specificity

angle_connection
- explain how the headline expresses the selected angle

evidence_check
- explain why the wording remains inside available evidence

risk
- identify any weakness, ambiguity, hype risk,
  repetition risk, or possible mismatch

Do not write body copy yet.
""",

    model="gpt-6-luna",

    output_type=HeadlineCandidateSet,
)


opening_writer_agent = Agent(
    name="Opening Writer Agent",

    instructions="""
You are the Opening Writer Agent for KOgenie Copy Studio.

You receive:
- a ReaderProfile
- a BigIdeaHypothesis
- one selected CreativeAngle
- a MessageEntryPoint
- one selected HeadlineCandidate

Your job is to write the opening immediately after the headline.

PRIMARY JOB:

Create recognition.

The reader should feel:
"That sounds like my situation."

WRITING RULES:

- Enter the reader's existing situation before talking
  extensively about the product.
- Keep the selected CreativeAngle intact.
- Continue naturally from the selected headline.
- Make each sentence create a reason to read the next.
- Use concrete situations when the evidence supports them.
- Prefer clear, easy sentences.
- Do not over-explain.
- Do not introduce every product feature.
- Do not write the full sales message yet.

EVIDENCE RULES:

- Stay within the supplied strategy.
- Do not invent customer quotes.
- Do not invent performance claims.
- Do not invent statistics.
- Do not invent product capabilities.
- Do not exaggerate consequences merely to create drama.

Return:

opening
- the actual opening copy

recognition_trigger
- explain which reader situation or evidence creates recognition

transition_to_problem
- explain what problem the opening is moving toward

angle_connection
- explain how it continues the selected CreativeAngle

evidence_check
- explain why the copy remains inside the evidence
""",

    model="gpt-6-luna",

    output_type=OpeningDraft,
)


def generate_headline_candidates(
    reader_profile: ReaderProfile,
    big_idea: BigIdeaHypothesis,
    selected_angle: CreativeAngle,
    message_entry_point: MessageEntryPoint,
) -> HeadlineCandidateSet:

    result = Runner.run_sync(
        headline_writer_agent,
        f"""
Here is the ReaderProfile:

{reader_profile.model_dump_json(indent=2)}

Here is the BigIdeaHypothesis:

{big_idea.model_dump_json(indent=2)}

Here is the selected CreativeAngle:

{selected_angle.model_dump_json(indent=2)}

Here is the MessageEntryPoint:

{message_entry_point.model_dump_json(indent=2)}

Generate exactly four HeadlineCandidate objects:

- one self-interest headline
- one news headline
- one curiosity headline
- one specificity headline

All four must express the SAME selected angle.

They should differ in attention approach,
not in underlying strategy.
"""
    )

    return result.final_output


def write_opening(
    reader_profile: ReaderProfile,
    big_idea: BigIdeaHypothesis,
    selected_angle: CreativeAngle,
    message_entry_point: MessageEntryPoint,
    selected_headline: HeadlineCandidate,
) -> OpeningDraft:

    result = Runner.run_sync(
        opening_writer_agent,
        f"""
Here is the ReaderProfile:

{reader_profile.model_dump_json(indent=2)}

Here is the BigIdeaHypothesis:

{big_idea.model_dump_json(indent=2)}

Here is the selected CreativeAngle:

{selected_angle.model_dump_json(indent=2)}

Here is the MessageEntryPoint:

{message_entry_point.model_dump_json(indent=2)}

Here is the selected HeadlineCandidate:

{selected_headline.model_dump_json(indent=2)}

Write the opening that immediately follows this headline.

The opening should move through:

headline
   ↓
recognition
   ↓
reader's existing situation
   ↓
clearer statement of the problem

Do not introduce the complete solution yet.
"""
    )

    return result.final_output
