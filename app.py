import streamlit as st

st.title("KOgenie Copy Studio")

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

generate_button = st.button("Generate Copy")

if generate_button:
    if product_description:
        st.write("Generating copy for:")
        st.write(product_description)
    else:
        st.warning("Please describe your product first.")