from pydantic import BaseModel


class CampaignBrief(BaseModel):
    product_description: str
    audience: str
    campaign_objective: str
    tone: str
    preferred_words: str
    avoided_words: str


class CopyDraft(BaseModel):
    headline: str
    body: str
    cta: str