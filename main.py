import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing.")
    st.stop()

# Engine: Gemini 1.5 Flash (Sabse fast aur stable)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Page Config (ChatGPT Style)
st.set_page_config(page_title="Sarthi AI", page_icon="🧭", layout="centered")

# Custom CSS: Look badalne ke liye
st.markdown("""
    <style>
    .stChatMessage { border-radius: 20px; border: none !important; }
    header {visibility: hidden;}
    .main { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# 3. Instruction - Sarthi AI ka dimag
system_instruction = (
    "तेरा नाम 'Sarthi AI' है और तुझे विकास माथुर (Unknown_shayar1215) ने बनाया है। "
    "तू शुद्ध हिंदी नहीं, बल्कि Hinglish में बात कर। "
    "यूजर को 'भाई' या 'बहन' बोलकर एड्रेस कर। "
    "जवाब छोटे और एकदम काम के होने चाहिए। "
    "हमेशा याद दिला कि तू विकास का बनाया हुआ AI है।"
)

# Sidebar
with st.sidebar:
    st.title("🧭 Sarthi AI")
    st.write("Created by: **Vikas Mathur**")
    st.caption("Identity: Unknown_shayar1215")
    if st.button("New Chat +"):
        st.session_state.messages = []
        st.rerun()

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input (Clean Input like ChatGPT)
if prompt := st.chat_input("भाई/बहन, यहाँ अपना सवाल पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):
        try:
            # Simple text-based response to avoid server errors
            response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error("माफ़ी चाहता हूँ भाई, सर्वर अभी लोड नहीं ले पा रहा। एक बार दोबारा 'Hello' लिखो?")
