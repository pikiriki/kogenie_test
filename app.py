import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("KOgenie Copy Studio")

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

generate_button = st.button("Generate Copy")

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    st.success("OpenAI API key loaded.")
else:
    st.warning("OpenAI API key not found.")

if generate_button:
    if product_description:
        st.write("Generating copy for:")
        st.write(product_description)
    else:
        st.warning("Please describe your product first.")