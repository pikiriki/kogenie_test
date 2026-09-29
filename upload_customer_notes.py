import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

vector_store_id = os.getenv(
    "OPENAI_VECTOR_STORE_ID"
)

if not vector_store_id:
    raise RuntimeError(
        "OPENAI_VECTOR_STORE_ID is missing from .env"
    )


with open(
    "knowledge/customer_notes.txt",
    "rb"
) as file_content:
    uploaded_file = client.files.create(
        file=file_content,
        purpose="assistants"
    )


print("File uploaded:")
print(uploaded_file.id)


vector_store_file = (
    client.vector_stores.files.create_and_poll(
        vector_store_id=vector_store_id,
        file_id=uploaded_file.id
    )
)


print("\nVector store status:")
print(vector_store_file.status)
