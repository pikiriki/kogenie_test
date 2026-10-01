from pydantic import BaseModel


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
    deeper_desire: str
    awareness: str
    sophistication: str
    message_entry: str
    mechanism: str
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
