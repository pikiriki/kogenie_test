from agents import Agent, Runner

from models import (
    BrandProfile,
    BrandVoiceReview,
    CompleteSalesMessage,
    RevisedSalesMessage,
)


from config import (
    get_config,
)


CONFIG = get_config()


ALLOWED_SECTIONS = [
    "headline",
    "opening",
    "mechanism_section",
    "proof_section",
    "objection_section",
    "offer_section",
]


brand_voice_reviser_agent = Agent(
    name="Brand Voice Reviser",

    instructions="""
You are the Brand Voice Reviser
for KOgenie Copy Studio.

You receive:

- an original CompleteSalesMessage
- a BrandProfile
- a BrandVoiceReview

Your task is narrow:

Revise ONLY the sections listed in
BrandVoiceReview.sections_to_revise.

Your job is to change EXPRESSION,
not strategic or factual meaning.

PRESERVE EXACTLY IN MEANING:

- reader
- reader problem
- Big Idea
- selected campaign argument
- product mechanism
- factual claims
- claim strength
- proof limitations
- objections
- offer terms
- CTA
- commercial conditions

BRAND TONE

Move the flagged sections toward the tone
specified in BrandProfile.

Do not invent brand traits that are not supplied.

PREFERRED WORDS

Use preferred terminology naturally when relevant.

Do not force every preferred word into the copy.
Do not keyword-stuff.

AVOIDED WORDS

Remove or replace avoided language when possible
without changing factual meaning.

VOICE DRIFT

Correct stylistic drift such as excessive hype,
formality, casualness, jargon, or emotional exaggeration
only when the BrandProfile establishes that it is off-brand.

CRITICAL CLAIM RULE:

Never make a claim stronger while changing tone.

For example:

"generates multiple concepts"

must NOT become:

"generates winning concepts"

unless "winning" was already supported and present.

Do not invent:

- statistics
- testimonials
- performance improvements
- product capabilities
- proprietary technology
- prices
- discounts
- trials
- guarantees
- bonuses
- deadlines
- urgency
- scarcity

Do not change sections that were not approved for revision.

Return a CompleteSalesMessage.

The application will independently restore
all locked sections after your response.
""",

    model=CONFIG.text_model,

    output_type=CompleteSalesMessage,
)


def revise_brand_voice(
    complete_message: CompleteSalesMessage,
    brand_profile: BrandProfile,
    brand_review: BrandVoiceReview,
) -> RevisedSalesMessage:

    requested_sections = list(
        dict.fromkeys(
            brand_review.sections_to_revise
        )
    )

    invalid_sections = [
        section
        for section in requested_sections
        if section not in ALLOWED_SECTIONS
    ]


    if invalid_sections:
        raise ValueError(
            "Unknown sections requested for brand revision: "
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
        brand_voice_reviser_agent,
        f"""
Here is the original CompleteSalesMessage:

{complete_message.model_dump_json(indent=2)}

Here is the BrandProfile:

{brand_profile.model_dump_json(indent=2)}

Here is the BrandVoiceReview:

{brand_review.model_dump_json(indent=2)}

The ONLY sections permitted to change are:

{requested_sections}

Revise those sections only for brand-voice alignment.

Preserve their factual and strategic meaning.

Do not strengthen claims.
Do not change proof boundaries.
Do not change offer terms.
Do not change the campaign CTA.
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
