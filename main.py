import streamlit as st
import google.generativeai as genai

# 1. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("System Error: API Key missing.")
    st.stop()

# 2. Engine Setup (Wahi purana stable model)
model = genai.GenerativeModel('gemini-pro') 

# 3. UI Setup
st.set_page_config(
    page_title="Sarthi AI", 
    page_icon="🧭",
    layout="centered"
)

# Header Section
st.title("Sarthi AI")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.write("दस्तावेज़ों और सरकारी प्रक्रियाओं को समझना अब हुआ आसान।")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & Response
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sarthi's Personal Touch
            system_msg = (
                "तुम 'Sarthi AI' हो—एक भरोसेमंद और विनम्र दोस्त जिसे विकास माथुर ने बनाया है। "
                "जवाब बहुत ही सरल हिंदी/Hinglish में दो और पॉइंट्स में समझाओ।"
            )

            response = model.generate_content(f"{system_msg}\n\nयूजर का सवाल: {prompt}")

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error("माफ़ी चाहता हूँ, अभी सिस्टम थोड़ा बिज़ी है।")

