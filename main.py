
import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में चाबी नहीं मिली!")
    st.stop()

# 2. model = genai.GenerativeModel('gemini-1.5-flash')

# 3. UI Setup
st.set_page_config(page_title="TheSarkariMitra", page_icon="🤖")
st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते विकाश भाई! मैं आपका डिजिटल सरकारी सहायक हूँ।")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input and Response
if prompt := st.chat_input("अपनी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # AI से जवाब मांगना
            response = model.generate_content(f"तुम एक सरकारी सहायक 'TheSarkariMitra' हो। सरल हिंदी में जवाब दो: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
