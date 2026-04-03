
import streamlit as st
import google.generativeai as genai

# 1. API Setup (आपकी नई Billing वाली चाबी)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में चाबी नहीं मिली!")
    st.stop()

# 2.  model = genai.GenerativeModel('gemini-1.5-flash')
 genai.GenerativeModel('gemini-2.0-flash')

# 3. UI Design (वेबसाइट का चेहरा)
st.set_page_config(page_title="TheSarkariMitra", page_icon="🤖")
st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते भाई! मैं आपका प्रीमियम डिजिटल सरकारी सहायक हूँ।")

# 4. Chat History (पुरानी बातें याद रखने के लिए)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & Response (यही हिस्सा अटक रहा था, अब ठीक है)
if prompt := st.chat_input("अपनी सरकारी समस्या यहाँ लिखें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # यहाँ हमने नाम एकदम सही कर दिया है: 'full_text'
            full_text = f"तुम एक एक्सपर्ट सरकारी सहायक 'TheSarkariMitra' हो। यूजर का नाम विकाश है। सरकारी योजनाओं के बारे में सरल हिंदी में जवाब दो: {prompt}"
            
            # अब कंप्यूटर को सही रास्ता मिल जाएगा
            response = model.generate_content(full_text)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Error: {e}")
