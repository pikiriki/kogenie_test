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