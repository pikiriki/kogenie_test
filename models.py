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