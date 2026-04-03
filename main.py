
import streamlit as st
from google import genai

# 1. नई लाइब्रेरी के साथ सेटअप
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Secrets!")
    st.stop()

st.title("🤖 @TheSarkariMitra")
st.write("आपका डिजिटल सरकारी सहायक (Updated Version)")

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
        try:
            # नया तरीका जवाब मांगने का
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=f"तुम एक सरकारी सहायक हो। हिंदी में जवाब दो: {prompt}"
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("कनेक्शन में दिक्कत है। कृपया एक बार 'Reboot' बटन दबाएं।")
