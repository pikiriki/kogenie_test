import base64

from pathlib import Path

from dotenv import load_dotenv

from openai import OpenAI

from models import (
    GeneratedVisual,
    VisualCreativeBrief,
    VisualGenerationSpec,
    VisualReviewReport,
    VisualStyleSpec,
)


load_dotenv()


client = OpenAI()


VISUAL_REVIEW_MODEL = "gpt-6-astra"


def image_to_data_url(
    image_path: str,
) -> str:

    path = Path(
        image_path
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Visual does not exist: {image_path}"
        )

    suffix = path.suffix.lower()

    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    if suffix not in media_types:

        raise ValueError(
            f"Unsupported visual format: {suffix}"
        )

    media_type = media_types[
        suffix
    ]

    image_bytes = path.read_bytes()

    encoded = base64.b64encode(
        image_bytes
    ).decode(
        "utf-8"
    )

    return (
        f"data:{media_type};base64,"
        f"{encoded}"
    )


def review_generated_visual(
    generated_visual: GeneratedVisual,
    generation_spec: VisualGenerationSpec,
    visual_brief: VisualCreativeBrief,
    style_spec: VisualStyleSpec,
) -> VisualReviewReport:

    image_data_url = image_to_data_url(
        generated_visual.image_path
    )

    reviewer_instructions = """
You are the Visual Reviewer for KOgenie Copy Studio.

You receive:

1. The actual generated advertising image.
2. The VisualGenerationSpec used to create it.
3. The upstream VisualCreativeBrief.
4. The upstream VisualStyleSpec.

Your job is to compare the ACTUAL IMAGE
against the INTENDED VISUAL CONTRACT.

Do not redesign the image.

Do not write replacement copy.

Do not create a new strategy.

OBJECTIVE ALIGNMENT

Use exactly:
- aligned
- partially aligned
- misaligned

Ask whether the image performs the intended
primary strategic visual job.

REQUIRED ELEMENTS

List required elements that are visibly present.

List important required elements that are missing.

Do not claim an element is present unless it is
reasonably visible in the image.

TEXT ACCURACY

Use exactly:
- accurate
- partially accurate
- inaccurate
- unreadable

Compare visible text against
VisualGenerationSpec.text_to_render.

Do not judge whether the copy itself is persuasive.
Judge whether the intended text was rendered correctly.

COMPOSITION ALIGNMENT

Use exactly:
- aligned
- partially aligned
- misaligned

Compare actual spatial relationships and hierarchy
against the required composition.

STYLE ALIGNMENT

Use exactly:
- aligned
- partially aligned
- misaligned

Compare the image against the VisualStyleSpec.

Do not reject harmless minor artistic variation.

EVIDENCE VIOLATIONS

Look for visual or textual elements that imply
unsupported:
- performance results
- ROAS improvements
- conversion improvements
- CAC improvements
- quantified time savings
- predictive winner scores
- customer results
- testimonials
- product capabilities
- offer terms

Use the supplied evidence constraints as the boundary.

NEGATIVE CONSTRAINT VIOLATIONS

Check whether anything explicitly prohibited
by the generation specification visibly appears.

REVISION NEEDED

Set revision_needed=true when a meaningful problem exists,
including:
- important strategic misalignment
- important missing required element
- inaccurate or unreadable required text
- composition that damages intended meaning
- material style mismatch
- any meaningful evidence violation
- any important negative-constraint violation

Do not demand revision for trivial aesthetic variation.

Be conservative and evidence-based.

If something cannot be confidently determined
from the image, do not pretend that it can.
"""

    comparison_context = f"""
VISUAL GENERATION SPEC

{generation_spec.model_dump_json(indent=2)}


VISUAL CREATIVE BRIEF

{visual_brief.model_dump_json(indent=2)}


VISUAL STYLE SPEC

{style_spec.model_dump_json(indent=2)}


GENERATED VISUAL METADATA

{generated_visual.model_dump_json(indent=2)}
"""

    response = client.responses.parse(
        model=VISUAL_REVIEW_MODEL,
        input=[
            {
                "role": "system",
                "content": reviewer_instructions,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": comparison_context,
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                        "detail": "high",
                    },
                ],
            },
        ],
        text_format=VisualReviewReport,
    )

    report = (
        response.output_parsed
    )

    if report is None:

        raise RuntimeError(
            "Visual reviewer returned "
            "no parsed review report."
        )

    return report
