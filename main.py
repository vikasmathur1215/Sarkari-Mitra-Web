
import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("System configuration error. Please check secrets.")
    st.stop()

# 2. Engine Setup
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Professional & Modern UI (यहाँ हमने सरकारी लुक हटा दिया है)
st.set_page_config(
    page_title="TheSarkariMitra", 
    page_icon="🤝", # एक दोस्ताना हाथ मिलाने वाला आइकन
    layout="centered"
)

# Custom CSS: थोड़ा और सुंदर बनाने के लिए
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_status=True)

# Header: अब यह सरकारी नहीं, हेल्पफुल लग रहा है
st.title("TheSarkariMitra")
st.subheader("आपकी उलझनें, हमारा समाधान।")
st.write("दस्तावेज़ों और सरकारी प्रक्रियाओं को समझना अब हुआ आसान। अपना सवाल नीचे लिखें।")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Friendly AI Logic
if prompt := st.chat_input("यहाँ अपना सवाल पूछें (जैसे: पैन कार्ड कैसे सुधारें?)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("सोच रहा हूँ..."):
            try:
                # Instruction: यहाँ हमने 'सरकारी' शब्द कम कर दिया है और 'मित्र' भाव बढ़ाया है
                friendly_instruction = (
                    "तुम 'TheSarkariMitra' हो—एक भरोसेमंद दोस्त जो लोगों को सरकारी कागजी कार्रवाई में मदद करता है। "
                    "तुम्हारी भाषा बहुत ही सरल, विनम्र और मददगार होनी चाहिए। "
                    "जवाब ऐसे दो जैसे एक बड़ा भाई छोटे भाई को समझा रहा हो। "
                    "ज़्यादा स्टिकर्स मत यूज़ करो, बस ज़रूरत पड़ने पर 1-2 अच्छे आइकन लगाओ। "
                    "अगर किसी को प्रक्रिया समझानी हो, तो उसे स्टेप-दर-स्टेप (1, 2, 3) बताओ।"
                )
                
                response = model.generate_content(f"{friendly_instruction}\n\nयूजर का सवाल: {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error("माफ़ी चाहता हूँ, अभी सिस्टम थोड़ा बिज़ी है। एक बार फिर कोशिश करेंगे?")
