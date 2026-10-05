import os

from dotenv import load_dotenv

from config import (
    get_config,
)

from database import (
    get_connection,
    initialize_database,
)

from models import (
    RuntimeHealth,
)


load_dotenv()


CONFIG = get_config()


REQUIRED_ENVIRONMENT_VARIABLES = [
    "OPENAI_API_KEY",
]


REQUIRED_DATABASE_TABLES = {
    "campaigns",
    "draft_versions",
    "brand_profiles",
    "approved_claims",
    "approval_records",
    "campaign_memories",
    "visual_approval_records",
    "visual_assets",
    "campaign_outcomes",
}


RUNTIME_DIRECTORIES = [
    CONFIG.generated_visuals_path,
    CONFIG.approved_visuals_path,
    CONFIG.workflow_checkpoints_path,
]


def check_environment() -> tuple[
    bool,
    list[str],
]:

    problems = []

    for variable_name in (
        REQUIRED_ENVIRONMENT_VARIABLES
    ):

        value = os.getenv(
            variable_name,
            "",
        ).strip()

        if not value:

            problems.append(
                (
                    "Missing environment variable: "
                    + variable_name
                )
            )

    if not CONFIG.vector_store_id:

        problems.append(
            (
                "Missing configuration: "
                "OPENAI_VECTOR_STORE_ID"
            )
        )

    return (
        len(problems) == 0,
        problems,
    )


def check_database() -> tuple[
    bool,
    list[str],
]:

    problems = []

    try:

        initialize_database()

    except Exception as error:

        return (
            False,
            [
                (
                    "Database initialization failed: "
                    + str(error)
                )
            ],
        )

    connection = None

    try:

        connection = get_connection()

        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

        existing_tables = {
            row[0]
            for row in rows
        }

        missing_tables = (
            REQUIRED_DATABASE_TABLES
            - existing_tables
        )

        for table_name in sorted(
            missing_tables
        ):

            problems.append(
                (
                    "Missing database table: "
                    + table_name
                )
            )

    except Exception as error:

        problems.append(
            (
                "Database health check failed: "
                + str(error)
            )
        )

    finally:

        if connection is not None:
            connection.close()

    return (
        len(problems) == 0,
        problems,
    )


def check_storage() -> tuple[
    bool,
    list[str],
]:

    problems = []

    for directory in (
        RUNTIME_DIRECTORIES
    ):

        try:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            sentinel = (
                directory
                / ".kogenie_runtime_health"
            )

            sentinel.write_text(
                "runtime-health-ok",
                encoding="utf-8",
            )

            sentinel.unlink()

        except Exception as error:

            problems.append(
                (
                    "Cannot use runtime directory "
                    f"'{directory}': "
                    f"{error}"
                )
            )

    return (
        len(problems) == 0,
        problems,
    )


def check_model_configuration() -> tuple[
    bool,
    list[str],
]:

    problems = []

    configured_models = {
        "text": CONFIG.text_model,
        "vision": CONFIG.vision_model,
        "image": CONFIG.image_model,
    }

    for role, model_name in (
        configured_models.items()
    ):

        if not isinstance(
            model_name,
            str,
        ):

            problems.append(
                (
                    f"{role} model configuration "
                    "is not a string."
                )
            )

            continue

        if not model_name.strip():

            problems.append(
                (
                    f"{role} model configuration "
                    "is empty."
                )
            )

    return (
        len(problems) == 0,
        problems,
    )


def check_runtime_health() -> RuntimeHealth:

    (
        environment_ok,
        environment_problems,
    ) = check_environment()

    (
        database_ok,
        database_problems,
    ) = check_database()

    (
        storage_ok,
        storage_problems,
    ) = check_storage()

    (
        model_configuration_ok,
        model_problems,
    ) = check_model_configuration()

    missing_requirements = (
        environment_problems
        + database_problems
        + storage_problems
        + model_problems
    )

    ready = (
        environment_ok
        and database_ok
        and storage_ok
        and model_configuration_ok
    )

    return RuntimeHealth(
        environment_ok=(
            environment_ok
        ),

        database_ok=(
            database_ok
        ),

        storage_ok=(
            storage_ok
        ),

        model_configuration_ok=(
            model_configuration_ok
        ),

        missing_requirements=(
            missing_requirements
        ),

        ready=ready,
    )
