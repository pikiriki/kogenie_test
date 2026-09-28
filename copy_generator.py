from openai import OpenAI


def generate_copy(product_description):
    client = OpenAI()

    instructions = """
You are a direct-response advertising copywriter.

Your job is to communicate the product clearly and persuasively.

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

Create one advertising draft.

Return exactly these three sections:

### Headline
Write one clear headline.

### Body
Write one short advertising paragraph.

### CTA
Write one simple call to action.
"""

    response = client.responses.create(
        model="gpt-6-luna",
        instructions=instructions,
        input=input_text
    )

    return response.output_text