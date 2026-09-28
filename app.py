import os

import streamlit as st
from dotenv import load_dotenv

from copy_generator import generate_copy

load_dotenv()

st.title("KOgenie Copy Studio")

st.write(
    "Describe a product and generate a simple advertising draft."
)

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

generate_button = st.button("Generate Copy")

api_key = os.getenv("OPENAI_API_KEY")

if generate_button:
    if product_description:
        if api_key:
            generated_copy = generate_copy(product_description)

            st.subheader("Generated Draft")
            st.markdown(generated_copy)

        else:
            st.error("OpenAI API key is missing.")

    else:
        st.warning("Please describe your product first.")