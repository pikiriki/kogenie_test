from typing import Literal

from pydantic import BaseModel, ConfigDict


class BrandProfile(BaseModel):
    name: str
    tone: str
    preferred_words: str = ""
    avoided_words: str = ""


class CampaignBrief(BaseModel):
    product_description: str
    audience: str
    campaign_objective: str
    tone: str
    preferred_words: str
    avoided_words: str
    approved_claims: list[str]


class CopyDraft(BaseModel):
    headline: str
    body: str
    cta: str


class CustomerEvidence(BaseModel):
    exact_quote: str
    source: str
    problem: str
    desired_outcome: str
    interpretation: str


class CustomerEvidenceReport(BaseModel):
    evidence: list[CustomerEvidence]


class CompetitorMessage(BaseModel):
    competitor: str
    observed_claim: str
    mechanism: str
    audience: str
    offer_or_cta: str
    source: str


class CompetitorMessageMap(BaseModel):
    messages: list[CompetitorMessage]


class ResearchDocument(BaseModel):
    product_facts: list[str]
    approved_claims: list[str]
    customer_evidence: list[CustomerEvidence]
    problems: list[str]
    desired_outcomes: list[str]
    competitor_messages: list[CompetitorMessage]
    evidence_gaps: list[str]
    unanswered_questions: list[str]


class ReaderProfile(BaseModel):
    who_they_are: str
    current_situation: str
    primary_problem: str
    desired_outcome: str


class DesireHypothesis(BaseModel):
    product_capability: str
    functional_benefit: str
    deeper_desire: str
    supporting_evidence: list[str]
    confidence: str


class DesireIntensity(BaseModel):
    level: str
    evidence: list[str]
    urgency_signals: list[str]
    uncertainty: str


class AwarenessHypothesis(BaseModel):
    level: str
    what_the_reader_knows: list[str]
    what_the_reader_does_not_yet_know: list[str]
    supporting_evidence: list[str]
    confidence: str


class MessageEntryPoint(BaseModel):
    starting_point: str
    why_this_start: str
    information_to_introduce_next: list[str]
    information_to_avoid_leading_with: list[str]


class SophisticationHypothesis(BaseModel):
    stage: str
    common_market_claims: list[str]
    signs_of_saturation: list[str]
    mechanism_presence: list[str]
    supporting_evidence: list[str]
    confidence: str


class MechanismHypothesis(BaseModel):
    desired_outcome: str
    product_capability: str
    causal_explanation: str
    supporting_evidence: list[str]
    unsupported_leaps: list[str]
    confidence: str


class ObjectionItem(BaseModel):
    objection: str
    objection_type: str
    supporting_evidence: list[str]
    what_answer_is_needed: str
    proof_required: list[str]
    confidence: str


class ObjectionMap(BaseModel):
    objections: list[ObjectionItem]


class OfferStrategy(BaseModel):
    core_product: str
    price: str
    bonuses: list[str]
    guarantee: str
    terms: list[str]
    urgency: str
    verified_elements: list[str]
    missing_elements: list[str]


class BigIdeaHypothesis(BaseModel):
    reader_problem: str
    deeper_desire: str
    mechanism: str
    central_thought: str
    promise_boundary: str
    supporting_evidence: list[str]
    confidence: str


class CreativeAngle(BaseModel):
    angle_name: str
    central_argument: str
    reader_hook: str
    mechanism_emphasis: str
    supporting_evidence: list[str]
    risk_of_repetition: str


class CreativeAngleSet(BaseModel):
    angles: list[CreativeAngle]


class HeadlineCandidate(BaseModel):
    headline: str
    attention_principle: str
    angle_connection: str
    evidence_check: str
    risk: str


class HeadlineCandidateSet(BaseModel):
    headlines: list[HeadlineCandidate]


class OpeningDraft(BaseModel):
    opening: str
    recognition_trigger: str
    transition_to_problem: str
    angle_connection: str
    evidence_check: str


class MechanismSectionDraft(BaseModel):
    problem_explanation: str
    mechanism_explanation: str
    reason_why: str
    bridge_to_product: str
    evidence_check: str


class ProofSectionDraft(BaseModel):
    proof_points: list[str]
    demonstration_plan: list[str]
    verified_claims_used: list[str]
    missing_proof: list[str]
    proof_copy: str


class ObjectionResponse(BaseModel):
    objection: str
    answer: str
    proof_used: list[str]
    status: str


class ObjectionSectionDraft(BaseModel):
    objection_responses: list[ObjectionResponse]
    unresolved_objections: list[str]
    risk_reversal_available: str
    objection_copy: str


class OfferSectionDraft(BaseModel):
    offer_copy: str
    terms_stated: list[str]
    urgency_used: str
    cta: str
    evidence_check: str


class CompleteSalesMessage(BaseModel):
    headline: str
    opening: str
    mechanism_section: str
    proof_section: str
    objection_section: str
    offer_section: str
    full_copy: str


class CopyStrategyCard(BaseModel):
    reader: str
    primary_problem: str

    active_reader_tension: str = ""

    deeper_desire: str
    awareness: str
    sophistication: str
    message_entry: str

    mechanism: str

    mechanism_emphasis: str = ""

    big_idea: str
    selected_angle: str

    major_objections: list[str]

    proof_boundary: list[str]
    offer_boundary: list[str]

    final_message: str


class ChannelSpec(BaseModel):
    channel: str
    placement: str
    objective: str
    length_constraint: str
    required_fields: list[str]
    formatting_rules: list[str]


class MetaFeedAdDraft(BaseModel):
    primary_text: str
    headline: str
    cta: str
    strategy_preserved: str
    evidence_check: str


class SearchAdDraft(BaseModel):
    headlines: list[str]
    descriptions: list[str]
    cta: str
    intent_connection: str
    strategy_preserved: str
    evidence_check: str


class EmailDraft(BaseModel):
    subject_lines: list[str]
    preview_text: str
    body: str
    cta: str
    strategy_preserved: str
    evidence_check: str


class LandingPageDraft(BaseModel):
    hero_headline: str
    hero_subheadline: str
    problem_section: str
    mechanism_section: str
    proof_section: str
    objection_section: str
    offer_section: str
    cta: str
    strategy_preserved: str
    evidence_check: str


class XDraft(BaseModel):
    hook: str
    posts: list[str]
    cta: str
    strategy_preserved: str
    evidence_check: str


class MetaFeedVariant(BaseModel):
    variant_name: str
    execution_choice: str
    primary_text: str
    headline: str
    cta: str
    strategy_preserved: str
    evidence_check: str


class ChannelVariantSet(BaseModel):
    channel: str
    variants: list[MetaFeedVariant]


class CampaignPack(BaseModel):
    strategy_card: CopyStrategyCard
    meta: MetaFeedAdDraft
    search: SearchAdDraft
    email: EmailDraft
    landing_page: LandingPageDraft
    x: XDraft


class ChannelReview(BaseModel):
    channel: str
    strategy_alignment: str
    drift_found: list[str]
    unsupported_claims: list[str]
    cta_conflict: str
    revision_needed: bool


class ChannelConsistencyReport(BaseModel):
    shared_strategy: str
    channel_findings: list[ChannelReview]
    strategy_drift: list[str]
    unsupported_claims: list[str]
    cta_conflicts: list[str]
    revision_needed: bool

class CampaignRepairResult(BaseModel):
    campaign_pack: CampaignPack
    repaired_channels: list[str]
    untouched_channels: list[str]


class CopyCritique(BaseModel):
    clarity_issues: list[str]
    specificity_issues: list[str]
    credibility_issues: list[str]
    flow_issues: list[str]
    repetition_issues: list[str]
    weak_sections: list[str]
    revision_instructions: list[str]
    sections_to_revise: list[str]


class RevisedSalesMessage(BaseModel):
    headline: str
    opening: str
    mechanism_section: str
    proof_section: str
    objection_section: str
    offer_section: str
    full_copy: str
    revised_sections: list[str]
    preserved_sections: list[str]


class ClaimReview(BaseModel):
    section: str
    claim: str
    support_status: str
    supporting_evidence: list[str]
    unsupported_part: str
    required_action: str


class ClaimEvidenceReport(BaseModel):
    claims: list[ClaimReview]
    unsupported_claims: list[str]
    revision_needed: bool


class ClaimRepairResult(BaseModel):
    section: str
    original_claim: str
    repaired_claim: str
    action_taken: str
    evidence_preserved: list[str]


class BrandVoiceReview(BaseModel):
    tone_alignment: str
    preferred_language_usage: list[str]
    avoided_language_violations: list[str]
    voice_drift: list[str]
    sections_to_revise: list[str]
    revision_instructions: list[str]


class UnifiedReviewReport(BaseModel):
    copy_issues: list[str]
    claim_issues: list[str]
    brand_voice_issues: list[str]
    channel_issues: list[str]
    sections_requiring_work: list[str]
    research_needed: list[str]
    ready_for_approval: bool


class RevisionPlan(BaseModel):
    research_tasks: list[str]
    evidence_repairs: list[str]
    brand_repairs: list[str]
    copy_repairs: list[str]
    channel_repairs: list[str]
    execution_order: list[str]


class RevisionOrchestrationResult(BaseModel):
    status: str
    actions_taken: list[str]
    research_blockers: list[str]

    complete_message: CompleteSalesMessage
    campaign_pack: CampaignPack

    copy_critique: CopyCritique
    claim_report: ClaimEvidenceReport
    brand_review: BrandVoiceReview
    channel_report: ChannelConsistencyReport

    unified_report: UnifiedReviewReport


class ApprovalRecord(BaseModel):
    id: int | None = None
    campaign_id: int
    status: str
    reviewer: str
    note: str
    approved_message_snapshot: str
    approved_at: str | None = None


class CampaignMemory(BaseModel):
    campaign_id: int
    approved_angle: str
    approved_big_idea: str
    approved_message: str
    evidence_boundaries: list[str]
    outcome_context: str


class SimilarCampaignMatch(BaseModel):
    campaign_id: int
    overlap_level: str
    similarity_reason: str
    shared_elements: list[str]
    meaningful_differences: list[str]


class RepetitionReport(BaseModel):
    proposed_big_idea: str
    proposed_angle: str
    similar_campaigns: list[SimilarCampaignMatch]
    repeated_patterns: list[str]
    novelty_gaps: list[str]
    revision_needed: bool


class NoveltyGuidance(BaseModel):
    what_must_stay_fixed: list[str]
    overused_patterns: list[str]
    unexplored_reader_tensions: list[str]
    unexplored_mechanism_emphases: list[str]
    forbidden_shortcuts: list[str]
    strategy_guidance: list[str]


class AlternativeStrategy(BaseModel):
    reader_tension: str
    mechanism_emphasis: str
    proposed_big_idea: str
    proposed_angle: str
    evidence_used: list[str]
    evidence_boundary: list[str]
    historical_difference: str


class AlternativeStrategySet(BaseModel):
    strategies: list[AlternativeStrategy]


class AlternativeStrategyEvaluation(BaseModel):
    strategy_index: int
    research_grounding: str
    historical_distinctness: str
    mechanism_fit: str
    evidence_safety: str
    reader_relevance: str
    weaknesses: list[str]
    recommendation: str


class AlternativeStrategyEvaluationSet(BaseModel):
    evaluations: list[AlternativeStrategyEvaluation]


class StrategySelection(BaseModel):
    candidate_index: int | None
    evaluation_summary: str
    selection_status: str
    human_reason: str
    selected_at: str | None


class StrategyApplicationResult(BaseModel):
    updated_strategy_card: CopyStrategyCard
    selected_strategy_index: int
    applied_changes: list[str]
    preserved_constraints: list[str]
    human_reason: str


class StrategyRegenerationResult(BaseModel):
    updated_strategy_card: CopyStrategyCard
    complete_message: CompleteSalesMessage
    invalidated_artifacts: list[str]
    regeneration_reason: str


class CampaignRefreshResult(BaseModel):
    status: str

    campaign_pack: CampaignPack | None = None

    channel_report: ChannelConsistencyReport | None = None

    repaired_channels: list[str] = []


class VisualCreativeBrief(BaseModel):
    visual_job: str
    subject: str
    scene: str
    composition: str
    text_hierarchy: list[str]
    product_role: str
    visual_proof: str
    avoid: list[str]
    copy_connection: str


class VisualStyleSpec(BaseModel):
    aesthetic_direction: str
    palette_direction: str
    typography_direction: str
    imagery_style: str
    spacing_density: str
    shape_language: str
    brand_consistency_rules: list[str]
    prohibited_styles: list[str]


class VisualGenerationSpec(BaseModel):
    objective: str

    width: int
    height: int
    canvas: str

    required_elements: list[str]
    text_to_render: list[str]

    composition: str
    style: str

    evidence_constraints: list[str]
    negative_constraints: list[str]

    generation_instruction: str


class GeneratedVisual(BaseModel):
    campaign_id: int

    image_path: str
    metadata_path: str

    generation_spec_snapshot: str

    channel: str
    model: str

    created_at: str

    approval_status: str

    source_image_path: str | None = None
    repair_plan_snapshot: str | None = None


class VisualReviewReport(BaseModel):
    objective_alignment: Literal[
        "aligned",
        "partially aligned",
        "misaligned",
    ]

    required_elements_present: list[str]

    missing_elements: list[str]

    text_accuracy: Literal[
        "accurate",
        "partially accurate",
        "inaccurate",
        "unreadable",
    ]

    composition_alignment: Literal[
        "aligned",
        "partially aligned",
        "misaligned",
    ]

    style_alignment: Literal[
        "aligned",
        "partially aligned",
        "misaligned",
    ]

    evidence_violations: list[str]

    negative_constraint_violations: list[str]

    revision_needed: bool


class VisualRepairPlan(BaseModel):
    preserve: list[str]
    fix: list[str]
    evidence_constraints: list[str]
    repair_instruction: str


class VisualApprovalRecord(BaseModel):
    id: int | None = None

    campaign_id: int

    visual_path: str
    visual_sha256: str

    generation_spec_snapshot: str
    visual_review_snapshot: str

    status: Literal[
        "awaiting human approval",
        "approved",
        "rejected",
    ]

    reviewer: str | None = None
    note: str = ""

    approved_visual_snapshot_path: str | None = None
    approved_visual_sha256: str | None = None

    created_at: str | None = None
    decided_at: str | None = None


class VisualAsset(BaseModel):
    id: int | None = None

    campaign_id: int

    visual_path: str
    approved_snapshot_path: str

    sha256: str

    channel: str

    strategy_angle: str
    visual_job: str

    created_at: str

    approval_record_id: int

    usage_status: Literal[
        "available",
        "in_use",
        "retired",
    ]


class VisualSimilarityMatch(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    asset_id: int

    overlap_level: Literal[
        "low",
        "medium",
        "high",
    ]

    same_visual_territory: bool

    similarity_reason: str

    shared_visual_patterns: list[str]

    meaningful_differences: list[str]

    novelty_gaps: list[str]


class VisualSimilarityReport(BaseModel):
    history_available: bool

    exact_duplicate_asset_ids: list[int]

    similar_assets: list[
        VisualSimilarityMatch
    ]

    repeated_visual_patterns: list[str]

    meaningful_differences: list[str]

    novelty_gaps: list[str]

    revision_needed: bool

    history_note: str
