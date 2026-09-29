from dotenv import load_dotenv

from research_agent import (
    research_public_company_info,
)


load_dotenv()


company_or_product = "Notion"

result = research_public_company_info(
    company_or_product
)


print("RESEARCH ANSWER\n")
print(result.final_output)


print("\nSOURCES\n")


seen_urls = set()


for response in result.raw_responses:
    for item in response.output:
        if getattr(item, "type", None) != "message":
            continue

        for content in getattr(item, "content", []):
            if getattr(content, "type", None) != "output_text":
                continue

            for annotation in getattr(
                content,
                "annotations",
                []
            ):
                if getattr(
                    annotation,
                    "type",
                    None
                ) != "url_citation":
                    continue

                url = annotation.url
                title = annotation.title

                if url not in seen_urls:
                    print(f"- {title}")
                    print(f"  {url}")

                    seen_urls.add(url)
