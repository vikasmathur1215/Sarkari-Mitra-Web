import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets mein API Key nahi mili!")
    st.stop()

# 2. Model Setup (System Instruction ke saath)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="तुम एक सरकारी सहायक 'TheSarkariMitra' हो। सरकारी योजनाओं और आधार कार्ड जैसे कामों के बारे में सरल हिंदी में सटीक जानकारी दो।"
)

# 3. UI Setup
st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते! मैं आपका डिजिटल सरकारी सहायक हूँ।")

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
            # Model se response lena
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
