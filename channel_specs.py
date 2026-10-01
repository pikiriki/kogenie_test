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
