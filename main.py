import streamlit as st
import google.generativeai as genai

# API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में API Key नहीं मिली!")
    st.stop()

# मॉडल का नाम यहाँ सही कर दिया है
model = genai.GenerativeModel('gemini-1.5-flash')

 

st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते! मैं आपका डिजिटल सरकारी सहायक हूँ।")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("अपनी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"तुम एक सरकारी सहायक हो। सरल हिंदी में जवाब दो: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

