from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()


vector_store = client.vector_stores.create(
    name="KOgenie Research Documents"
)

print("Vector store created:")
print(vector_store.id)


with open(
    "knowledge/kogenie_product_notes.txt",
    "rb"
) as file_content:
    uploaded_file = client.files.create(
        file=file_content,
        purpose="assistants"
    )


print("\nFile uploaded:")
print(uploaded_file.id)


vector_store_file = (
    client.vector_stores.files.create_and_poll(
        vector_store_id=vector_store.id,
        file_id=uploaded_file.id
    )
)


print("\nVector store file status:")
print(vector_store_file.status)

print("\nSave this in your .env file:")
print(
    f"OPENAI_VECTOR_STORE_ID={vector_store.id}"
)
