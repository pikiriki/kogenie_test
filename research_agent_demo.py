from dotenv import load_dotenv

from research_agent import (
    research_verified_brand_claims,
)


load_dotenv()


brand_profile_id = 1

result = research_verified_brand_claims(
    brand_profile_id
)

print(result)
