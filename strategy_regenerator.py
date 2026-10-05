from agents import Agent, Runner

from models import (
    BrandProfile,
    CompleteSalesMessage,
    OfferStrategy,
    ResearchDocument,
    StrategyApplicationResult,
    StrategyRegenerationResult,
)


strategy_regeneration_writer = Agent(
    name="Strategy Locked Campaign Writer",

    instructions="""
You are the Strategy Locked Campaign Writer
for KOgenie Copy Studio.

You receive:

- an active CopyStrategyCard
- the current ResearchDocument
- verified brand claims and evidence metadata
- the current OfferStrategy
- the BrandProfile
- the campaign objective

The active CopyStrategyCard represents a strategy
that has already passed evaluation and human selection.

You are NOT allowed to choose another strategy.

PRESERVE THE ACTIVE STRATEGY

Preserve in meaning:

- reader
- core reader problem
- active reader tension
- deeper desire
- awareness
- sophistication
- message entry
- documented mechanism
- mechanism emphasis
- Big Idea
- selected angle
- major objections
- proof boundary
- offer boundary

Do not replace the selected Big Idea or angle merely
because another one sounds more persuasive.

HEADLINE

Express the active Big Idea and selected angle.

Do not introduce a stronger promise.

OPENING

Create recognition around the active_reader_tension.

Do not revert to an older reader tension.

MECHANISM SECTION

Use the documented mechanism as factual truth.

Use mechanism_emphasis to decide which part of the
real mechanism deserves emphasis.

Do not invent another mechanism.

PROOF SECTION

Use only supplied product facts, approved claims,
and real evidence.

Preserve proof boundaries.

Do not convert missing proof into a claim.

OBJECTION SECTION

Address the major objections only as far as
available evidence allows.

Do not pretend unresolved objections are resolved.

OFFER SECTION

Use only supplied OfferStrategy information.

Do not invent:
- price
- discount
- trial
- guarantee
- bonus
- urgency
- scarcity
- deadline

Use only the real campaign objective for the CTA.

BRAND VOICE

Follow the supplied BrandProfile without changing
factual or strategic meaning.

NEVER INVENT:

- product capabilities
- statistics
- customer quotations
- testimonials
- performance improvements
- ROAS improvement
- conversion improvement
- CAC improvement
- quantified time savings
- proprietary technology

Return one CompleteSalesMessage containing:

- headline
- opening
- mechanism_section
- proof_section
- objection_section
- offer_section
- full_copy
""",

    model="gpt-6-luna",

    output_type=CompleteSalesMessage,
)


def regenerate_core_message(
    application: StrategyApplicationResult,
    research_document: ResearchDocument,
    verified_claims_json: str,
    offer_strategy: OfferStrategy,
    brand_profile: BrandProfile,
    campaign_objective: str,
) -> StrategyRegenerationResult:

    strategy_card = (
        application.updated_strategy_card
    )

    if strategy_card.final_message.strip():

        raise ValueError(
            "Expected the newly applied strategy "
            "to have an invalidated final_message."
        )

    if not strategy_card.active_reader_tension.strip():

        raise ValueError(
            "Active reader tension is missing."
        )

    if not strategy_card.mechanism_emphasis.strip():

        raise ValueError(
            "Mechanism emphasis is missing."
        )

    if not strategy_card.big_idea.strip():

        raise ValueError(
            "Big Idea is missing."
        )

    if not strategy_card.selected_angle.strip():

        raise ValueError(
            "Selected angle is missing."
        )

    result = Runner.run_sync(
        strategy_regeneration_writer,
        f"""
Here is the ACTIVE CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the current ResearchDocument:

{research_document.model_dump_json(indent=2)}

Here are the verified brand claims
with evidence metadata:

{verified_claims_json}

Here is the current OfferStrategy:

{offer_strategy.model_dump_json(indent=2)}

Here is the BrandProfile:

{brand_profile.model_dump_json(indent=2)}

Campaign objective:

{campaign_objective}

Write a completely new core sales message
for the active strategy.

This is regeneration after an intentional
human-selected strategy change.

Do not reuse the old campaign argument merely
because historical copy exists.

Do not choose another strategy.
"""
    )

    candidate = result.final_output

    full_copy = "\n\n".join([
        candidate.headline,
        candidate.opening,
        candidate.mechanism_section,
        candidate.proof_section,
        candidate.objection_section,
        candidate.offer_section,
    ])

    complete_message = (
        candidate.model_copy(
            update={
                "full_copy": full_copy,
            }
        )
    )

    updated_strategy_card = (
        strategy_card.model_copy(
            update={
                "final_message": full_copy,
            }
        )
    )

    invalidated_artifacts = [
        "Previous complete sales message",
        "Previous Meta feed execution",
        "Previous Google Search execution",
        "Previous email execution",
        "Previous landing page execution",
        "Previous X execution",
        (
            "Previous human approval applies only "
            "to its historical snapshot, not to "
            "this regenerated message"
        ),
    ]

    return StrategyRegenerationResult(
        updated_strategy_card=(
            updated_strategy_card
        ),
        complete_message=(
            complete_message
        ),
        invalidated_artifacts=(
            invalidated_artifacts
        ),
        regeneration_reason=(
            "The human-selected active strategy "
            f"changed to candidate "
            f"{application.selected_strategy_index}, "
            "so copy derived from the previous "
            "strategy was invalidated and regenerated."
        ),
    )
