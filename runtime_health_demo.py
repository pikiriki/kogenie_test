from runtime_health import (
    check_runtime_health,
)


health = check_runtime_health()


print("=" * 70)
print("KOgenie RUNTIME HEALTH")
print("=" * 70)


print("\nENVIRONMENT")

print(
    "OK"
    if health.environment_ok
    else "FAILED"
)


print("\nDATABASE")

print(
    "OK"
    if health.database_ok
    else "FAILED"
)


print("\nSTORAGE")

print(
    "OK"
    if health.storage_ok
    else "FAILED"
)


print("\nMODEL CONFIGURATION")

print(
    "OK"
    if health.model_configuration_ok
    else "FAILED"
)


print("\nMISSING REQUIREMENTS / FAILURES")


if health.missing_requirements:

    for problem in (
        health.missing_requirements
    ):

        print(
            f"- {problem}"
        )

else:

    print("- None")


print("\n" + "=" * 70)

print(
    "READY TO START"
)

print(
    health.ready
)
