import streamlit as st
from google import genai # अब हम नया तरीका इस्तेमाल करेंगे

# 1. API Setup (Naya Tarika)
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Secrets में API Key नहीं मिली भाई!")
    st.stop()

# 2. UI Setup
st.set_page_config(page_title="Sarthi AI", page_icon="🧭")

st.title("Sarthi AI 🧭")
st.markdown("### आपकी उलझनें, हमारा समाधान।")

# 3. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Input & Response
if prompt := st.chat_input("भाई/बहन, यहाँ सवाल पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sarthi AI ka dimag (Hinglish + Friendliness)
            instruction = (
                "तेरा नाम 'Sarthi AI' है और तुझे विकास माथुर (Unknown_shayar1215) ने बनाया है। "
                "एकदम Hinglish में भाई/बहन बोलकर जवाब दे। पॉइंट्स में समझा।"
            )
            
            # Naya AI Call (Gemini 2.0 Flash)
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=f"{instruction}\n\nUser: {prompt}"
            )

            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"ओह! कुछ दिक्कत है भाई: {e}")
