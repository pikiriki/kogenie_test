import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

st.title("KOgenie Copy Studio")

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

generate_button = st.button("Generate Copy")

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    st.success("OpenAI API key loaded.")
else:
    st.warning("OpenAI API key not found.")

if generate_button:
    if product_description:
        if api_key:
            client = OpenAI()

            prompt = f"""
Write one simple advertising draft for this product:

{product_description}

Return exactly these three sections:

Headline:
Body:
CTA:

Rules:
- Keep the draft concise.
- Do not invent statistics.
- Do not invent testimonials.
- Do not invent prices or guarantees.
- Do not invent product capabilities.
- Only use facts provided in the product description.
"""

            response = client.responses.create(
                model="gpt-6-luna",
                input=prompt
            )

            st.subheader("Generated Draft")
            st.write(response.output_text)

        else:
            st.error("OpenAI API key is missing.")
    else:
        st.warning("Please describe your product first.")