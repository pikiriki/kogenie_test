import streamlit as st

st.title("KOgenie Copy Studio")

product_description = st.text_area(
    "Describe your product",
    placeholder="Example: An AI platform that helps marketers create and test ad campaigns."
)

st.write("You entered:")
st.write(product_description)