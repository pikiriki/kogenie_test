import base64

from datetime import (
    datetime,
    timezone,
)

from pathlib import Path

from openai import OpenAI

from models import (
    GeneratedVisual,
    VisualGenerationSpec,
    VisualRepairPlan,
    VisualReviewReport,
)

from visual_generator import (
    IMAGE_MODEL,
    make_artifact_stem,
    validate_image_size,
)


client = OpenAI()


def build_visual_repair_plan(
    review: VisualReviewReport,
    generation_spec: VisualGenerationSpec,
) -> VisualRepairPlan:

    preserve = []
    fix = []

    if review.objective_alignment == "aligned":

        preserve.append(
            (
                "Preserve the current visual's "
                "successful communication of the "
                "primary objective: "
                + generation_spec.objective
            )
        )

    else:

        fix.append(
            (
                "Correct the visual so it clearly "
                "communicates the intended objective: "
                + generation_spec.objective
            )
        )

    for element in (
        review.required_elements_present
    ):

        preserve.append(
            (
                "Preserve this successfully rendered "
                f"required element: {element}"
            )
        )

    for element in review.missing_elements:

        fix.append(
            (
                "Add or restore this missing "
                f"required element: {element}"
            )
        )

    if review.text_accuracy == "accurate":

        preserve.append(
            (
                "Preserve all currently correct "
                "required text exactly."
            )
        )

    else:

        exact_text = "; ".join(
            generation_spec.text_to_render
        )

        fix.append(
            (
                "Correct the required visible text. "
                "Render these required strings exactly: "
                + exact_text
            )
        )

    if (
        review.composition_alignment
        == "aligned"
    ):

        preserve.append(
            (
                "Preserve the current successful "
                "composition and spatial hierarchy."
            )
        )

    else:

        fix.append(
            (
                "Correct the composition to match "
                "this intended structure: "
                + generation_spec.composition
            )
        )

    if review.style_alignment == "aligned":

        preserve.append(
            (
                "Preserve the current visual style, "
                "palette character, typography character, "
                "spacing, and shape language."
            )
        )

    else:

        fix.append(
            (
                "Correct the visual styling so it "
                "matches this approved style direction: "
                + generation_spec.style
            )
        )

    for violation in (
        review.evidence_violations
    ):

        fix.append(
            (
                "Remove this unsupported visual or "
                f"textual implication: {violation}"
            )
        )

    for violation in (
        review
        .negative_constraint_violations
    ):

        fix.append(
            (
                "Remove or replace this prohibited "
                f"visual element: {violation}"
            )
        )

    evidence_constraints = list(
        generation_spec.evidence_constraints
    )

    if not review.revision_needed:

        return VisualRepairPlan(
            preserve=[
                (
                    "Preserve the current visual. "
                    "The automated review did not "
                    "identify a material issue."
                )
            ],
            fix=[],
            evidence_constraints=(
                evidence_constraints
            ),
            repair_instruction=(
                "No image edit is required."
            ),
        )

    preserve_text = "\n".join(
        f"- {item}"
        for item in preserve
    )

    fix_text = "\n".join(
        f"- {item}"
        for item in fix
    )

    evidence_text = "\n".join(
        f"- {item}"
        for item in evidence_constraints
    )

    repair_instruction = f"""
Edit the supplied advertising image.

This is a TARGETED REPAIR.

Do not redesign the campaign from scratch.

PRESERVE

{preserve_text}

FIX ONLY THESE MATERIAL ISSUES

{fix_text}

EVIDENCE CONSTRAINTS

{evidence_text}

ORIGINAL VISUAL CONTRACT

Objective:
{generation_spec.objective}

Required elements:
{chr(10).join(
    f"- {item}"
    for item in generation_spec.required_elements
)}

Exact required text:
{chr(10).join(
    f"- {item}"
    for item in generation_spec.text_to_render
)}

Composition:
{generation_spec.composition}

Style:
{generation_spec.style}

NEGATIVE CONSTRAINTS

{chr(10).join(
    f"- {item}"
    for item in generation_spec.negative_constraints
)}

IMPORTANT

Keep everything that already satisfies the contract.

Change only what is required to fix the listed failures.

Do not add new claims, metrics, capabilities,
customer outcomes, offer terms, urgency,
scarcity, or visual proof.

Do not create a new campaign strategy.

The repaired image must remain an execution
of the same VisualGenerationSpec.
""".strip()

    return VisualRepairPlan(
        preserve=preserve,
        fix=fix,
        evidence_constraints=(
            evidence_constraints
        ),
        repair_instruction=(
            repair_instruction
        ),
    )


def repair_visual_once(
    generated_visual: GeneratedVisual,
    generation_spec: VisualGenerationSpec,
    repair_plan: VisualRepairPlan,
    output_directory: str = "generated_visuals",
) -> GeneratedVisual:

    if not repair_plan.fix:

        raise ValueError(
            "Visual repair was requested, "
            "but the repair plan contains no fixes."
        )

    validate_image_size(
        generation_spec.width,
        generation_spec.height,
    )

    source_path = Path(
        generated_visual.image_path
    )

    if not source_path.exists():

        raise FileNotFoundError(
            (
                "Source visual does not exist: "
                + str(source_path)
            )
        )

    allowed_suffixes = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }

    if (
        source_path.suffix.lower()
        not in allowed_suffixes
    ):

        raise ValueError(
            "Source visual must be PNG, JPG, "
            "JPEG, or WEBP."
        )

    file_size = source_path.stat().st_size

    max_size = 50 * 1024 * 1024

    if file_size >= max_size:

        raise ValueError(
            "Source visual must be smaller "
            "than 50 MB."
        )

    output_dir = Path(
        output_directory
    )


    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    artifact_stem = make_artifact_stem(
        generated_visual.campaign_id,
        (
            generated_visual.channel
            + "_repair"
        ),
    )

    size = (
        f"{generation_spec.width}"
        f"x"
        f"{generation_spec.height}"
    )

    with source_path.open("rb") as source_file:

        response = client.images.edit(
            model=IMAGE_MODEL,
            image=source_file,
            prompt=(
                repair_plan.repair_instruction
            ),
            n=1,
            size=size,
            quality="medium",
            output_format="png",
            background="opaque",
        )

    if not response.data:

        raise RuntimeError(
            "Image edit returned no image data."
        )

    encoded_image = (
        response.data[0].b64_json
    )

    if not encoded_image:

        raise RuntimeError(
            "Image edit returned no "
            "base64 image payload."
        )

    image_bytes = base64.b64decode(
        encoded_image
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

    repaired_visual = GeneratedVisual(
        campaign_id=(
            generated_visual.campaign_id
        ),

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

        channel=(
            generated_visual.channel
        ),

        model=IMAGE_MODEL,

        created_at=created_at,

        approval_status="unreviewed",

        source_image_path=(
            generated_visual.image_path
        ),

        repair_plan_snapshot=(
            repair_plan.model_dump_json(
                indent=2
            )
        ),
    )

    metadata_path.write_text(
        repaired_visual.model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )

    return repaired_visual
