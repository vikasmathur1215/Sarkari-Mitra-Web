import streamlit as st
import google.generativeai as genai

# API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Secrets!")
    st.stop()

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
        try:
            response = model.generate_content(f"तुम एक सरकारी सहायक हो। हिंदी में जवाब दो: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Google AI से कनेक्ट नहीं हो पा रहा। कृपया अपनी API Key चेक करें।")

