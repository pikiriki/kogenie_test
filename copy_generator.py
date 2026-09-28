from openai import OpenAI
from pydantic import BaseModel


class CopyDraft(BaseModel):
    headline: str
    body: str
    cta: str


def generate_copy(
    product_description,
    audience,
    campaign_objective
):
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

{product_description}

Audience:

{audience}

Campaign objective:

{campaign_objective}

Create one advertising draft.

The headline should be clear.
The body should be one short advertising paragraph.
The CTA should support the campaign objective.
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