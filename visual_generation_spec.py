from models import (
    ChannelSpec,
    CopyStrategyCard,
    MetaFeedAdDraft,
    VisualCreativeBrief,
    VisualGenerationSpec,
    VisualStyleSpec,
)


def format_list(
    items: list[str],
) -> str:

    return "\n".join(
        f"- {item}"
        for item in items
    )


def build_visual_generation_spec(
    strategy_card: CopyStrategyCard,
    visual_brief: VisualCreativeBrief,
    style_spec: VisualStyleSpec,
    meta_draft: MetaFeedAdDraft,
    channel_spec: ChannelSpec,
    width: int,
    height: int,
) -> VisualGenerationSpec:

    if width <= 0:
        raise ValueError(
            "Canvas width must be greater than zero."
        )


    if height <= 0:
        raise ValueError(
            "Canvas height must be greater than zero."
        )

    aspect_ratio = (
        width / height
    )

    canvas = (
        f"{width} × {height} px "
        f"(aspect ratio {aspect_ratio:.2f}:1)"
    )

    required_elements = [
        (
            "Primary subject: "
            + visual_brief.subject
        ),
        (
            "Scene: "
            + visual_brief.scene
        ),
        (
            "Product role: "
            + visual_brief.product_role
        ),
    ]

    required_elements.append(
        (
            "Visual proof requirement: "
            + visual_brief.visual_proof
        )
    )

    text_to_render = [
        (
            "Headline: "
            + meta_draft.headline
        ),
        (
            "CTA: "
            + meta_draft.cta
        ),
    ]

    style = "\n".join([
        (
            "Aesthetic: "
            + style_spec.aesthetic_direction
        ),
        (
            "Palette: "
            + style_spec.palette_direction
        ),
        (
            "Typography: "
            + style_spec.typography_direction
        ),
        (
            "Imagery: "
            + style_spec.imagery_style
        ),
        (
            "Spacing: "
            + style_spec.spacing_density
        ),
        (
            "Shape language: "
            + style_spec.shape_language
        ),
    ])

    evidence_constraints = []

    for boundary in (
        strategy_card.proof_boundary
    ):

        evidence_constraints.append(
            "Proof boundary: "
            + boundary
        )

    for boundary in (
        strategy_card.offer_boundary
    ):

        evidence_constraints.append(
            "Offer boundary: "
            + boundary
        )

    evidence_constraints.append(
        (
            "Do not visually imply any result, metric, "
            "capability, offer, or customer outcome that "
            "is not supported by the supplied campaign."
        )
    )

    negative_constraints = (
        visual_brief.avoid
        + style_spec.prohibited_styles
    )

    negative_constraints = list(
        dict.fromkeys(
            negative_constraints
        )
    )

    generation_instruction = f"""
Create one advertising visual.

CHANNEL
{channel_spec.channel}

PLACEMENT
{channel_spec.placement}

CANVAS
{canvas}

PRIMARY VISUAL OBJECTIVE
{visual_brief.visual_job}

REQUIRED VISUAL ELEMENTS
{format_list(required_elements)}

EXACT TEXT TO RENDER
{format_list(text_to_render)}

COMPOSITION
{visual_brief.composition}

TEXT HIERARCHY
{format_list(visual_brief.text_hierarchy)}

VISUAL STYLE
{style}

BRAND CONSISTENCY RULES
{format_list(style_spec.brand_consistency_rules)}

EVIDENCE CONSTRAINTS
{format_list(evidence_constraints)}

NEGATIVE CONSTRAINTS
{format_list(negative_constraints)}

CHANNEL REQUIREMENTS
{format_list(channel_spec.formatting_rules)}

COPY CONNECTION
{visual_brief.copy_connection}

IMPORTANT

Preserve the exact campaign meaning.

Do not invent additional text, metrics,
product capabilities, customer results,
commercial terms, proof, urgency, or scarcity.

The visual must support the existing campaign.
It must not create a new campaign strategy.
""".strip()

    return VisualGenerationSpec(
        objective=visual_brief.visual_job,
        canvas=canvas,
        required_elements=required_elements,
        text_to_render=text_to_render,
        composition=visual_brief.composition,
        style=style,
        evidence_constraints=(
            evidence_constraints
        ),
        negative_constraints=(
            negative_constraints
        ),
        generation_instruction=(
            generation_instruction
        ),
    )
