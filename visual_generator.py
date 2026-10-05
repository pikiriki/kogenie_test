import base64

from datetime import (
    datetime,
    timezone,
)

from pathlib import Path

from uuid import uuid4

from dotenv import load_dotenv

from openai import OpenAI

from models import (
    GeneratedVisual,
    VisualGenerationSpec,
)


from config import (
    get_config,
)


CONFIG = get_config()


load_dotenv()


client = OpenAI()




def validate_image_size(
    width: int,
    height: int,
) -> None:

    if width <= 0 or height <= 0:

        raise ValueError(
            "Image dimensions must be positive."
        )

    if width % 16 != 0:

        raise ValueError(
            "Image width must be divisible by 16 "
            "for arbitrary GPT Image 2/2.5 sizes."
        )

    if height % 16 != 0:

        raise ValueError(
            "Image height must be divisible by 16 "
            "for arbitrary GPT Image 2/2.5 sizes."
        )

    ratio = width / height

    if ratio < (1 / 3) or ratio > 3:

        raise ValueError(
            "Image aspect ratio must be between "
            "1:3 and 3:1."
        )


def make_artifact_stem(
    campaign_id: int,
    channel: str,
) -> str:

    safe_channel = (
        channel
        .strip()
        .lower()
        .replace(" ", "_")
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    short_id = uuid4().hex[:8]

    return (
        f"campaign_{campaign_id}_"
        f"{safe_channel}_"
        f"{timestamp}_"
        f"{short_id}"
    )


def generate_visual(
    campaign_id: int,
    channel: str,
    generation_spec: VisualGenerationSpec,
    output_directory: str | None = None,
) -> GeneratedVisual:

    validate_image_size(
        generation_spec.width,
        generation_spec.height,
    )

    if output_directory is None:

        output_dir = (
            CONFIG.generated_visuals_path
        )

    else:

        output_dir = Path(
            output_directory
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    size = (
        f"{generation_spec.width}"
        f"x"
        f"{generation_spec.height}"
    )

    response = client.images.generate(
        model=CONFIG.image_model,
        prompt=(
            generation_spec
            .generation_instruction
        ),
        n=1,
        size=size,
        quality="medium",
        output_format="png",
        background="opaque",
    )

    if not response.data:

        raise RuntimeError(
            "Image API returned no image data."
        )

    encoded_image = (
        response.data[0].b64_json
    )

    if not encoded_image:

        raise RuntimeError(
            "Image API returned no "
            "base64 image payload."
        )

    image_bytes = base64.b64decode(
        encoded_image
    )

    artifact_stem = make_artifact_stem(
        campaign_id,
        channel,
    )

    image_path = (
        output_dir
        / f"{artifact_stem}.png"
    )

    metadata_path = (
        output_dir
        / f"{artifact_stem}.json"
    )

    image_path.write_bytes(
        image_bytes
    )

    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    generated_visual = GeneratedVisual(
        campaign_id=campaign_id,

        image_path=str(
            image_path
        ),

        metadata_path=str(
            metadata_path
        ),

        generation_spec_snapshot=(
            generation_spec.model_dump_json(
                indent=2
            )
        ),

        channel=channel,

        model=CONFIG.image_model,

        created_at=created_at,

        approval_status="unreviewed",
    )

    metadata_path.write_text(
        generated_visual.model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )

    return generated_visual
