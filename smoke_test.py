from pathlib import Path
from typing import Literal
from uuid import uuid4

from openai import OpenAI
from pydantic import BaseModel

from config import (
    get_config,
)

from database import (
    get_connection,
)

from external_health import (
    describe_openai_error,
)

from models import (
    SmokeTestReport,
)


CONFIG = get_config()


client = OpenAI(
    timeout=20.0,
    max_retries=0,
)


VECTOR_SMOKE_QUERY = (
    "KOgenie product capabilities"
)


class SmokeStructuredOutput(
    BaseModel
):
    status: Literal[
        "ok"
    ]

    component: Literal[
        "structured_output"
    ]


def smoke_database_round_trip(
    failures: list[str],
) -> bool:

    connection = None

    table_name = (
        "_kogenie_smoke_"
        + uuid4().hex
    )

    try:

        connection = get_connection()

        connection.execute(
            "BEGIN"
        )

        connection.execute(
            f"""
            CREATE TABLE {table_name} (
                value TEXT NOT NULL
            )
            """
        )

        expected_value = (
            "smoke-"
            + uuid4().hex
        )

        connection.execute(
            f"""
            INSERT INTO {table_name} (
                value
            )
            VALUES (?)
            """,
            (
                expected_value,
            ),
        )

        row = connection.execute(
            f"""
            SELECT value
            FROM {table_name}
            LIMIT 1
            """
        ).fetchone()

        if row is None:

            failures.append(
                (
                    "Database smoke test wrote "
                    "a record but could not "
                    "read it back."
                )
            )

            return False

        actual_value = row[0]

        if (
            actual_value
            != expected_value
        ):

            failures.append(
                (
                    "Database smoke-test "
                    "round-trip value mismatch."
                )
            )

            return False

        return True

    except Exception as error:

        failures.append(
            (
                "Database round-trip "
                "smoke test failed: "
                + type(error).__name__
            )
        )

        return False

    finally:

        if connection is not None:

            connection.rollback()

            connection.close()


def smoke_artifact_write_read(
    failures: list[str],
) -> bool:

    directories = [
        CONFIG.generated_visuals_path,
        CONFIG.approved_visuals_path,
    ]

    all_ok = True

    for directory in directories:

        test_path = None

        try:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            expected = (
                "kogenie-smoke-"
                + uuid4().hex
            )

            test_path = (
                directory
                / (
                    ".smoke_"
                    + uuid4().hex
                    + ".txt"
                )
            )

            test_path.write_text(
                expected,
                encoding="utf-8",
            )

            actual = (
                test_path.read_text(
                    encoding="utf-8"
                )
            )

            if actual != expected:

                all_ok = False

                failures.append(
                    (
                        "Artifact smoke test "
                        "read-back mismatch in: "
                        + str(directory)
                    )
                )

        except Exception as error:

            all_ok = False

            failures.append(
                (
                    "Artifact write/read "
                    "smoke test failed in "
                    f"'{directory}': "
                    + type(error).__name__
                )
            )

        finally:

            if (
                test_path is not None
                and test_path.exists()
            ):

                try:

                    test_path.unlink()

                except Exception:

                    pass

    return all_ok


def smoke_vector_retrieval(
    failures: list[str],
) -> bool:

    if not CONFIG.vector_store_id:

        failures.append(
            (
                "Vector retrieval smoke "
                "test cannot run because "
                "vector_store_id is missing."
            )
        )

        return False

    try:

        results = (
            client.vector_stores.search(
                vector_store_id=(
                    CONFIG.vector_store_id
                ),

                query=(
                    VECTOR_SMOKE_QUERY
                ),

                max_num_results=1,
            )
        )

        if not results.data:

            failures.append(
                (
                    "Vector search request succeeded, "
                    "but no knowledge chunk was "
                    "retrieved for the smoke query."
                )
            )

            return False

        first_result = (
            results.data[0]
        )

        if not first_result.file_id:

            failures.append(
                (
                    "Vector retrieval returned "
                    "a result without a file ID."
                )
            )

            return False

        return True

    except Exception as error:

        failures.append(
            (
                "Vector retrieval smoke "
                "test failed: "
                + describe_openai_error(
                    error
                )
            )
        )

        return False


def smoke_structured_output(
    failures: list[str],
) -> bool:

    try:

        response = (
            client.responses.parse(
                model=(
                    CONFIG.text_model
                ),

                input=[
                    {
                        "role": "system",
                        "content": (
                            "Return the required "
                            "structured smoke-test "
                            "object."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Confirm the structured "
                            "output integration works."
                        ),
                    },
                ],

                text_format=(
                    SmokeStructuredOutput
                ),
            )
        )

        parsed = (
            response.output_parsed
        )

        if parsed is None:

            failures.append(
                (
                    "Structured-output smoke "
                    "test returned no parsed object."
                )
            )

            return False

        if (
            parsed.status != "ok"
            or parsed.component
            != "structured_output"
        ):

            failures.append(
                (
                    "Structured-output smoke "
                    "test returned unexpected data."
                )
            )

            return False

        return True

    except Exception as error:

        failures.append(
            (
                "Structured-output smoke "
                "test failed: "
                + describe_openai_error(
                    error
                )
            )
        )

        return False


def run_application_smoke_test(
) -> SmokeTestReport:

    failures = []

    database_round_trip_ok = (
        smoke_database_round_trip(
            failures
        )
    )

    artifact_write_read_ok = (
        smoke_artifact_write_read(
            failures
        )
    )

    vector_retrieval_ok = (
        smoke_vector_retrieval(
            failures
        )
    )

    structured_output_ok = (
        smoke_structured_output(
            failures
        )
    )

    passed = all([
        database_round_trip_ok,
        vector_retrieval_ok,
        structured_output_ok,
        artifact_write_read_ok,
    ])

    return SmokeTestReport(
        database_round_trip_ok=(
            database_round_trip_ok
        ),

        vector_retrieval_ok=(
            vector_retrieval_ok
        ),

        structured_output_ok=(
            structured_output_ok
        ),

        artifact_write_read_ok=(
            artifact_write_read_ok
        ),

        failures=failures,

        passed=passed,
    )
