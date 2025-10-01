import streamlit as st

st.set_page_config(page_title="Bold Futures — Grant Matcher", layout="wide")
st.title("Bold Futures — Grant Matcher")

st.write("👋 Welcome! This is your Streamlit starter.")
st.write("Try the button below to see that everything works.")

if st.button("Say hello"):
    st.success("Hello! Streamlit and your project are set up. 🎉")
