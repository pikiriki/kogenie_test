from openai import OpenAI

from models import CampaignBrief, CopyDraft


from config import (
    get_config,
)


CONFIG = get_config()


def generate_copy(brief: CampaignBrief):
    client = OpenAI()

    instructions = """
You are a direct-response advertising copywriter.

Your job is to communicate the product clearly and persuasively to the specified audience.

Follow these rules:
- Use only facts supplied in the product information and approved claims.
- Treat approved claims as the factual claims you are explicitly permitted to state.
- Do not create additional factual performance claims that are not supported by the supplied information.
- Do not invent statistics.
- Do not invent testimonials.
- Do not invent prices.
- Do not invent guarantees.
- Do not invent product capabilities.
- Prefer clear language over clever language.
- Keep the draft concise.
"""

    approved_claims_text = "\n".join(
        f"- {claim}"
        for claim in brief.approved_claims
    )

    input_text = f"""
Product information:

{brief.product_description}

Audience:

{brief.audience}

Campaign objective:

{brief.campaign_objective}

Brand voice:

Tone:
{brief.tone}

Preferred vocabulary:
{brief.preferred_words}

Avoid this vocabulary:
{brief.avoided_words}

Approved factual claims:

{approved_claims_text if approved_claims_text else "No approved claims provided."}

Create one advertising draft.

The headline should be clear.
The body should be one short advertising paragraph.
The CTA should support the campaign objective.

Use the brand voice naturally.
Do not force preferred words where they do not fit.
Do not use avoided words.
"""

    response = client.responses.parse(
        model=CONFIG.text_model,
        input=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        text_format=CopyDraft
    )

    return response.output_parsed