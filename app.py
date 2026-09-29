import os

import streamlit as st
from dotenv import load_dotenv

from copy_generator import generate_copy
from exporter import create_campaign_export
from database import (
    get_approved_claims,
    get_brand_profiles,
    get_campaigns,
    get_draft_versions,
    initialize_database,
    save_approved_claim,
    save_brand_profile,
    save_campaign,
    save_draft_version,
)

from models import BrandProfile, CampaignBrief, CopyDraft

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

if "working_copy_source" not in st.session_state:
    st.session_state.working_copy_source = None

saved_campaigns = get_campaigns()

st.title("KOgenie Copy Studio")

st.subheader("Brand Profiles")

new_brand_name = st.text_input(
    "Brand name",
    key="new_brand_name",
    placeholder="Example: KOgenie"
)

new_brand_tone = st.text_input(
    "Brand tone",
    key="new_brand_tone",
    placeholder="Example: Clear, confident, and practical"
)

new_brand_preferred_words = st.text_input(
    "Preferred words",
    key="new_brand_preferred_words",
    placeholder="Example: performance, creative, testing"
)

new_brand_avoided_words = st.text_input(
    "Words to avoid",
    key="new_brand_avoided_words",
    placeholder="Example: revolutionary, magic, effortless"
)

save_brand_profile_button = st.button(
    "Save Brand Profile"
)

if save_brand_profile_button:
    if new_brand_name and new_brand_tone:
        profile = BrandProfile(
            name=new_brand_name,
            tone=new_brand_tone,
            preferred_words=new_brand_preferred_words,
            avoided_words=new_brand_avoided_words
        )

        save_brand_profile(profile)

        st.success(
            f"Brand profile '{profile.name}' saved."
        )

    else:
        st.warning(
            "Please provide at least a brand name and tone."
        )

saved_brand_profiles = get_brand_profiles()

brand_options = {
    "Manual brand voice": None
}

for profile in saved_brand_profiles:
    brand_options[profile["name"]] = profile

selected_brand_name = st.selectbox(
    "Brand for this campaign",
    brand_options.keys()
)

selected_brand_profile = brand_options[
    selected_brand_name
]

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
            avoided_words=selected_campaign["avoided_words"] or "",
            approved_claims=[]
        )

        loaded_copy = CopyDraft(
            headline=selected_campaign["headline"],
            body=selected_campaign["body"],
            cta=selected_campaign["cta"]
        )

        st.session_state.generated_copy = loaded_copy
        st.session_state.working_copy = loaded_copy
        st.session_state.working_copy_source = None

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

if selected_brand_profile is None:
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

    approved_claims = []

else:
    selected_brand = BrandProfile(
        name=selected_brand_profile["name"],
        tone=selected_brand_profile["tone"],
        preferred_words=(
            selected_brand_profile["preferred_words"] or ""
        ),
        avoided_words=(
            selected_brand_profile["avoided_words"] or ""
        )
    )

    tone = selected_brand.tone
    preferred_words = selected_brand.preferred_words
    avoided_words = selected_brand.avoided_words

    st.caption(
        f"Using saved voice for {selected_brand.name}"
    )

    st.write(f"Tone: {tone}")

    if preferred_words:
        st.write(
            f"Preferred words: {preferred_words}"
        )

    if avoided_words:
        st.write(
            f"Avoid: {avoided_words}"
        )

    st.markdown("#### Approved Claims")

    new_claim = st.text_input(
        "Add an approved claim",
        placeholder="Example: Turns one campaign brief into multiple creative concepts.",
        key="new_approved_claim"
    )

    claim_evidence = st.text_area(
        "Evidence for this claim",
        placeholder=(
            "Example: Confirmed in the product specification "
            "and demonstrated in the current application."
        ),
        key="new_claim_evidence"
    )

    claim_source = st.text_input(
        "Source reference",
        placeholder=(
            "Example: Product specification v1, section 3"
        ),
        key="new_claim_source"
    )

    claim_status = st.selectbox(
        "Verification status",
        [
            "unverified",
            "verified"
        ],
        key="new_claim_status"
    )

    add_claim_button = st.button(
        "Add Approved Claim"
    )

    if add_claim_button:
        if new_claim:
            save_approved_claim(
                selected_brand_profile["id"],
                new_claim,
                claim_evidence,
                claim_source,
                claim_status
            )

            st.success(
                f"Claim saved with status: {claim_status}."
            )

        else:
            st.warning(
                "Please enter a claim first."
            )

    approved_claim_rows = get_approved_claims(
        selected_brand_profile["id"]
    )

    verified_claims = [
        claim["claim_text"]
        for claim in approved_claim_rows
        if claim["verification_status"] == "verified"
    ]

    approved_claims = verified_claims

    if approved_claim_rows:
        for claim in approved_claim_rows:
            status = claim["verification_status"]

            if status == "verified":
                st.write(
                    f"✅ {claim['claim_text']}"
                )
            else:
                st.write(
                    f"⚠️ {claim['claim_text']}"
                )

            st.caption(
                f"Status: {status}"
            )

            if claim["evidence_note"]:
                st.caption(
                    f"Evidence: {claim['evidence_note']}"
                )

            if claim["source_reference"]:
                st.caption(
                    f"Source: {claim['source_reference']}"
                )

            st.markdown("---")

    else:
        st.caption(
            "No claims saved for this brand yet."
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
                avoided_words=avoided_words,
                approved_claims=approved_claims
            )

            try:
                generated_copy = generate_copy(brief)

                st.session_state.current_campaign_id = None
                st.session_state.current_brief = brief
                st.session_state.generated_copy = generated_copy
                st.session_state.working_copy = generated_copy
                st.session_state.working_copy_source = "ai"

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
        st.session_state.working_copy_source = "human"

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

    version_note = st.text_input(
        "Version note",
        placeholder="Example: Tightened headline and CTA"
    )

    if st.session_state.current_campaign_id is None:
        save_button = st.button("Save Campaign")

        if save_button:
            campaign_id = save_campaign(
                st.session_state.current_brief,
                st.session_state.working_copy
            )

            st.session_state.current_campaign_id = campaign_id

            first_version = save_draft_version(
                campaign_id,
                st.session_state.generated_copy,
                "ai",
                "Initial AI generation"
            )

            if (
                st.session_state.working_copy
                != st.session_state.generated_copy
            ):
                second_version = save_draft_version(
                    campaign_id,
                    st.session_state.working_copy,
                    "human",
                    version_note or "Human applied edits"
                )

                st.success(
                    f"Campaign {campaign_id} saved with versions "
                    f"{first_version} and {second_version}."
                )

            else:
                st.success(
                    f"Campaign {campaign_id} saved as version "
                    f"{first_version}."
                )

    else:
        save_version_button = st.button("Save New Version")

        if save_version_button:
            version_number = save_draft_version(
                st.session_state.current_campaign_id,
                st.session_state.working_copy,
                st.session_state.working_copy_source or "unknown",
                version_note or "No note provided"
            )

            st.success(
                f"Version {version_number} saved."
            )

if st.session_state.current_campaign_id is not None:
    st.markdown("---")
    st.subheader("Version History")

    versions = get_draft_versions(
        st.session_state.current_campaign_id
    )

    if versions:
        version_options = {
            f"Version {version['version_number']} — "
            f"{version['source'].upper()} — "
            f"{version['created_at']}": version
            for version in versions
        }

        selected_version_label = st.selectbox(
            "Inspect a saved version",
            version_options.keys()
        )

        selected_version = version_options[
            selected_version_label
        ]

        st.markdown("### Historical Snapshot")

        st.write(
            f"Source: {selected_version['source']}"
        )

        if selected_version["note"]:
            st.write(
                f"Note: {selected_version['note']}"
            )

        st.markdown("#### Headline")
        st.write(selected_version["headline"])

        st.markdown("#### Body")
        st.write(selected_version["body"])

        st.markdown("#### CTA")
        st.write(selected_version["cta"])

    else:
        st.caption("No draft versions saved yet.")

if (
    st.session_state.current_campaign_id is not None
    and st.session_state.current_brief
    and st.session_state.working_copy
):
    st.markdown("---")
    st.subheader("Export Campaign")

    export_versions = get_draft_versions(
        st.session_state.current_campaign_id
    )

    campaign_export = create_campaign_export(
        st.session_state.current_campaign_id,
        st.session_state.current_brief,
        st.session_state.working_copy,
        export_versions
    )

    st.download_button(
        label="Download Campaign JSON",
        data=campaign_export,
        file_name=(
            f"campaign_"
            f"{st.session_state.current_campaign_id}"
            f"_export.json"
        ),
        mime="application/json"
    )