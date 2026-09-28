from openai import OpenAI

from models import CampaignBrief, CopyDraft


def generate_copy(brief: CampaignBrief):
    client = OpenAI()

    instructions = """
You are a direct-response advertising copywriter.

Your job is to communicate the product clearly and persuasively to the specified audience.

Follow these rules:
- Use only facts supplied in the product information.
- Do not invent statistics.
- Do not invent testimonials.
- Do not invent prices.
- Do not invent guarantees.
- Do not invent product capabilities.
- Prefer clear language over clever language.
- Keep the draft concise.
"""

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

Create one advertising draft.

The headline should be clear.
The body should be one short advertising paragraph.
The CTA should support the campaign objective.

Use the brand voice naturally.
Do not force preferred words where they do not fit.
Do not use avoided words.
"""

    response = client.responses.parse(
        model="gpt-6-luna",
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