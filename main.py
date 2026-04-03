import streamlit as st
import google.generativeai as genai

# 1. API Setup (आपकी नई Billing वाली चाबी)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में चाबी नहीं मिली!")
    st.stop()

# 2. Latest 2026 'Live' Model (विकाश भाई की पसंद)
# यहाँ हमने आपका लेटेस्ट 'Live Preview' मॉडल सेट कर दिया है
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# 3. UI Setup (वेबसाइट की सजावट)
st.set_page_config(page_title="TheSarkariMitra", page_icon="🤖")
st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते विकाश भाई! मैं आपका 'Live Preview' सरकारी सहायक हूँ।")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input and Response (अब यहाँ 'Live' रफ़्तार दिखेगी)
if prompt := st.chat_input("अपनी सरकारी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # एआई को साफ़ निर्देश
            instruction = f"तुम एक एक्सपर्ट सरकारी सहायक 'TheSarkariMitra' हो। सरल हिंदी में जवाब दो: {prompt}"
            response = model.generate_content(instruction)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # अगर अभी भी Quota का एरर आए, तो समझो गूगल बिलिंग अपडेट कर रहा है
            st.error(f"Error: {e}")
            st.info("विकाश भाई, एक बार 'Reboot app' बटन ज़रूर दबाएं।")
