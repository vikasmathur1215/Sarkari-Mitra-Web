import streamlit as st
import google.generativeai as genai
import os

# 🔑 API Key load
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ API Key load nahi ho rahi. Secrets check karo!")
    st.stop()

genai.configure(api_key=api_key)

# 🤖 Model setup
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# 🎨 UI
st.set_page_config(page_title="The Sarkari Mitra", page_icon="⚖️")

st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते! मैं आपका डिजिटल सरकारी सहायक हूँ।")

# 🧠 Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट दिखाओ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 💬 User input
if prompt := st.chat_input("अपनी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(
                f"""
                तुम एक सरकारी मित्र हो।
                यूज़र की मदद आसान हिंदी और हिंग्लिश में करो।
                Step-by-step समझाओ।

                सवाल: {prompt}
                """
            )

            if response and response.text:
                st.markdown(response.text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text
                })
            else:
                st.error("❌ Empty response आया")

        except Exception as e:
            st.error(f"🔥 Error: {str(e)}")
