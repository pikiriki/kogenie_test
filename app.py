import os

import streamlit as st
from dotenv import load_dotenv

from copy_generator import generate_copy
from database import (
    get_campaigns,
    initialize_database,
    save_campaign,
    save_draft_version,
)

from models import CampaignBrief, CopyDraft

load_dotenv()
initialize_database()

if "current_brief" not in st.session_state:
    st.session_state.current_brief = None

if "generated_copy" not in st.session_state:
    st.session_state.generated_copy = None

if "working_copy" not in st.session_state:
    st.session_state.working_copy = None

if "current_campaign_id" not in st.session_state:
    st.session_state.current_campaign_id = None

saved_campaigns = get_campaigns()

st.title("KOgenie Copy Studio")

st.subheader("Saved Campaigns")

if saved_campaigns:
    campaign_options = {
        f"Campaign {campaign['id']} — {campaign['headline']}": campaign
        for campaign in saved_campaigns
    }

    selected_campaign_label = st.selectbox(
        "Choose a saved campaign",
        campaign_options.keys()
    )

    load_campaign_button = st.button("Load Campaign")

    if load_campaign_button:
        selected_campaign = campaign_options[
            selected_campaign_label
        ]

        st.session_state.current_campaign_id = (
            selected_campaign["id"]
        )

        st.session_state.current_brief = CampaignBrief(
            product_description=selected_campaign["product_description"],
            audience=selected_campaign["audience"],
            campaign_objective=selected_campaign["campaign_objective"],
            tone=selected_campaign["tone"],
            preferred_words=selected_campaign["preferred_words"] or "",
            avoided_words=selected_campaign["avoided_words"] or ""
        )

        loaded_copy = CopyDraft(
            headline=selected_campaign["headline"],
            body=selected_campaign["body"],
            cta=selected_campaign["cta"]
        )

        st.session_state.generated_copy = loaded_copy
        st.session_state.working_copy = loaded_copy

        st.session_state.edit_headline = loaded_copy.headline
        st.session_state.edit_body = loaded_copy.body
        st.session_state.edit_cta = loaded_copy.cta

        st.session_state.input_product = (
            selected_campaign["product_description"]
        )

        st.session_state.input_audience = (
            selected_campaign["audience"]
        )

        st.session_state.input_objective = (
            selected_campaign["campaign_objective"]
        )

        st.session_state.input_tone = (
            selected_campaign["tone"]
        )

        st.session_state.input_preferred_words = (
            selected_campaign["preferred_words"] or ""
        )

        st.session_state.input_avoided_words = (
            selected_campaign["avoided_words"] or ""
        )

        st.success(
            f"Campaign {selected_campaign['id']} loaded."
        )

else:
    st.caption("No saved campaigns yet.")

st.write(
    "Describe a product and generate a simple advertising draft."
)

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns.",
    key="input_product"
)

audience = st.text_input(
    "Who is this ad for?",
    placeholder="Example: Ecommerce marketing managers",
    key="input_audience"
)

campaign_objective = st.text_input(
    "What should the reader do?",
    placeholder="Example: Start a free trial",
    key="input_objective"
)

tone = st.text_input(
    "How should the brand sound?",
    placeholder="Example: Clear, confident, and practical",
    key="input_tone"
)

preferred_words = st.text_input(
    "Words the brand likes to use",
    placeholder="Example: performance, creative, testing",
    key="input_preferred_words"
)

avoided_words = st.text_input(
    "Words the brand should avoid",
    placeholder="Example: revolutionary, game-changing, magic",
    key="input_avoided_words"
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
                generated_copy = generate_copy(brief)

                st.session_state.current_campaign_id = None
                st.session_state.current_brief = brief
                st.session_state.generated_copy = generated_copy
                st.session_state.working_copy = generated_copy

                st.session_state.edit_headline = generated_copy.headline
                st.session_state.edit_body = generated_copy.body
                st.session_state.edit_cta = generated_copy.cta

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

    if st.session_state.current_campaign_id is None:
        save_button = st.button("Save Campaign")

        if save_button:
            campaign_id = save_campaign(
                st.session_state.current_brief,
                st.session_state.working_copy
            )

            st.session_state.current_campaign_id = campaign_id

            version_number = save_draft_version(
                campaign_id,
                st.session_state.working_copy
            )

            st.success(
                f"Campaign {campaign_id} saved as version {version_number}."
            )

    else:
        save_version_button = st.button("Save New Version")

        if save_version_button:
            version_number = save_draft_version(
                st.session_state.current_campaign_id,
                st.session_state.working_copy
            )

            st.success(
                f"Version {version_number} saved."
            )