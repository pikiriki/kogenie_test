from external_health import (
    probe_external_services,
)

from runtime_health import (
    check_runtime_health,
)

from smoke_test import (
    run_application_smoke_test,
)


local_health = (
    check_runtime_health()
)


if not local_health.ready:

    print(
        "\nLOCAL RUNTIME NOT READY"
    )

    for failure in (
        local_health
        .missing_requirements
    ):

        print(
            f"- {failure}"
        )

    raise SystemExit


print(
    "\nLocal readiness passed."
)

print(
    "Checking remote dependencies..."
)


external_health = (
    probe_external_services()
)


if not external_health.ready:

    print(
        "\nREMOTE DEPENDENCIES "
        "NOT READY"
    )

    for failure in (
        external_health.failures
    ):

        print(
            f"- {failure}"
        )

    raise SystemExit


print(
    "\nRunning application smoke test...\n"
)


report = (
    run_application_smoke_test()
)


print("=" * 70)
print("KOgenie APPLICATION SMOKE TEST")
print("=" * 70)


print("\nDATABASE ROUND TRIP")

print(
    "PASS"
    if report.database_round_trip_ok
    else "FAIL"
)


print("\nVECTOR RETRIEVAL")

print(
    "PASS"
    if report.vector_retrieval_ok
    else "FAIL"
)


print("\nSTRUCTURED OUTPUT")

print(
    "PASS"
    if report.structured_output_ok
    else "FAIL"
)


print("\nARTIFACT WRITE / READ")

print(
    "PASS"
    if report.artifact_write_read_ok
    else "FAIL"
)


print("\nFAILURES")


if report.failures:

    for failure in report.failures:

        print(
            f"- {failure}"
        )

else:

    print("- None")


print("\n" + "=" * 70)

print(
    "SMOKE TEST PASSED"
)

print(
    report.passed
)
