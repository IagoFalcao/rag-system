import streamlit as st

st.title("RAG Chatbot")
query = st.text_input("Pergunta:")

if query:
    st.write("Resposta virá aqui...")
