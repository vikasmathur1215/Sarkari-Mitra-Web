import streamlit as st
import google.generativeai as genai

# 1. API Setup (Paid Tier Key)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में चाबी नहीं मिली! कृपया Settings > Secrets चेक करें।")
    st.stop()

# 2. Advanced Model Selection (Billing के बाद अब Pro इस्तेमाल करें)
model = genai.GenerativeModel('gemini-1.5-pro')

# 3. UI/Page Design
st.set_page_config(page_title="TheSarkariMitra", page_icon="🤖", layout="centered")
st.title("🤖 @TheSarkariMitra")
st.markdown("---")
st.write("नमस्ते विकाश भाई! मैं आपका प्रीमियम डिजिटल सरकारी सहायक हूँ।")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & AI Brain
if prompt := st.chat_input("अपनी सरकारी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # System Instruction यहीं जोड़ दी है
            full_prompt = f"तुम एक एक्सपर्ट सरकारी सहायक 'TheSarkariMitra' हो। यूजर का नाम विकाश है। दिल्ली और भारत की सरकारी योजनाओं के बारे में सरल और सटीक हिंदी में जवाब दो: {prompt}"
            
            response = model.generate_content(full_instruction)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("सुझाव: एक बार 'Reboot app' बटन दबाएं।")
