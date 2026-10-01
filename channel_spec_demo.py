from channel_specs import get_meta_feed_spec


campaign_objective = "Join the waitlist"


channel_spec = get_meta_feed_spec(
    campaign_objective
)


print("CHANNEL SPEC\n")


print("CHANNEL")
print(channel_spec.channel)


print("\nPLACEMENT")
print(channel_spec.placement)


print("\nOBJECTIVE")
print(channel_spec.objective)


print("\nLENGTH CONSTRAINT")
print(channel_spec.length_constraint)


print("\nREQUIRED FIELDS")

for field in channel_spec.required_fields:
    print(f"- {field}")


print("\nFORMATTING RULES")

for rule in channel_spec.formatting_rules:
    print(f"- {rule}")
