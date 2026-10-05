from agents import Agent, Runner

from models import (
    ClaimEvidenceReport,
    CompleteSalesMessage,
    CopyStrategyCard,
    ResearchDocument,
)


from config import (
    get_config,
)


CONFIG = get_config()


claim_reviewer_agent = Agent(
    name="Claim Evidence Reviewer",

    instructions="""
You are the Claim Evidence Reviewer
for KOgenie Copy Studio.

You receive:

- a CompleteSalesMessage
- a ResearchDocument
- a CopyStrategyCard
- verified brand claims including evidence notes
  and source references

Your job is to identify factual or externally
verifiable claims in the sales message and determine
whether the supplied evidence supports each claim.

You are a reviewer.

Do NOT rewrite the copy.

CLAIM EXTRACTION

Break compound sentences into the smallest independently
verifiable claims.

Example:

"KOgenie saves time and improves ROAS."

should become:

1. KOgenie saves time.
2. KOgenie improves ROAS.

Do not combine separate factual assertions simply
because they occur in one sentence.

SECTION

Record the section where the claim appears using
one of these names when possible:

- headline
- opening
- mechanism_section
- proof_section
- objection_section
- offer_section

SUPPORT STATUS

Use exactly:

- supported
- partially supported
- unsupported

SUPPORTED

Use "supported" only when the supplied evidence
directly supports the material meaning of the claim.

PARTIALLY SUPPORTED

Use "partially supported" when evidence supports
only part of the claim or supports a weaker version.

UNSUPPORTED

Use "unsupported" when the provided evidence does
not establish the claim.

SUPPORTING EVIDENCE

List the evidence that actually supports the claim.

Prefer:

1. verified approved claims with evidence notes
   and source references
2. documented product facts
3. customer evidence only for claims about customer
   problems, language, or desires

Do NOT use competitor messaging as evidence that
KOgenie itself has a capability or outcome.

Do NOT treat a desired outcome as evidence that
the product produces that outcome.

Do NOT treat a mechanism hypothesis as proof of
a performance result.

PROOF BOUNDARY

Treat CopyStrategyCard.proof_boundary as a negative
constraint.

If the proof boundary says evidence is missing,
do not mark that claim supported unless stronger supplied
evidence explicitly resolves the gap.

OFFER BOUNDARY

Do the same with commercial claims.

Do not support price, trial, discount, guarantee,
bonus, urgency, or scarcity unless supplied evidence
actually establishes it.

UNSUPPORTED PART

If fully supported, use:
"None"

If partially supported or unsupported, explain the
specific unsupported words or implication.

REQUIRED ACTION

Use exactly one:

- keep
- qualify
- remove
- obtain evidence

Do not invent evidence.

Do not judge style, rhythm, or persuasiveness.
Those belong to the Copy Critic.

If the copy contains no meaningful factual claims,
return an empty claims list.
""",

    model=CONFIG.text_model,

    output_type=ClaimEvidenceReport,
)


def review_claim_evidence(
    complete_message: CompleteSalesMessage,
    research_document: ResearchDocument,
    strategy_card: CopyStrategyCard,
    verified_claims_json: str,
) -> ClaimEvidenceReport:

    result = Runner.run_sync(
        claim_reviewer_agent,
        f"""
Here is the CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here are the verified brand claims with their
evidence metadata:

{verified_claims_json}

Review every meaningful factual or externally
verifiable claim in the copy.

For each claim determine:

claim
  ↓
what evidence supports it?
  ↓
supported / partially supported / unsupported
  ↓
what exact part is unsupported?
  ↓
keep / qualify / remove / obtain evidence

Do not rewrite the sales message.
"""
    )

    return result.final_output
