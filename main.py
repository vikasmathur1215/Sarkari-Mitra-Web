import streamlit as st
import google.generativeai as genai
# --- मिशन 2: सुंदर डिज़ाइन (CSS) ---
st.markdown("""
    <style>
    /* पूरे ऐप का बैकग्राउंड */
    .stApp {
        background-color: #f8f9fa;
    }
    /* बटन्स को सुंदर बनाना */
    .stButton>button {
        border-radius: 20px;
        border: 2px solid #ff4b4b;
        background-color: white;
        color: #ff4b4b;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: white;
    }
    /* चैट मैसेज को गोल करना */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        /* 🚀 मिशन: लाल लोगो और प्रोफाइल फोटो का सफाया */
    
    /* 1. नीचे की पूरी पट्टी (Footer) को जड़ से मिटाना */
    footer {display: none !important;}
    header {display: none !important;}
    
    /* 2. स्ट्रीमलिट का लाल लोगो और 'Hosted with' टेक्स्ट */
    div[data-testid="stStatusWidget"],
    .stAppViewFooter,
    .st-emotion-cache-1vt4y6f,
    .st-emotion-cache-12fmjuu {
        display: none !important;
        height: 0px !important;
    }

    /* 3. आपकी प्रोफाइल फोटो वाला बटन (Toolbar) */
    div[data-testid="stToolbar"],
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    /* 4. स्क्रीन के नीचे की फालतू जगह खत्म करना */
    .stApp {
        bottom: 0px !important;
        padding-bottom: 0px !important;
    }



    </style>
    """, unsafe_allow_html=True)

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    st.error("System Error: API Key missing.")
    st.stop()

# 2. Session State Initialize (Isse AttributeError khatam hoga)
if "messages" not in st.session_state:
    st.session_state.messages = []
# --- मिशन: डायरेक्ट चैट शुरू करें (सफ़ाई के बाद) ---
if "user_name" not in st.session_state:
    st.session_state.user_name = "दोस्त"

st.title("Sarthi AI 🧭")
st.markdown("### आपकी सेवा में हाज़िर! नमस्ते भाई, मैं आपकी क्या मदद कर सकता हूँ?")

                
                # 
                
                # सुंदर व्हाट्सएप बटन st.markdown(f"""
                    
                                

# 3. UI Setup
st.set_page_config(page_title="Sarthi AI", page_icon="🧭")
st.title("Sarthi AI")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.write("दस्तावेज़ों और सरकारी प्रक्रियाओं को समझना अब हुआ आसान।")

# 4. Quick Buttons
st.write("---") 
col1, col2, col3 = st.columns(3)
button_prompt = None

with col1:
    if st.button("📄 Resume"):
        button_prompt = "मुझे एक प्रोफेशनल Resume बनाना है, मेरी मदद करो।"
with col2:
    if st.button("🏠 Rent Draft"):
        button_prompt = "मुझे एक Rent Agreement का ड्राफ्ट बना कर दो।"
with col3:
    if st.button("📜 Affidavit"):
        button_prompt = "मुझे एक सामान्य Affidavit का फॉर्मेट चाहिए।"

# बटन दबाने पर AI जवाब देगा
if button_prompt:
    st.session_state.messages.append({"role": "user", "content": button_prompt})
    # AI Response Trigger
    system_msg = (
                "तुम 'Sarthi AI' हो। अगर कोई Resume मांगे, तो उससे नाम, पढ़ाई और अनुभव पूछो। "
                "अगर Rent Draft मांगे, तो मकान मालिक-किराएदार का नाम पूछो। "
                "जवाब सरल Hinglish में और पॉइंट्स में दो।"
            )


    response = model.generate_content(f"{system_msg}\n\nUser: {button_prompt}")
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()

# 5. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input & AI Response
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # एआई को निर्देश देना
            system_msg = "तुम Sarthi AI हो। सरल Hinglish में जवाब दो और डॉक्यूमेंट का पूरा ड्राफ्ट तैयार करो।"
            response = model.generate_content(f"{system_msg}\n\nUser: {prompt}")
            
            # जवाब स्क्रीन पर दिखाना
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # डाउनलोड बटन (यहाँ जादू शुरू होता है)
            st.download_button(
                label="📩 इस डॉक्यूमेंट को डाउनलोड करें",
                data=response.text,
                file_name="Sarthi_Document.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error("माफ़ी चाहता हूँ, सिस्टम अभी कनेक्ट नहीं हो पा रहा।")
