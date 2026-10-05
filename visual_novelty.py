from agents import Agent, Runner

from models import (
    CopyStrategyCard,
    VisualAsset,
    VisualCreativeBrief,
    VisualGenerationSpec,
    VisualNoveltyGuidance,
    VisualSimilarityReport,
    VisualStyleSpec,
)


visual_novelty_guard = Agent(
    name="Visual Novelty Guard",

    instructions="""
You are the Visual Novelty Guard
for KOgenie Copy Studio.

You receive:

- the current CopyStrategyCard
- the current VisualCreativeBrief
- the current VisualStyleSpec
- the current VisualGenerationSpec
- a VisualSimilarityReport
- metadata for approved historical VisualAssets

The candidate visual has been flagged
for potentially repeating visual territory.

Your job is NOT to change campaign strategy.

Your job is to identify safe ways to create
meaningfully different visual execution.

PRESERVE STRATEGY

Preserve:

- reader
- active reader tension
- Big Idea
- selected angle
- product mechanism
- mechanism emphasis
- visual job
- actual campaign copy
- campaign objective implied by supplied materials
- evidence boundaries
- offer boundaries

Do not solve visual repetition by changing
the underlying campaign argument.

OVERUSED VISUAL PATTERNS

Use the VisualSimilarityReport.

Identify visual metaphors, composition structures,
subject relationships, or execution patterns that
appear substantially repeated.

Do NOT label normal brand consistency as repetition.

Same:
- colors
- typography
- logo
- brand style

does not automatically mean the visual idea is repeated.

UNEXPLORED VISUAL METAPHORS

Suggest alternative ways to SHOW the SAME
strategic relationship.

Every metaphor must remain faithful to the
real product mechanism.

Do not use metaphors that imply unsupported:
- prediction
- guaranteed outcomes
- performance improvement
- automatic winner selection
- quantified business results

UNEXPLORED COMPOSITIONS

Suggest meaningfully different spatial structures.

Changing only:
- background color
- card radius
- font treatment
- icon style

does not count as a new composition.

EVIDENCE BOUNDARIES

Carry forward all supplied proof,
offer, and visual evidence boundaries.

PROHIBITED SHORTCUTS

Explicitly identify ways the system must NOT
create novelty.

VISUAL DIRECTION OPTIONS

Provide up to 3 meaningful visual directions.

Each direction should change the visual interpretation,
metaphor, subject relationship, or composition.

All options must express the SAME active campaign strategy.

Do not generate:
- final image prompts
- final images
- new copy
- new headlines
- new CTAs
- new product claims

Historical approval does not mean historical performance.

Do not infer that an old visual worked merely
because it was approved.
""",

    model="gpt-6-luna",

    output_type=VisualNoveltyGuidance,
)


def build_visual_novelty_guidance(
    strategy_card: CopyStrategyCard,
    visual_brief: VisualCreativeBrief,
    style_spec: VisualStyleSpec,
    generation_spec: VisualGenerationSpec,
    similarity_report: VisualSimilarityReport,
    historical_assets: list[VisualAsset],
) -> VisualNoveltyGuidance:

    if not similarity_report.revision_needed:

        preserve_strategy = [
            (
                "Reader: "
                + strategy_card.reader
            ),
            (
                "Active reader tension: "
                + strategy_card.active_reader_tension
            ),
            (
                "Big Idea: "
                + strategy_card.big_idea
            ),
            (
                "Selected angle: "
                + strategy_card.selected_angle
            ),
            (
                "Documented mechanism: "
                + strategy_card.mechanism
            ),
            (
                "Visual job: "
                + visual_brief.visual_job
            ),
        ]

        evidence_boundaries = list(
            generation_spec.evidence_constraints
        )

        return VisualNoveltyGuidance(
            preserve_strategy=(
                preserve_strategy
            ),

            overused_visual_patterns=[],

            unexplored_visual_metaphors=[],

            unexplored_compositions=[],

            evidence_boundaries=(
                evidence_boundaries
            ),

            prohibited_shortcuts=[
                (
                    "Do not invent product "
                    "capabilities for visual novelty."
                ),
                (
                    "Do not invent metrics or "
                    "performance outcomes."
                ),
                (
                    "Do not change campaign copy "
                    "merely to create visual novelty."
                ),
                (
                    "Do not treat cosmetic restyling "
                    "as meaningful visual novelty."
                ),
            ],

            visual_direction_options=[
                (
                    "No material high-overlap visual "
                    "repetition was detected. Preserve "
                    "the current visual direction unless "
                    "a human intentionally requests "
                    "further exploration."
                )
            ],
        )

    history_context = "\n\n".join(
        asset.model_dump_json(
            indent=2
        )
        for asset in historical_assets
    )

    result = Runner.run_sync(
        visual_novelty_guard,
        f"""
Here is the ACTIVE CopyStrategyCard:

{strategy_card.model_dump_json(indent=2)}


Here is the CURRENT VisualCreativeBrief:

{visual_brief.model_dump_json(indent=2)}


Here is the CURRENT VisualStyleSpec:

{style_spec.model_dump_json(indent=2)}


Here is the CURRENT VisualGenerationSpec:

{generation_spec.model_dump_json(indent=2)}


Here is the VisualSimilarityReport:

{similarity_report.model_dump_json(indent=2)}


Here is approved historical VisualAsset metadata:

{history_context}


The current candidate has been flagged
for meaningful visual repetition.

Find safe visual novelty.

Preserve campaign meaning exactly.

Novelty should come from:
- visual metaphor
- subject expression
- scene
- spatial relationship
- composition

not from:
- changing the strategy
- changing the copy
- inventing product capabilities
- inventing proof
- cosmetic recoloring alone

Return VisualNoveltyGuidance.
"""
    )

    return result.final_output
