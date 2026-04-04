import streamlit as st
import google.generativeai as genai

# 1. API Setup (Wahi purana aur pakka tarika)
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Stable Model: gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"API Setup Error: {e}")
else:
    st.error("Secrets में API Key नहीं मिली भाई!")
    st.stop()

# 2. UI Setup (Sarthi AI Branding)
st.set_page_config(page_title="Sarthi AI", page_icon="🧭", layout="centered")

st.title("Sarthi AI 🧭")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.caption("Created by Vikas Mathur (Unknown_shayar1215)")

# 3. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input & Response
if prompt := st.chat_input("भाई/बहन, यहाँ अपना सवाल पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sarthi AI Dimag (Friendly & Hinglish)
            system_msg = (
                "तेरा नाम 'Sarthi AI' है और तुझे विकास माथुर ने बनाया है। "
                "तू एकदम Hinglish में भाई/बहन बोलकर जवाब दे। "
                "जवाब पॉइंट्स में और छोटे होने चाहिए।"
            )
            
            response = model.generate_content(f"{system_msg}\n\nUser: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Agar limit khatam ho jaye to ye message dikhega
            st.error("भाई, लगता है आज की लिमिट खत्म हो गई है या API Key में दिक्कत है।")
