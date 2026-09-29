import json


def create_campaign_export(
    campaign_id,
    brief,
    working_copy,
    versions
):
    export_data = {
        "campaign_id": campaign_id,
        "campaign_brief": brief.model_dump(),
        "current_working_copy": working_copy.model_dump(),
        "version_history": [
            dict(version)
            for version in versions
        ]
    }

    return json.dumps(
        export_data,
        indent=2
    )
