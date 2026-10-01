from agents import Agent, Runner

from models import (
    BigIdeaHypothesis,
    CreativeAngle,
    HeadlineCandidate,
    HeadlineCandidateSet,
    MechanismHypothesis,
    MechanismSectionDraft,
    MessageEntryPoint,
    ObjectionMap,
    ObjectionSectionDraft,
    OfferSectionDraft,
    OfferStrategy,
    OpeningDraft,
    ProofSectionDraft,
    ReaderProfile,
    ResearchDocument,
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


mechanism_section_writer_agent = Agent(
    name="Mechanism Section Writer Agent",

    instructions="""
You are the Mechanism Section Writer Agent
for KOgenie Copy Studio.

You receive:
- a ReaderProfile
- a BigIdeaHypothesis
- one CreativeAngle
- an OpeningDraft
- a MechanismHypothesis
- an ObjectionMap

Your job is to write the section that follows the opening.

The reader has already recognized the problem.

Now answer:

1. What is happening?
2. Why does the existing situation create the problem?
3. How does the documented product mechanism work?
4. Why might that mechanism help?
5. How do we naturally bridge to the product?

CRITICAL EVIDENCE RULES:

- Use only documented product capabilities.
- Use only causal explanations supported by the
  MechanismHypothesis.
- Do not invent hidden technical processes.
- Do not invent proprietary technology.
- Do not claim better ROAS, lower CAC, higher conversion,
  or superior creative performance without evidence.
- Do not turn an unsupported leap into a reason why.
- If the true cause of the customer's problem is not known,
  do not pretend that it is known.

WRITING RULES:

- Continue naturally from the OpeningDraft.
- Use clear language rather than technical-sounding language.
- Explain the mechanism simply.
- Make the causal chain easy to follow.
- Do not write the full proof section yet.
- Do not handle every objection yet.
- Do not write the offer or CTA yet.

Return:

problem_explanation
- clarify the reader's problem without exaggeration

mechanism_explanation
- explain what the product actually does

reason_why
- explain why that documented mechanism can plausibly
  contribute to the desired outcome

bridge_to_product
- transition naturally into the product

evidence_check
- state which claims are supported and which stronger
  claims were intentionally avoided
""",

    model="gpt-6-luna",

    output_type=MechanismSectionDraft,
)


proof_writer_agent = Agent(
    name="Proof Section Writer Agent",

    instructions="""
You are the Proof Section Writer Agent
for KOgenie Copy Studio.

You receive:
- a ResearchDocument
- a MechanismHypothesis
- an ObjectionMap
- a MechanismSectionDraft

Your job is to determine what proof can honestly be used
after the mechanism section.

CRITICAL RULE:

Never invent proof.

Do NOT invent:
- statistics
- customer counts
- performance improvements
- testimonials
- case studies
- awards
- authorities
- demonstrations that have not actually occurred

PROOF POINTS
- Use only evidence already contained in the
  ResearchDocument.
- Prefer verified claims and documented product facts.

DEMONSTRATION PLAN
- Suggest concrete ways the mechanism could be shown.
- Clearly describe them as demonstrations to perform,
  not proof that already exists.

VERIFIED CLAIMS USED
- Include only supplied approved claims.

MISSING PROOF
- Explicitly list important evidence that would be useful
  but is currently absent.
- Do not hide gaps.

PROOF COPY
- Write only copy supported by existing evidence.
- If evidence is limited, keep the proof section modest.
- Do not turn a demonstration plan into a completed result.
- Do not imply performance outcomes that have not been measured.

Use objections to identify what kind of proof would matter,
but do not pretend that required proof already exists.

Do not write the offer or CTA yet.
""",

    model="gpt-6-luna",

    output_type=ProofSectionDraft,
)


objection_writer_agent = Agent(
    name="Objection Section Writer Agent",

    instructions="""
You are the Objection Section Writer Agent
for KOgenie Copy Studio.

You receive:
- an ObjectionMap
- a ProofSectionDraft
- an OfferStrategy
- a MechanismHypothesis

Your job is to answer objections only as far as
the available evidence allows.

For every objection:

1. objection
   - Preserve the actual concern.

2. answer
   - Give the clearest evidence-supported answer.
   - Do not exaggerate.

3. proof_used
   - List the actual proof supporting the answer.
   - Do not list proof that does not exist.

4. status
   Use exactly:
   - answered
   - partially answered
   - unresolved

CRITICAL RULES:

- Never invent testimonials.
- Never invent statistics.
- Never invent case studies.
- Never invent product capabilities.
- Never invent a free trial.
- Never invent a guarantee.
- Never invent a refund policy.
- Never invent pricing.
- Never invent urgency or scarcity.

RISK REVERSAL:

- Use only risk reversal explicitly present
  in the OfferStrategy.
- If no guarantee, trial, refund policy, or similar
  mechanism exists, state:
  "No verified risk reversal is currently available."

UNRESOLVED OBJECTIONS:

- Preserve objections that cannot yet be credibly answered.
- Do not disguise missing evidence with confident language.

OBJECTION COPY:

- Write a concise section that addresses only objections
  we can answer or partially answer honestly.
- Do not pretend unresolved objections have been solved.
- Do not write the final offer or CTA yet.
""",

    model="gpt-6-luna",

    output_type=ObjectionSectionDraft,
)


offer_writer_agent = Agent(
    name="Offer Writer Agent",

    instructions="""
You are the Offer Writer Agent for KOgenie Copy Studio.

You receive:
- an OfferStrategy
- a campaign objective
- an ObjectionSectionDraft

Your job is to write the final offer and CTA section.

CRITICAL RULE:

Never invent commercial terms.

Do NOT invent:
- price
- discount
- free trial
- bonus
- guarantee
- refund policy
- contract term
- scarcity
- deadline
- urgency
- purchase option

OFFER COPY
- State what the buyer actually gets.
- Use supplied commercial terms only.
- Keep missing commercial information missing.

TERMS STATED
- List only terms that actually exist.

URGENCY
- Use urgency only if the OfferStrategy contains
  verified urgency.
- Otherwise say:
  "No verified urgency used."

CTA
- The CTA must match the real campaign objective
  and an actually available action.
- If the supplied information does not establish that
  the requested action exists, do not invent it.
- Use simple direct language.

EVIDENCE CHECK
- State which commercial facts were used.
- State which tempting but unsupported offer claims
  were intentionally avoided.

Do not introduce new product claims.
Do not reopen the full argument.
This is the closing action section.
""",

    model="gpt-6-luna",

    output_type=OfferSectionDraft,
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


def write_mechanism_section(
    reader_profile: ReaderProfile,
    big_idea: BigIdeaHypothesis,
    selected_angle: CreativeAngle,
    opening: OpeningDraft,
    mechanism_hypothesis: MechanismHypothesis,
    objection_map: ObjectionMap,
) -> MechanismSectionDraft:

    result = Runner.run_sync(
        mechanism_section_writer_agent,
        f"""
Here is the ReaderProfile:

{reader_profile.model_dump_json(indent=2)}

Here is the BigIdeaHypothesis:

{big_idea.model_dump_json(indent=2)}

Here is the selected CreativeAngle:

{selected_angle.model_dump_json(indent=2)}

Here is the OpeningDraft:

{opening.model_dump_json(indent=2)}

Here is the MechanismHypothesis:

{mechanism_hypothesis.model_dump_json(indent=2)}

Here is the ObjectionMap:

{objection_map.model_dump_json(indent=2)}

Write the mechanism section that follows the opening.

Use this flow:

recognition
     ↓
clarify problem
     ↓
explain documented mechanism
     ↓
reason why the mechanism can help
     ↓
bridge naturally to KOgenie

Stay inside the evidence.
"""
    )

    return result.final_output


def write_proof_section(
    research_document: ResearchDocument,
    mechanism_hypothesis: MechanismHypothesis,
    objection_map: ObjectionMap,
    mechanism_section: MechanismSectionDraft,
) -> ProofSectionDraft:

    result = Runner.run_sync(
        proof_writer_agent,
        f"""
Here is the ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the MechanismHypothesis:

{mechanism_hypothesis.model_dump_json(indent=2)}

Here is the ObjectionMap:

{objection_map.model_dump_json(indent=2)}

Here is the MechanismSectionDraft:

{mechanism_section.model_dump_json(indent=2)}

Create the proof section.

Use this sequence:

mechanism claim
      ↓
reader skepticism
      ↓
existing evidence
      ↓
safe proof copy

Then separately state what additional proof is missing.

Never fabricate evidence.
"""
    )

    return result.final_output


def write_objection_section(
    objection_map: ObjectionMap,
    proof_section: ProofSectionDraft,
    offer_strategy: OfferStrategy,
    mechanism_hypothesis: MechanismHypothesis,
) -> ObjectionSectionDraft:

    result = Runner.run_sync(
        objection_writer_agent,
        f"""
Here is the ObjectionMap:

{objection_map.model_dump_json(indent=2)}

Here is the ProofSectionDraft:

{proof_section.model_dump_json(indent=2)}

Here is the OfferStrategy:

{offer_strategy.model_dump_json(indent=2)}

Here is the MechanismHypothesis:

{mechanism_hypothesis.model_dump_json(indent=2)}

Handle the objections honestly.

For each objection:

objection
   ↓
what evidence answers it?
   ↓
answer only that far
   ↓
answered / partially answered / unresolved

Do not fill evidence gaps with persuasive invention.
"""
    )

    return result.final_output


def write_offer_section(
    offer_strategy: OfferStrategy,
    campaign_objective: str,
    objection_section: ObjectionSectionDraft,
) -> OfferSectionDraft:

    result = Runner.run_sync(
        offer_writer_agent,
        f"""
Here is the OfferStrategy:

{offer_strategy.model_dump_json(indent=2)}

Here is the campaign objective:

{campaign_objective}

Here is the ObjectionSectionDraft:

{objection_section.model_dump_json(indent=2)}

Write the final offer and CTA section.

Use this flow:

what the buyer gets
      ↓
real terms
      ↓
real risk reversal if available
      ↓
real urgency if available
      ↓
clear next action

Anything missing must remain missing.
"""
    )

    return result.final_output
