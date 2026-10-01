from models import ChannelSpec


def get_meta_feed_spec(
    objective: str,
) -> ChannelSpec:

    return ChannelSpec(
        channel="Meta",
        placement="Feed ad",
        objective=objective,
        length_constraint=(
            "Short-form execution. Compress the complete "
            "sales message into a concise advertisement."
        ),
        required_fields=[
            "primary_text",
            "headline",
            "cta",
        ],
        formatting_rules=[
            "Lead quickly with the selected creative angle.",
            "Keep one dominant argument.",
            "Preserve the documented mechanism.",
            "Do not invent proof or performance claims.",
            "Do not invent offer terms.",
            "Use one clear CTA matching the objective.",
        ],
    )


def get_google_search_spec(
    objective: str,
) -> ChannelSpec:

    return ChannelSpec(
        channel="Google Search",
        placement="Search ad",
        objective=objective,
        length_constraint=(
            "Compact search execution. Use short headlines "
            "and concise descriptions."
        ),
        required_fields=[
            "headlines",
            "descriptions",
            "cta",
        ],
        formatting_rules=[
            "Connect directly to the supplied search intent.",
            "Keep the documented product capability clear.",
            "Preserve the selected creative angle where relevant.",
            "Do not invent superiority claims.",
            "Do not invent proof or performance results.",
            "Do not invent commercial terms.",
            "Use a CTA matching the real campaign objective.",
        ],
    )


def get_email_spec(
    objective: str,
) -> ChannelSpec:

    return ChannelSpec(
        channel="Email",
        placement="Campaign email",
        objective=objective,
        length_constraint=(
            "Concise email execution. Use a short subject line, "
            "brief preview text, and one focused body argument."
        ),
        required_fields=[
            "subject_lines",
            "preview_text",
            "body",
            "cta",
        ],
        formatting_rules=[
            "Generate three subject-line options.",
            "Make the subject earn the open without clickbait.",
            "Use preview text to extend rather than merely repeat the subject.",
            "Keep one dominant campaign argument.",
            "Make the opening easy to continue reading.",
            "Preserve the documented mechanism.",
            "Do not invent proof or commercial terms.",
            "Use one clear CTA matching the objective.",
        ],
    )


def get_landing_page_spec(
    objective: str,
) -> ChannelSpec:

    return ChannelSpec(
        channel="Landing Page",
        placement="Campaign landing page",
        objective=objective,
        length_constraint=(
            "Long-form execution. Give the campaign argument "
            "enough space to develop through clear page sections."
        ),
        required_fields=[
            "hero_headline",
            "hero_subheadline",
            "problem_section",
            "mechanism_section",
            "proof_section",
            "objection_section",
            "offer_section",
            "cta",
        ],
        formatting_rules=[
            "Keep one dominant Big Idea throughout the page.",
            "Preserve the selected creative angle.",
            "Create recognition before pushing the product.",
            "Explain the documented mechanism clearly.",
            "Use only proof that actually exists.",
            "Preserve unresolved objections and evidence gaps.",
            "Use only verified commercial terms.",
            "Use one clear CTA matching the campaign objective.",
        ],
    )
