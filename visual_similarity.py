from dotenv import load_dotenv

from openai import OpenAI

from models import (
    CopyStrategyCard,
    GeneratedVisual,
    VisualAsset,
    VisualCreativeBrief,
    VisualSimilarityMatch,
    VisualSimilarityReport,
)

from visual_approval import (
    sha256_file,
)

from visual_reviewer import (
    image_to_data_url,
)


from config import (
    get_config,
)


CONFIG = get_config()


load_dotenv()


client = OpenAI()




def dedupe_strings(
    items: list[str],
) -> list[str]:

    cleaned = []

    seen = set()

    for item in items:

        value = item.strip()

        if not value:
            continue

        if value in seen:
            continue

        seen.add(value)
        cleaned.append(value)

    return cleaned


def build_exact_duplicate_match(
    asset: VisualAsset,
) -> VisualSimilarityMatch:

    if asset.id is None:

        raise ValueError(
            "Historical VisualAsset has no ID."
        )

    return VisualSimilarityMatch(
        asset_id=asset.id,

        overlap_level="high",

        same_visual_territory=True,

        similarity_reason=(
            "The candidate visual has the "
            "same SHA-256 fingerprint as this "
            "approved historical visual."
        ),

        shared_visual_patterns=[
            (
                "The candidate and historical "
                "asset are the exact same image bytes."
            )
        ],

        meaningful_differences=[],

        novelty_gaps=[
            (
                "There is no visual execution "
                "difference from this historical asset."
            )
        ],
    )


def compare_visual_pair(
    candidate_visual: GeneratedVisual,
    current_strategy: CopyStrategyCard,
    current_visual_brief: VisualCreativeBrief,
    historical_asset: VisualAsset,
) -> VisualSimilarityMatch:

    if historical_asset.id is None:

        raise ValueError(
            "Historical VisualAsset has no ID."
        )

    candidate_image = image_to_data_url(
        candidate_visual.image_path
    )

    historical_image = image_to_data_url(
        historical_asset
        .approved_snapshot_path
    )

    instructions = """
You are the Visual Strategic Repetition Reviewer
for KOgenie Copy Studio.

You receive two advertising images.

IMAGE A:
the newly proposed candidate visual.

IMAGE B:
one human-approved historical visual.

Determine whether the NEW candidate materially
repeats the same visual strategic territory.

This is NOT an exact-pixel comparison.

Focus on:

- visual metaphor
- subject relationship
- composition logic
- persuasive visual argument
- mechanism depiction
- visual job
- information hierarchy

DO NOT treat these by themselves as repetition:

- same brand colors
- same logo
- same type family
- same general brand style
- both using cards
- both using product UI

Those may simply be brand consistency.

Different colors or styling do NOT automatically
make the visual strategically different.

Ask:

"If the styling and exact copy were stripped away,
would these two images still communicate essentially
the same visual advertising idea?"

OVERLAP LEVEL

Use exactly:
- low
- medium
- high

SAME VISUAL TERRITORY

Set true when the central visual metaphor,
relationship, or strategic visual argument is
substantially the same.

MEANINGFUL DIFFERENCES

Identify real strategic or compositional differences,
not superficial color/font differences.

NOVELTY GAPS

Identify cases where the new candidate appears
different cosmetically but does not introduce
a meaningful new visual interpretation.

Do not infer campaign performance.

Historical approval means the old asset was approved,
not that it performed well.

Do not redesign either visual.
"""

    context = f"""
CURRENT CANDIDATE

Campaign:
{candidate_visual.campaign_id}

Current strategy angle:
{current_strategy.selected_angle}

Current visual job:
{current_visual_brief.visual_job}

Current visual subject:
{current_visual_brief.subject}

Current copy connection:
{current_visual_brief.copy_connection}


HISTORICAL APPROVED ASSET

Asset ID:
{historical_asset.id}

Campaign:
{historical_asset.campaign_id}

Historical strategy angle:
{historical_asset.strategy_angle}

Historical visual job:
{historical_asset.visual_job}
"""

    schema = (
        VisualSimilarityMatch
        .model_json_schema()
    )

    response = client.responses.create(
        model=CONFIG.vision_model,

        input=[
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            context
                            + "\n\nIMAGE A — "
                            "NEW CANDIDATE"
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            candidate_image
                        ),
                        "detail": "high",
                    },
                    {
                        "type": "input_text",
                        "text": (
                            "IMAGE B — "
                            "HISTORICAL APPROVED ASSET"
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            historical_image
                        ),
                        "detail": "high",
                    },
                ],
            },
        ],

        text={
            "format": {
                "type": "json_schema",
                "name": (
                    "visual_similarity_match"
                ),
                "strict": True,
                "schema": schema,
            }
        },
    )

    match = (
        VisualSimilarityMatch
        .model_validate_json(
            response.output_text
        )
    )

    return VisualSimilarityMatch(
        asset_id=historical_asset.id,

        overlap_level=(
            match.overlap_level
        ),

        same_visual_territory=(
            match.same_visual_territory
        ),

        similarity_reason=(
            match.similarity_reason
        ),

        shared_visual_patterns=(
            match.shared_visual_patterns
        ),

        meaningful_differences=(
            match.meaningful_differences
        ),

        novelty_gaps=(
            match.novelty_gaps
        ),
    )


def review_visual_repetition(
    candidate_visual: GeneratedVisual,
    current_strategy: CopyStrategyCard,
    current_visual_brief: VisualCreativeBrief,
    historical_assets: list[VisualAsset],
) -> VisualSimilarityReport:

    if not historical_assets:

        return VisualSimilarityReport(
            history_available=False,

            exact_duplicate_asset_ids=[],

            similar_assets=[],

            repeated_visual_patterns=[],

            meaningful_differences=[],

            novelty_gaps=[],

            revision_needed=False,

            history_note=(
                "No approved historical visual "
                "assets are available. Visual "
                "novelty was not assessed."
            ),
        )

    candidate_sha256 = sha256_file(
        candidate_visual.image_path
    )

    exact_duplicate_asset_ids = []

    matches = []

    for asset in historical_assets:

        if asset.id is None:

            continue

        if (
            candidate_sha256
            == asset.sha256
        ):

            exact_duplicate_asset_ids.append(
                asset.id
            )

            matches.append(
                build_exact_duplicate_match(
                    asset
                )
            )

            continue

        match = compare_visual_pair(
            candidate_visual=(
                candidate_visual
            ),
            current_strategy=(
                current_strategy
            ),
            current_visual_brief=(
                current_visual_brief
            ),
            historical_asset=asset,
        )

        if (
            match.overlap_level
            in {
                "medium",
                "high",
            }
            or match.same_visual_territory
        ):

            matches.append(
                match
            )

    repeated_patterns = (
        dedupe_strings(
            [
                pattern

                for match in matches

                for pattern in (
                    match
                    .shared_visual_patterns
                )
            ]
        )
    )

    meaningful_differences = (
        dedupe_strings(
            [
                difference

                for match in matches

                for difference in (
                    match
                    .meaningful_differences
                )
            ]
        )
    )

    novelty_gaps = (
        dedupe_strings(
            [
                gap

                for match in matches

                for gap in (
                    match.novelty_gaps
                )
            ]
        )
    )

    exact_duplicate_found = bool(
        exact_duplicate_asset_ids
    )

    high_semantic_repetition = any(
        (
            match.overlap_level == "high"
            and match.same_visual_territory
        )
        for match in matches
    )

    revision_needed = (
        exact_duplicate_found
        or high_semantic_repetition
    )

    history_note = (
        "Compared the candidate visual against "
        f"{len(historical_assets)} "
        "human-approved historical visual assets."
    )

    return VisualSimilarityReport(
        history_available=True,

        exact_duplicate_asset_ids=(
            exact_duplicate_asset_ids
        ),

        similar_assets=matches,

        repeated_visual_patterns=(
            repeated_patterns
        ),

        meaningful_differences=(
            meaningful_differences
        ),

        novelty_gaps=novelty_gaps,

        revision_needed=(
            revision_needed
        ),

        history_note=history_note,
    )
