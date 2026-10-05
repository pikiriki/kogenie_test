from models import (
    AlternativeStrategyEvaluationSet,
    AlternativeStrategySet,
    CopyStrategyCard,
    StrategyApplicationResult,
    StrategySelection,
)


FIXED_STRATEGY_FIELDS = [
    "reader",
    "primary_problem",
    "deeper_desire",
    "awareness",
    "sophistication",
    "message_entry",
    "mechanism",
    "major_objections",
    "proof_boundary",
    "offer_boundary",
]


def apply_selected_strategy(
    current_strategy: CopyStrategyCard,
    strategy_set: AlternativeStrategySet,
    evaluation_set: AlternativeStrategyEvaluationSet,
    selection: StrategySelection,
    campaign_objective: str,
) -> StrategyApplicationResult:

    if selection.selection_status != "selected":

        raise ValueError(
            "No strategy was selected for application."
        )

    if selection.candidate_index is None:

        raise ValueError(
            "Selected strategy has no candidate index."
        )

    candidate_index = (
        selection.candidate_index
    )


    if candidate_index < 1:

        raise ValueError(
            "Candidate index must start at 1."
        )


    if candidate_index > len(
        strategy_set.strategies
    ):

        raise ValueError(
            "Selected candidate does not exist."
        )

    if (
        len(strategy_set.strategies)
        != len(evaluation_set.evaluations)
    ):

        raise ValueError(
            "Strategy and evaluation counts do not match."
        )

    candidate = strategy_set.strategies[
        candidate_index - 1
    ]


    evaluation = evaluation_set.evaluations[
        candidate_index - 1
    ]

    if (
        evaluation.strategy_index
        != candidate_index
    ):

        raise ValueError(
            "Evaluation does not match "
            "the selected candidate."
        )

    if evaluation.recommendation != "viable":

        raise ValueError(
            (
                f"Strategy {candidate_index} "
                "is no longer eligible for application. "
                f"Recommendation: "
                f"{evaluation.recommendation}"
            )
        )

    updated_strategy = (
        current_strategy.model_copy(
            deep=True
        )
    )

    updated_strategy.active_reader_tension = (
        candidate.reader_tension
    )

    updated_strategy.mechanism_emphasis = (
        candidate.mechanism_emphasis
    )

    updated_strategy.big_idea = (
        candidate.proposed_big_idea
    )

    updated_strategy.selected_angle = (
        candidate.proposed_angle
    )

    updated_strategy.final_message = ""

    applied_changes = [
        (
            "Changed active reader tension from: "
            f"{current_strategy.active_reader_tension} "
            "→ "
            f"{updated_strategy.active_reader_tension}"
        ),
        (
            "Changed mechanism emphasis from: "
            f"{current_strategy.mechanism_emphasis} "
            "→ "
            f"{updated_strategy.mechanism_emphasis}"
        ),
        (
            "Changed Big Idea from: "
            f"{current_strategy.big_idea} "
            "→ "
            f"{updated_strategy.big_idea}"
        ),
        (
            "Changed selected angle from: "
            f"{current_strategy.selected_angle} "
            "→ "
            f"{updated_strategy.selected_angle}"
        ),
        (
            "Invalidated the previous final message "
            "because it was written for the old strategy."
        ),
    ]

    preserved_constraints = [
        f"Reader: {current_strategy.reader}",
        (
            "Core problem: "
            + current_strategy.primary_problem
        ),
        (
            "Documented mechanism: "
            + current_strategy.mechanism
        ),
        (
            "Campaign objective: "
            + campaign_objective
        ),
    ]

    for boundary in (
        current_strategy.proof_boundary
    ):

        preserved_constraints.append(
            "Proof boundary: "
            + boundary
        )

    for boundary in (
        current_strategy.offer_boundary
    ):

        preserved_constraints.append(
            "Offer boundary: "
            + boundary
        )

    for field in FIXED_STRATEGY_FIELDS:

        old_value = getattr(
            current_strategy,
            field,
        )

        new_value = getattr(
            updated_strategy,
            field,
        )

        if old_value != new_value:

            raise RuntimeError(
                (
                    "Fixed strategy field changed "
                    f"unexpectedly: {field}"
                )
            )

    return StrategyApplicationResult(
        updated_strategy_card=updated_strategy,
        selected_strategy_index=(
            candidate_index
        ),
        applied_changes=applied_changes,
        preserved_constraints=(
            preserved_constraints
        ),
        human_reason=(
            selection.human_reason
        ),
    )
