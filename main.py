
import streamlit as st
import google.generativeai as genai

# --- 1. पेज कॉन्फ़िगरेशन (सबसे ऊपर होना चाहिए) ---
st.set_page_config(page_title="Sarthi AI 🧭", layout="centered")

# --- 2. CSS डिज़ाइन (प्रोफेशनल लुक + लोगो हटाना) ---
st.markdown("""
    <style>
    /* लाल पट्टी और प्रोफाइल फोटो को जड़ से हटाना */
    [data-testid="stStatusWidget"], header, footer, #MainMenu, .stApp > header, div[data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* बटन का सुंदर डिज़ाइन */
    .stButton>button {
        width: 100%;
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

    /* चैट मैसेज को गोल और सुंदर बनाना */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* स्क्रीन के नीचे की फालतू जगह खत्म करना */
    .stApp { bottom: 0px !important; padding-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Gemini AI Setup ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # 1.5-flash सबसे स्टेबल और तेज है
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("System Error: API Key missing in Secrets.")
    st.stop()

# --- 4. मेमोरी सेटअप (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "दोस्त"

# --- 5. मुख्य हेडर ---
st.title("Sarthi AI 🧭")
st.markdown("### आपकी सेवा में हाज़िर! नमस्ते भाई, मैं आपकी क्या मदद कर सकता हूँ?")
st.write("---")

# --- 6. क्विक बटन्स (Quick Actions) ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📄 Resume"):
        st.session_state.messages.append({"role": "user", "content": "मुझे एक प्रोफेशनल रिज्यूमे बनाना है, मेरी मदद करो।"})
with col2:
    if st.button("🏠 Rent Draft"):
        st.session_state.messages.append({"role": "user", "content": "मुझे एक रेंट एग्रीमेंट का ड्राफ्ट चाहिए।"})
with col3:
    if st.button("📜 Affidavit"):
        st.session_state.messages.append({"role": "user", "content": "मुझे एक एफिडेविट का फॉर्मेट दिखाओ।"})

# --- 7. चैट डिस्प्ले ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 8. चैट इनपुट और AI रिस्पॉन्स ---
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    # यूजर का मैसेज दिखाना
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI का जवाब तैयार करना
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # सिस्टम इंस्ट्रक्शन (Sarthi AI का व्यक्तित्व)
        system_msg = "तुम 'सारथी AI' हो, एक मददगार भारतीय सहायक। तुम लोगों को रिज्यूमे, रेंट ड्राफ्ट और सरकारी कागजी कार्रवाई में मदद करते हो। हमेशा सरल हिंदी में जवाब दो और भाई जैसा व्यवहार रखो।"
        
        try:
            response = model.generate_content(f"{system_msg}\n\nUser: {prompt}")
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error("ओह! गूगल की फ्री लिमिट खत्म हो गई है। कृपया 5-10 मिनट बाद फिर से कोशिश करें।")
