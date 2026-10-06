import os

from functools import lru_cache

from pathlib import Path

from dotenv import load_dotenv

from pydantic import (
    BaseModel,
    ConfigDict,
)


load_dotenv()


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
)


def resolve_project_path(
    value: str,
) -> Path:

    path = Path(
        value
    ).expanduser()

    if path.is_absolute():
        return path

    return (
        PROJECT_ROOT
        / path
    ).resolve()


class AppConfig(BaseModel):

    model_config = ConfigDict(
        frozen=True
    )

    text_model: str

    vision_model: str

    image_model: str

    vector_store_id: str

    database_path: Path

    generated_visuals_path: Path

    approved_visuals_path: Path

    workflow_checkpoints_path: Path

    workflow_lease_seconds: int


@lru_cache(maxsize=1)
def get_config() -> AppConfig:

    text_model = os.getenv(
        "KOGENIE_TEXT_MODEL",
        "gpt-6-luna",
    ).strip()

    vision_model = os.getenv(
        "KOGENIE_VISION_MODEL",
        "gpt-6-astra",
    ).strip()

    image_model = os.getenv(
        "KOGENIE_IMAGE_MODEL",
        "gpt-image-2.5-flare",
    ).strip()

    vector_store_id = os.getenv(
        "OPENAI_VECTOR_STORE_ID",
        "",
    ).strip()

    # Existing project database file (see database.py history).
    database_path = resolve_project_path(
        os.getenv(
            "KOGENIE_DATABASE_PATH",
            "copy_studio.db",
        )
    )

    generated_visuals_path = (
        resolve_project_path(
            os.getenv(
                "KOGENIE_GENERATED_VISUALS_PATH",
                "generated_visuals",
            )
        )
    )

    approved_visuals_path = (
        resolve_project_path(
            os.getenv(
                "KOGENIE_APPROVED_VISUALS_PATH",
                "approved_visuals",
            )
        )
    )

    workflow_checkpoints_path = (
        resolve_project_path(
            os.getenv(
                "KOGENIE_WORKFLOW_CHECKPOINTS_PATH",
                "workflow_checkpoints",
            )
        )
    )

    workflow_lease_seconds = int(
        os.getenv(
            "KOGENIE_WORKFLOW_LEASE_SECONDS",
            "900",
        ).strip()
    )

    if workflow_lease_seconds <= 0:

        raise ValueError(
            (
                "KOGENIE_WORKFLOW_LEASE_SECONDS "
                "must be greater than zero."
            )
        )

    return AppConfig(
        text_model=text_model,

        vision_model=vision_model,

        image_model=image_model,

        vector_store_id=(
            vector_store_id
        ),

        database_path=(
            database_path
        ),

        generated_visuals_path=(
            generated_visuals_path
        ),

        approved_visuals_path=(
            approved_visuals_path
        ),

        workflow_checkpoints_path=(
            workflow_checkpoints_path
        ),

        workflow_lease_seconds=(
            workflow_lease_seconds
        ),
    )
