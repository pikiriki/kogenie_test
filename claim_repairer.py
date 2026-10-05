from agents import Agent, Runner

from models import (
    ClaimRepairResult,
    ClaimReview,
    CopyStrategyCard,
    ResearchDocument,
)


from config import (
    get_config,
)


CONFIG = get_config()


ALLOWED_ACTIONS = {
    "keep",
    "qualify",
    "remove",
    "obtain evidence",
}


claim_qualification_agent = Agent(
    name="Claim Qualification Agent",

    instructions="""
You are the Claim Qualification Agent
for KOgenie Copy Studio.

You receive:

- one partially supported ClaimReview
- the ResearchDocument
- the CopyStrategyCard
- verified claim evidence

Your job is narrow:

Rewrite ONE partially supported claim into the
strongest version directly supported by the evidence.

You are NOT writing new marketing copy.

RULES:

- Preserve the supported factual core.
- Remove or weaken the unsupported part.
- Do not strengthen the claim.
- Do not add another benefit.
- Do not add a new product capability.
- Do not add statistics.
- Do not add a performance outcome.
- Do not invent evidence.
- Do not turn a hypothesis into a fact.
- Do not turn customer desire into product proof.
- Do not use competitor messaging as evidence for KOgenie.

If the evidence supports only:

"KOgenie generates multiple advertising concepts
from one campaign brief"

then do not add:

- winning
- higher-performing
- more effective
- meaningfully different
- faster
- better ROAS

unless supplied evidence separately supports them.

Return one ClaimRepairResult.

The repaired_claim should contain only
the evidence-supported version.
""",

    model=CONFIG.text_model,

    output_type=ClaimRepairResult,
)


def repair_claim(
    claim_review: ClaimReview,
    research_document: ResearchDocument,
    strategy_card: CopyStrategyCard,
    verified_claims_json: str,
) -> ClaimRepairResult:

    action = (
        claim_review
        .required_action
        .strip()
        .lower()
    )

    if action not in ALLOWED_ACTIONS:
        raise ValueError(
            f"Unsupported claim action: {action}"
        )

    if action == "keep":

        return ClaimRepairResult(
            section=claim_review.section,
            original_claim=claim_review.claim,
            repaired_claim=claim_review.claim,
            action_taken="keep",
            evidence_preserved=(
                claim_review.supporting_evidence
            ),
        )

    if action == "remove":

        return ClaimRepairResult(
            section=claim_review.section,
            original_claim=claim_review.claim,
            repaired_claim="",
            action_taken="remove",
            evidence_preserved=[],
        )

    if action == "obtain evidence":

        return ClaimRepairResult(
            section=claim_review.section,
            original_claim=claim_review.claim,
            repaired_claim="",
            action_taken="obtain evidence",
            evidence_preserved=(
                claim_review.supporting_evidence
            ),
        )

    result = Runner.run_sync(
        claim_qualification_agent,
        f"""
Here is the ClaimReview:

{claim_review.model_dump_json(indent=2)}

Here is the ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here are verified brand claims and evidence metadata:

{verified_claims_json}

Rewrite only the claim.

Preserve the strongest evidence-supported core.

Remove or qualify only the unsupported meaning.
"""
    )

    candidate = result.final_output

    return ClaimRepairResult(
        section=claim_review.section,
        original_claim=claim_review.claim,
        repaired_claim=candidate.repaired_claim,
        action_taken="qualify",
        evidence_preserved=(
            claim_review.supporting_evidence
        ),
    )
