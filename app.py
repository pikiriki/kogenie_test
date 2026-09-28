import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.title("KOgenie Copy Studio")

st.write(
    "Describe a product and generate a simple advertising draft."
)

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

generate_button = st.button("Generate Copy")

api_key = os.getenv("OPENAI_API_KEY")

if generate_button:
    if product_description:
        if api_key:
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

            st.subheader("Generated Draft")

            st.markdown(response.output_text)

        else:
            st.error("OpenAI API key is missing.")

    else:
        st.warning("Please describe your product first.")