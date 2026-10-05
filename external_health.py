from datetime import (
    datetime,
    timezone,
)

import openai

from openai import OpenAI

from config import (
    get_config,
)

from models import (
    ExternalServiceHealth,
)


CONFIG = get_config()


client = OpenAI(
    timeout=10.0,
    max_retries=0,
)


def describe_openai_error(
    error: Exception,
) -> str:

    if isinstance(
        error,
        openai.AuthenticationError,
    ):

        return (
            "Authentication failed. "
            "Check OPENAI_API_KEY."
        )

    if isinstance(
        error,
        openai.PermissionDeniedError,
    ):

        return (
            "Permission denied for the "
            "requested OpenAI resource."
        )

    if isinstance(
        error,
        openai.NotFoundError,
    ):

        return (
            "The requested OpenAI resource "
            "was not found."
        )

    if isinstance(
        error,
        openai.APITimeoutError,
    ):

        return (
            "The OpenAI request timed out."
        )

    if isinstance(
        error,
        openai.APIConnectionError,
    ):

        return (
            "Could not connect to the "
            "OpenAI API."
        )

    if isinstance(
        error,
        openai.RateLimitError,
    ):

        return (
            "The OpenAI API rate limit "
            "was reached."
        )

    if isinstance(
        error,
        openai.APIStatusError,
    ):

        return (
            "OpenAI API returned "
            f"HTTP {error.status_code}."
        )

    return (
        "Unexpected probe failure: "
        + type(error).__name__
    )


def probe_openai_api(
    failures: list[str],
) -> bool:

    try:

        client.models.list()

        return True

    except Exception as error:

        failures.append(
            (
                "OpenAI API probe failed: "
                + describe_openai_error(
                    error
                )
            )
        )

        return False


def probe_model_access(
    model_name: str,
    role: str,
    failures: list[str],
    warnings: list[str],
) -> bool:

    try:

        model = client.models.retrieve(
            model_name
        )

        if model.id != model_name:

            failures.append(
                (
                    f"{role} model probe returned "
                    "an unexpected model ID."
                )
            )

            return False

        shutdown_date = getattr(
            model,
            "shutdown_date",
            None,
        )

        if shutdown_date:

            warnings.append(
                (
                    f"{role} model "
                    f"'{model_name}' has an "
                    f"announced shutdown date: "
                    f"{shutdown_date}."
                )
            )

        return True

    except Exception as error:

        failures.append(
            (
                f"{role} model "
                f"'{model_name}' probe failed: "
                + describe_openai_error(
                    error
                )
            )
        )

        return False


def probe_vector_store(
    failures: list[str],
    warnings: list[str],
) -> bool:

    vector_store_id = (
        CONFIG.vector_store_id
    )

    if not vector_store_id:

        failures.append(
            (
                "Vector store probe failed: "
                "OPENAI_VECTOR_STORE_ID "
                "is not configured."
            )
        )

        return False

    try:

        vector_store = (
            client.vector_stores.retrieve(
                vector_store_id
            )
        )

        if (
            vector_store.status
            != "completed"
        ):

            failures.append(
                (
                    "Vector store exists but "
                    "is not ready. "
                    f"Status: "
                    f"{vector_store.status}."
                )
            )

            return False

        failed_files = (
            vector_store
            .file_counts
            .failed
        )

        if failed_files > 0:

            warnings.append(
                (
                    "Vector store is completed, "
                    f"but {failed_files} file(s) "
                    "are marked failed."
                )
            )

        return True

    except Exception as error:

        failures.append(
            (
                "Vector store probe failed: "
                + describe_openai_error(
                    error
                )
            )
        )

        return False


def probe_text_inference(
    failures: list[str],
) -> bool:

    try:

        response = (
            client.responses.create(
                model=CONFIG.text_model,

                input=(
                    "Reply exactly with: ok"
                ),

                max_output_tokens=64,

                store=False,
            )
        )

        output = (
            response.output_text
            .strip()
        )

        if not output:

            failures.append(
                (
                    "Text inference probe "
                    "returned no output text."
                )
            )

            return False

        return True

    except Exception as error:

        failures.append(
            (
                "Text inference probe failed: "
                + describe_openai_error(
                    error
                )
            )
        )

        return False


def probe_external_services(
) -> ExternalServiceHealth:

    failures = []
    warnings = []

    openai_api_ok = probe_openai_api(
        failures
    )

    if not openai_api_ok:

        return ExternalServiceHealth(
            openai_api_ok=False,

            text_model_access_ok=False,
            vision_model_access_ok=False,
            image_model_access_ok=False,

            vector_store_ok=False,

            text_inference_ok=False,

            failures=failures,

            warnings=warnings,

            checked_at=datetime.now(
                timezone.utc
            ).isoformat(),

            ready=False,
        )

    text_model_access_ok = (
        probe_model_access(
            model_name=(
                CONFIG.text_model
            ),

            role="Text",

            failures=failures,

            warnings=warnings,
        )
    )

    vision_model_access_ok = (
        probe_model_access(
            model_name=(
                CONFIG.vision_model
            ),

            role="Vision",

            failures=failures,

            warnings=warnings,
        )
    )

    image_model_access_ok = (
        probe_model_access(
            model_name=(
                CONFIG.image_model
            ),

            role="Image",

            failures=failures,

            warnings=warnings,
        )
    )

    if image_model_access_ok:

        warnings.append(
            (
                "Image model metadata access "
                "was verified, but no image "
                "generation request was made."
            )
        )

    vector_store_ok = (
        probe_vector_store(
            failures=failures,
            warnings=warnings,
        )
    )

    if text_model_access_ok:

        text_inference_ok = (
            probe_text_inference(
                failures
            )
        )

    else:

        text_inference_ok = False

        failures.append(
            (
                "Text inference probe was "
                "skipped because the text "
                "model access probe failed."
            )
        )

    if vision_model_access_ok:

        warnings.append(
            (
                "Vision model metadata access "
                "was verified, but no image-input "
                "vision request was made."
            )
        )

    ready = all([
        openai_api_ok,

        text_model_access_ok,
        vision_model_access_ok,
        image_model_access_ok,

        vector_store_ok,

        text_inference_ok,
    ])

    return ExternalServiceHealth(
        openai_api_ok=(
            openai_api_ok
        ),

        text_model_access_ok=(
            text_model_access_ok
        ),

        vision_model_access_ok=(
            vision_model_access_ok
        ),

        image_model_access_ok=(
            image_model_access_ok
        ),

        vector_store_ok=(
            vector_store_ok
        ),

        text_inference_ok=(
            text_inference_ok
        ),

        failures=failures,

        warnings=warnings,

        checked_at=datetime.now(
            timezone.utc
        ).isoformat(),

        ready=ready,
    )
