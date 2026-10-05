from config import (
    get_config,
)


config = get_config()


print("=" * 70)
print("KOgenie APPLICATION CONFIG")
print("=" * 70)


print("\nTEXT MODEL")
print(
    config.text_model
)


print("\nVISION MODEL")
print(
    config.vision_model
)


print("\nIMAGE MODEL")
print(
    config.image_model
)


print("\nVECTOR STORE")

print(
    "configured"
    if config.vector_store_id
    else "missing"
)


print("\nDATABASE")
print(
    config.database_path
)


print("\nGENERATED VISUALS")
print(
    config.generated_visuals_path
)


print("\nAPPROVED VISUALS")
print(
    config.approved_visuals_path
)


config_again = get_config()


print("\nSAME CONFIG OBJECT")

print(
    config is config_again
)
