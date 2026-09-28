import os

import streamlit as st
from dotenv import load_dotenv

from copy_generator import generate_copy
from models import CampaignBrief

load_dotenv()

if "generated_copy" not in st.session_state:
    st.session_state.generated_copy = None

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

tone = st.text_input(
    "How should the brand sound?",
    placeholder="Example: Clear, confident, and practical"
)

preferred_words = st.text_input(
    "Words the brand likes to use",
    placeholder="Example: performance, creative, testing"
)

avoided_words = st.text_input(
    "Words the brand should avoid",
    placeholder="Example: revolutionary, game-changing, magic"
)

generate_button = st.button("Generate Copy")

api_key = os.getenv("OPENAI_API_KEY")

if generate_button:
    if (
        product_description
        and audience
        and campaign_objective
        and tone
    ):
        if api_key:
            brief = CampaignBrief(
                product_description=product_description,
                audience=audience,
                campaign_objective=campaign_objective,
                tone=tone,
                preferred_words=preferred_words,
                avoided_words=avoided_words
            )

            try:
                st.session_state.generated_copy = generate_copy(brief)

            except Exception:
                st.error(
                    "Something went wrong while generating the copy. Please try again."
                )

        else:
            st.error("OpenAI API key is missing.")

    else:
        st.warning(
            "Please provide the product, audience, campaign objective, and tone."
        )

if st.session_state.generated_copy:
    st.subheader("Generated Draft")

    st.markdown("### Headline")
    st.write(st.session_state.generated_copy.headline)

    st.markdown("### Body")
    st.write(st.session_state.generated_copy.body)

    st.markdown("### CTA")
    st.write(st.session_state.generated_copy.cta)