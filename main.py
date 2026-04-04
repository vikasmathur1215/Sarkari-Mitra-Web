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
st.title("Sarthi AI 🧭")
st.markdown("### आपकी उलझनें, हमारा समाधान।")
st.write("दस्तावेज़ों और सरकारी प्रक्रियाओं को समझना अब हुआ आसान।")
st.caption("Created by Vikas Mathur (Unknown_shayar1215)")

# 4. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input & Friendly Response
if prompt := st.chat_input("अपना सवाल यहाँ पूछें..."):
    # यूजर का सवाल दिखाना
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # एआई का दोस्ताना जवाब
    with st.chat_message("assistant"):
        try:
            # Sarthi AI के लिए क्लियर निर्देश
            system_msg = (
                "तुम 'Sarthi AI' हो—एक भरोसेमंद और विनम्र दोस्त जिसे विकास माथुर ने बनाया है। "
                "जवाब बहुत ही सरल Hinglish में और पॉइंट्स (1, 2, 3) में दो। "
                "कोशिश करो कि जवाब ऐसा लगे जैसे कोई अपना भाई/दोस्त सलाह दे रहा हो।"
            )

            response = model.generate_content(f"{system_msg}\n\nयूजर का सवाल: {prompt}")

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error("माफ़ी चाहता हूँ भाई, सिस्टम थोड़ा बिज़ी है। एक बार दोबारा कोशिश करें?")
