
import streamlit as st
import google.generativeai as genai

# 1. API Setup (Secrets से चाबी उठाएगा)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में API Key नहीं मिली! कृपया Manage app > Settings > Secrets चेक करें।")
    st.stop()

# 2. Model Setup (बिना किसी एक्स्ट्रा सेटिंग के, ताकि Error न आए)
# हमने मॉडल का नाम एकदम सरल रखा है: 'gemini-1.5-flash'
gemini-1.5-flash-latest 

# 3. UI Setup (आपका ब्रांड नाम)
st.set_page_config(page_title="TheSarkariMitra", page_icon="🤖")
st.title("🤖 @TheSarkariMitra")
st.write("नमस्ते विकाश भाई! मैं आपका डिजिटल सरकारी सहायक हूँ।")

# 4. Chat History (मैसेज याद रखने के लिए)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input and Response (असली काम यहाँ होगा)
if prompt := st.chat_input("अपनी समस्या यहाँ लिखें..."):
    # यूजर का मैसेज स्क्रीन पर दिखाओ
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI का जवाब यहाँ से आएगा
    with st.chat_message("assistant"):
        try:
            # हम प्रॉम्प्ट में ही बता रहे हैं कि उसे 'सरकारी मित्र' बनकर जवाब देना है
            full_instruction = f"तुम एक एक्सपर्ट सरकारी सहायक 'TheSarkariMitra' हो। इस सवाल का सरल और सटीक हिंदी में जवाब दो: {prompt}"
            
            response = model.generate_content(full_instruction)
            
            # जवाब को स्क्रीन पर दिखाना
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # अगर कोई भी एरर आए तो यहाँ साफ़ दिखेगा
            st.error(f"ओह! कुछ दिक्कत आई है: {e}")
            st.info("सुझाव: एक बार 'Manage app' में जाकर 'Reboot app' बटन दबाएं।")
