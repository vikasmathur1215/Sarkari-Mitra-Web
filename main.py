import streamlit as st
import google.generativeai as genai

# API Setup (Streamlit Secrets se)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing! Please add it in Streamlit Secrets.")

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 @TheSarkariMitra")
st.write("आपका डिजिटल सरकारी सहायक।")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("कैसे मदद कर सकता हूँ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
