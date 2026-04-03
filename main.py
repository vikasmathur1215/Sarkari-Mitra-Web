
import streamlit as st
import google.generativeai as genai

# 1. API Setup (आपकी सुरक्षित चाबी)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("System Error: API Key missing. Please contact administrator.")
    st.stop()

# 2. Latest 2026 Engine
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Professional UI Design
st.set_page_config(
    page_title="TheSarkariMitra - Your Digital Assistant", 
    page_icon="🇮🇳",
    layout="centered"
)

# Header Section
st.title("🇮🇳 @TheSarkariMitra")
st.markdown("### आपका डिजिटल सरकारी सहायक")
st.info("नमस्ते! मैं भारत की सरकारी योजनाओं और दस्तावेज़ों से जुड़ी जानकारी देने में आपकी मदद कर सकता हूँ।")

# 4. Chat History (बातचीत याद रखने के लिए)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & Professional Response
if prompt := st.chat_input("अपनी सरकारी समस्या या सवाल यहाँ लिखें..."):
    # यूजर का मैसेज
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # एआई का प्रोफेशनल जवाब
    with st.chat_message("assistant"):
        with st.spinner("जानकारी खोजी जा रही है..."):
            try:
                # System Instruction: इसे अब 'Professional' बनाया गया है
                system_instruction = (
                    "तुम एक प्रोफेशनल और विनम्र सरकारी सहायक 'TheSarkariMitra' हो। "
                    "यूजर का स्वागत 'नमस्ते' से करो (अगर बातचीत की शुरुआत हो)। "
                    "भारत की सरकारी योजनाओं, आधार, पैन, राशन कार्ड और अन्य दस्तावेज़ों के बारे में "
                    "एकदम सटीक और सरल हिंदी में जानकारी दो। जवाब को पॉइंट्स में लिखो ताकि पढ़ना आसान हो।"
                )
                
                response = model.generate_content(f"{system_instruction}\n\nUser Question: {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error("क्षमा करें, तकनीकी कारणों से जवाब नहीं मिल पाया। कृपया दोबारा प्रयास करें।")
