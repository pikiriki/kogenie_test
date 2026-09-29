import json

from database import get_approved_claims


def get_approved_brand_claims(brand_profile_id):
    claim_rows = get_approved_claims(
        brand_profile_id
    )

    verified_claims = []

    for claim in claim_rows:
        if claim["verification_status"] == "verified":
            verified_claims.append(
                {
                    "claim_text": claim["claim_text"],
                    "evidence_note": claim["evidence_note"],
                    "source_reference": claim["source_reference"],
                }
            )

    return json.dumps(
        verified_claims,
        indent=2
    )


APPROVED_CLAIMS_TOOL = {
    "type": "function",
    "name": "get_approved_brand_claims",
    "description": (
        "Retrieve verified factual claims, evidence notes, "
        "and source references for a saved brand profile."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "brand_profile_id": {
                "type": "integer",
                "description": (
                    "The database ID of the saved brand profile."
                ),
            }
        },
        "required": [
            "brand_profile_id"
        ],
        "additionalProperties": False,
    },
    "strict": True,
}
