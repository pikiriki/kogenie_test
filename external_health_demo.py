from external_health import (
    probe_external_services,
)

from runtime_health import (
    check_runtime_health,
)


local_health = (
    check_runtime_health()
)


if not local_health.ready:

    print(
        "\nLocal runtime readiness failed."
    )

    print(
        "Remote probes will not run."
    )

    print(
        "\nFix these first:"
    )

    for issue in (
        local_health
        .missing_requirements
    ):

        print(f"- {issue}")

    raise SystemExit


print(
    "\nLocal readiness passed."
)

print(
    "\nRunning explicit remote "
    "dependency probes..."
)

print(
    "\nNote: this includes one tiny "
    "text inference request."
)


health = probe_external_services()


print("\n" + "=" * 70)
print("EXTERNAL SERVICE HEALTH")
print("=" * 70)


print("\nOPENAI API")

print(
    "OK"
    if health.openai_api_ok
    else "FAILED"
)


print("\nTEXT MODEL ACCESS")

print(
    "OK"
    if health.text_model_access_ok
    else "FAILED"
)


print("\nVISION MODEL ACCESS")

print(
    "OK"
    if health.vision_model_access_ok
    else "FAILED"
)


print("\nIMAGE MODEL ACCESS")

print(
    "OK"
    if health.image_model_access_ok
    else "FAILED"
)


print("\nVECTOR STORE")

print(
    "OK"
    if health.vector_store_ok
    else "FAILED"
)


print("\nTEXT INFERENCE")

print(
    "OK"
    if health.text_inference_ok
    else "FAILED"
)


print("\nFAILURES")


if health.failures:

    for item in health.failures:
        print(f"- {item}")

else:

    print("- None")


print("\nWARNINGS")


if health.warnings:

    for item in health.warnings:
        print(f"- {item}")

else:

    print("- None")


print("\nCHECKED AT")

print(
    health.checked_at
)


print("\n" + "=" * 70)

print(
    "REMOTE PROBES READY"
)

print(
    health.ready
)
