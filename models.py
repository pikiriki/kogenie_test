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