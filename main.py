import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="The Sarkari Mitra", page_icon="⚖️")

# 🔑 API Key
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ API Key missing (Secrets check karo)")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते! मैं आपका डिजिटल सरकारी सहायक हूँ।")

# 🧠 Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat dikhao
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 💬 Input
if prompt := st.chat_input("अपनी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "तुम एक सरकारी सहायक हो। आसान हिंदी में जवाब दो।"},
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"🔥 Error: {str(e)}")