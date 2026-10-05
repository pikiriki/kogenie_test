from agents import Agent, Runner

from models import (
    CreativeEvidenceLedger,
    CreativeLearning,
    NextTestPlan,
)


def dedupe_strings(
    items: list[str],
) -> list[str]:

    result = []

    seen = set()

    for item in items:

        cleaned = item.strip()

        if not cleaned:
            continue

        if cleaned in seen:
            continue

        seen.add(cleaned)
        result.append(cleaned)

    return result


next_test_planner_agent = Agent(
    name="Next Test Planner",

    instructions="""
You are the Next Test Planner
for KOgenie Copy Studio.

You receive:

- one CreativeEvidenceLedger
- one CreativeLearning
- a human-supplied control description
- a campaign objective

Your job is to convert uncertain historical learning
into a disciplined next test.

You are planning a test.
You are NOT reporting that the test happened.

HYPOTHESIS

Create one falsifiable directional hypothesis.

The hypothesis must preserve:
- the ledger creative key
- the ledger primary metric
- the ledger desired direction
- the measurement context

Do not claim the hypothesis is already true.

CONTROL

Use the human-supplied control.
Do not replace or invent another control.

TREATMENT

The treatment should test the creative idea represented
by CreativeLearning / CreativeEvidenceLedger.

VARIABLE TO CHANGE

Change one primary creative variable.

For an angle-level ledger, the primary variable
is the creative angle.

Necessary copy and visual changes may express the angle,
but do not deliberately change unrelated strategic variables.

VARIABLES TO HOLD STABLE

Identify important variables that should remain
as stable as practical, such as:

- campaign objective
- audience
- offer
- landing destination
- channel
- conversion definition
- attribution model
- budget/bidding approach
- placement logic
- measurement window

Do not pretend perfect control is always possible.

MEASUREMENT

Use the ledger's primary metric.

Do not switch the primary success metric after
seeing the outcome.

EVIDENCE NEEDED

Specify what data should be captured so the test
can later be audited and interpreted.

DECISION RULE

Do not invent:
- statistical significance thresholds
- p-values
- sample sizes
- confidence intervals
- minimum detectable effects

unless those values are explicitly supplied.

Use a cautious directional decision rule.

CAUSALITY

A planned controlled test may provide stronger evidence
than uncontrolled historical observation.

But do not state that causality has been established
before the test is run and its validity is checked.

Do not write campaign copy.
Do not redesign the campaign.
""",

    model="gpt-6-luna",

    output_type=NextTestPlan,
)


def build_next_test_plan(
    ledger: CreativeEvidenceLedger,
    learning: CreativeLearning,
    control_description: str,
    campaign_objective: str,
) -> NextTestPlan:

    if (
        learning.creative_key
        != ledger.creative_key
    ):

        raise ValueError(
            (
                "CreativeLearning and "
                "CreativeEvidenceLedger "
                "refer to different creative keys."
            )
        )

    control_description = (
        control_description.strip()
    )


    if not control_description:

        raise ValueError(
            (
                "A human-supplied control "
                "description is required."
            )
        )

    campaign_objective = (
        campaign_objective.strip()
    )


    if not campaign_objective:

        raise ValueError(
            "Campaign objective cannot be empty."
        )

    result = Runner.run_sync(
        next_test_planner_agent,
        f"""
Here is the CreativeEvidenceLedger:

{ledger.model_dump_json(indent=2)}


Here is the CreativeLearning:

{learning.model_dump_json(indent=2)}


Human-supplied control:

{control_description}


Campaign objective:

{campaign_objective}


Design one next test.

The purpose is to generate stronger evidence
about the creative hypothesis.

Do not treat historical association as causal proof.

Do not invent sample sizes or statistical thresholds.
"""
    )

    candidate = result.final_output

    metric = ledger.metric_name

    treatment = (
        "Test the creative hypothesis: "
        + learning.creative_key
    )

    variable_to_change = (
        "Primary creative angle represented "
        f"by {learning.creative_key}."
    )

    mandatory_stable = [
        (
            "Campaign objective: "
            + campaign_objective
        ),
        (
            "Channel: "
            + ledger.channel
        ),
        (
            "Conversion definition: "
            + ledger.conversion_definition
        ),
        (
            "Attribution context: "
            + ledger.attribution_context
        ),
        (
            "Audience targeting or eligibility "
            "should remain the same between "
            "control and treatment."
        ),
        (
            "Offer and landing destination "
            "should remain the same."
        ),
        (
            "Budget, bidding, and optimization "
            "settings should remain as comparable "
            "as practical."
        ),
        (
            "Measurement-window timing and duration "
            "should be the same for both variants."
        ),
        (
            "Avoid unrelated strategic changes. "
            "Copy and visual differences should "
            "exist only as needed to express the "
            "tested creative angle."
        ),
    ]

    variables_to_hold_stable = (
        dedupe_strings(
            mandatory_stable
            + candidate.variables_to_hold_stable
        )
    )

    measurement_context = (
        f"Campaign objective: {campaign_objective}. "
        f"Channel: {ledger.channel}. "
        f"Conversion definition: "
        f"{ledger.conversion_definition}. "
        f"Attribution context: "
        f"{ledger.attribution_context}. "
        f"Primary metric: {ledger.metric_name}. "
        f"Desired metric direction: "
        f"{ledger.desired_direction}. "
        "Control and treatment should use the "
        "same measurement definitions and window."
    )

    mandatory_evidence = [
        (
            "Record a stable identifier for "
            "the control variant."
        ),
        (
            "Record a stable identifier for "
            "the treatment variant."
        ),
        (
            "Record the traffic-allocation or "
            "randomization method used."
        ),
        (
            "Capture impressions separately "
            "for control and treatment."
        ),
        (
            "Capture clicks separately "
            "for control and treatment."
        ),
        (
            "Capture conversions separately "
            "for control and treatment."
        ),
        (
            "Capture spend separately "
            "for control and treatment."
        ),
        (
            "Capture revenue separately when "
            "ROAS is the metric being evaluated."
        ),
        (
            "Record exact measurement start "
            "and end times."
        ),
        (
            "Record any material audience, placement, "
            "budget, bidding, offer, or landing-page "
            "changes during the test."
        ),
    ]

    evidence_needed = (
        dedupe_strings(
            mandatory_evidence
            + candidate.evidence_needed
        )
    )

    desired_direction = (
        ledger.desired_direction
    )

    decision_rule = (
        "After the pre-specified measurement window, "
        f"compare treatment versus control on "
        f"the primary metric '{metric}' using the "
        "same measurement definitions. "
        f"Record the result as directionally "
        f"supportive if treatment {metric} is "
        f"{desired_direction} than control, "
        "contradictory if it moves in the opposite "
        "direction, and neutral/inconclusive if the "
        "metric is equal or unavailable. "
        "This directional rule is not a statistical "
        "significance test and does not by itself "
        "establish causal effect."
    )

    causal_boundary = [
        (
            "This object is an experiment plan, "
            "not evidence that the treatment "
            "improves performance."
        ),
        (
            "Historical CreativeLearning remains "
            "observational evidence and is only the "
            "reason this hypothesis is worth testing."
        ),
        (
            "A controlled comparison provides stronger "
            "evidence only if control and treatment "
            "receive sufficiently comparable conditions."
        ),
        (
            "If audience, offer, budget, placement, "
            "landing experience, attribution, or other "
            "important conditions change materially, "
            "causal interpretation becomes weaker."
        ),
        (
            "The current decision rule is directional "
            "and is not a statistical significance test."
        ),
        (
            "No sample size, power calculation, "
            "confidence interval, or minimum detectable "
            "effect has been specified in this lesson."
        ),
        (
            "One completed test should not be "
            "generalized into a universal creative law."
        ),
    ]

    hypothesis = (
        candidate.hypothesis.strip()
    )

    if not hypothesis:

        raise RuntimeError(
            "Next Test Planner returned "
            "an empty hypothesis."
        )

    return NextTestPlan(
        hypothesis=hypothesis,

        metric=metric,

        control=(
            control_description
        ),

        treatment=treatment,

        variable_to_change=(
            variable_to_change
        ),

        variables_to_hold_stable=(
            variables_to_hold_stable
        ),

        measurement_context=(
            measurement_context
        ),

        evidence_needed=(
            evidence_needed
        ),

        decision_rule=(
            decision_rule
        ),

        causal_boundary=(
            causal_boundary
        ),
    )
