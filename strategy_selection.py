from datetime import datetime, timezone

from models import (
    AlternativeStrategyEvaluationSet,
    AlternativeStrategySet,
    StrategySelection,
)


def get_viable_candidate_indices(
    evaluation_set: AlternativeStrategyEvaluationSet,
) -> list[int]:

    viable_indices = []

    for evaluation in evaluation_set.evaluations:

        if evaluation.recommendation == "viable":

            viable_indices.append(
                evaluation.strategy_index
            )

    return viable_indices


def build_evaluation_summary(
    evaluation,
) -> str:

    return (
        f"research={evaluation.research_grounding}; "
        f"history={evaluation.historical_distinctness}; "
        f"mechanism={evaluation.mechanism_fit}; "
        f"evidence={evaluation.evidence_safety}; "
        f"reader={evaluation.reader_relevance}; "
        f"recommendation={evaluation.recommendation}"
    )


def create_strategy_selection(
    strategy_set: AlternativeStrategySet,
    evaluation_set: AlternativeStrategyEvaluationSet,
    candidate_index: int | None,
    human_reason: str,
) -> StrategySelection:

    if (
        len(strategy_set.strategies)
        != len(evaluation_set.evaluations)
    ):
        raise ValueError(
            "Strategy and evaluation counts do not match."
        )

    if candidate_index is None:

        reason = human_reason.strip()

        if not reason:
            reason = (
                "Human declined all available "
                "strategy candidates."
            )

        return StrategySelection(
            candidate_index=None,
            evaluation_summary=(
                "No strategy candidate selected."
            ),
            selection_status="declined",
            human_reason=reason,
            selected_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

    if candidate_index < 1:

        raise ValueError(
            "Candidate index must start at 1."
        )

    if candidate_index > len(
        strategy_set.strategies
    ):

        raise ValueError(
            "Candidate index does not exist."
        )

    evaluation = (
        evaluation_set.evaluations[
            candidate_index - 1
        ]
    )

    if (
        evaluation.strategy_index
        != candidate_index
    ):

        raise ValueError(
            "Evaluation index does not match "
            "the selected strategy."
        )

    if evaluation.recommendation != "viable":

        raise ValueError(
            (
                f"Strategy {candidate_index} "
                "is not eligible for selection. "
                f"Recommendation: "
                f"{evaluation.recommendation}"
            )
        )

    reason = human_reason.strip()


    if not reason:

        raise ValueError(
            "Please provide a reason for "
            "selecting this strategy."
        )

    return StrategySelection(
        candidate_index=candidate_index,
        evaluation_summary=(
            build_evaluation_summary(
                evaluation
            )
        ),
        selection_status="selected",
        human_reason=reason,
        selected_at=datetime.now(
            timezone.utc
        ).isoformat(),
    )
