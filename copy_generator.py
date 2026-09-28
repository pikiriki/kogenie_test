from openai import OpenAI


def generate_copy(product_description):
    client = OpenAI()

    prompt = f"""
You are writing a simple advertising draft.

Product information:

{product_description}

Write exactly these three sections:

### Headline
Write one clear headline.

### Body
Write a short advertising paragraph.

### CTA
Write one simple call to action.

Rules:
- Only use product information supplied above.
- Do not invent statistics.
- Do not invent testimonials.
- Do not invent prices.
- Do not invent guarantees.
- Do not invent product capabilities.
- Keep the copy concise.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text