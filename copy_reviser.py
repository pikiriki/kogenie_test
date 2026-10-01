from agents import Agent, Runner

from models import (
    CompleteSalesMessage,
    CopyCritique,
    CopyStrategyCard,
    RevisedSalesMessage,
)


ALLOWED_SECTIONS = [
    "headline",
    "opening",
    "mechanism_section",
    "proof_section",
    "objection_section",
    "offer_section",
]


copy_reviser_agent = Agent(
    name="Targeted Copy Reviser",

    instructions="""
You are the Targeted Copy Reviser
for KOgenie Copy Studio.

You receive:

- the original CompleteSalesMessage
- the CopyStrategyCard
- the CopyCritique

Your job is to improve ONLY the sections listed
in CopyCritique.sections_to_revise.

CRITICAL RULE:

Do not redesign the campaign.

Preserve:
- reader
- primary problem
- deeper desire
- awareness strategy
- Big Idea
- selected creative angle
- documented mechanism
- proof boundary
- offer boundary
- actual CTA

Use the CopyCritique.revision_instructions
as the repair instructions.

CLARITY

If a section is unclear:
- simplify it
- replace unnecessary abstraction with concrete language
- preserve its strategic meaning

SPECIFICITY

If a section is vague:
- use existing concrete situations
- use the documented mechanism
- do not invent statistics or numerical claims

CREDIBILITY

If a claim is too strong:
- weaken it to the strongest supported version
- preserve evidence limitations
- never manufacture proof

FLOW

If transitions are weak:
- make the revised section connect naturally to
  the surrounding message

REPETITION

If a section repeats previous information:
- remove redundant wording
- make the section advance the argument

NEVER INVENT:

- statistics
- testimonials
- case studies
- customer counts
- performance improvements
- awards
- rankings
- product capabilities
- proprietary mechanisms
- prices
- discounts
- trials
- guarantees
- bonuses
- urgency
- scarcity

IMPORTANT:

Sections that are NOT listed in sections_to_revise
must remain unchanged.

Return a CompleteSalesMessage.

The application will independently enforce preservation
of unapproved sections after your response.
""",

    model="gpt-6-luna",

    output_type=CompleteSalesMessage,
)


def revise_sales_message(
    complete_message: CompleteSalesMessage,
    strategy_card: CopyStrategyCard,
    critique: CopyCritique,
) -> RevisedSalesMessage:

    requested_sections = list(
        dict.fromkeys(
            critique.sections_to_revise
        )
    )

    invalid_sections = [
        section
        for section in requested_sections
        if section not in ALLOWED_SECTIONS
    ]


    if invalid_sections:
        raise ValueError(
            "Unknown sections requested for revision: "
            + ", ".join(invalid_sections)
        )

    if not requested_sections:

        return RevisedSalesMessage(
            headline=complete_message.headline,
            opening=complete_message.opening,
            mechanism_section=(
                complete_message.mechanism_section
            ),
            proof_section=(
                complete_message.proof_section
            ),
            objection_section=(
                complete_message.objection_section
            ),
            offer_section=(
                complete_message.offer_section
            ),
            full_copy=complete_message.full_copy,
            revised_sections=[],
            preserved_sections=ALLOWED_SECTIONS.copy(),
        )

    result = Runner.run_sync(
        copy_reviser_agent,
        f"""
Here is the original CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}

Here is the CopyCritique:

{critique.model_dump_json(indent=2)}

The ONLY sections you may revise are:

{requested_sections}

Make the minimum revisions needed to address
the critic's identified problems.

Preserve every other section.
"""
    )


    candidate = result.final_output

    final_sections = {}


    for section in ALLOWED_SECTIONS:

        if section in requested_sections:

            final_sections[section] = getattr(
                candidate,
                section,
            )

        else:

            final_sections[section] = getattr(
                complete_message,
                section,
            )

    full_copy = "\n\n".join([
        final_sections["headline"],
        final_sections["opening"],
        final_sections["mechanism_section"],
        final_sections["proof_section"],
        final_sections["objection_section"],
        final_sections["offer_section"],
    ])

    preserved_sections = [
        section
        for section in ALLOWED_SECTIONS
        if section not in requested_sections
    ]

    return RevisedSalesMessage(
        headline=final_sections["headline"],
        opening=final_sections["opening"],
        mechanism_section=(
            final_sections["mechanism_section"]
        ),
        proof_section=(
            final_sections["proof_section"]
        ),
        objection_section=(
            final_sections["objection_section"]
        ),
        offer_section=(
            final_sections["offer_section"]
        ),
        full_copy=full_copy,
        revised_sections=requested_sections,
        preserved_sections=preserved_sections,
    )
