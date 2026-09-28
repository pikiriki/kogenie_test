import os

import streamlit as st
from dotenv import load_dotenv

from copy_generator import generate_copy
from models import CampaignBrief, CopyDraft

load_dotenv()

if "generated_copy" not in st.session_state:
    st.session_state.generated_copy = None

if "working_copy" not in st.session_state:
    st.session_state.working_copy = None

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

                st.session_state.working_copy = (
                    st.session_state.generated_copy
                )

                st.session_state.edit_headline = (
                    st.session_state.generated_copy.headline
                )

                st.session_state.edit_body = (
                    st.session_state.generated_copy.body
                )

                st.session_state.edit_cta = (
                    st.session_state.generated_copy.cta
                )

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
    st.subheader("Working Draft")

    st.text_input(
        "Headline",
        key="edit_headline"
    )

    st.text_area(
        "Body",
        key="edit_body",
        height=150
    )

    st.text_input(
        "CTA",
        key="edit_cta"
    )

    apply_edits_button = st.button("Apply Edits")

    if apply_edits_button:
        st.session_state.working_copy = CopyDraft(
            headline=st.session_state.edit_headline,
            body=st.session_state.edit_body,
            cta=st.session_state.edit_cta
        )

        st.success("Edits applied.")

    if st.session_state.working_copy:
        st.markdown("---")
        st.subheader("Current Working Version")

        st.markdown("### Headline")
        st.write(st.session_state.working_copy.headline)

        st.markdown("### Body")
        st.write(st.session_state.working_copy.body)

        st.markdown("### CTA")
        st.write(st.session_state.working_copy.cta)