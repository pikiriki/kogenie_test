import os

import streamlit as st
from dotenv import load_dotenv

from copy_generator import generate_copy

load_dotenv()

st.title("KOgenie Copy Studio")

st.write(
    "Describe a product and generate a simple advertising draft."
)

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

audience = st.text_input(
    "Who is this ad for?",
    placeholder="Example: Ecommerce marketing managers"
)

campaign_objective = st.text_input(
    "What should the reader do?",
    placeholder="Example: Start a free trial"
)

generate_button = st.button("Generate Copy")

api_key = os.getenv("OPENAI_API_KEY")

if generate_button:
    if product_description and audience and campaign_objective:
        if api_key:
            generated_copy = generate_copy(
                product_description,
                audience,
                campaign_objective
            )

            st.subheader("Generated Draft")

            st.markdown("### Headline")
            st.write(generated_copy.headline)

            st.markdown("### Body")
            st.write(generated_copy.body)

            st.markdown("### CTA")
            st.write(generated_copy.cta)

        else:
            st.error("OpenAI API key is missing.")

    else:
        st.warning(
            "Please provide the product, audience, and campaign objective."
        )