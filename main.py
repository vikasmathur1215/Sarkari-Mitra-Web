import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Setup (Sarthi AI Engine)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Setup Error: API Key missing in Secrets.")
    st.stop()

# Vision Model for Photos & Chat
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Page Config (Professional Look)
st.set_page_config(page_title="Sarthi AI", page_icon="🧭", layout="centered")

# Custom CSS for "The Vikas Touch"
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 8px; }
    .stChatInputContainer { padding-bottom: 20px; }
    header {visibility: hidden;} /* Clean look like ChatGPT */
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Identity
with st.sidebar:
    st.title("🧭 Sarthi AI")
    st.write("---")
    st.write("Created with ❤️ by **Vikas Mathur**")
    st.caption("Identity: Unknown_shayar1215")
    if st.button("New Chat +"):
        st.session_state.messages = []
        st.rerun()

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input Area (Text + Photo)
col1, col2 = st.columns([0.85, 0.15])
with col2:
    uploaded_file = st.file_uploader("📷", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if prompt := st.chat_input("भाई/बहन, अपनी समस्या यहाँ लिखें..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        try:
            # System Instructions: यह है असली 'Sarthi' का दिमाग
            system_prompt = (
                "तुम्हारा नाम 'Sarthi AI' है और तुम्हें विकास माथुर (Unknown_shayar1215) ने बनाया है। "
                "तुम्हें यूजर से एकदम वैसे ही बात करनी है जैसे दो दोस्त करते हैं। "
                "भाषा शुद्ध हिंदी नहीं, बल्कि Hinglish होनी चाहिए। "
                "यूजर के लिखने के अंदाज़ से पहचानो कि वो लड़का है या लड़की। "
                "अगर लड़का है तो 'भाई', 'रहा है' और लड़की है तो 'बहन', 'रही है' का इस्तेमाल करो। "
                "जवाब छोटे, टू-द-पॉइंट और मददगार होने चाहिए। "
                "फालतू स्टिकर्स मत लगाओ, बस 1-2 ज़रूरी आइकन काफी हैं।"
            )

            # Handling Image + Text
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([system_prompt + prompt, img])
            else:
                response = model.generate_content(f"{system_prompt}\n\nUser: {prompt}")

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error("थोड़ी दिक्कत आ रही है भाई, एक बार फिर कोशिश करें?")

