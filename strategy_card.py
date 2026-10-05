from models import (
    AwarenessHypothesis,
    BigIdeaHypothesis,
    CompleteSalesMessage,
    CopyStrategyCard,
    CreativeAngle,
    DesireHypothesis,
    MessageEntryPoint,
    ObjectionMap,
    OfferStrategy,
    ProofSectionDraft,
    ReaderProfile,
    SophisticationHypothesis,
    MechanismHypothesis,
)


def build_copy_strategy_card(
    reader_profile: ReaderProfile,
    desire_hypothesis: DesireHypothesis,
    awareness_hypothesis: AwarenessHypothesis,
    sophistication_hypothesis: SophisticationHypothesis,
    message_entry_point: MessageEntryPoint,
    mechanism_hypothesis: MechanismHypothesis,
    big_idea: BigIdeaHypothesis,
    selected_angle: CreativeAngle,
    objection_map: ObjectionMap,
    proof_section: ProofSectionDraft,
    offer_strategy: OfferStrategy,
    complete_message: CompleteSalesMessage,
) -> CopyStrategyCard:

    major_objections = [
        item.objection
        for item in objection_map.objections
    ]

    selected_angle_summary = (
        f"{selected_angle.angle_name}: "
        f"{selected_angle.central_argument}"
    )

    return CopyStrategyCard(
        reader=reader_profile.who_they_are,
        primary_problem=reader_profile.primary_problem,
        active_reader_tension=(
            reader_profile.primary_problem
        ),
        deeper_desire=desire_hypothesis.deeper_desire,
        awareness=awareness_hypothesis.level,
        sophistication=sophistication_hypothesis.stage,
        message_entry=message_entry_point.starting_point,
        mechanism=mechanism_hypothesis.causal_explanation,
        mechanism_emphasis=(
            mechanism_hypothesis.causal_explanation
        ),
        big_idea=big_idea.central_thought,
        selected_angle=selected_angle_summary,
        major_objections=major_objections,
        proof_boundary=proof_section.missing_proof,
        offer_boundary=offer_strategy.missing_elements,
        final_message=complete_message.full_copy,
    )
