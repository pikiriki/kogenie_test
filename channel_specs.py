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
