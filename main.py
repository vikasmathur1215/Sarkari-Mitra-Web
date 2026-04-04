import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Page Setup & ChatGPT-like CSS
st.set_page_config(page_title="Sarthi AI", page_icon="🧭", layout="centered")

st.markdown("""
    <style>
    /* चैट बॉक्स को राउंड और सुंदर बनाने के लिए */
    .stChatMessage { border-radius: 20px; margin-bottom: 10px; border: none !important; }
    
    /* इनपुट बार को नीचे फिक्स करने के लिए */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent !important;
    }
    
    /* फालतू हेडर हटाने के लिए */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* बैकग्राउंड को थोड़ा डार्क या साफ रखने के लिए */
    .main { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Identity)
with st.sidebar:
    st.title("🧭 Sarthi AI")
    st.subheader("Vikas Mathur")
    st.caption("Unknown_shayar1215")
    st.write("---")
    if st.button("New Chat +"):
        st.session_state.messages = []
        st.rerun()

# 4. Chat logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Image & Text Input (The "Photo Icon" Feature)
# यहाँ हम प्लस बटन की जगह फाइल अपलोडर दे रहे हैं जो इनपुट के ठीक ऊपर दिखेगा
with st.expander("➕ Add Image/Document"):
    uploaded_file = st.file_uploader("Upload photo for Sarthi to see", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if prompt := st.chat_input("Ask Sarthi AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sarthi's Personal Instructions
            sys_msg = "तुम Sarthi AI हो, जिसे विकास माथुर ने बनाया है। एकदम Hinglish में भाई/बहन बोलकर बात करो।"
            
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content([sys_msg + "\n" + prompt, img])
                st.image(img, caption="Analyzed by Sarthi", width=200)
            else:
                response = model.generate_content(f"{sys_msg}\nUser: {prompt}")

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error("सर्वर थोड़ा बिज़ी है भाई, दोबारा ट्राई करें?")
